from .token import Token, TokenType

class Lexer():
    
    def __init__(self):
        self._pos = 0
        self._text = ""
        self._current_char = None

    def init(self, s:str):
        self._pos = 0
        self._text = s
        self._current_char = self._text[self._pos]

    def __forward(self):
        self._pos += 1
        if self._pos > len(self._text) - 1:
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def __skip(self):
        while (self._current_char is not None and self._current_char.isspace()):
            self.__forward()

    def __number(self):
        result = ""
        while self._current_char is not None and (self._current_char.isdigit() or self._current_char == "."):
            result += self._current_char
            self.__forward()
        return result
    
    def __variable(self):
        result = ""
        while self._current_char is not None and (self._current_char.isalpha() or self._current_char == "_" or self._current_char.isdigit()):
            result += self._current_char
            self.__forward()
        if not result:
            raise SyntaxError("Invalid identifier")
        return result

    def __assignment(self):
        while self._current_char is not None:
            self.__forward()
            if self._current_char.isspace():
                self.__skip()
                continue
            if self._current_char == "=":
                self.__forward()
                return ":="
            raise SyntaxError("bad token")

    def next(self) -> Token:
        while self._current_char:
            if self._current_char.isspace():
                self.__skip()
                continue
            if self._current_char.isdigit():
                return Token(TokenType.NUMBER, self.__number())
            if self._current_char in ["+", "-",  "*", "/"]:
                op = self._current_char
                self.__forward()
                return Token(TokenType.OPERATOR, op)
            if self._current_char == "(":
                val = self._current_char
                self.__forward()
                return Token(TokenType.LPAREN, val)
            if self._current_char == ")":
                val = self._current_char
                self.__forward()
                return Token(TokenType.RPAREN, val)
            if self._current_char == ":":
                return Token(TokenType.ASSIGN, self.__assignment())
            if self._current_char == ";":
                semicolon = self._current_char
                self.__forward()
                return Token(TokenType.SEMICOL, semicolon)
            if self._current_char == "B" and self._text[self._pos:self._pos+5] == "BEGIN":
                self._pos += 5
                self._current_char = self._text[self._pos] if self._pos < len(self._text) else None
                return Token(TokenType.BEGIN, "BEGIN")
            if self._current_char == "E" and self._text[self._pos:self._pos+3] == "END":
                self._pos += 3
                self._current_char = self._text[self._pos] if self._pos < len(self._text) else None
                return Token(TokenType.END, "END")
            if self._current_char == ".":
                val = self._current_char
                self.__forward()
                return Token(TokenType.DOT, val)
            if self._current_char.isalpha() or self._current_char == "_":
                return Token(TokenType.IDENTIFIER, self.__variable()) 
            else:
                raise SyntaxError('bad token')