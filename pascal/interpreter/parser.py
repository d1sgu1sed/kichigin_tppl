from .token import TokenType
from .lexer import Lexer
from .ast import BinOp, Number, UnaryOp, Variable, Assignment, Semicolon

class Parser():
    def __init__(self) -> None:
        self._lexer = Lexer()
        self._current_token = None

    def __check_token(self, type_: TokenType):
        if self._current_token:
            if self and self._current_token.type_ == type_:
                self._current_token = self._lexer.next()
        else:
            raise SyntaxError('invalid token order')
        
    def __factor(self):
        token = self._current_token
        if token:
            if token.value == "+":
                self.__check_token(TokenType.OPERATOR)
                return UnaryOp(token, self.__factor())
            if token.value == "-":
                self.__check_token(TokenType.OPERATOR)
                return UnaryOp(token, self.__factor())
            if token.type_ == TokenType.NUMBER:
                self.__check_token(TokenType.NUMBER)
                return Number(token)
            if token.type_ == TokenType.LPAREN:
                self.__check_token(TokenType.LPAREN)
                result = self.__expr()
                self.__check_token(TokenType.RPAREN)
                return result
            if token.type_ == TokenType.IDENTIFIER:
                self.__check_token(TokenType.IDENTIFIER)
                return Variable(token)
        raise SyntaxError("Invalid factor")

    def __term(self):
        result = self.__factor()
        while self._current_token and self._current_token.type_ == TokenType.OPERATOR and self._current_token.value in ["*", "/"]:
            token = self._current_token
            self.__check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.__term())
        return result

    def __expr(self) -> BinOp:
        result = self.__term()
        while self._current_token and self._current_token.type_ == TokenType.OPERATOR and self._current_token.value in ["+", "-"]:
            token = self._current_token
            self.__check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.__term())
        return result

    def __assignment(self):
        variable = self._current_token
        self.__check_token(TokenType.IDENTIFIER)
        self.__check_token(TokenType.ASSIGN)
        return Assignment(variable, self.__expr())

    def __statement(self):
        if self._current_token:
            if self._current_token.type_ == TokenType.BEGIN:
                return self.__complex_statement()
            if self._current_token.type_ == TokenType.IDENTIFIER:
                return self.__assignment()
            if self._current_token.type_ == TokenType.END:
                return None
        raise SyntaxError("Invalid statement")

    def __statement_list(self):
        result = self.__statement()
        if self._current_token and self._current_token.type_ == TokenType.SEMICOL:
            self._current_token = self._lexer.next()
            result = Semicolon(result, self.__statement_list())
        return result
    
    def __complex_statement(self):
        self.__check_token(TokenType.BEGIN)
        result = self.__statement_list()
        self.__check_token(TokenType.END)
        return result
    
    def __program(self):
        result = self.__complex_statement()
        self.__check_token(TokenType.DOT)
        return result

    def parse(self, code):
        self._lexer.init(code)
        self._current_token = self._lexer.next()
        return self.__program()