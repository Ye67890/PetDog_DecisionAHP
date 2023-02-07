# 以AHP法協助飼主做寵物犬體型最佳配適選擇
協助飼主找尋適合自身飼養的寵物犬大小，減少寵物犬的棄養率。

### 內容簡介
分析層級程序法(Analytic Hierarchy Process, AHP)最早是由匹茲堡大學教授(Thomas L. Saaty)於1971年所提出的一套理論，主要運用在不確定情況且具有多屬性評估準則的決策問題上，而由於理論簡單、具實用性以及容易操作，目前已被廣泛應用。
AHP方法發展目的就是透過樹狀層級結構將複雜問題系統化，首先將決策元素以不同維度給予層級劃分，並將問題加以層級與架構來分解成多個子問題，最後透過量化方式分別比較進行評估後統整，讓決策者能夠以結構性方式來分析問題，從中選擇出最適當的方案，以此降低錯誤決策的風險(鄧振源、曾國雄，1989)。

**以下為本研究建構之樹狀層級架構**
 ![image](https://user-images.githubusercontent.com/81035275/217170054-4f81ce1f-330f-42a1-900e-b042846e5a7b.png)
 
**以下為根本目標與屬性之定義**
 ![image](https://user-images.githubusercontent.com/81035275/217171029-8fb5b5c0-933b-42ed-89a6-e52af0a9421b.png)

透過建構各屬性之大中小型犬兩兩進行比較，最後將12個屬性中的大中小型犬分數個別加總，如下圖
<img width="698" alt="截圖 2023-02-07 下午3 08 32" src="https://user-images.githubusercontent.com/81035275/217172618-40556513-e63c-4f24-82a1-f000d2784b69.png">

分數最高則為系統推薦飼養之寵物犬體型大小。

以下連結為透過[Streamlit](https://streamlit.io/)建構之Web app
+ https://ye67890-petdog-decisionahp-st-petdogahp-4kuysu.streamlit.app/
