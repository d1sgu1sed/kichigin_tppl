def is_operator(token):
    return token in ['+', '-', '*', '/']

def prefix_to_infix(expression: str) -> str:
    tokens = expression.split()[::-1]
    stack = []

    for token in tokens:
        if token.isdigit():
            stack.append(token)
        elif is_operator(token):
            if len(stack) < 2:
                raise ValueError("Мало операндов.")
            oper1 = stack.pop()
            oper2 = stack.pop()
            stack.append(f"({oper1} {token} {oper2})")
        else:
            raise ValueError(f"Неправильный операнд.")
    
    if len(stack) != 1:
        raise ValueError("Неправильное выражение.")
    
    return stack[0]
