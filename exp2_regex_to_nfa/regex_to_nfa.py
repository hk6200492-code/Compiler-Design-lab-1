"""
Experiment 2: Conversion from Regular Expression to NFA
Compiler Design Lab (18CSC304J)
SRM Institute of Science and Technology

Uses Thompson's Construction algorithm.
Supported operators: | (union), * (Kleene star), + (one-or-more), . (concat)
Grouping via parentheses is also supported.
"""


def regex_to_nfa(regex: str):
    """
    Converts a regular expression to an NFA using Thompson's Construction.
    Returns (start_state, accept_state, transitions_dict).
    transitions: { (state, symbol): [list_of_states] }
    """
    state_counter = [0]

    def new_state():
        s = state_counter[0]
        state_counter[0] += 1
        return s

    # --- NFA fragment builders ---

    def nfa_literal(ch):
        """Single character NFA:  s0 --ch--> s1"""
        s0, s1 = new_state(), new_state()
        return s0, s1, {(s0, ch): [s1]}

    def merge_transitions(*trans_dicts):
        merged = {}
        for td in trans_dicts:
            for key, val in td.items():
                merged.setdefault(key, []).extend(val)
        return merged

    def nfa_concat(nfa1, nfa2):
        """NFA for nfa1 followed by nfa2."""
        s1, e1, t1 = nfa1
        s2, e2, t2 = nfa2
        merged = merge_transitions(t1, t2)
        merged.setdefault((e1, 'ε'), []).append(s2)
        return s1, e2, merged

    def nfa_union(nfa1, nfa2):
        """NFA for nfa1 | nfa2."""
        s1, e1, t1 = nfa1
        s2, e2, t2 = nfa2
        s0, sf = new_state(), new_state()
        merged = merge_transitions(t1, t2)
        merged.setdefault((s0, 'ε'), []).extend([s1, s2])
        merged.setdefault((e1, 'ε'), []).append(sf)
        merged.setdefault((e2, 'ε'), []).append(sf)
        return s0, sf, merged

    def nfa_star(nfa1):
        """NFA for nfa1*."""
        s1, e1, t1 = nfa1
        s0, sf = new_state(), new_state()
        merged = dict(t1)
        merged.setdefault((s0, 'ε'), []).extend([s1, sf])
        merged.setdefault((e1, 'ε'), []).extend([s1, sf])
        return s0, sf, merged

    def nfa_plus(nfa1):
        """NFA for nfa1+ = nfa1 . nfa1*"""
        # Clone is not possible without re-parsing; use ε link instead:
        # a+ : s0 --a--> s1, s1 --ε--> s0 (loop) and s1 is also accept
        s1, e1, t1 = nfa1
        sf = new_state()
        merged = dict(t1)
        merged.setdefault((e1, 'ε'), []).extend([s1, sf])
        return s1, sf, merged

    # --- Recursive-descent parser ---
    pos = [0]

    def parse_expr():
        """expr  ::= term ( '|' term )*"""
        left = parse_term()
        while pos[0] < len(regex) and regex[pos[0]] == '|':
            pos[0] += 1
            right = parse_term()
            left = nfa_union(left, right)
        return left

    def parse_term():
        """term  ::= factor factor*"""
        left = parse_factor()
        while pos[0] < len(regex) and regex[pos[0]] not in ('|', ')'):
            right = parse_factor()
            left = nfa_concat(left, right)
        return left

    def parse_factor():
        """factor ::= atom ( '*' | '+' )?"""
        base = parse_atom()
        if pos[0] < len(regex):
            if regex[pos[0]] == '*':
                pos[0] += 1
                return nfa_star(base)
            if regex[pos[0]] == '+':
                pos[0] += 1
                return nfa_plus(base)
        return base

    def parse_atom():
        """atom ::= '(' expr ')' | literal"""
        if pos[0] < len(regex) and regex[pos[0]] == '(':
            pos[0] += 1          # consume '('
            nfa = parse_expr()
            if pos[0] < len(regex) and regex[pos[0]] == ')':
                pos[0] += 1      # consume ')'
            return nfa
        # plain character
        ch = regex[pos[0]]
        pos[0] += 1
        return nfa_literal(ch)

    start, accept, transitions = parse_expr()
    return start, accept, transitions, state_counter[0]


def print_nfa(regex, start, accept, transitions, total_states):
    print(f"\nRegular Expression : {regex}")
    print(f"Start State        : q{start}")
    print(f"Accept State       : q{accept}")
    print(f"Total States       : {total_states}")

    all_symbols = sorted({sym for (_, sym) in transitions.keys()})

    col_w = 16
    header = f"{'State':<10}" + "".join(f"{sym:<{col_w}}" for sym in all_symbols)
    print("\n" + header)
    print("-" * len(header))

    for state in range(total_states):
        label = f"q{state}" + ("*" if state == accept else "")
        row = f"{label:<10}"
        for sym in all_symbols:
            dest = transitions.get((state, sym), [])
            cell = "{" + ", ".join(f"q{d}" for d in dest) + "}" if dest else "∅"
            row += f"{cell:<{col_w}}"
        print(row)


if __name__ == "__main__":
    print("=" * 55)
    print("EXPERIMENT 2: REGULAR EXPRESSION TO NFA")
    print("=" * 55)

    test_cases = ["a|b", "a*b", "ab+", "(a|b)*", "a(b|c)*"]

    for regex in test_cases:
        print("\n" + "─" * 55)
        start, accept, transitions, total = regex_to_nfa(regex)
        print_nfa(regex, start, accept, transitions, total)

    # Interactive
    print("\n" + "=" * 55)
    user_regex = input("Enter your own regular expression: ").strip()
    if user_regex:
        start, accept, transitions, total = regex_to_nfa(user_regex)
        print_nfa(user_regex, start, accept, transitions, total)
