def to_number(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError("Input must be a valid number")
