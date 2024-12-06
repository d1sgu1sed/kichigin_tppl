from .parser import Parser
from .ast import Number, BinOp, UnaryOp, Variable, Assignment, Semicolon

class NodeVisitor:
    def visit(self):
        pass

class Interpreter(NodeVisitor):
    def __init__(self):
        self.parser = Parser()
        self.variables = {}

    def visit(self, node):
        if isinstance(node, Number):
            return self._visit_number(node)
        elif isinstance(node, BinOp):
            return self._visit_binop(node)
        elif isinstance(node, UnaryOp):
            return self._visit_unaryop(node)
        elif isinstance(node, Variable):
            return self._visit_variable(node)
        elif isinstance(node, Assignment):
            return self._visit_assignment(node)
        elif isinstance(node, type(None)):
            return None
        elif isinstance(node, Semicolon):
            return self._visit_semicolon(node)
        
    def _visit_number(self, node: Number) -> float:
        return float(node.token.value)

    def _visit_binop(self, node: BinOp):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)
            case "-":
                return self.visit(node.left) - self.visit(node.right)
            case "*":
                return self.visit(node.left) * self.visit(node.right)
            case "/":
                return self.visit(node.left) / self.visit(node.right)
            case _:
                raise RuntimeError("Invalid operator")
            
    def _visit_unaryop(self, node):
        match node.op.value:
            case "+":
                return +self.visit(node.expr)
            case "-":
                return -self.visit(node.expr)
            case _:
                raise RuntimeError("Bad UnaryOp")
            
    def _visit_variable(self, node):
        print(node)
        variable_name = node.name.value
        if variable_name in self.variables.keys():
            return self.variables[variable_name]
        raise ValueError(f"Variable '{variable_name}' is not defined")
    
    def _visit_assignment(self, node):
        if node.variable.value not in self.variables.keys():
            self.variables[node.variable.value] = 0
        self.variables[node.variable.value] = self.visit(node.expr)

    def _visit_semicolon(self, node):
        self.visit(node.left)
        return self.visit(node.right) 

    def eval(self, code):
        tree = self.parser.parse(code)
        self.visit(tree)
        return self.variables