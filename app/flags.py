def check_flag_conditions(game, moves):
    # Flag 1: Win by buffer overflow (invalid coordinates)
    if any(x >= 3 or y >= 3 or x < -3 or y < -3 for x, y in moves) and game.winner == 'X':
        return {
        'flag_part': 'BUF53R_0V3RFL0W_',
        'message': 'You exploited the buffer overflow!'
        }

    # Flag 2: Win by negative index (wraparound)
    if any((x < 0 and x >= -3) or (y < 0 and y >= -3) for x, y in moves) and game.winner == 'X':
        return {
        'flag_part': 'NEGATIVE_INDEX}',
        'message': 'You exploited the negative index bug!'
        }

    # Flag 3: Win by race condition (sending all moves at once)
    if len(moves) > 1 and game.winner == 'X':
        return {
            'flag_part': 'CTF{R4C3_C0ND1T10N_',
            'message': 'You found the race condition vulnerability!'
        }
    # ... rest unchanged ...
    
    # Flag 4: Win by sending duplicate moves (same cell more than once in a single request)
    seen = set()
    duplicates = False
    for x, y in moves:
        if (x, y) in seen:
            duplicates = True
            break
        seen.add((x, y))
    if duplicates and game.winner == 'X':
        return {
            'flag_part': 'DUPLICATE_CELL}',
            'message': 'You exploited the duplicate cell race condition!'
        }
    
    # Flag 4: Win by forcing a draw (which counts as beating the machine)
    if game.is_game_over() and game.winner is None:
        # Check if user played optimally to force a draw
        user_moves = [moves[i] for i in range(0, len(moves), 2)]  # User moves are every other
        if len(user_moves) >= 3 and all(0 <= x < 3 and 0 <= y < 3 for x, y in user_moves):
            # Check if user played a perfect defensive game
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
            center = (1, 1)
            
            # User must have played center and at least two corners/edges
            if center in user_moves and (
                sum(1 for move in user_moves if move in corners) >= 2 or
                sum(1 for move in user_moves if move in edges) >= 2
            ):
                return {
                    'flag_part': 'DRAW_F0RC3D}',
                    'message': 'You forced a draw against the perfect AI!'
                }
    
    return None