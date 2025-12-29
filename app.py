import streamlit as st

# =====================
# 기본 설정
# =====================
ROWS, COLS = 5, 6
EMPTY, USED = 0, 1

# =====================
# 세션 상태 초기화
# =====================
if "users" not in st.session_state:
    st.session_state.users = {"admin": "0000"}

if "seats" not in st.session_state:
    st.session_state.seats = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

if "user_seat" not in st.session_state:
    st.session_state.user_seat = {}  # {user_id: (r, c)}

if "login_user" not in st.session_state:
    st.session_state.login_user = None

# =====================
# 좌석 표시 함수
# =====================
def show_seats():
    st.subheader("좌석 현황 (□: 빈 좌석 / ■: 사용 중)")
    for r in range(ROWS):
        cols = st.columns(COLS)
        for c in range(COLS):
            if st.session_state.seats[r][c] == EMPTY:
                if cols[c].button("□", key=f"{r}-{c}"):
                    select_seat(r, c)
            else:
                cols[c].button("■", disabled=True, key=f"{r}-{c}")

# =====================
# 좌석 선택
# =====================
def select_seat(r, c):
    user = st.session_state.login_user

    if user in st.session_state.user_seat:
        st.warning("이미 좌석을 사용 중입니다.")
        return

    st.session_state.seats[r][c] = USED
    st.session_state.user_seat[user] = (r, c)
    st.success(f"{user}님 좌석이 배정되었습니다.")

# =====================
# 로그아웃
# =====================
def logout():
    user = st.session_state.login_user

    if user in st.session_state.user_seat:
        r, c = st.session_state.user_seat[user]
        st.session_state.seats[r][c] = EMPTY
        del st.session_state.user_seat[user]

    st.session_state.login_user = None
    st.success("로그아웃 완료 (좌석 반납됨)")
    st.rerun()

# =====================
# 메인 화면
# =====================
st.title("📌 스터디카페 웹 키오스크")

# ---------- 로그인 상태 ----------
if st.session_state.login_user:
    st.info(f"👤 로그인 사용자: {st.session_state.login_user}")

    show_seats()

    st.button("🔓 로그아웃", on_click=logout)

# ---------- 비로그인 ----------
else:
    menu = st.radio("메뉴 선택", ["로그인", "회원가입"])

    # 로그인
    if menu == "로그인":
        user_id = st.text_input("ID")
        password = st.text_input("PW", type="password")

        if st.button("로그인"):
            if user_id in st.session_state.users and st.session_state.users[user_id] == password:
                st.session_state.login_user = user_id
                st.success("로그인 성공")
                st.rerun()
            else:
                st.error("ID 또는 PW가 틀렸습니다.")

    # 회원가입
    else:
        new_id = st.text_input("새 ID")
        new_pw = st.text_input("새 PW", type="password")

        if st.button("회원가입"):
            if new_id in st.session_state.users:
                st.error("이미 존재하는 ID입니다.")
            elif new_id == "" or new_pw == "":
                st.warning("ID와 PW를 모두 입력하세요.")
            else:
                st.session_state.users[new_id] = new_pw
                st.success("회원가입 완료! 로그인해주세요.")

