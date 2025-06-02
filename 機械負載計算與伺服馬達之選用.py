import streamlit as st
import math

st.set_page_config(page_title="馬達選型工具", layout="centered")
st.title("馬達選型一頁式計算工具")

# --- 步驟 1 ---
st.header("Step 1.決定機械系統參數")
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("參數輸入區")

    # 負載質量 M
    M_option = st.selectbox("負載質量 M (kg)", [1, 3, 5, 10, "自訂"], index=2)
    if M_option == "自訂":
        M = st.number_input("請輸入自訂的 M 值 (kg)", value=5.0, min_value=0.0)
    else:
        M = float(M_option)

    # 滾珠螺桿節距 p
    p_option = st.selectbox("滾珠螺桿節距 p (mm)", [5, 10, 20, "自訂"], index=1)
    if p_option == "自訂":
        p = st.number_input("請輸入自訂的 p 值 (mm)", value=10.0, min_value=0.1)
    else:
        p = float(p_option)

    # 滾珠螺桿外徑 D
    D_option = st.selectbox("滾珠螺桿外徑 D (mm)", [10, 20, 25, "自訂"], index=1)
    if D_option == "自訂":
        D = st.number_input("請輸入自訂的 D 值 (mm)", value=20.0, min_value=0.1)
    else:
        D = float(D_option)

    # 滾珠螺桿慣性質量 Mb
    Mb_option = st.selectbox("滾珠螺桿慣性質量 Mb (kg)", [1, 2, 3, 5, "自訂"], index=2)
    if Mb_option == "自訂":
        Mb = st.number_input("請輸入自訂的 Mb 值 (kg)", value=3.0, min_value=0.0)
    else:
        Mb = float(Mb_option)

    # 滾珠螺桿摩擦係數 μ
    mu_option = st.selectbox("滾珠螺桿摩擦係數 μ", [0.05, 0.1, 0.15, "自訂"], index=1)
    if mu_option == "自訂":
        mu = st.number_input("請輸入自訂的 μ 值", value=0.1, min_value=0.0)
    else:
        mu = float(mu_option)

    # 減速比 G
    G_option = st.selectbox("減速比 G", [1, 2, 5, 10, "自訂"], index=0)
    if G_option == "自訂":
        G = st.number_input("請輸入自訂的 G 值", value=1.0, min_value=0.01)
    else:
        G = float(G_option)

    # 無單位效率 γ
    gamma_option = st.selectbox("無單位效率 γ", [0.8, 0.9, 1, "自訂"], index=2)
    if gamma_option == "自訂":
        gamma = st.number_input("請輸入自訂的 γ 值", value=1.0, min_value=0.01, max_value=1.0)
    else:
        gamma = float(gamma_option)

    # 重力加速度（固定）
    g = 9.8

with col2:
    st.subheader("流程圖示區")
    st.image("files/3.png", caption="決定機械系統")

# --- 步驟 2 ---
st.header("Step 2.決定動作模式參數")
col3, col4 = st.columns([1, 1])
with col3:
    st.subheader("參數輸入區")
    motion_mode = st.selectbox("動作模式", ["三角形", "梯形", "α加速度"], index=1)
    V = st.number_input("最大移動速度 V (mm/s)", value=300)
    L = st.number_input("行程距離 L (mm)", value=360)
    tS = st.number_input("行程週期時間 tS (s)", value=1.4)
    tA = st.number_input("加減速時間 tA (s)", value=0.2)
    AP = st.number_input("定位精度 AP (mm)", value=0.01)
with col4:
    st.subheader("動作模式圖示")
    if motion_mode == "三角形":
        st.image("files/motion_triangle.png", caption="三角形動作模式")
    elif motion_mode == "梯形":
        st.image("files/motion_trapezoid.png", caption="梯形動作模式")
    elif motion_mode == "α加速度":
        st.image("files/motion_alpha.png", caption="α加速度動作模式")

# --- 步驟 3～9 ---
st.header("Step 3.計算慣量")
st.image("files/5.png", caption="步驟3：慣量計算")

st.header("Step 4.計算負載扭矩")
st.image("files/6.png", caption="步驟4：負載扭矩公式")

st.header("Step 5.計算轉速")
st.image("files/7.png", caption="步驟5：轉速計算")

st.header("Step 6.初步選定馬達")
st.image("files/8.png", caption="步驟6：選型與判斷")

st.header("Step 7.計算加減速扭矩")
st.image("files/9.png", caption="步驟7：加速度扭矩圖示")

st.header("Step 8.計算峰值與有效扭矩")
st.image("files/10.png", caption="步驟8：有效扭矩圖與區段")

st.header("Step 9.特性條件檢查")
if st.button("執行計算"):
    Jb = Mb * (D / 1000)**2 / 8
    Jw = M * (p / (2 * math.pi))**2 * 1e-6
    JL = G**2 * (Jb + Jw)
    TW = M * g * mu * p / (2 * math.pi) * 1e-3
    TL = TW / (G * gamma)
    N = 60 * V / (p * G)
    JM = 1.23e-5
    Tm = 0.637
    inertia_ratio = JL / JM
    TA = 2 * math.pi * N / 60 * JL / tA
    T1 = TA + TL
    T2 = TL
    T3 = TL - TA
    T_rms = math.sqrt((T1**2 * tA + T2**2 * (tS - 2*tA) + T3**2 * tA) / tS)
    R = int((p * G) / AP)

    st.subheader("計算結果彙總")
    st.write(f"總等效慣量 JL = {JL:.2e} kg·m²")
    st.write(f"負載扭矩 TL = {TL:.4f} N·m")
    st.write(f"加速度扭矩 TA = {TA:.4f} N·m")
    st.write(f"轉速 N = {N:.0f} rpm")
    st.write(f"峰值扭矩 T1 = {T1:.4f} N·m")
    st.write(f"有效扭矩 Trms = {T_rms:.4f} N·m")

    st.subheader("判定結果")
    st.image("files/11.png", caption="步驟9：條件檢查與整理")
    st.write(f"慣量比 JL/JM = {inertia_ratio:.2f} {'通過' if inertia_ratio <= 30 else '過大'}")
    st.write(f"有效扭矩 Trms {'通過' if T_rms < Tm * 0.8 else '超出'}")
    st.write(f"峰值扭矩 T1 {'通過' if T1 < 1.91 * 0.8 else '超出'}")
    st.write(f"最大轉速 {'通過' if N <= 3000 else '超出'}")
    st.write(f"解析度需求 = {R} (脈衝/轉) {'通過' if R <= 2048 else '請使用高解析度編碼器'}")

# --- 補充教學與公式區 ---
st.header("附錄：常用公式與參考圖")
with st.expander("動作模式公式總覽"):
    st.image("files/12.png")
    st.image("files/13.png")

with st.expander("慣量計算公式"):
    st.image("files/14.png")
    st.image("files/15.png")

with st.expander("扭矩計算相關"):
    st.image("files/16.png")
    st.image("files/17.png")
    st.image("files/18.png")

with st.expander("精度與轉速公式"):
    st.image("files/19.png")
    st.image("files/20.png")
