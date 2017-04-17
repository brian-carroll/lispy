import re

from .primitives import quotes, eof_object, Sym


def build_tokenizer():
    """
    Build up the (unintelligibly complex) tokenizer regex
    """
    backslash_and_another_char = r'\\.'
    anything_except_backslash_or_double_quote = r'[^\\"]'
    string_character = (
        backslash_and_another_char +
        '|' +
        anything_except_backslash_or_double_quote
    )
    non_capturing_group_string_contents = '(?:' + string_character + ')*'

    string_token = '"' + non_capturing_group_string_contents + '"'

    unquote_splicing_token = r",@"
    any_single_char_token = r"[('`,)]"
    comment_token = r";.*"
    atom_token = r'''[^\s('"`,;)]*'''

    capture_token = (
        "(" + unquote_splicing_token +
        "|" + any_single_char_token +
        "|" + string_token +
        "|" + comment_token +
        "|" + atom_token +
        ")"
    )

    ignore_leading_whitespace = r"\s*"
    capture_rest_of_line = r"(.*)"

    return ignore_leading_whitespace + capture_token + capture_rest_of_line


class InPort(object):
    "An input port. Retains a line of chars."

    tokenizer = build_tokenizer()

    def __init__(self, file):
        self.file = file
        self.line = ''

    def next_token(self):
        "Return the next token, reading new text into line buffer if needed."
        while True:
            if self.line == '':
                self.line = self.file.readline()
            if self.line == '':
                return eof_object
            token, self.line = re.match(InPort.tokenizer, self.line).groups()
            if token != '' and not token.startswith(';'):
                return token


def readchar(inport):
    "Read the next character from an input port."
    if inport.line != '':
        ch, inport.line = inport.line[0], inport.line[1:]
        return ch
    else:
        return inport.file.read(1) or eof_object


def read(inport):
    "Read a Scheme expression from an input port."
    def read_ahead(token):
        if '(' == token:
            L = []
            while True:
                token = inport.next_token()
                if token == ')':
                    return L
                else:
                    L.append(read_ahead(token))
        elif ')' == token:
            raise SyntaxError('unexpected )')
        elif token in quotes:
            return [quotes[token], read(inport)]
        elif token is eof_object:
            raise SyntaxError('unexpected EOF in list')
        else:
            return atom(token)
    # body of read:
    token1 = inport.next_token()
    return eof_object if token1 is eof_object else read_ahead(token1)


def atom(token):
    """
    Numbers become numbers
    #t and #f are booleans
    "..." string
    otherwise Symbol.
    """
    if token == '#t':
        return True
    elif token == '#f':
        return False
    elif token[0] == '"':
        return token[1:-1].decode('string_escape')
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            try:
                return complex(token.replace('i', 'j', 1))
            except ValueError:
                return Sym(token)
