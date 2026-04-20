"""
Experiment 5: FIRST and FOLLOW Computation
Compiler Design Lab (18CSC304J)
SRM Institute of Science and Technology
"""


def compute_first_and_follow(productions: dict, start_symbol: str):
    """
    Computes FIRST and FOLLOW sets for all non-terminals.

    Parameters
    ----------
    productions   : dict  { 'E': ['TR', '+TR', ...], ... }
                    Use 'ε' to represent epsilon.
    start_symbol  : str   The grammar's start symbol.

    Returns
    -------
    first  : dict { non_terminal: set_of_terminals_including_ε }
    follow : dict { non_terminal: set_of_terminals_including_$ }
    """
    non_terminals = set(productions.keys())

    def is_terminal(sym: str) -> bool:
        return sym not in non_terminals and sym != 'ε'

    # ── FIRST ──────────────────────────────────────────────────────

    first: dict = {nt: set() for nt in non_terminals}

    def first_of(symbol: str) -> set:
        """Return FIRST set of a single grammar symbol."""
        if symbol == 'ε':
            return {'ε'}
        if is_terminal(symbol):
            return {symbol}
        return set(first[symbol])   # current approximation

    def first_of_string(symbols: list) -> set:
        """Return FIRST set of a sequence of grammar symbols."""
        result = set()
        for sym in symbols:
            sym_first = first_of(sym)
            result |= (sym_first - {'ε'})
            if 'ε' not in sym_first:
                return result        # ε cannot propagate past this symbol
        result.add('ε')              # every symbol can derive ε
        return result

    changed = True
    while changed:
        changed = False
        for nt in non_terminals:
            for rhs in productions[nt]:
                if rhs == 'ε':
                    if 'ε' not in first[nt]:
                        first[nt].add('ε')
                        changed = True
                    continue
                new = first_of_string(list(rhs))
                before = len(first[nt])
                first[nt] |= new
                if len(first[nt]) > before:
                    changed = True

    # ── FOLLOW ─────────────────────────────────────────────────────

    follow: dict = {nt: set() for nt in non_terminals}
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                if rhs == 'ε':
                    continue
                for i, sym in enumerate(rhs):
                    if sym not in non_terminals:
                        continue
                    # Compute FIRST of everything after sym in this production
                    rest = list(rhs[i+1:])
                    rest_first = first_of_string(rest) if rest else {'ε'}

                    before = len(follow[sym])
                    # Add FIRST(rest) - {ε} to FOLLOW(sym)
                    follow[sym] |= (rest_first - {'ε'})
                    # If ε ∈ FIRST(rest), add FOLLOW(lhs) to FOLLOW(sym)
                    if 'ε' in rest_first:
                        follow[sym] |= follow[lhs]
                    if len(follow[sym]) > before:
                        changed = True

    return first, follow


def print_sets(first: dict, follow: dict):
    """Display FIRST and FOLLOW sets in a formatted table."""
    all_nt = sorted(first.keys())

    print(f"\n{'Non-Terminal':<15} {'FIRST':<35} FOLLOW")
    print("─" * 75)
    for nt in all_nt:
        f_set  = "{ " + ", ".join(sorted(first[nt]))  + " }"
        fo_set = "{ " + ", ".join(sorted(follow[nt])) + " }"
        print(f"{nt:<15} {f_set:<35} {fo_set}")


if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 5: FIRST AND FOLLOW COMPUTATION")
    print("=" * 60)

    # ── Example 1: Standard expression grammar ──────────────────────
    # E  -> TR
    # R  -> +TR | ε
    # T  -> FY
    # Y  -> *FY | ε
    # F  -> (E) | i
    g1 = {
        'E': ['TR'],
        'R': ['+TR', 'ε'],
        'T': ['FY'],
        'Y': ['*FY', 'ε'],
        'F': ['(E)', 'i'],
    }
    print("\n--- Example 1: Expression Grammar ---")
    print("Productions:")
    for lhs, rhs in g1.items():
        print(f"  {lhs} -> {' | '.join(rhs)}")

    first1, follow1 = compute_first_and_follow(g1, 'E')
    print_sets(first1, follow1)

    # ── Example 2: Grammar with multiple ε-productions ───────────────
    # S  -> aBc
    # B  -> b | ε
    g2 = {
        'S': ['aBc'],
        'B': ['b', 'ε'],
    }
    print("\n--- Example 2: Grammar with ε ---")
    print("Productions:")
    for lhs, rhs in g2.items():
        print(f"  {lhs} -> {' | '.join(rhs)}")

    first2, follow2 = compute_first_and_follow(g2, 'S')
    print_sets(first2, follow2)

    # ── Example 3: if-then-else ───────────────────────────────────────
    g3 = {
        'S': ['iCtS', 'iCtSeS', 'a'],
        'C': ['b'],
    }
    print("\n--- Example 3: if-then-else Grammar ---")
    print("Productions:")
    for lhs, rhs in g3.items():
        print(f"  {lhs} -> {' | '.join(rhs)}")

    first3, follow3 = compute_first_and_follow(g3, 'S')
    print_sets(first3, follow3)

    # ── Interactive mode ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Interactive Mode")
    print("Enter productions (e.g.  E -> TR | +TR ).")
    print("Use 'e' for ε.  Type 'done' when finished.")
    prods = {}
    while True:
        line = input("  > ").strip()
        if line.lower() == 'done':
            break
        if '->' not in line:
            print("  Invalid. Use  LHS -> rhs1 | rhs2")
            continue
        lhs, rhs_part = line.split('->', 1)
        lhs = lhs.strip()
        rhs_list = [r.strip().replace('e', 'ε') for r in rhs_part.split('|')]
        prods[lhs] = rhs_list

    if prods:
        start = input("Enter start symbol: ").strip()
        f, fo = compute_first_and_follow(prods, start)
        print_sets(f, fo)
