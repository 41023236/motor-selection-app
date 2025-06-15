import streamlit as st
import math

st.set_page_config(page_title="皮帶選型工具", layout="centered")
st.title("皮帶選用計算")

# --- Step 1: 基本條件輸入 ---
st.header("Step 1.已知條件輸入")
col1, col2 = st.columns(2)
with col1:
    Pe = st.number_input("輸入驅動功率 Pe (kW)", value=5.5)
    N = st.number_input("馬達轉速 N (rpm)", value=3000)
    i = st.number_input("速比 i (驅動輪/從動輪)", value=2.0)
    Nx = st.number_input("從動輪轉速 Nx (rpm)", value=1500)
with col2:
    custom_hour = st.checkbox("自行輸入每日工作時間", value=False)
    if custom_hour:
        h = st.number_input("每日工作時間 (hr)", min_value=1.0, max_value=24.0, value=10.0, step=0.5)
    else:
        h = st.selectbox("每日工作時間類型", ["I 類：3~5 小時", "II 類：8~10 小時", "III 類：16~24 小時"], index=1)
        h = {"I 類：3~5 小時": 4.0, "II 類：8~10 小時": 9.0, "III 類：16~24 小時": 18.0}[h]

    use_case = st.selectbox("使用機械類型", [
        "攪拌機、鼓風機(10HP以下)、壓心泵",  # Ko = 1.0
        "風扇、混合機、運輸機",              # Ko = 1.3
        "重型破碎機、木工機械",              # Ko = 1.5
        "鋼軋機、吊車、連續作業設備"           # Ko = 1.8
    ])
    Ko_map = {
        "攪拌機、鼓風機(10HP以下)、壓心泵": 1.0,
        "風扇、混合機、運輸機": 1.3,
        "重型破碎機、木工機械": 1.5,
        "鋼軋機、吊車、連續作業設備": 1.8
    }
    Ko = Ko_map[use_case]

# --- Step 2: 皮帶型號與轉速修正選擇 ---
st.header("Step 2.使用條件與皮帶型號選擇")
col3, col4 = st.columns(2)
with col3:
    auto_belt = st.checkbox("自動建議皮帶型號", value=True)
    if not auto_belt:
        belt_type = st.selectbox("指定皮帶型號", ["3V", "5V", "8V"], index=0)
    else:
        # 簡單依功率推薦（你可改進為查圖）
        if Pe <= 7.5:
            belt_type = "3V"
        elif Pe <= 20:
            belt_type = "5V"
        else:
            belt_type = "8V"
with col4:
    D1 = st.number_input("預估大輪直徑 D1 (mm)", value=90)
    alpha = st.slider("包角 α (deg)", 90, 180, 170)

# --- 修正係數計算與查表模擬 ---
Kt = 1.3  # 假設從表8-11查得
Ks_map = {"3V": 0.94, "5V": 0.96, "8V": 0.97}  # 簡化值
Ka_map = {90: 0.69, 100: 0.74, 110: 0.78, 120: 0.82, 130: 0.86, 140: 0.88, 150: 0.91, 160: 0.93, 170: 0.96, 180: 1.0}

# 套用最接近的角度
closest_angle = min(Ka_map.keys(), key=lambda x: abs(x - alpha))
Ka = Ka_map[closest_angle]
Ks = Ks_map[belt_type]

# 設計馬力
Pd = Pe * Ko * Ks * Kt * Ka
Z = math.ceil(Pd / Pe)  # 示意條數

# --- Step 3: 結果輸出 ---
st.header("Step 3.計算結果")
st.markdown(f"**建議皮帶型號：** {belt_type}")
st.markdown(f"**修正係數：** Ko={Ko}, Ks={Ks}, Kt={Kt}, Kα={Ka}")
st.markdown(f"**設計馬力 Pd：** {Pd:.2f} kW")
st.markdown(f"**預估需求皮帶條數 Z：** {Z} 條")

# --- 說明圖片區 ---
st.header("圖片參考區")
st.image("files/22.png", caption="窄V行皮帶3V的基本額定功率")
st.image("files/23.png", caption="窄V行皮帶3V的基本額定功率(續)")
st.image("files/24.png", caption="窄V行皮帶3V的馬力額定容量")
st.image("files/25.png", caption="窄V行皮帶3V的馬力額定容量(續)")
st.image("files/26.png", caption="皮帶長度修正係數")
st.image("files/27.png", caption="接觸角修正係數")
st.image("files/28.png", caption="皮帶長度規格表")
st.image("files/29.png", caption="過負載修正係數")
st.image("files/30.png", caption="窄V型皮帶型號選擇基準")

