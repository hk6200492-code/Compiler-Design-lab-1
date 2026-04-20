"""
Experiment 3: Conversion from NFA to DFA
Compiler Design Lab (18CSC304J)
SRM Institute of Science and Technology

Uses the Subset Construction (Powerset) algorithm.
Supports NFA with ε-transitions.
"""


def epsilon_closure(states: set, transitions: dict) -> frozenset:
    """Compute ε-closure of a set of NFA states."""
    closure = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        for t in transitions.get((s, 'ε'), []):
            if t not in closure:
                closure.add(t)
                stack.append(t)
    return frozenset(closure)


def move(states: frozenset, symbol: str, transitions: dict) -> set:
    """Compute the set of NFA states reachable from 'states' on 'symbol'."""
    result = set()
    for s in states:
        result.update(transitions.get((s, symbol), []))
    return result


def nfa_to_dfa(nfa_start: int, nfa_accept: set, nfa_transitions: dict,
               input_symbols: list):
    """
    Converts NFA to DFA using Subset Construction.

    Parameters
    ----------
    nfa_start       : int         - NFA start state
    nfa_accept      : set         - Set of NFA accept states
    nfa_transitions : dict        - { (state, symbol): [states] }
    input_symbols   : list        - Non-ε symbols in the alphabet

    Returns
    -------
    dfa_states, dfa_transitions, dfa_accept, dfa_start_name
    """
    start_closure = epsilon_closure({nfa_start}, nfa_transitions)
    dfa_states = {start_closure: "D0"}
    dfa_transitions = {}
    dfa_accept = set()
    unmarked = [start_closure]
    counter = 1

    while unmarked:
        current = unmarked.pop(0)
        current_name = dfa_states[current]

        # Check if this DFA state is an accept state
        if any(s in nfa_accept for s in current):
            dfa_accept.add(current_name)

        for sym in input_symbols:
            next_nfa = epsilon_closure(move(current, sym, nfa_transitions),
                                       nfa_transitions)
            if not next_nfa:
                continue
            if next_nfa not in dfa_states:
                dfa_states[next_nfa] = f"D{counter}"
                counter += 1
                unmarked.append(next_nfa)
            dfa_transitions[(current_name, sym)] = dfa_states[next_nfa]

    return dfa_states, dfa_transitions, dfa_accept, "D0"


def print_dfa(dfa_states, dfa_transitions, dfa_accept, dfa_start,
              input_symbols, nfa_transitions):
    """Pretty-print the DFA transition table."""
    print(f"\nDFA Start State  : {dfa_start}")
    print(f"DFA Accept States: {sorted(dfa_accept)}")
    print(f"Total DFA States : {len(dfa_states)}\n")

    col_w = 10
    header = f"{'State':<12}" + "".join(f"{sym:<{col_w}}" for sym in input_symbols)
    print(header)
    print("-" * len(header))

    for subset, name in sorted(dfa_states.items(), key=lambda x: x[1]):
        marker = "*" if name in dfa_accept else " "
        label = f"{name}{marker}"
        row = f"{label:<12}"
        for sym in input_symbols:
            dest = dfa_transitions.get((name, sym), "-")
            row += f"{dest:<{col_w}}"
        print(row)


def simulate_dfa(dfa_transitions, dfa_accept, dfa_start, input_string,
                 input_symbols):
    """Simulate the DFA on input_string and return True if accepted."""
    current = dfa_start
    print(f"\nSimulating DFA on input: '{input_string}'")
    print(f"{'Step':<6} {'Current State':<16} {'Symbol':<10} {'Next State'}")
    print("-" * 50)

    for i, ch in enumerate(input_string):
        if ch not in input_symbols:
            print(f"  Symbol '{ch}' not in alphabet — REJECTED")
            return False
        next_state = dfa_transitions.get((current, ch), None)
        print(f"{i:<6} {current:<16} {ch:<10} {next_state if next_state else 'DEAD'}")
        if next_state is None:
            print(f"\nResult: REJECTED (no transition from {current} on '{ch}')")
            return False
        current = next_state

    accepted = current in dfa_accept
    print(f"\nFinal State: {current}  →  {'ACCEPTED ✓' if accepted else 'REJECTED ✗'}")
    return accepted


if __name__ == "__main__":
    print("=" * 55)
    print("EXPERIMENT 3: NFA TO DFA (Subset Construction)")
    print("=" * 55)

    # ----------------------------------------------------------------
    # Example 1: NFA for (a|b)*
    # States: 0–5
    # 0 -ε-> 1, 0 -ε-> 3
    # 1 -a-> 2, 3 -b-> 4
    # 2 -ε-> 5, 4 -ε-> 5
    # 5 -ε-> 0  (loop for *)
    # ----------------------------------------------------------------
    print("\n--- Example 1: NFA for (a|b)* ---")
    nfa1_trans = {
        (0, 'ε'): [1, 3],
        (1, 'a'): [2],
        (3, 'b'): [4],
        (2, 'ε'): [5],
        (4, 'ε'): [5],
        (5, 'ε'): [0],
    }
    syms1 = ['a', 'b']
    states1, trans1, accept1, start1 = nfa_to_dfa(0, {5}, nfa1_trans, syms1)
    print_dfa(states1, trans1, accept1, start1, syms1, nfa1_trans)
    simulate_dfa(trans1, accept1, start1, "ababba", syms1)
    simulate_dfa(trans1, accept1, start1, "", syms1)

    # ----------------------------------------------------------------
    # Example 2: NFA for a(a|b)*b  (starts with a, ends with b)
    # ----------------------------------------------------------------
    print("\n--- Example 2: NFA for a(a|b)*b ---")
    nfa2_trans = {
        (0, 'a'): [1],
        (1, 'ε'): [2, 4],
        (2, 'a'): [3],
        (4, 'b'): [5],
        (3, 'ε'): [6],
        (5, 'ε'): [6],
        (6, 'ε'): [1, 7],
        (7, 'b'): [8],
    }
    syms2 = ['a', 'b']
    states2, trans2, accept2, start2 = nfa_to_dfa(0, {8}, nfa2_trans, syms2)
    print_dfa(states2, trans2, accept2, start2, syms2, nfa2_trans)
    simulate_dfa(trans2, accept2, start2, "ab", syms2)
    simulate_dfa(trans2, accept2, start2, "aab", syms2)
    simulate_dfa(trans2, accept2, start2, "ba", syms2)

    # Interactive
    print("\n" + "=" * 55)
    print("Interactive: Build NFA manually")
    n_states = int(input("Enter number of NFA states: "))
    alphabet  = input("Enter alphabet symbols (space-separated, no ε): ").split()
    n_start   = int(input("Enter start state number: "))
    accepts_in = list(map(int, input("Enter accept state(s) (space-separated): ").split()))
    n_trans = int(input("Enter number of transitions: "))
    print("Enter transitions as: from_state  symbol  to_state  (use 'e' for ε)")
    user_trans = {}
    for _ in range(n_trans):
        parts = input("  > ").split()
        frm, sym, to = int(parts[0]), parts[1], int(parts[2])
        if sym == 'e':
            sym = 'ε'
        user_trans.setdefault((frm, sym), []).append(to)

    u_states, u_trans, u_accept, u_start = nfa_to_dfa(
        n_start, set(accepts_in), user_trans, alphabet
    )
    print_dfa(u_states, u_trans, u_accept, u_start, alphabet, user_trans)

    test_str = input("\nEnter a string to simulate on DFA: ")
    simulate_dfa(u_trans, u_accept, u_start, test_str, alphabet)
