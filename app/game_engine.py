class TicTacToeGame:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # User is X, machine is O
        self.game_over = False
        self.winner = None
        self.move_count = 0
        self.user_moves = 0
        self.ai_moves = 0
    
    def make_move(self, x, y):
        if self.game_over:
            return {'error': 'Game is already over'}
        if self.user_moves >= 3 or self.ai_moves >= 3:
            self.game_over = True
            return {'error': 'Maximum moves reached. Game over!'}
        
        # Buffer overflow vulnerability - if coordinates are out of bounds
        try:
            if x < 0 or y < 0 or x >= 3 or y >= 3:
                # This is where the buffer overflow vulnerability exists
                # We'll let it pass for the CTF but mark it
                self.move_count += 1
                return {'error': 'Invalid coordinates', 'vulnerability': 'buffer_overflow'}
            
            if self.board[x][y] != ' ':
                return {'error': 'Cell already occupied'}
        except IndexError:
            self.move_count += 1
            return {'error': 'Invalid coordinates', 'vulnerability': 'buffer_overflow'}
        
        # User's move
        self.board[x][y] = 'X'
        self.move_count += 1
        self.user_moves += 1
        
        # Check if user won
        if self.check_winner('X'):
            self.game_over = True
            self.winner = 'X'
            return {'winner': 'X', 'message': 'You won!'}
        
        # Check for draw
        if self.is_board_full() or (self.user_moves >= 3 and self.ai_moves >= 3):
            self.game_over = True
            return {'message': 'Game ended in a draw!'}
        
        # Machine's move (perfect AI that never loses)
        if self.user_moves > self.ai_moves and self.ai_moves < 3:
            self.machine_move()
            self.ai_moves += 1
            
            # Check if machine won
            if self.check_winner('O'):
                self.game_over = True
                self.winner = 'O'
                return {'winner': 'O', 'message': 'Machine won!'}
        
        # End game if both have 3 moves
        if self.user_moves >= 3 and self.ai_moves >= 3:
            self.game_over = True
            return {'message': 'Game ended in a draw!'}
        
        return {'message': 'Move accepted', 'next_player': 'X'}
    
    def machine_move(self):
        # Perfect AI implementation (never loses)
        
        # 1. Check if machine can win in the next move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    if self.check_winner('O'):
                        return
                    self.board[i][j] = ' '  # Undo move
        
        # 2. Check if player can win in the next move and block
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'X'
                    if self.check_winner('X'):
                        self.board[i][j] = 'O'
                        return
                    self.board[i][j] = ' '  # Undo move
        
        # 3. Take center if available
        if self.board[1][1] == ' ':
            self.board[1][1] = 'O'
            return
        
        # 4. Take corners if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for i, j in corners:
            if self.board[i][j] == ' ':
                self.board[i][j] = 'O'
                return
        
        # 5. Take any remaining edge
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for i, j in edges:
            if self.board[i][j] == ' ':
                self.board[i][j] = 'O'
                return
    
    def check_winner(self, player):
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        
        return False
    
    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)
    
    def is_game_over(self):
        return self.game_over or self.is_board_full()