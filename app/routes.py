from flask import Blueprint, request, jsonify, render_template
from .game_engine import TicTacToeGame
from .flags import check_flag_conditions
import time

main = Blueprint('main', __name__)
games = {}

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/start_game', methods=['POST'])
def start_game():
    game_id = request.remote_addr + str(time.time())
    games[game_id] = TicTacToeGame()
    return jsonify({'game_id': game_id, 'board': games[game_id].board})

@main.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    game_id = data.get('game_id')
    moves = data.get('moves', [])
    
    if game_id not in games:
        return jsonify({'error': 'Invalid game ID'}), 400
    
    game = games[game_id]
    result = None
    
    # Single move processing
    if len(moves) == 1:
        x, y = moves[0]
        result = game.make_move(x, y)
    # Multiple moves processing (race condition vulnerability)
    elif len(moves) > 1:
        buffer_overflow_triggered = False
        for x, y in moves:
            if game.game_over:
                break
            # Only skip moves that are truly out of bounds for a 3x3 board
            if x >= 3 or y >= 3 or x < -3 or y < -3:
                buffer_overflow_triggered = True
                continue  # Skip this move, but keep going
            if game.board[x][y] != ' ':
                continue  # Skip occupied cells, but keep going
            game.board[x][y] = 'X'
            game.user_moves += 1
            if game.check_winner('X'):
                game.game_over = True
                game.winner = 'X'
                result = {'winner': 'X', 'message': 'You won!'}
                break
            if game.user_moves >= 3:
                break
        if buffer_overflow_triggered and not result:
            result = {'error': 'Invalid coordinates', 'vulnerability': 'buffer_overflow'}
    
    # Check for flag conditions
    flag_info = check_flag_conditions(game, moves)
    if flag_info:
        if not result:
            result = {}
        result['flag'] = flag_info
    
    return jsonify({
        'board': game.board,
        'result': result,
        'game_over': game.is_game_over()
    })

@main.route('/reset_game', methods=['POST'])
def reset_game():
    data = request.get_json()
    game_id = data.get('game_id')
    
    if game_id in games:
        games[game_id] = TicTacToeGame()
        return jsonify({'status': 'reset', 'board': games[game_id].board})
    
    return jsonify({'error': 'Invalid game ID'}), 400