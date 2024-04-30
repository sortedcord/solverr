def in_latex(string_sequence, delimeter='$') -> tuple[bool, bool]:
    """
    Returns (true, false) if the string's last index is in inside a latex equation or not [enclosed by single delimiter $]
    Returns (true, true) if in block equation [enclosed by double delimiter $$]
    """
    current = False
    block = False
    i = 0
    while i < len(string_sequence)-1:
        if string_sequence[i] == delimeter:
            current = not current
            # If the next char is also delimiter then set it to block equation and skip the next char
            if string_sequence[i+1] == delimeter:
                block = not block
                i += 1
        i += 1

    return current, block
