import  streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import ahpy

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

DATA_URL = 'https://hellobucketbucket.s3.ap-northeast-1.amazonaws.com/%E5%AF%B5%E7%89%A9%E7%8A%AC%E5%93%81%E7%A8%AE%E8%B3%87%E6%96%99%E5%BA%AB.csv'

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis = "columns", inplace = True)
#     data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data = load_data()

menu = ["Home", "About"]
st.title("以AHP法協助飼主做寵物犬體型最佳配適選擇 :dog2:")
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("尋找最適合之寵物犬大小 :dog:")
    # information

    # Change font size and font color
    # https://discuss.streamlit.io/t/change-font-size-and-font-color/12377/2
    # original_title = '<p style="font-family:Courier; color:White; font-size: 22px;">環境</p>'
    # st.markdown(original_title, unsafe_allow_html=True)

    # 基本資料
    with st.form(key='基本資料問卷'):
        with st.container():
            st.markdown("#### 基本資料")

            col1, col2 = st.columns(2)
            with col1:
                variety = st.selectbox(
                        "選擇一種您喜愛的寵物狗",
                        ("拉不拉多", "德國牧羊犬", "黃金獵犬", "哈士奇", "秋田犬",
                         "柯基", "薩摩耶", "鬆獅犬", "狐狸犬", "法國鬥牛犬",
                         "玩具貴賓犬", "臘腸犬", "吉娃娃", "迷你雪納瑞", "傑克羅素㹴"))
            with col2:
                dog_character = st.selectbox(
                        "您喜好狗狗之性格",
                        ("獨立型", "敏感型", "自信型", "樂天型", "適應型"))

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")

    # A1.家裡空間
    with st.form(key='家裡空間問卷'):
        with st.container():
            st.markdown("#### A1.家裡空間")

            col1, col2 = st.columns([2, 3])

            with col1:
                A1L_A1M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                A1L_A1M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)


        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                A1L_A1S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)

            with col2:
                A1L_A1S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                A1M_A1S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)

            with col2:
                A1M_A1S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    # st.write("您選擇了:", A1_A2)
    if A1L_A1M == '大型犬':
        A1L_A1M_scores = int(A1L_A1M_scores)
        # st.write("分數:", A1_A2_scores)
    else:
        A1L_A1M_scores = round((1 / int(A1L_A1M_scores)), 3)
        # st.write("分數:", A1_A2_scores)
    # 1_3
    # st.write("您選擇了:", A1_A3)
    if A1L_A1S == '大型犬':
        A1L_A1S_scores = int(A1L_A1S_scores)
        # st.write("分數:", A1_A3_scores)
    else:
        A1L_A1S_scores = round((1 / int(A1L_A1S_scores)), 3)
        # st.write("分數:", A1_A3_scores)
    # 2_3
    # st.write("您選擇了:", A2_A3)
    if A1M_A1S == '中型犬':
        A1M_A1S_scores = int(A1M_A1S_scores)
        # st.write("分數:", A2_A3_scores)
    else:
        A1M_A1S_scores = round((1 / int(A1M_A1S_scores)), 3)
        # st.write("分數:", A2_A3_scores)

    # AHPy
    homeSpace_comparisons = {('大型犬', '中型犬'): A1L_A1M_scores,
                         ('大型犬', '小型犬'): A1L_A1S_scores,
                         ('中型犬', '小型犬'): A1M_A1S_scores}
    # st.text(env_comparisons)

    #
    homeSpace = ahpy.Compare(name='HomeSpaces', comparisons=homeSpace_comparisons, precision=3, random_index='saaty')
    AHPtable = pd.DataFrame(columns=["屬性", "大型犬", "中型犬", "小型犬"])
    # write attributes into DataFrame
    AHPtable.loc[0] = ["A1.家裡空間",
                       homeSpace.target_weights["大型犬"],
                       homeSpace.target_weights["中型犬"],
                       homeSpace.target_weights["小型犬"]]
    attr_homeSpace = 0.223
    attr_homeSpace_l = attr_homeSpace * homeSpace.target_weights["大型犬"]
    attr_homeSpace_m = attr_homeSpace * homeSpace.target_weights["中型犬"]
    attr_homeSpace_s = attr_homeSpace * homeSpace.target_weights["小型犬"]
    # st.write("各屬性權重 :", homeSpace.target_weights)
    # st.write("CR :", homeSpace.consistency_ratio)

    # A2.活動範圍
    with st.form(key='活動範圍問卷'):
        with st.container():
            st.markdown("#### A2.活動範圍")

            col1, col2 = st.columns([2, 3])

            with col1:
                A2L_A2M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                A2L_A2M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)


        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                A2L_A2S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)

            with col2:
                A2L_A2S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                A2M_A2S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)

            with col2:
                A2M_A2S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if A2L_A2M == '大型犬':
        A2L_A2M_scores = int(A2L_A2M_scores)
    else:
        A2L_A2M_scores = round((1 / int(A2L_A2M_scores)), 3)
    # 1_3
    if A2L_A2S == '大型犬':
        A2L_A2S_scores = int(A2L_A2S_scores)
    else:
        A2L_A2S_scores = round((1 / int(A2L_A2S_scores)), 3)
    # 2_3
    if A2M_A2S == '中型犬':
        A2M_A2S_scores = int(A2M_A2S_scores)
    else:
        A2M_A2S_scores = round((1 / int(A2M_A2S_scores)), 3)

    # AHPy
    activityRange_comparisons = {('大型犬', '中型犬'): A2L_A2M_scores,
                         ('大型犬', '小型犬'): A2L_A2S_scores,
                         ('中型犬', '小型犬'): A2M_A2S_scores}
    #
    activityRange = ahpy.Compare(name='ActivityRanges', comparisons=activityRange_comparisons, precision=3, random_index='saaty')
    AHPtable_n = pd.DataFrame({'屬性': "A2.家裡空間",
                                    '大型犬': activityRange.target_weights["大型犬"],
                                    '中型犬': activityRange.target_weights["中型犬"],
                                    '小型犬': activityRange.target_weights["小型犬"]
                               },
                              index=[1]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_activityRange = 0.182
    attr_activityRange_l = attr_activityRange * activityRange.target_weights["大型犬"]
    attr_activityRange_m = attr_activityRange * activityRange.target_weights["中型犬"]
    attr_activityRange_s = attr_activityRange * activityRange.target_weights["小型犬"]
    # st.write("各屬性權重 :", activityRange.target_weights)
    # st.write("CR :", activityRange.consistency_ratio)

    # A3.居住人數
    with st.form(key='居住人數問卷'):
        with st.container():
            st.markdown("#### A3.居住人數")

            col1, col2 = st.columns([2, 3])

            with col1:
                A3L_A3M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                A3L_A3M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                A3L_A3S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                A3L_A3S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                A3M_A3S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                A3M_A3S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if A3L_A3M == '大型犬':
        A3L_A3M_scores = int(A3L_A3M_scores)
    else:
        A3L_A3M_scores = round((1 / int(A3L_A3M_scores)), 3)
    # 1_3
    if A3L_A3S == '大型犬':
        A3L_A3S_scores = int(A3L_A3S_scores)
    else:
        A3L_A3S_scores = round((1 / int(A3L_A3S_scores)), 3)
    # 2_3
    if A3M_A3S == '中型犬':
        A3M_A3S_scores = int(A3M_A3S_scores)
    else:
        A3M_A3S_scores = round((1 / int(A3M_A3S_scores)), 3)

    # AHPy
    numResidents_comparisons = {('大型犬', '中型犬'): A3L_A3M_scores,
                          ('大型犬', '小型犬'): A3L_A3S_scores,
                          ('中型犬', '小型犬'): A3M_A3S_scores}
    #
    numResident = ahpy.Compare(name='numResidents', comparisons=numResidents_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "A3.居住人數",
                               '大型犬': numResident.target_weights["大型犬"],
                               '中型犬': numResident.target_weights["中型犬"],
                               '小型犬': numResident.target_weights["小型犬"]
                               },
                              index=[2]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_numResident = 0.049
    attr_numResident_l = attr_numResident * numResident.target_weights["大型犬"]
    attr_numResident_m = attr_numResident * numResident.target_weights["中型犬"]
    attr_numResident_s = attr_numResident * numResident.target_weights["小型犬"]

    # st.write("各屬性權重 :", numResident.target_weights)
    # st.write("CR :", numResident.consistency_ratio)
    # st.write("資料：", AHPtable)

    # B1.配件
    with st.form(key='配件問卷'):
        with st.container():
            st.markdown("#### B1.配件")

            col1, col2 = st.columns([2, 3])

            with col1:
                B1L_B1M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                B1L_B1M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                B1L_B1S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                B1L_B1S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                B1M_B1S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                B1M_B1S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if B1L_B1M == '大型犬':
        B1L_B1M_scores = int(B1L_B1M_scores)
    else:
        B1L_B1M_scores = round((1 / int(B1L_B1M_scores)), 3)
    # 1_3
    if B1L_B1S == '大型犬':
        B1L_B1S_scores = int(B1L_B1S_scores)
    else:
        B1L_B1S_scores = round((1 / int(B1L_B1S_scores)), 3)
    # 2_3
    if B1M_B1S == '中型犬':
        B1M_B1S_scores = int(B1M_B1S_scores)
    else:
        B1M_B1S_scores = round((1 / int(B1M_B1S_scores)), 3)

    # AHPy
    Accessory_comparisons = {('大型犬', '中型犬'): B1L_B1M_scores,
                                ('大型犬', '小型犬'): B1L_B1S_scores,
                                ('中型犬', '小型犬'): B1M_B1S_scores}
    #
    Accessory = ahpy.Compare(name='Accessories', comparisons=Accessory_comparisons, precision=3,
                               random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "B1.配件",
                               '大型犬': Accessory.target_weights["大型犬"],
                               '中型犬': Accessory.target_weights["中型犬"],
                               '小型犬': Accessory.target_weights["小型犬"]
                               },
                              index=[3]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_Accessory = 0.009
    attr_Accessory_l = attr_Accessory * Accessory.target_weights["大型犬"]
    attr_Accessory_m = attr_Accessory * Accessory.target_weights["中型犬"]
    attr_Accessory_s = attr_Accessory * Accessory.target_weights["小型犬"]

    # st.write("各屬性權重 :", Accessory.target_weights)
    # st.write("CR :", Accessory.consistency_ratio)


    # B2.食物
    with st.form(key='食物問卷'):
        with st.container():
            st.markdown("#### B2.食物")

            col1, col2 = st.columns([2, 3])

            with col1:
                B2L_B2M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                B2L_B2M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)


        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                B2L_B2S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)

            with col2:
                B2L_B2S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                B2M_B2S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)

            with col2:
                B2M_B2S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if B2L_B2M == '大型犬':
        B2L_B2M_scores = int(B2L_B2M_scores)
    else:
        B2L_B2M_scores = round((1 / int(B2L_B2M_scores)), 3)
    # 1_3
    if B2L_B2S == '大型犬':
        B2L_B2S_scores = int(B2L_B2S_scores)
    else:
        B2L_B2S_scores = round((1 / int(B2L_B2S_scores)), 3)
    # 2_3
    if B2M_B2S == '中型犬':
        B2M_B2S_scores = int(B2M_B2S_scores)
    else:
        B2M_B2S_scores = round((1 / int(B2M_B2S_scores)), 3)

    # AHPy
    food_comparisons = {('大型犬', '中型犬'): B2L_B2M_scores,
                         ('大型犬', '小型犬'): B2L_B2S_scores,
                         ('中型犬', '小型犬'): B2M_B2S_scores}
    #
    food = ahpy.Compare(name='food', comparisons=food_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "B2.食物",
                               '大型犬': food.target_weights["大型犬"],
                               '中型犬': food.target_weights["中型犬"],
                               '小型犬': food.target_weights["小型犬"]
                               },
                              index=[4]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_food = 0.039
    attr_food_l = attr_food * food.target_weights["大型犬"]
    attr_food_m = attr_food * food.target_weights["中型犬"]
    attr_food_s = attr_food * food.target_weights["小型犬"]

    # st.write("各屬性權重 :", food.target_weights)
    # st.write("CR :", food.consistency_ratio)


    # B3.醫療
    with st.form(key='醫療問卷'):
        with st.container():
            st.markdown("#### B3.醫療")

            col1, col2 = st.columns([2, 3])

            with col1:
                B3L_B3M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                B3L_B3M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                B3L_B3S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                B3L_B3S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                B3M_B3S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                B3M_B3S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if B3L_B3M == '大型犬':
        B3L_B3M_scores = int(B3L_B3M_scores)
    else:
        B3L_B3M_scores = round((1 / int(B3L_B3M_scores)), 3)
    # 1_3
    if B3L_B3S == '大型犬':
        B3L_B3S_scores = int(B3L_B3S_scores)
    else:
        B3L_B3S_scores = round((1 / int(B3L_B3S_scores)), 3)
    # 2_3
    if B3M_B3S == '中型犬':
        B3M_B3S_scores = int(B3M_B3S_scores)
    else:
        B3M_B3S_scores = round((1 / int(B3M_B3S_scores)), 3)

    # AHPy
    medical_comparisons = {('大型犬', '中型犬'): B3L_B3M_scores,
                          ('大型犬', '小型犬'): B3L_B3S_scores,
                          ('中型犬', '小型犬'): B3M_B3S_scores}
    #
    medical = ahpy.Compare(name='medical', comparisons=medical_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "B3.醫療",
                               '大型犬': medical.target_weights["大型犬"],
                               '中型犬': medical.target_weights["中型犬"],
                               '小型犬': medical.target_weights["小型犬"]
                               },
                              index=[5]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_medical = 0.062
    attr_medical_l = attr_medical * medical.target_weights["大型犬"]
    attr_medical_m = attr_medical * medical.target_weights["中型犬"]
    attr_medical_s = attr_medical * medical.target_weights["小型犬"]

    # st.write("各屬性權重 :", medical.target_weights)
    # st.write("CR :", medical.consistency_ratio)

    # C1.體重
    with st.form(key='體重問卷'):
        with st.container():
            st.markdown("#### C1.體重")

            col1, col2 = st.columns([2, 3])

            with col1:
                C1L_C1M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                C1L_C1M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                C1L_C1S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                C1L_C1S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                C1M_C1S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                C1M_C1S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if C1L_C1M == '大型犬':
        C1L_C1M_scores = int(C1L_C1M_scores)
    else:
        C1L_C1M_scores = round((1 / int(C1L_C1M_scores)), 3)
    # 1_3
    if C1L_C1S == '大型犬':
        C1L_C1S_scores = int(C1L_C1S_scores)
    else:
        C1L_C1S_scores = round((1 / int(C1L_C1S_scores)), 3)
    # 2_3
    if C1M_C1S == '中型犬':
        C1M_C1S_scores = int(C1M_C1S_scores)
    else:
        C1M_C1S_scores = round((1 / int(C1M_C1S_scores)), 3)

    # AHPy
    weight_comparisons = {('大型犬', '中型犬'): C1L_C1M_scores,
                           ('大型犬', '小型犬'): C1L_C1S_scores,
                           ('中型犬', '小型犬'): C1M_C1S_scores}
    #
    weight = ahpy.Compare(name='Weight', comparisons=weight_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "C1.體重",
                               '大型犬': weight.target_weights["大型犬"],
                               '中型犬': weight.target_weights["中型犬"],
                               '小型犬': weight.target_weights["小型犬"]
                               },
                              index=[6]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_weight = 0.034
    attr_weight_l = attr_weight * weight.target_weights["大型犬"]
    attr_weight_m = attr_weight * weight.target_weights["中型犬"]
    attr_weight_s = attr_weight * weight.target_weights["小型犬"]

    # st.write("各屬性權重 :", weight.target_weights)
    # st.write("CR :", weight.consistency_ratio)
    # st.write("資料：", AHPtable)

    # C2.腿長
    with st.form(key='腿長問卷'):
        with st.container():
            st.markdown("#### C2.腿長")

            col1, col2 = st.columns([2, 3])

            with col1:
                C2L_C2M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                C2L_C2M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                C2L_C2S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                C2L_C2S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                C2M_C2S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                C2M_C2S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if C2L_C2M == '大型犬':
        C2L_C2M_scores = int(C2L_C2M_scores)
    else:
        C2L_C2M_scores = round((1 / int(C2L_C2M_scores)), 3)
    # 1_3
    if C2L_C2S == '大型犬':
        C2L_C2S_scores = int(C2L_C2S_scores)
    else:
        C2L_C2S_scores = round((1 / int(C2L_C2S_scores)), 3)
    # 2_3
    if C2M_C2S == '中型犬':
        C2M_C2S_scores = int(C2M_C2S_scores)
    else:
        C2M_C2S_scores = round((1 / int(C2M_C2S_scores)), 3)

    # AHPy
    leglong_comparisons = {('大型犬', '中型犬'): C2L_C2M_scores,
                          ('大型犬', '小型犬'): C2L_C2S_scores,
                          ('中型犬', '小型犬'): C2M_C2S_scores}
    #
    leglong = ahpy.Compare(name='Leglong', comparisons=leglong_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "C2.腿長",
                               '大型犬': leglong.target_weights["大型犬"],
                               '中型犬': leglong.target_weights["中型犬"],
                               '小型犬': leglong.target_weights["小型犬"]
                               },
                              index=[7]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_leglong = 0.002
    attr_leglong_l = attr_leglong * leglong.target_weights["大型犬"]
    attr_leglong_m = attr_leglong * leglong.target_weights["中型犬"]
    attr_leglong_s = attr_leglong * leglong.target_weights["小型犬"]

    # st.write("各屬性權重 :", leglong.target_weights)
    # st.write("CR :", leglong.consistency_ratio)

    # C3.體長
    with st.form(key='體長問卷'):
        with st.container():
            st.markdown("#### C3.體長")

            col1, col2 = st.columns([2, 3])

            with col1:
                C3L_C3M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                C3L_C3M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                C3L_C3S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                C3L_C3S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                C3M_C3S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                C3M_C3S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if C3L_C3M == '大型犬':
        C3L_C3M_scores = int(C3L_C3M_scores)
    else:
        C3L_C3M_scores = round((1 / int(C3L_C3M_scores)), 3)
    # 1_3
    if C3L_C3S == '大型犬':
        C3L_C3S_scores = int(C3L_C3S_scores)
    else:
        C3L_C3S_scores = round((1 / int(C3L_C3S_scores)), 3)
    # 2_3
    if C3M_C3S == '中型犬':
        C3M_C3S_scores = int(C3M_C3S_scores)
    else:
        C3M_C3S_scores = round((1 / int(C3M_C3S_scores)), 3)

    # AHPy
    bodyleng_comparisons = {('大型犬', '中型犬'): C3L_C3M_scores,
                          ('大型犬', '小型犬'): C3L_C3S_scores,
                          ('中型犬', '小型犬'): C3M_C3S_scores}
    #
    bodyleng = ahpy.Compare(name='Bodyleng', comparisons=bodyleng_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "C3.體長",
                               '大型犬': bodyleng.target_weights["大型犬"],
                               '中型犬': bodyleng.target_weights["中型犬"],
                               '小型犬': bodyleng.target_weights["小型犬"]
                               },
                              index=[8]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_bodyleng = 0.018
    attr_bodyleng_l = attr_bodyleng * bodyleng.target_weights["大型犬"]
    attr_bodyleng_m = attr_bodyleng * bodyleng.target_weights["中型犬"]
    attr_bodyleng_s = attr_bodyleng * bodyleng.target_weights["小型犬"]

    # st.write("各屬性權重 :", bodyleng.target_weights)
    # st.write("CR :", bodyleng.consistency_ratio)

    # D1.散步時間
    with st.form(key='散步時間問卷'):
        with st.container():
            st.markdown("#### D1.散步時間")

            col1, col2 = st.columns([2, 3])

            with col1:
                D1L_D1M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                D1L_D1M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                D1L_D1S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                D1L_D1S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                D1M_D1S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                D1M_D1S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if D1L_D1M == '大型犬':
        D1L_D1M_scores = int(D1L_D1M_scores)
    else:
        D1L_D1M_scores = round((1 / int(D1L_D1M_scores)), 3)
    # 1_3
    if D1L_D1S == '大型犬':
        D1L_D1S_scores = int(D1L_D1S_scores)
    else:
        D1L_D1S_scores = round((1 / int(D1L_D1S_scores)), 3)
    # 2_3
    if D1M_D1S == '中型犬':
        D1M_D1S_scores = int(D1M_D1S_scores)
    else:
        D1M_D1S_scores = round((1 / int(D1M_D1S_scores)), 3)

    # AHPy
    walk_comparisons = {('大型犬', '中型犬'): D1L_D1M_scores,
                          ('大型犬', '小型犬'): D1L_D1S_scores,
                          ('中型犬', '小型犬'): D1M_D1S_scores}
    #
    walk = ahpy.Compare(name='Walk', comparisons=walk_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "D1.散步時間",
                               '大型犬': walk.target_weights["大型犬"],
                               '中型犬': walk.target_weights["中型犬"],
                               '小型犬': walk.target_weights["小型犬"]
                               },
                              index=[9]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_walk = 0.198
    attr_walk_l = attr_walk * walk.target_weights["大型犬"]
    attr_walk_m = attr_walk * walk.target_weights["中型犬"]
    attr_walk_s = attr_walk * walk.target_weights["小型犬"]

    # st.write("各屬性權重 :", walk.target_weights)
    # st.write("CR :", walk.consistency_ratio)

    # D2.睡覺時間
    with st.form(key='睡覺時間問卷'):
        with st.container():
            st.markdown("#### D2.睡覺時間")

            col1, col2 = st.columns([2, 3])

            with col1:
                D2L_D2M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                D2L_D2M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                D2L_D2S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                D2L_D2S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                D2M_D2S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                D2M_D2S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if D2L_D2M == '大型犬':
        D2L_D2M_scores = int(D2L_D2M_scores)
    else:
        D2L_D2M_scores = round((1 / int(D2L_D2M_scores)), 3)
    # 1_3
    if D2L_D2S == '大型犬':
        D2L_D2S_scores = int(D2L_D2S_scores)
    else:
        D2L_D2S_scores = round((1 / int(D2L_D2S_scores)), 3)
    # 2_3
    if D2M_D2S == '中型犬':
        D2M_D2S_scores = int(D2M_D2S_scores)
    else:
        D2M_D2S_scores = round((1 / int(D2M_D2S_scores)), 3)

    # AHPy
    sleep_comparisons = {('大型犬', '中型犬'): D2L_D2M_scores,
                          ('大型犬', '小型犬'): D2L_D2S_scores,
                          ('中型犬', '小型犬'): D2M_D2S_scores}
    #
    sleep = ahpy.Compare(name='Sleep', comparisons=sleep_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "D2.睡覺時間",
                               '大型犬': sleep.target_weights["大型犬"],
                               '中型犬': sleep.target_weights["中型犬"],
                               '小型犬': sleep.target_weights["小型犬"]
                               },
                              index=[10]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_sleep = 0.089
    attr_sleep_l = attr_sleep * sleep.target_weights["大型犬"]
    attr_sleep_m = attr_sleep * sleep.target_weights["中型犬"]
    attr_sleep_s = attr_sleep * sleep.target_weights["小型犬"]

    # st.write("各屬性權重 :", sleep.target_weights)
    # st.write("CR :", sleep.consistency_ratio)


    # D3.訓練時間
    with st.form(key='訓練時間問卷'):
        with st.container():
            st.markdown("#### D3.訓練時間")

            col1, col2 = st.columns([2, 3])

            with col1:
                D3L_D3M = st.radio(
                    "選擇 大型犬 或 中型犬",
                    ('大型犬', '中型犬'), horizontal=True)

            with col2:
                D3L_D3M_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                D3L_D3S = st.radio(
                    "選擇 大型犬 或 小型犬",
                    ('大型犬', '小型犬'), horizontal=True)
            with col2:
                D3L_D3S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！） ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        with st.container():
            col1, col2 = st.columns([2, 3])

            with col1:
                D3M_D3S = st.radio(
                    "選擇 中型犬 或 小型犬",
                    ('中型犬', '小型犬'), horizontal=True)
            with col2:
                D3M_D3S_scores = st.radio(
                    "屬性分數（若選填'1'表示兩屬性同樣重要！）  ",
                    ('1', '2', '3', '4', '5',
                     '6', '7', '8', '9'), horizontal=True)

        original_title = '<p style="font-family:Courier; color:Red; font-size: 12px;">以上填完後，請按下方送出鍵！</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="送出")
    # 1_2
    if D3L_D3M == '大型犬':
        D3L_D3M_scores = int(D3L_D3M_scores)
    else:
        D3L_D3M_scores = round((1 / int(D3L_D3M_scores)), 3)
    # 1_3
    if D3L_D3S == '大型犬':
        D3L_D3S_scores = int(D3L_D3S_scores)
    else:
        D3L_D3S_scores = round((1 / int(D3L_D3S_scores)), 3)
    # 2_3
    if D3M_D3S == '中型犬':
        D3M_D3S_scores = int(D3M_D3S_scores)
    else:
        D3M_D3S_scores = round((1 / int(D3M_D3S_scores)), 3)

    # AHPy
    train_comparisons = {('大型犬', '中型犬'): D3L_D3M_scores,
                          ('大型犬', '小型犬'): D3L_D3S_scores,
                          ('中型犬', '小型犬'): D3M_D3S_scores}
    #
    train = ahpy.Compare(name='Train', comparisons=train_comparisons, precision=3, random_index='saaty')
    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "D3.訓練時間",
                               '大型犬': train.target_weights["大型犬"],
                               '中型犬': train.target_weights["中型犬"],
                               '小型犬': train.target_weights["小型犬"]
                               },
                              index=[11]
                              )

    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)
    attr_train = 0.076
    attr_train_l = attr_train * train.target_weights["大型犬"]
    attr_train_m = attr_train * train.target_weights["中型犬"]
    attr_train_s = attr_train * train.target_weights["小型犬"]

    # st.write("各屬性權重 :", sleep.target_weights)
    # st.write("CR :", sleep.consistency_ratio)
    # st.write("資料：", AHPtable)

    ## 12個屬性權重各別依大中小相加 ##
    l_case_weight_sum = round(attr_homeSpace_l+attr_activityRange_l+attr_numResident_l+
                              attr_Accessory_l+attr_food_l+attr_medical_l+
                              attr_weight_l+attr_leglong_l+attr_bodyleng_l+
                              attr_walk_l+attr_sleep_l+attr_train_l, 3)
    m_case_weight_sum = round(attr_homeSpace_m+attr_activityRange_m+attr_numResident_m+
                              attr_Accessory_m+attr_food_m+attr_medical_m+
                              attr_weight_m+attr_leglong_m+attr_bodyleng_m+
                              attr_walk_m+attr_sleep_m+attr_train_m, 3)
    s_case_weight_sum = round(attr_homeSpace_s+attr_activityRange_s+attr_numResident_s+
                              attr_Accessory_s+attr_food_s+attr_medical_s+
                              attr_weight_s+attr_leglong_s+attr_bodyleng_s+
                              attr_walk_s+attr_sleep_s+attr_train_s, 3)

    # l_case_weight_sumPer = ('{:.2f}%'.format(l_case_weight_sum*100)
    # m_case_weight_sumPer = ('{:.2f}%'.format(m_case_weight_sum*100)
    # s_case_weight_sumPer = ('{:.2f}%'.format(s_case_weight_sum*100)

    # write attributes into DataFrame
    AHPtable_n = pd.DataFrame({'屬性': "總和",
                               '大型犬': l_case_weight_sum,
                               '中型犬': m_case_weight_sum,
                               '小型犬': s_case_weight_sum
                               },
                              index=[12]
                              )
    AHPtable = AHPtable.append(AHPtable_n, ignore_index=False)

    # st.write("資料：", AHPtable)

    d = {'寵物犬體型大小': ["大型犬", "中型犬", "小型犬"],
         '佔比': [l_case_weight_sum, m_case_weight_sum, s_case_weight_sum]
         # '佔比': ['{:.2f}%'.format(l_case_weight_sum*100),
         #          '{:.2f}%'.format(m_case_weight_sum*100),
         #          '{:.2f}%'.format(s_case_weight_sum*100)]
         }
    df_dogLMS = pd.DataFrame(data=d)
    # Bar Chart
    bar_chart = px.bar(df_dogLMS,
                       x = '寵物犬體型大小',
                       y = '佔比',
                       text = '佔比',
                       color_discrete_sequence=['#F63366']*len(df_dogLMS),
                       template = 'plotly_white')
    st.plotly_chart(bar_chart)

    #
    # chart_data = pd.DataFrame(
    #     AHPtable,
    #     columns=["大型犬", "中型犬", "小型犬"])
    #
    # st.bar_chart(chart_data)

    # max(l_case_weight_sum, m_case_weight_sum, s_case_weight_sum)
    # st.write("AHPtable[12]", AHPtable.大型犬[12])

    if l_case_weight_sum == max(l_case_weight_sum, m_case_weight_sum, s_case_weight_sum):
        MLS_test = '大型犬'
    elif m_case_weight_sum == max(l_case_weight_sum, m_case_weight_sum, s_case_weight_sum):
        MLS_test = '中型犬'
    else:
        MLS_test = '小型犬'

    st.write("系統選擇的寵物體型為：", MLS_test)

    # data["犬種"] == variety
    # st.write(data.loc[(data['犬種'].str.contains(variety))])
    df_T = data.loc[(data['狗狗品種'].str.contains(variety))]
    # ind = data.index[data['狗狗品種'].str.contains(variety)].tolist()

    df_F = (data.loc[(data['體型大小'].str.contains(MLS_test)) & (data['寵物性格'].str.contains(dog_character))])

    # st.write("狗狗品種：", df_T)
        # st.write("狗狗品種大小：", df_T.iat[0, 1])
    # st.write("體型大小&寵物性格：", df_F)

    # st.write("體型", df_T.loc[0].iat[1])
    # st.write(df.iat[0,2])
    # st.write("size", df_T.size)
    if df_T.size > 0:
        if (df_T.iat[0, 1] == MLS_test):
            st.markdown("##### **結果**")
            st.write("恭喜您非常了解自己的喜好")
            st.write("適合飼養的品種犬為", variety)
            st.write("以下為其資訊")
            st.write(df_T)
        else:
            st.markdown("##### **結果**")
            st.write("抱歉與您欲飼養之寵物犬體型大小不合")
            st.write("但本系統依據您喜好的寵物犬性格，推薦以下為您可以選擇的寵物犬大小與品種狗種類")
            st.write(df_F)
    else:
        st.write("請填問卷！")
        original_title = '<p style="font-family:Courier; color:Red; font-size: 20px;">請填寫問卷！</p>'
        st.markdown(original_title, unsafe_allow_html=True)

    # 隱藏made with streamlit
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


else:
    st.subheader("About")

    st.markdown("##### **摘要**")
    st.markdown(
        "人類是群居動物，被愛與陪伴是天性。隨著近年社會少子化與高齡化影響，加上現代人生育觀念的改變，導致未婚人口比例增加，越來越多民眾將飼養寵物視為一種滿足需求的方式，其中又以寵物犬作為主要選擇對象，但也間接導致了遊蕩犬數量的提升，根據農委會畜牧處最新調查，2018年至2020年全國遊蕩犬數量呈現6.19%的成長。")
    st.markdown(
        "有鑑於此，本研究欲協助飼主在做決策前，預先評估自身需求及狀況，透過AHP方法建立層級架構圖，分析飼養寵物犬時各體型皆會面臨到的各方面問題，並進行專家問卷來評估兩兩屬性間之權重關係，接著再針對具有飼養寵物犬意願的飼主進行問卷調查，建構出一寵物體型決策系統，減少日後相處不合的情況及降低棄養率，讓寵物犬能夠幸福過完一生。")
    st.markdown("*關鍵字：分析層級程序法、流浪動物、永續發展*")

