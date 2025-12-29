// =====================================
// Study Cafe Kiosk System (Pro Version)
// SignUp + Login + Seat + Logout
// Node.js Console
// =====================================

const readline = require("readline");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const ROWS = 5;
const COLS = 6;
const EMPTY = 0;
const USED = 1;

// 사용자 데이터
const users = {
  admin: "0000"
};

// 좌석 상태
const seats = Array.from({ length: ROWS }, () =>
  Array(COLS).fill(EMPTY)
);

// 사용자별 좌석 기록
const userSeat = {}; // { userId: [r, c] }

// ---------- 입력 유틸 ----------
function ask(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

// ---------- 회원가입 ----------
async function signup() {
  console.log("\n📝 회원가입");
  while (true) {
    const userId = await ask("새 ID 입력 (취소: 0): ");
    if (userId === "0") return;

    if (users[userId]) {
      console.log("❌ 이미 존재하는 ID입니다.");
      continue;
    }

    const password = await ask("새 PW 입력: ");
    users[userId] = password;
    console.log(`✅ 회원가입 완료! (${userId})`);
    return;
  }
}

// ---------- 로그인 ----------
async function login() {
  console.log("\n🔐 로그인");
  for (let i = 0; i < 3; i++) {
    const userId = await ask("ID 입력: ");
    const password = await ask("PW 입력: ");

    if (users[userId] && users[userId] === password) {
      console.log(`✅ ${userId}님 환영합니다.`);
      return userId;
    } else {
      console.log("❌ ID 또는 PW가 틀렸습니다.");
    }
  }
  console.log("🚫 로그인 실패");
  return null;
}

// ---------- 좌석 출력 ----------
function displaySeats() {
  console.log("\n===== 좌석 현황 =====");
  console.log("□ : 빈 좌석   ■ : 사용 중");

  let header = "    ";
  for (let c = 1; c <= COLS; c++) header += c + " ";
  console.log(header);

  for (let r = 0; r < ROWS; r++) {
    let row = `${r + 1}   `;
    for (let c = 0; c < COLS; c++) {
      row += seats[r][c] === EMPTY ? "□ " : "■ ";
    }
    console.log(row);
  }
  console.log("=====================");
}

// ---------- 좌석 선택 ----------
async function selectSeat(user) {
  if (userSeat[user]) {
    console.log("❌ 이미 좌석을 이용 중입니다.");
    return;
  }

  while (true) {
    const rInput = await ask("행 번호 입력 (취소: 0): ");
    const r = Number(rInput);

    if (r === 0) return;

    const c = Number(await ask("열 번호 입력: "));

    const row = r - 1;
    const col = c - 1;

    if (
      row < 0 || col < 0 ||
      row >= ROWS || col >= COLS
    ) {
      console.log("❌ 존재하지 않는 좌석입니다.");
      continue;
    }

    if (seats[row][col] === USED) {
      console.log("❌ 이미 사용 중인 좌석입니다.");
      continue;
    }

    seats[row][col] = USED;
    userSeat[user] = [row, col];
    console.log(`✅ 좌석 배정 완료 (${user})`);
    return;
  }
}

// ---------- 로그아웃 ----------
function logout(user) {
  if (userSeat[user]) {
    const [r, c] = userSeat[user];
    seats[r][c] = EMPTY;
    delete userSeat[user];
    console.log("🔓 로그아웃 완료 (좌석 해제됨)");
  } else {
    console.log("ℹ️ 사용 중인 좌석이 없습니다.");
  }
}

// ---------- 사용자 메뉴 ----------
async function userMenu(user) {
  while (true) {
    console.log(`\n👤 ${user}님 메뉴`);
    console.log("1. 좌석 선택");
    console.log("2. 로그아웃 (자리 반납)");
    console.log("0. 메인 화면");

    const choice = await ask("선택: ");

    if (choice === "1") {
      displaySeats();
      await selectSeat(user);
    } else if (choice === "2") {
      logout(user);
      return;
    } else if (choice === "0") {
      return;
    } else {
      console.log("❌ 올바른 메뉴를 선택하세요.");
    }
  }
}

// ---------- 메인 ----------
async function runKiosk() {
  console.log("📌 스터디카페 키오스크 시작");

  while (true) {
    console.log("\n=== 메인 화면 ===");
    console.log("1. 로그인");
    console.log("2. 회원가입");
    console.log("0. 종료");

    const choice = await ask("선택: ");

    if (choice === "1") {
      const user = await login();
      if (user) await userMenu(user);
    } else if (choice === "2") {
      await signup();
    } else if (choice === "0") {
      console.log("이용해주셔서 감사합니다.");
      rl.close();
      break;
    } else {
      console.log("❌ 올바른 메뉴를 선택하세요.");
    }
  }
}

runKiosk();
