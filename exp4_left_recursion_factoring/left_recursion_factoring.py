"""
Experiment 4: Elimination of Ambiguity, Left Recursion and Left Factoring
Compiler Design Lab (18CSC304J)
SRM Institute of Science and Technology
"""

from collections import defaultdict


# ──────────────────────────────────────────────────────────────
# PART A: Eliminate Immediate Left Recursion
# ──────────────────────────────────────────────────────────────

def eliminate_left_recursion(productions: dict) -> dict:
    """
    Eliminates IMMEDIATE left recursion from a grammar.

    For each rule  A -> Aα₁ | Aα₂ | β₁ | β₂
    Transforms to: A  -> β₁A' | β₂A'
                   A' -> α₁A' | α₂A' | ε
    """
    result = {}
    for lhs, rhs_list in productions.items():
        alpha = []   # right-hand sides that start with lhs  (recursive)
        beta  = []   # right-hand sides that do NOT start with lhs

        for rhs in rhs_list:
            if rhs.startswith(lhs):
                alpha.append(rhs[len(lhs):])   # strip leading non-terminal
            else:
                beta.append(rhs)

        if alpha:                               # left recursion found
            prime = lhs + "'"
            # A  -> βA'  for each β
            result[lhs]  = [b + prime for b in beta] if beta else [prime]
            # A' -> αA'  for each α, plus ε
            result[prime] = [a + prime for a in alpha] + ['ε']
        else:
            result[lhs] = rhs_list

    return result


# ──────────────────────────────────────────────────────────────
# PART B: Left Factoring
# ──────────────────────────────────────────────────────────────

def longest_common_prefix(strings: list) -> str:
    """Return the longest common prefix of a list of strings."""
    if not strings:
        return ""
    prefix = strings[0]
    for s in strings[1:]:
        new_prefix = ""
        for c1, c2 in zip(prefix, s):
            if c1 == c2:
                new_prefix += c1
            else:
                break
        prefix = new_prefix
        if not prefix:
            break
    return prefix


def left_factor(productions: dict) -> dict:
    """
    Applies left factoring to remove common prefixes.

    A -> αβ₁ | αβ₂ | γ
    becomes:
    A  -> αA' | γ
    A' -> β₁  | β₂
    """
    result = {}
    primes_used: dict = defaultdict(int)

    def factor_one(lhs: str, rhs_list: list) -> dict:
        """Factor a single non-terminal. Returns {lhs: [...], extras...}"""
        # Group alternatives by their first character
        groups: dict = defaultdict(list)
        for rhs in rhs_list:
            groups[rhs[0] if rhs != 'ε' else ''].append(rhs)

        factored = []
        extras   = {}

        for _, bodies in groups.items():
            if len(bodies) == 1:
                factored.append(bodies[0])
                continue

            prefix = longest_common_prefix(bodies)
            if not prefix or prefix == 'ε':
                factored.extend(bodies)
                continue

            # Generate a unique new non-terminal name
            primes_used[lhs] += 1
            new_nt = lhs + "'" * primes_used[lhs]

            suffixes = [b[len(prefix):] if b[len(prefix):] else 'ε' for b in bodies]
            factored.append(prefix + new_nt)
            extras[new_nt] = suffixes

        return {lhs: factored, **extras}

    # Iteratively apply left factoring until no changes
    current = dict(productions)
    while True:
        new_prods = {}
        changed = False
        for lhs, rhs_list in current.items():
            sub = factor_one(lhs, rhs_list)
            new_prods.update(sub)
            if sub != {lhs: rhs_list}:
                changed = True
        current = new_prods
        if not changed:
            break

    return current


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def print_grammar(title: str, productions: dict):
    print(f"\n{title}")
    print("-" * 40)
    for lhs, rhs_list in productions.items():
        print(f"  {lhs}  ->  {' | '.join(rhs_list)}")


def parse_grammar_input() -> dict:
    """Read a grammar interactively from the user."""
    print("\nEnter productions (e.g.  E -> E+T | T ).")
    print("Type 'done' when finished.")
    prods = {}
    while True:
        line = input("  > ").strip()
        if line.lower() == 'done':
            break
        if '->' not in line:
            print("  Invalid format. Use  LHS -> rhs1 | rhs2")
            continue
        lhs, rhs_part = line.split('->', 1)
        lhs = lhs.strip()
        rhs_list = [r.strip() for r in rhs_part.split('|')]
        prods[lhs] = rhs_list
    return prods


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("EXPERIMENT 4: ELIMINATION OF LEFT RECURSION & LEFT FACTORING")
    print("=" * 55)

    # ── Example 1: Classic expression grammar with left recursion ──
    g1 = {
        'E': ['E+T', 'T'],
        'T': ['T*F', 'F'],
        'F': ['(E)', 'id'],
    }
    print_grammar("Original Grammar (Example 1):", g1)

    g1_no_lr = eliminate_left_recursion(g1)
    print_grammar("After Eliminating Left Recursion:", g1_no_lr)

    g1_lf = left_factor(g1_no_lr)
    print_grammar("After Left Factoring:", g1_lf)

    # ── Example 2: Grammar requiring left factoring ──
    g2 = {
        'S': ['iEtS', 'iEtSeS', 'a'],
        'E': ['b'],
    }
    print_grammar("\nOriginal Grammar (Example 2 - if-then-else):", g2)

    g2_no_lr = eliminate_left_recursion(g2)
    print_grammar("After Eliminating Left Recursion:", g2_no_lr)

    g2_lf = left_factor(g2_no_lr)
    print_grammar("After Left Factoring:", g2_lf)

    # ── Example 3: Mixed left recursion + common prefix ──
    g3 = {
        'A': ['Aa', 'Ab', 'c', 'd'],
    }
    print_grammar("\nOriginal Grammar (Example 3):", g3)

    g3_no_lr = eliminate_left_recursion(g3)
    print_grammar("After Eliminating Left Recursion:", g3_no_lr)

    g3_lf = left_factor(g3_no_lr)
    print_grammar("After Left Factoring:", g3_lf)

    # ── Interactive mode ──
    print("\n" + "=" * 55)
    print("Interactive Mode")
    user_grammar = parse_grammar_input()
    if user_grammar:
        print_grammar("Your Grammar:", user_grammar)
        no_lr = eliminate_left_recursion(user_grammar)
        print_grammar("After Eliminating Left Recursion:", no_lr)
        lf = left_factor(no_lr)
        print_grammar("After Left Factoring:", lf)
