"""
Experiment 8: Computation of LEADING and TRAILING Sets
         (Operator Precedence Relations)
Compiler Design Lab (18CSC304J)
SRM Institute of Science and Technology
"""


def compute_leading_trailing(productions: dict):
    """
    Computes LEADING and TRAILING sets for an operator grammar,
    then derives the operator-precedence relations (<·, =·, >·).

    Parameters
    ----------
    productions : dict  { 'E': ['E+T', 'T'], ... }
                  Terminals are single lowercase chars / symbols.
                  Non-terminals are uppercase letters.

    Returns
    -------
    leading  : dict { NT: set_of_terminals }
    trailing : dict { NT: set_of_terminals }
    lt, eq, gt : sets of (terminal, terminal) pairs
    """
    non_terminals = set(productions.keys())

    def is_terminal(sym: str) -> bool:
        return sym not in non_terminals

    # ── LEADING ───────────────────────────────────────────────────────
    # LEADING(A) = { a | A =>* aγ  or  A =>* Baγ, B is non-terminal }

    leading: dict = {nt: set() for nt in non_terminals}

    changed = True
    while changed:
        changed = False
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                i = 0
                while i < len(rhs):
                    sym = rhs[i]
                    if is_terminal(sym):
                        if sym not in leading[lhs]:
                            leading[lhs].add(sym)
                            changed = True
                        # Also add next terminal if it exists right after
                        if i + 1 < len(rhs) and is_terminal(rhs[i+1]):
                            if rhs[i+1] not in leading[lhs]:
                                leading[lhs].add(rhs[i+1])
                                changed = True
                        break
                    else:
                        # sym is non-terminal: add its leading set
                        before = len(leading[lhs])
                        leading[lhs] |= leading[sym]
                        if len(leading[lhs]) > before:
                            changed = True
                        # Also check the symbol immediately after this NT
                        if i + 1 < len(rhs) and is_terminal(rhs[i+1]):
                            if rhs[i+1] not in leading[lhs]:
                                leading[lhs].add(rhs[i+1])
                                changed = True
                        i += 1

    # ── TRAILING ──────────────────────────────────────────────────────
    # TRAILING(A) = { a | A =>* γa  or  A =>* γaB, B is non-terminal }

    trailing: dict = {nt: set() for nt in non_terminals}

    changed = True
    while changed:
        changed = False
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                i = len(rhs) - 1
                while i >= 0:
                    sym = rhs[i]
                    if is_terminal(sym):
                        if sym not in trailing[lhs]:
                            trailing[lhs].add(sym)
                            changed = True
                        # Also add the terminal just before this position
                        if i - 1 >= 0 and is_terminal(rhs[i-1]):
                            if rhs[i-1] not in trailing[lhs]:
                                trailing[lhs].add(rhs[i-1])
                                changed = True
                        break
                    else:
                        before = len(trailing[lhs])
                        trailing[lhs] |= trailing[sym]
                        if len(trailing[lhs]) > before:
                            changed = True
                        if i - 1 >= 0 and is_terminal(rhs[i-1]):
                            if rhs[i-1] not in trailing[lhs]:
                                trailing[lhs].add(rhs[i-1])
                                changed = True
                        i -= 1

    # ── Operator Precedence Relations ─────────────────────────────────
    less_than  = set()   # a <· b
    equal_prec = set()   # a =· b
    greater    = set()   # a >· b

    for lhs, rhs_list in productions.items():
        for rhs in rhs_list:
            for i in range(len(rhs)):
                a = rhs[i]
                # Pattern: terminal a  followed by  terminal b → a =· b
                if i + 1 < len(rhs):
                    b = rhs[i+1]
                    if is_terminal(a) and is_terminal(b):
                        equal_prec.add((a, b))

                # Pattern: terminal a  followed by  NT B → a <· LEADING(B)
                if i + 1 < len(rhs):
                    b = rhs[i+1]
                    if is_terminal(a) and not is_terminal(b):
                        for t in leading[b]:
                            less_than.add((a, t))

                # Pattern: NT A  followed by  terminal b → TRAILING(A) >· b
                if i + 1 < len(rhs):
                    b = rhs[i+1]
                    if not is_terminal(a) and is_terminal(b):
                        for t in trailing[a]:
                            greater.add((t, b))

                # Pattern: terminal a  NT B  terminal c → a =· c
                if i + 2 < len(rhs):
                    b = rhs[i+1]
                    c = rhs[i+2]
                    if is_terminal(a) and not is_terminal(b) and is_terminal(c):
                        equal_prec.add((a, c))

                # Pattern: NT B  terminal b followed by anything
                #          TRAILING(B) >· b
                if i + 2 < len(rhs):
                    b = rhs[i+1]
                    c = rhs[i+2]
                    if not is_terminal(a) and is_terminal(b) and not is_terminal(c):
                        for t in trailing[a]:
                            greater.add((t, b))
                    if not is_terminal(b) and is_terminal(c):
                        for t in trailing[b]:
                            greater.add((t, c))
                    if is_terminal(b) and not is_terminal(c):
                        for t in leading[c]:
                            less_than.add((b, t))

    return leading, trailing, less_than, equal_prec, greater


