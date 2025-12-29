import streamlit as st

ROWS, COLS = 5, 6
EMPTY, USED = 0, 1

if "users" not in st.session_state:
    st.session_state.users = {"admin": "0000"}

if "seats" not in st.session_state:
    st.session_state.seats = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

if "user_seat" not in st.session_state:
    st.session_state.user_seat = {}

if "login_user" not in st.session_state:
    st.session_state.login_user = None

def show_seats():
    st.subheader("좌석 현황")
    for r in range(ROWS):
        cols = st.columns(COLS)
        for c in range(COLS):
            if st.session_state.seats[r][c] == EMPTY:
                if cols[c].button("□", key=f"{r}-{c}"):
                    select_seat(r, c)
            else:
                cols[c].button("■", disabled=True, key=f"{r}-{c}")

def select_seat(r, c):
    user = st.session_state.login_user
    if user in st.session_state.user_seat:
        st.warning("이미 좌석 사용 중")
        return
    st.session_state.seats[r][c] = USED
    st.session_state.user_seat[user] = (r, c)
    st.success("좌석 배정 완료")

def logout():
    user = st.session_state.login_user
    if user in st.session_state.user_seat:
        r, c = st.session_state.user_seat[user]
        st.session_state.seats[r][c] = EMPTY
        del st.session_state.user_seat[user]
    st.session_state.login_user = None
    st.rerun()

st.title("스터디카페 웹 키오스크")

if st.session_state.login_user:
    st.write("로그인:", st.session_state.login_user)
    show_seats()
    st.button("로그아웃", on_click=logout)
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
                st.error("로그인 실패")

    else:
        uid = st.text_input("새 ID")
        pw = st.text_input("새 PW", type="password")
        if st.button("회원가입"):
            if uid in st.session_state.users:
                st.error("이미 존재하는 ID")
            else:
                st.session_state.users[uid] = pw
                st.success("회원가입 완료")

