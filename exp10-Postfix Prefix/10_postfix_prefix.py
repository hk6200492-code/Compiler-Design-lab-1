# Topic 10: Intermediate Code Gen – Postfix & Prefix


class ExprNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def to_postfix(node):
    """Generate postfix (Reverse Polish Notation) from AST."""
    if node is None:
        return ""
    if node.left is None and node.right is None:
        return node.val
    left = to_postfix(node.left)
    right = to_postfix(node.right)
    return f"{left} {right} {node.val}"


def to_prefix(node):
    """Generate prefix (Polish Notation) from AST."""
    if node is None:
        return ""
    if node.left is None and node.right is None:
        return node.val
    left = to_prefix(node.left)
    right = to_prefix(node.right)
    return f"{node.val} {left} {right}"


def parse_infix(tokens):
    """Simple recursive descent parser for infix expressions."""
    tokens = list(tokens)
    pos = [0]

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def consume():
        t = tokens[pos[0]]
        pos[0] += 1
        return t

    def parse_expr():
        node = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            node = ExprNode(op, node, parse_term())
        return node

    def parse_term():
        node = parse_factor()
        while peek() in ('*', '/'):
            op = consume()
            node = ExprNode(op, node, parse_factor())
        return node

    def parse_factor():
        t = consume()
        if t == '(':
            node = parse_expr()
            consume()  # ')'
            return node
        return ExprNode(t)

    return parse_expr()


# Test expressions
test_cases = [
    (['(', 'a', '+', 'b', ')', '*', '(', 'c', '-', 'd', ')'],
     "(a + b) * (c - d)"),
    (['a', '+', 'b', '*', 'c'],
     "a + b * c"),
    (['(', 'a', '+', 'b', ')', '/', 'c'],
     "(a + b) / c"),
]

for tokens, infix_str in test_cases:
    tree = parse_infix(tokens)
    print(f"Infix   : {infix_str}")
    print(f"Postfix : {to_postfix(tree)}")
    print(f"Prefix  : {to_prefix(tree)}")
    print()
