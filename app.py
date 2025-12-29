import streamlit as st

ROWS, COLS = 5, 6
EMPTY, USED = 0, 1

# =====================
# 세션 초기화
# =====================
if "users" not in st.session_state:
    st.session_state.users = {"admin": "0000"}

if "seats" not in st.session_state:
    st.session_state.seats = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

if "user_seat" not in st.session_state:
    st.session_state.user_seat = {}  # {user: (r, c)}

if "login_user" not in st.session_state:
    st.session_state.login_user = None

# =====================
# 좌석 선택 처리 (키오스크 핵심)
# =====================
def select_seat(r, c):
    user = st.session_state.login_user

    if user in st.session_state.user_seat:
        st.warning("이미 좌석을 이용 중입니다.")
        return

    st.session_state.seats[r][c] = USED
    st.session_state.user_seat[user] = (r, c)

    st.success(f"{user}님 좌석 배정 완료!")
    st.info("이용이 시작되었습니다. 다음 이용자를 위해 로그아웃합니다.")

    # 🔥 키오스크 핵심: 자동 로그아웃
    st.session_state.login_user = None
    st.rerun()

# =====================
# 좌석 표시
# =====================
def show_seats():
    st.subheader("좌석 선택")
    for r in range(ROWS):
        cols = st.columns(COLS)
        for c in range(COLS):
            if st.session_state.seats[r][c] == EMPTY:
                cols[c].button("□", key=f"{r}-{c}", on_click=select_seat, args=(r, c))
            else:
                cols[c].button("■", disabled=True, key=f"{r}-{c}")

# =====================
# 메인 화면
# =====================
st.title("📌 스터디카페 키오스크")

# ---------- 로그인 상태 ----------
if st.session_state.login_user:
    st.write(f"👤 사용자: {st.session_state.login_user}")
    show_seats()

# ---------- 비로그인 ----------
else:
    menu = st.radio("메뉴", ["로그인", "회원가입"])

    if menu == "로그인":
        uid = st.text_input("ID")
        pw = st.text_input("PW", type="password")

        if st.button("로그인"):
            if uid in st.session_state.users and st.session_state.users[uid] == pw:
                st.session_state.login_user = uid
                st.rerun()
            else:
                st.error("ID 또는 PW가 틀렸습니다.")

    else:
        uid = st.text_input("새 ID")
        pw = st.text_input("새 PW", type="password")

        if st.button("회원가입"):
            if uid in st.session_state.users:
                st.error("이미 존재하는 ID입니다.")
            elif uid == "" or pw == "":
                st.warning("ID와 PW를 모두 입력하세요.")
            else:
                st.session_state.users[uid] = pw
                st.success("회원가입 완료! 로그인해주세요.")
