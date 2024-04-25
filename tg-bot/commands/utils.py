from re import fullmatch

NUMBER_PHONE_LENGTH_RU = 11


def is_number_phone(data: str, *lengths):
    return data.startswith('+') and (len(data) - 1) in lengths and data[1:].isdigit()


def is_username(data: str):
    """for tg version 10.3.2"""
    return bool(fullmatch(r'@?\D[_A-Za-z\d]{4,}', data))


def normalize_username(data: str):
    if not is_username(data):
        return data
    return data[1:] if (len(data) > 5 and data.startswith('@')) else data
