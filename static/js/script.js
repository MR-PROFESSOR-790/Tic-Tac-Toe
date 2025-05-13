document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('board');
    const statusElement = document.getElementById('status');
    const flagDisplayElement = document.getElementById('flag-display');
    const resetBtn = document.getElementById('reset-btn');
    
    let gameId = null;
    let gameBoard = null;
    let isGameOver = false;
    let userMoves = 0;
    let aiMoves = 0;
    let turn = 'user'; // user starts
    
    // Initialize the game
    async function initGame() {
        userMoves = 0;
        aiMoves = 0;
        turn = 'user';
        isGameOver = false;
        try {
            const response = await fetch('/start_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            gameId = data.game_id;
            gameBoard = data.board;
            updateBoard();
            statusElement.textContent = 'Your move!';
            flagDisplayElement.classList.remove('show');
        } catch (error) {
            console.error('Error starting game:', error);
        }
    }
    
    // Update the board display
    function updateBoard() {
        const cells = document.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            const row = Math.floor(index / 3);
            const col = index % 3;
            const value = gameBoard[row][col];
            cell.className = 'cell';
            if (value === 'X') {
                cell.classList.add('x');
                cell.textContent = 'X';
            } else if (value === 'O') {
                cell.classList.add('o');
                cell.textContent = 'O';
            } else {
                cell.textContent = '';
            }
        });
    }
    
    // Handle cell click
    async function handleCellClick(event) {
        if (isGameOver || turn !== 'user' || userMoves >= 3) return;
        const cell = event.target;
        const index = parseInt(cell.dataset.index);
        const row = Math.floor(index / 3);
        const col = index % 3;
        if (gameBoard[row][col] !== ' ') return;
        try {
            // User move
            const response = await fetch('/make_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    game_id: gameId,
                    moves: [[row, col]]
                })
            });
            const data = await response.json();
            gameBoard = data.board;
            updateBoard();
            userMoves++;
            if (data.result && data.result.winner) {
                handleGameResult(data.result);
                return;
            }
            if (userMoves >= 3) {
                isGameOver = true;
                statusElement.textContent = 'Game over!';
                return;
            }
            // AI move
            turn = 'ai';
            statusElement.textContent = 'Machine is thinking...';
            setTimeout(aiMove, 600);
        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    async function aiMove() {
        if (isGameOver || aiMoves >= 3) return;
        // Find first empty cell for AI (let backend handle AI logic)
        try {
            // Send a dummy move to trigger AI (no user move, just let backend do its turn)
            // But our backend expects a user move, so we need to let backend handle both
            // Instead, after user move, backend already does AI move, so just update board
            // So, we just need to update the turn
            // But to be sure, let's fetch the board again
            const response = await fetch('/start_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            // Actually, the backend already does the AI move after user, so just update state
            aiMoves++;
            turn = 'user';
            statusElement.textContent = 'Your move!';
            updateBoard();
            if (aiMoves >= 3) {
                isGameOver = true;
                statusElement.textContent = 'Game over!';
            }
        } catch (error) {
            console.error('Error with AI move:', error);
        }
    }

    // Handle game result
    function handleGameResult(result) {
        isGameOver = true;
        statusElement.textContent = result.message || 'Game over!';
        if (result.winner) {
            // Highlight winning cells
            const winningCells = findWinningCells();
            winningCells.forEach(index => {
                document.querySelector(`[data-index="${index}"]`).classList.add('winning-cell');
            });
        }
        if (result.flag) {
            flagDisplayElement.textContent = result.flag.flag_part;
            flagDisplayElement.classList.add('show');
        }
    }

    // Find winning cells
    function findWinningCells() {
        const winningCombos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
            [0, 4, 8], [2, 4, 6] // diagonals
        ];
        for (const combo of winningCombos) {
            const [a, b, c] = combo;
            const rowA = Math.floor(a / 3);
            const colA = a % 3;
            const rowB = Math.floor(b / 3);
            const colB = b % 3;
            const rowC = Math.floor(c / 3);
            const colC = c % 3;
            if (gameBoard[rowA][colA] === 'X' &&
                gameBoard[rowB][colB] === 'X' &&
                gameBoard[rowC][colC] === 'X') {
                return combo;
            }
        }
        return [];
    }

    // Reset game
    async function resetGame() {
        await initGame();
    }

    // Event listeners
    initGame();
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });
    resetBtn.addEventListener('click', resetGame);
});