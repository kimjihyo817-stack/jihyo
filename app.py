import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정 (IPython 관련 코드는 모두 삭제했습니다)
st.set_page_config(page_title="오목 프로젝트", layout="centered")

st.title("🎮 진로 탐구: 오목 게임 웹 앱")
st.write("JavaScript Canvas와 Streamlit을 결합한 프로그래밍 프로젝트")

# 2. HTML/JS 소스 코드
omok_html = """
<div id="game-container" style="display: flex; flex-direction: column; align-items: center; font-family: sans-serif;">
    <div style="display: flex; gap: 30px; margin-bottom: 15px; background: #eee; padding: 10px 30px; border-radius: 50px; box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);">
        <div style="text-align: center;">
            <div style="font-size: 0.8em; color: #666;">BLACK</div>
            <div id="score-black" style="font-size: 1.8em; font-weight: bold; color: #000;">0</div>
        </div>
        <div style="font-size: 1.5em; font-weight: bold; color: #aaa; align-self: center;">:</div>
        <div style="text-align: center;">
            <div style="font-size: 0.8em; color: #666;">WHITE</div>
            <div id="score-white" style="font-size: 1.8em; font-weight: bold; color: #444;">0</div>
        </div>
    </div>

    <div style="display: flex; gap: 20px; margin-bottom: 10px;">
        <div id="status" style="font-weight: bold; font-size: 1.2em; color: #333;">흑색 차례입니다.</div>
        <div style="padding: 5px 15px; border: 2px solid #d9534f; border-radius: 5px; background: #fff;">
            <span style="font-size: 0.9em; color: #666;">남은 시간: </span>
            <span id="timer" style="font-size: 1.2em; font-weight: bold; color: #d9534f;">30</span>초
        </div>
    </div>
    
    <div style="position: relative;">
        <canvas id="board" width="450" height="450" style="background: #ffce9e; border: 3px solid #444; cursor: crosshair;"></canvas>
        <div id="win-overlay" style="display: none; position: absolute; top: 0; left: 0; width: 450px; height: 450px; background: rgba(0,0,0,0.6); flex-direction: column; justify-content: center; align-items: center; z-index: 10;">
            <div id="win-text" style="color: white; font-size: 2.5em; font-weight: bold; margin-bottom: 20px; text-align: center;"></div>
            <button onclick="resetGame()" style="padding: 10px 30px; font-size: 1.2em; cursor: pointer; background: #28a745; color: white; border: none; border-radius: 5px;">다음 판 하기</button>
        </div>
    </div>
    
    <button onclick="resetTotalScore()" style="margin-top: 20px; padding: 8px 15px; color: #666; background: #fff; border: 1px solid #ccc; cursor: pointer;">스코어 초기화</button>
</div>

<script>
    const canvas = document.getElementById('board');
    const ctx = canvas.getContext('2d');
    const status = document.getElementById('status');
    const timerDisplay = document.getElementById('timer');
    const winOverlay = document.getElementById('win-overlay');
    const winText = document.getElementById('win-text');
    const scoreBlackDisplay = document.getElementById('score-black');
    const scoreWhiteDisplay = document.getElementById('score-white');
    
    const size = 15;
    const cellSize = 30;
    const padding = 15;
    const LIMIT_TIME = 30;
    
    let board = Array.from({ length: size }, () => Array(size).fill(0));
    let turn = 1; 
    let gameOver = false;
    let timeLeft = LIMIT_TIME;
    let timerInterval = null;
    let scoreBlack = 0;
    let scoreWhite = 0;

    function drawBoard() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#444';
        for (let i = 0; i < size; i++) {
            ctx.beginPath();
            ctx.moveTo(padding, padding + i * cellSize);
            ctx.lineTo(padding + (size - 1) * cellSize, padding + i * cellSize);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(padding + i * cellSize, padding);
            ctx.lineTo(padding + i * cellSize, padding + (size - 1) * cellSize);
            ctx.stroke();
        }
    }

    function drawStone(row, col, color) {
        ctx.beginPath();
        ctx.arc(padding + col * cellSize, padding + row * cellSize, 13, 0, Math.PI * 2);
        const grad = ctx.createRadialGradient(padding + col * cellSize - 4, padding + row * cellSize - 4, 2, padding + col * cellSize, padding + row * cellSize, 13);
        if (color === 1) { grad.addColorStop(0, '#666'); grad.addColorStop(1, '#000'); }
        else { grad.addColorStop(0, '#fff'); grad.addColorStop(1, '#ccc'); }
        ctx.fillStyle = grad;
        ctx.fill();
        ctx.stroke();
    }

    function startTimer() {
        clearInterval(timerInterval);
        timeLeft = LIMIT_TIME;
        timerDisplay.innerText = timeLeft;
        timerInterval = setInterval(() => {
            timeLeft--;
            timerDisplay.innerText = timeLeft;
            if (timeLeft <= 0) endGame(turn === 1 ? 2 : 1, true);
        }, 1000);
    }

    function checkWin(r, c) {
        const directions = [[1,0], [0,1], [1,1], [1,-1]];
        for (let [dr, dc] of directions) {
            let count = 1;
            let nr = r + dr, nc = c + dc;
            while (nr >= 0 && nr < size && nc >= 0 && nc < size && board[nr][nc] === turn) { count++; nr += dr; nc += dc; }
            nr = r - dr; nc = c - dc;
            while (nr >= 0 && nr < size && nc >= 0 && nc < size && board[nr][nc] === turn) { count++; nr -= dr; nc -= dc; }
            if (count >= 5) return true;
        }
        return false;
    }

    function endGame(winner, isTimeOut = false) {
        clearInterval(timerInterval);
        gameOver = true;
        if (winner === 1) { scoreBlack++; scoreBlackDisplay.innerText = scoreBlack; }
        else { scoreWhite++; scoreWhiteDisplay.innerText = scoreWhite; }
        winText.innerText = (winner === 1 ? "흑색" : "백색") + (isTimeOut ? " 시간초과 승리!" : " 승리!");
        winOverlay.style.display = 'flex';
    }

    canvas.onclick = function(e) {
        if (gameOver) return;
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left - padding;
        const y = e.clientY - rect.top - padding;
        const col = Math.round(x / cellSize);
        const row = Math.round(y / cellSize);

        if (row >= 0 && row < size && col >= 0 && col < size && board[row][col] === 0) {
            board[row][col] = turn;
            drawStone(row, col, turn);
            if (checkWin(row, col)) { endGame(turn); }
            else { turn = turn === 1 ? 2 : 1; status.innerText = (turn === 1 ? "흑색" : "백색") + " 차례"; startTimer(); }
        }
    };

    window.resetGame = function() {
        board = Array.from({ length: size }, () => Array(size).fill(0));
        turn = 1; gameOver = false;
        winOverlay.style.display = 'none';
        status.innerText = "흑색 차례";
        drawBoard(); startTimer();
    };

    window.resetTotalScore = function() {
        scoreBlack = 0; scoreWhite = 0;
        scoreBlackDisplay.innerText = "0"; scoreWhiteDisplay.innerText = "0";
        resetGame();
    };

    drawBoard();
    startTimer();
</script>
"""

# 3. Streamlit에 HTML 코드 주입 (height는 넉넉하게 800)
components.html(omok_html, height=800)
