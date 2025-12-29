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
# 함수 영역
# =====================

# 🔓 화면 전환용 로그아웃 (좌석 유지)
def logout_only():
    st.session_state.login_user = None
    st.rerun()

# 🪑 좌석 선택 (키오스크 핵심)
def select_seat(r, c):
    user = st.session_state.login_user

    if user in st.session_state.user_seat:
        st.warning("이미 좌석을 사용 중입니다.")
        return

    st.session_state.seats[r][c] = USED
    st.session_state.user_seat[user] = (r, c)

    st.success(f"{user}님 좌석 배정 완료!")
    st.info("다음 이용자를 위해 화면이 초기화됩니다.")

    # 좌석은 유지, 로그인만 해제
    logout_only()

# 🪑 좌석 표시
def show_seats():
    st.subheader("좌석 선택 (□: 빈 좌석 / ■: 사용 중)")
    for r in range(ROWS):
        cols = st.columns(COLS)
        for c in range(COLS):
            if st.session_state.seats[r][c] == EMPTY:
                cols[c].button("□", key=f"{r}-{c}", on_click=select_seat, args=(r, c))
            else:
                cols[c].button("■", disabled=True, key=f"{r}-{c}")

# 🚪 퇴실 처리 (자리 반납)
def checkout(user_id):
    if user_id in st.session_state.user_seat:
        r, c = st.session_state.user_seat[user_id]
        st.session_state.seats[r][c] = EMPTY
        del st.session_state.user_seat[user_id]
        st.success(f"{user_id} 퇴실 처리 완료")
    else:
        st.warning("해당 사용자는 좌석을 사용 중이 아닙니다.")

# =====================
# UI 시작
# =====================
st.title("📌 스터디카페 키오스크")

# ---------- 로그인 상태 ----------
if st.session_state.login_user:
    st.info(f"👤 현재 사용자: {st.session_state.login_user}")
    show_seats()

# ---------- 비로그인 ----------
else:
    menu = st.radio("메뉴 선택", ["로그인", "회원가입", "퇴실(관리자)"])

    # 🔐 로그인
    if menu == "로그인":
        uid = st.text_input("ID")
        pw = st.text_input("PW", type="password")

        if st.button("로그인"):
            if uid in st.session_state.users and st.session_state.users[uid] == pw:
                st.session_state.login_user = uid
                st.rerun()
            else:
                st.error("ID 또는 PW가 틀렸습니다.")

    # 📝 회원가입
    elif menu == "회원가입":
        uid = st.text_input("새 ID")
        pw = st.text_input("새 PW", type="password")

        if st.button("회원가입"):
            if uid == "" or pw == "":
                st.warning("ID와 PW를 모두 입력하세요.")
            elif uid in st.session_state.users:
                st.error("이미 존재하는 ID입니다.")
            else:
                st.session_state.users[uid] = pw
                st.success("회원가입 완료! 로그인해주세요.")

    # 🚪 퇴실 (관리자/퇴실 키오스크)
    else:
        st.subheader("퇴실 처리")
        out_id = st.text_input("퇴실할 ID")

        if st.button("퇴실"):
            checkout(out_id)
