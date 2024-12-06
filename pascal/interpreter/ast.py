from .token import Token

class Node:
    pass

class Number(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"{self.__class__.__name__} ({self.token})"
    
class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"{self.__class__.__name__} {self.op.value} ({self.left}, {self.right})"
    
class UnaryOp(Node):
    def __init__(self, op:Token, expr:Node):
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"{self.__class__.__name__}{self.op.value}{self.expr}"
    
class Variable(Node):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"
    
class Assignment(Node):
    def __init__(self, variable: Variable, expr: Node):
        self.variable = variable
        self.expr = expr

    def __str__(self):
        return f"{self.__class__.__name__}{self.variable}:={self.expr}"
    
class Semicolon(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.__class__.__name__}({self.left}, {self.right})"