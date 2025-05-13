def validate_coords(coord):
    try:
        x, y = coord
        return 0 <= x < 3 and 0 <= y < 3
    except Exception:
        return False
