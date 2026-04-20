# Topic 11: Intermediate Code Gen – Quadruple, Triple, Indirect Triple


class ICGGenerator:
    def __init__(self):
        self.temp_count = 0
        self.quads = []       # (op, arg1, arg2, result)
        self.triples = []     # (op, arg1, arg2)
        self.ind_table = []   # indices into triples

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, expr):
        """Parse and generate three-address code from an expression string."""
        self.temp_count = 0
        self.quads.clear()
        self.triples.clear()
        self.ind_table.clear()
        result = self._eval(expr.replace(' ', ''))
        return result

    def _eval(self, expr):
        # Find lowest precedence operator (+ or - first, then * or /)
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            if expr[i] == ')':
                depth += 1
            elif expr[i] == '(':
                depth -= 1
            elif depth == 0 and expr[i] in ('+', '-'):
                return self._binop(expr[:i], expr[i], expr[i + 1:])
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            if expr[i] == ')':
                depth += 1
            elif expr[i] == '(':
                depth -= 1
            elif depth == 0 and expr[i] in ('*', '/'):
                return self._binop(expr[:i], expr[i], expr[i + 1:])
        if expr.startswith('(') and expr.endswith(')'):
            return self._eval(expr[1:-1])
        return expr  # leaf operand

    def _binop(self, left, op, right):
        l = self._eval(left)
        r = self._eval(right)
        t = self.new_temp()
        idx = len(self.triples)
        self.quads.append((op, l, r, t))
        self.triples.append((op, l, r))
        self.ind_table.append(idx)
        return t


gen = ICGGenerator()

expressions = [
    "a + b * c - d",
    "a * b + c * d",
]

for expr in expressions:
    print(f"\nExpression: {expr}")
    gen.generate(expr)

    print("\n  Quadruples:")
    print(f"  {'#':<4} {'Op':<5} {'Arg1':<8} {'Arg2':<8} {'Result'}")
    print("  " + "-" * 35)
    for i, q in enumerate(gen.quads):
        print(f"  {i:<4} {q[0]:<5} {q[1]:<8} {q[2]:<8} {q[3]}")

    print("\n  Triples:")
    print(f"  {'#':<4} {'Op':<5} {'Arg1':<8} {'Arg2'}")
    print("  " + "-" * 28)
    for i, t in enumerate(gen.triples):
        print(f"  ({i}) {t[0]:<5} {t[1]:<8} {t[2]}")

    print("\n  Indirect Triples:")
    print(f"  {'Pos':<6} {'Ptr':<6} {'Instruction'}")
    print("  " + "-" * 30)
    for i, idx in enumerate(gen.ind_table):
        t = gen.triples[idx]
        print(f"  [{i}]  -> ({idx})  {t[0]} {t[1]} {t[2]}")
