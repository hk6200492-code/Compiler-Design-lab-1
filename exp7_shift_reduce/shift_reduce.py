"""
Experiment 7: Shift-Reduce Parsing
Compiler Design Lab (18CSC304J)
SRM Institute of Science and Technology
"""


def shift_reduce_parse(grammar_rules: list, start_symbol: str,
                       input_string: str) -> bool:
    """
    Simulates a bottom-up Shift-Reduce parser.

    Parameters
    ----------
    grammar_rules  : list of (lhs, rhs_string)
                     e.g. [('E','E+E'), ('E','E*E'), ('E','id')]
    start_symbol   : str  e.g. 'E'
    input_string   : str  e.g. 'id+id*id'
                     Multi-char tokens separated by spaces are supported.

    Returns
    -------
    bool: True if input is accepted, False otherwise.
    """
    # Tokenize: split on spaces if present, else treat each char as a token
    tokens = input_string.split() if ' ' in input_string else list(input_string)
    tokens.append('$')

    stack = ['$']
    idx   = 0

    col1, col2, col3 = 32, 22, 30
    print(f"\n{'Stack':<{col1}} {'Input':<{col2}} Action")
    print("─" * (col1 + col2 + col3))

    max_steps = 500
    steps     = 0

    while steps < max_steps:
        steps += 1
        stk_str = " ".join(stack)
        inp_str = " ".join(tokens[idx:])

        # ── Try to REDUCE ────────────────────────────────────────────
        reduced = False
        for lhs, rhs in grammar_rules:
            rhs_tokens = rhs.split() if ' ' in rhs else list(rhs)
            rhs_len    = len(rhs_tokens)

            # Stack must have at least '$' + rhs
            if len(stack) < rhs_len + 1:
                continue

            stack_top = stack[-rhs_len:]
            if stack_top == rhs_tokens:
                action = f"Reduce  {lhs} → {rhs}"
                print(f"{stk_str:<{col1}} {inp_str:<{col2}} {action}")
                for _ in rhs_tokens:
                    stack.pop()
                stack.append(lhs)
                reduced = True
                break

        if reduced:
            # Check ACCEPT condition
            if (stack == ['$', start_symbol] and tokens[idx] == '$'):
                stk_str = " ".join(stack)
                print(f"{stk_str:<{col1}} {'$':<{col2}} ACCEPT ✓")
                return True
            continue

        # ── SHIFT ────────────────────────────────────────────────────
        current = tokens[idx]
        if current == '$':
            print(f"{stk_str:<{col1}} {'$':<{col2}} ERROR — unexpected end of input")
            return False

        action = f"Shift   '{current}'"
        print(f"{stk_str:<{col1}} {inp_str:<{col2}} {action}")
        stack.append(current)
        idx += 1

    print("ERROR: Max steps exceeded. Grammar may be ambiguous.")
    return False


def parse_grammar_rules() -> list:
    """Read grammar rules interactively."""
    print("Enter grammar rules as  LHS -> RHS  (one per line). Type 'done' to finish.")
    rules = []
    while True:
        line = input("  > ").strip()
        if line.lower() == 'done':
            break
        if '->' not in line:
            print("  Invalid format. Use  LHS -> RHS")
            continue
        lhs, rhs = line.split('->', 1)
        rules.append((lhs.strip(), rhs.strip()))
    return rules


if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 7: SHIFT-REDUCE PARSING")
    print("=" * 60)

    # ── Example 1: Simple expression grammar ────────────────────────
    g1 = [
        ('E', 'E+E'),
        ('E', 'E*E'),
        ('E', '(E)'),
        ('E', 'i'),
    ]
    print("\nGrammar Rules:")
    for lhs, rhs in g1:
        print(f"  {lhs} -> {rhs}")

    test_inputs = ['i+i*i', 'i*i+i', '(i+i)*i', 'i']
    for inp in test_inputs:
        print(f"\n{'─'*60}")
        print(f"Input string: '{inp}'")
        result = shift_reduce_parse(g1, 'E', inp)
        print(f"→ {'ACCEPTED' if result else 'REJECTED'}")

    # ── Example 2: Grammar with multi-char tokens (id) ───────────────
    g2 = [
        ('E', 'E + T'),
        ('E', 'T'),
        ('T', 'T * F'),
        ('T', 'F'),
        ('F', 'id'),
    ]
    print(f"\n{'='*60}")
    print("Grammar Rules (multi-char tokens):")
    for lhs, rhs in g2:
        print(f"  {lhs} -> {rhs}")

    inp2 = "id + id * id"
    print(f"\n{'─'*60}")
    print(f"Input string: '{inp2}'")
    result2 = shift_reduce_parse(g2, 'E', inp2)
    print(f"→ {'ACCEPTED' if result2 else 'REJECTED'}")

    # ── Interactive mode ─────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("Interactive Mode")
    user_rules = parse_grammar_rules()
    if user_rules:
        start = input("Enter start symbol: ").strip()
        while True:
            user_input = input("Enter string to parse (or 'quit'): ").strip()
            if user_input.lower() == 'quit':
                break
            res = shift_reduce_parse(user_rules, start, user_input)
            print(f"→ {'ACCEPTED' if res else 'REJECTED'}")
