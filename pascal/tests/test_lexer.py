import pytest
from interpreter.lexer import Lexer
from interpreter.token import Token, TokenType

@pytest.fixture
def lexer():
    return Lexer()


class TestLexer:
    def test_create_var(self, lexer):
        with pytest.raises(SyntaxError):
            lexer._Lexer__variable()

    def test_assignment_bad_token(self, lexer):
        lexer.init("  :-")
        with pytest.raises(SyntaxError):
            lexer._Lexer__assignment()

    def test_next(self, lexer):
        lexer.init("BEGIN x:=10; END.")
        tokens = [
            Token(TokenType.BEGIN, "BEGIN"),
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.ASSIGN, ":="),
            Token(TokenType.NUMBER, "10"),
            Token(TokenType.SEMICOL, ";"),
            Token(TokenType.END, "END"),
            Token(TokenType.DOT, ".")
        ]
        for token in tokens:
            assert str(lexer.next()) == str(token)

    def test_next_bad_token(self, lexer):
        lexer.init("BEGIN ^")
        assert str(lexer.next()) == str(Token(TokenType.BEGIN, "BEGIN"))
        with pytest.raises(SyntaxError):
            lexer.next()