import pytest
from interpreter.ast import BinOp, Number, UnaryOp, Variable, Assignment, Semicolon
from interpreter.token import Token, TokenType

class TestAst:
    @pytest.mark.parametrize("node, expected", [
        (Number(Token(TokenType.NUMBER, "1")), "Number (Token(TokenType.NUMBER, 1))"),
        (BinOp(Number(Token(TokenType.NUMBER, "1")), Token(TokenType.OPERATOR, "+"), Number(Token(TokenType.NUMBER, "2"))),
         "BinOp + (Number (Token(TokenType.NUMBER, 1)), Number (Token(TokenType.NUMBER, 2)))"),
        (UnaryOp(Token(TokenType.OPERATOR, "-"), Number(Token(TokenType.NUMBER, "3"))),
         "UnaryOp-Number (Token(TokenType.NUMBER, 3))"),
        (Variable("x"), "Variable(x)"),
        (Assignment(Variable("x"), Number(Token(TokenType.NUMBER, "5"))),
         "AssignmentVariable(x):=Number (Token(TokenType.NUMBER, 5))"),
        (Semicolon(Variable("x"), Variable("y")), "Semicolon(Variable(x), Variable(y))")
    ])
    def test_ast_nodes(self, node, expected):
        assert str(node) == expected