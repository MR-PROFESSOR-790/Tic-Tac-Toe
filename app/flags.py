def check_flag_conditions(game, moves):
    # Flag 1: Win by buffer overflow (invalid coordinates)
    if any(x >= 3 or y >= 3 or x < -3 or y < -3 for x, y in moves) and game.winner == 'X':
        return {
        'flag_part_2': 'BUF53R_0V3RFL0W_',
        'message': 'You exploited the buffer overflow!',
        }

    # Flag 2: Win by negative index (wraparound)
    if any((x < 0 and x >= -3) or (y < 0 and y >= -3) for x, y in moves) and game.winner == 'X':
        return {
        'flag_part_3': 'NEGATIVE_INDEX}',
        'message': 'You exploited the negative index bug!'
        }

    # Flag 3: Win by race condition (sending all moves at once)
    if len(moves) > 1 and game.winner == 'X':
        return {
            'flag_part_1': 'CTF{R4C3_C0ND1T10N_',
            'message': 'You found the race condition vulnerability!'
        }
    
    return None