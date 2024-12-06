import pytest
from interpreter.interpreter import Interpreter
from interpreter.ast import BinOp, Number, UnaryOp
from interpreter.token import Token, TokenType


@pytest.fixture
def interpreter():
    return Interpreter()


class TestInterpreter:
    @pytest.mark.parametrize("code", [
        "2+=-3",
        "(2+3"
    ])
    def test_invalid_syntax(self, interpreter, code):
        with pytest.raises(SyntaxError):
            interpreter.eval(code)

    def test_binop_invalid_operator(self, interpreter):
        invalid_op = BinOp(
            Number(Token(TokenType.NUMBER, "3")),
            Token(TokenType.OPERATOR, "%"),
            Number(Token(TokenType.NUMBER, "4"))
        )
        with pytest.raises(RuntimeError, match="Invalid operator"):
            interpreter._visit_binop(invalid_op)

    @pytest.mark.parametrize("code, expected", [
        ("BEGIN x:=2++++2 END.", {"x": 4}),
        ("BEGIN x:=2----2 END.", {"x": 4})
    ])
    def test_unaryop(self, interpreter, code, expected):
        assert interpreter.eval(code) == expected

    def test_bad_unaryop(self, interpreter):
        with pytest.raises(RuntimeError):
            interpreter._visit_unaryop(UnaryOp(Token(TokenType.OPERATOR, "&"), Number(Token(TokenType.NUMBER, 4))))

    def test_variable_assignment(self, interpreter):
        result = interpreter.eval("BEGIN x := 10; y := x + 5; END.")
        assert result == {"x": 10.0, "y": 15.0}

    def test_undefined_variable(self, interpreter):
        with pytest.raises(ValueError, match="Variable 'z' is not defined"):
            interpreter.eval("BEGIN x := 2; y := z; END.")

    def test_empty_program(self, interpreter):
        assert interpreter.eval("BEGIN END.") == {}

    def test_complex_expression(self, interpreter):
        code = "BEGIN x := 3 + 4 * (3 + 4); y := (x - 7) / 3; END."
        expected = {"x": 31.0, "y": 8.0}
        assert interpreter.eval(code) == expected

    def test_nested_statements(self, interpreter):
        code = (
            "BEGIN a := 2; b := 3; BEGIN c := a + b; d := c * 3; END; e := d - 2; END."
        )
        expected = {"a": 2.0, "b": 3.0, "c": 5.0, "d": 15.0, "e": 13.0}
        assert interpreter.eval(code) == expected

    def test_assignment_order(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN 2 := x; END.")

    def test_semicolon_handling(self, interpreter):
        code = "BEGIN x := 2; y := 3; z := x + y; END."
        expected = {"x": 2.0, "y": 3.0, "z": 5.0}
        assert interpreter.eval(code) == expected

    @pytest.mark.parametrize("code, expected", [
        ("BEGIN x := 2 + 2; END.", {"x": 4}),
        ("BEGIN x := -3 + 4; END.", {"x": 1})
    ])
    def test_eval(self, interpreter, code, expected):
        assert interpreter.eval(code) == expected

    def test_eval_syntax_error(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN x := 2 +; END.")

    @pytest.mark.parametrize("code, expected", [
        ("BEGIN END.", {}),
        ("BEGIN x:= 3 + 4 * (3 + 4); y:= 3 / 3 - 3 + 4 * ((2 + 2) + (2 + 2)); END.", {'x': 31.0, 'y': 30.0}),
        ("BEGIN y:= 3; BEGIN a := 4; a := a; b := 10 + a + 10 * y / 5; c := a - b; END; x := 12; END.", {'x': 12.0, 'y': 3.0, 'a': 4.0, 'b': 20.0, 'c': -16.0})
    ])
    def test_programs(self, interpreter, code, expected):
        assert interpreter.eval(code) == expected







