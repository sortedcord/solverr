import re
from urllib.parse import urlparse


class Url:
    def __init__(self, location):
        self.location = location
        if not self.is_valid():
            raise ValueError
        self.protocol = location.split("://")[0]
        self.domain = location.split("://")[-1].split("/")[0]

    def is_valid(self) -> bool:
        try:
            result = urlparse(self.location)
            return bool(result.netloc)
        except ValueError:
            return False

def in_latex(string_sequence, delimiter='$') -> tuple[bool, bool]:
    """
    Returns (true, false) if the string's last index is in inside a latex equation or not [enclosed by single delimiter $]
    Returns (true, true) if in block equation [enclosed by double delimiter $$]
    """
    current = False
    block = False
    i = 0
    while i < len(string_sequence)-1:
        if string_sequence[i] == delimiter:
            current = not current
            # If the next char is also delimiter then set it to block equation and skip the next char
            if string_sequence[i+1] == delimiter:
                block = not block
                i += 1
        i += 1

    return current, block


def sanitize_question(body) -> str:
    body = body.lower()

    # Remove newlines
    body = re.sub(r'\n','', body)

    # Remove latex arrows
    body = re.sub(r'\\[a-zA-Z]+arrow', '', body)

    # Sanitize latex keywords
    replace = {
        "\\end{cases}$": "",
        "\\begin{cases}": "",
        "\\left":"",
        "\\right":"",
        "\\frac":"",
        "log_e": "log",
    }

    for key, value in replace.items():
        body = body.replace(key, value)

    body = re.sub(r"""[ ,.`'\\_$^"&:{}|<>\]\[()/]""", '', body.lower())


    # Symbol Replace
    sym_replace = {
        'α': 'alpha',
        '∈': 'belong',
        'β': 'beta',
        '∞': 'infty',
        '°': 'circ',
        '≠': '!=',
        '≥': 'ge',
        '≤': 'le',
        'γ': 'gamma',
        'Δ': 'delta',
        'ε': 'epsilon',
        'θ': 'theta',
        'λ': 'lambda',
        'μ': 'mu',
        'π': 'pi',
        'Σ': 'sum',
        'σ': 'sigma',
        'Ω': 'omega',
        'ω': 'omega',
        '∫': 'int',
        '√': 'sqrt'
}

    for key, value in sym_replace.items():
        body = body.replace(key, value)
    return body

