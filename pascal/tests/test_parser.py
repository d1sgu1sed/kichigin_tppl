import pytest
from interpreter.parser import Parser
from interpreter.token import Token, TokenType

@pytest.fixture
def parser():
    return Parser()


class TestParser:
    def test_check_token(self, parser):
        with pytest.raises(SyntaxError):
            parser._Parser__check_token(Token(TokenType.NUMBER, "True"))