def print_leading_trailing(leading: dict, trailing: dict):
    print(f"\n{'Non-Terminal':<15} {'LEADING':<30} TRAILING")
    print("─" * 70)
    for nt in sorted(leading.keys()):
        l_str = "{ " + ", ".join(sorted(leading[nt]))  + " }"
        t_str = "{ " + ", ".join(sorted(trailing[nt])) + " }"
        print(f"{nt:<15} {l_str:<30} {t_str}")


def print_precedence_table(less_than, equal_prec, greater, all_terminals):
    """Print the operator-precedence matrix."""
    terms = sorted(all_terminals)
    col_w = 6

    print(f"\n{'Operator Precedence Table':^{6 + col_w * len(terms)}}")
    print(f"{'':>6}", end="")
    for t in terms:
        print(f"{t:>{col_w}}", end="")
    print()
    print("─" * (6 + col_w * len(terms)))

    for a in terms:
        print(f"{a:>6}", end="")
        for b in terms:
            if (a, b) in equal_prec:
                cell = "=·"
            elif (a, b) in less_than:
                cell = "<·"
            elif (a, b) in greater:
                cell = ">·"
            else:
                cell = "  "
            print(f"{cell:>{col_w}}", end="")
        print()

    print(f"\nRelations:")
    print(f"  <· (less-than)   : {sorted(less_than)}")
    print(f"  =· (equal)       : {sorted(equal_prec)}")
    print(f"  >· (greater-than): {sorted(greater)}")


if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 8: COMPUTATION OF LEADING AND TRAILING")
    print("=" * 60)

    # ── Example 1: Classic expression grammar ───────────────────────
    g1 = {
        'E': ['E+T', 'T'],
        'T': ['T*F', 'F'],
        'F': ['(E)', 'i'],
    }
    print("\nGrammar:")
    for lhs, rhs_list in g1.items():
        print(f"  {lhs} -> {' | '.join(rhs_list)}")

    leading1, trailing1, lt1, eq1, gt1 = compute_leading_trailing(g1)
    print_leading_trailing(leading1, trailing1)

    all_terms1 = {s for rhs_list in g1.values()
                    for rhs in rhs_list
                    for s in rhs
                    if s not in g1}
    print_precedence_table(lt1, eq1, gt1, all_terms1)

    # ── Example 2: Simpler grammar ──────────────────────────────────
    g2 = {
        'E': ['E+E', 'E*E', 'a', 'b'],
    }
    print(f"\n{'─'*60}")
    print("Grammar:")
    for lhs, rhs_list in g2.items():
        print(f"  {lhs} -> {' | '.join(rhs_list)}")

    leading2, trailing2, lt2, eq2, gt2 = compute_leading_trailing(g2)
    print_leading_trailing(leading2, trailing2)

    all_terms2 = {s for rhs_list in g2.values()
                    for rhs in rhs_list
                    for s in rhs
                    if s not in g2}
    print_precedence_table(lt2, eq2, gt2, all_terms2)

    # ── Interactive mode ─────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("Interactive Mode")
    print("Enter productions (e.g.  E -> E+T | T ).  Type 'done' to finish.")
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
        prods[lhs] = [r.strip() for r in rhs_part.split('|')]

    if prods:
        l, t, lt, eq, gt = compute_leading_trailing(prods)
        print_leading_trailing(l, t)
        all_t = {s for rhs_list in prods.values()
                   for rhs in rhs_list
                   for s in rhs
                   if s not in prods}
        print_precedence_table(lt, eq, gt, all_t)
