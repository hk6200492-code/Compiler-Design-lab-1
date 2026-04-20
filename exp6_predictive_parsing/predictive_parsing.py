"""
Experiment 6: Construction of Predictive Parsing Table (LL(1))
Compiler Design Lab (18CSC304J)
SRM Institute of Science and Technology
"""

from first_and_follow import compute_first_and_follow


def build_ll1_table(productions: dict, first: dict, follow: dict) -> dict:
    """
    Builds the LL(1) predictive parsing table.

    Returns
    -------
    table : dict  { (non_terminal, terminal): production_body }
    """
    non_terminals = set(productions.keys())

    def first_of_string(symbols: list) -> set:
        result = set()
        for sym in symbols:
            if sym in non_terminals:
                result |= (first[sym] - {'ε'})
                if 'ε' not in first[sym]:
                    return result
            else:
                if sym == 'ε':
                    result.add('ε')
                else:
                    result.add(sym)
                    return result
        result.add('ε')
        return result

    table = {}
    for lhs, rhs_list in productions.items():
        for rhs in rhs_list:
            syms = list(rhs) if rhs != 'ε' else ['ε']
            first_rhs = first_of_string(syms)

            for terminal in first_rhs - {'ε'}:
                if (lhs, terminal) in table:
                    print(f"  [WARNING] Conflict at M[{lhs}, {terminal}]"
                          f" — grammar may not be LL(1)")
                table[(lhs, terminal)] = rhs

            if 'ε' in first_rhs:
                for terminal in follow[lhs]:
                    if (lhs, terminal) in table:
                        print(f"  [WARNING] Conflict at M[{lhs}, {terminal}]"
                              f" — grammar may not be LL(1)")
                    table[(lhs, terminal)] = rhs

    return table


def print_ll1_table(table: dict, productions: dict, follow: dict):
    """Display the LL(1) parsing table."""
    non_terminals = sorted(productions.keys())
    all_terminals = sorted({t for (_, t) in table.keys()})

    col_w = max(18, max((len(f"{nt}->{rhs}") for (nt, _), rhs in table.items()),
                         default=10) + 2)

    print("\nLL(1) Parsing Table")
    print("─" * (12 + col_w * len(all_terminals)))
    header = f"{'NT':<12}" + "".join(f"{t:<{col_w}}" for t in all_terminals)
    print(header)
    print("─" * len(header))

    for nt in non_terminals:
        row = f"{nt:<12}"
        for t in all_terminals:
            entry = table.get((nt, t), "")
            cell = f"{nt}→{entry}" if entry else ""
            row += f"{cell:<{col_w}}"
        print(row)


def ll1_parse(table: dict, productions: dict, start_symbol: str,
              input_string: str) -> bool:
    """
    Simulates LL(1) stack-based parsing.

    Returns True if input_string is accepted, False otherwise.
    """
    non_terminals = set(productions.keys())
    tokens = list(input_string) + ['$']
    stack  = ['$', start_symbol]
    idx    = 0

    col1, col2, col3 = 30, 22, 35
    print(f"\n{'Stack':<{col1}} {'Input':<{col2}} Action")
    print("─" * (col1 + col2 + col3))

    while stack:
        top     = stack[-1]
        current = tokens[idx]
        stk_str = "".join(reversed(stack))
        inp_str = "".join(tokens[idx:])

        if top == '$' and current == '$':
            print(f"{stk_str:<{col1}} {'$':<{col2}} ACCEPT ✓")
            return True

        if top == current:                   # terminal match
            action = f"Match '{top}'"
            print(f"{stk_str:<{col1}} {inp_str:<{col2}} {action}")
            stack.pop()
            idx += 1

        elif top in non_terminals:           # non-terminal: consult table
            production = table.get((top, current))
            if production is None:
                print(f"{stk_str:<{col1}} {inp_str:<{col2}} ERROR — no entry M[{top},{current}]")
                return False
            action = f"{top} → {production}"
            print(f"{stk_str:<{col1}} {inp_str:<{col2}} {action}")
            stack.pop()
            if production != 'ε':
                for sym in reversed(production):
                    stack.append(sym)

        else:                                # terminal mismatch
            print(f"{stk_str:<{col1}} {inp_str:<{col2}} ERROR — expected '{top}', got '{current}'")
            return False

    return False


if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 6: PREDICTIVE PARSING TABLE (LL(1))")
    print("=" * 60)

    # ── Grammar: E->TR, R->+TR|ε, T->FY, Y->*FY|ε, F->(E)|i ──────
    g = {
        'E': ['TR'],
        'R': ['+TR', 'ε'],
        'T': ['FY'],
        'Y': ['*FY', 'ε'],
        'F': ['(E)', 'i'],
    }

    print("\nGrammar Productions:")
    for lhs, rhs_list in g.items():
        print(f"  {lhs}  ->  {' | '.join(rhs_list)}")

    first, follow = compute_first_and_follow(g, 'E')

    print("\nFIRST Sets:")
    for nt in sorted(g.keys()):
        print(f"  FIRST({nt}) = {{ {', '.join(sorted(first[nt]))} }}")

    print("\nFOLLOW Sets:")
    for nt in sorted(g.keys()):
        print(f"  FOLLOW({nt}) = {{ {', '.join(sorted(follow[nt]))} }}")

    table = build_ll1_table(g, first, follow)
    print_ll1_table(table, g, follow)

    # ── Parse built-in test cases ───────────────────────────────────
    test_strings = ["i+i*i", "i+i", "(i+i)*i", "i++i"]
    for s in test_strings:
        print(f"\n{'─'*60}")
        print(f"Parsing: '{s}'")
        result = ll1_parse(table, g, 'E', s)
        print(f"→ {'ACCEPTED' if result else 'REJECTED'}")

    # ── Interactive ─────────────────────────────────────────────────
    print("\n" + "=" * 60)
    while True:
        user_input = input("\nEnter string to parse (or 'quit'): ").strip()
        if user_input.lower() == 'quit':
            break
        result = ll1_parse(table, g, 'E', user_input)
        print(f"→ {'ACCEPTED' if result else 'REJECTED'}")
