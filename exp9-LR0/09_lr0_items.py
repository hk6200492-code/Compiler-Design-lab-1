# Topic 9: Computation of LR(0) Items
from collections import defaultdict


def compute_lr0_items(grammar, start):
    """Compute LR(0) items (closure + goto) for a grammar."""

    def closure(items):
        result = set(items)
        changed = True
        while changed:
            changed = False
            for (lhs, rhs, dot) in list(result):
                if dot < len(rhs) and rhs[dot] in grammar:
                    for prod in grammar[rhs[dot]]:
                        item = (rhs[dot], tuple(prod), 0)
                        if item not in result:
                            result.add(item)
                            changed = True
        return frozenset(result)

    def goto(items, symbol):
        moved = set()
        for (lhs, rhs, dot) in items:
            if dot < len(rhs) and rhs[dot] == symbol:
                moved.add((lhs, rhs, dot + 1))
        return closure(moved) if moved else frozenset()

    # Augmented start
    start_item = (start + "'", (start,), 0)
    I0 = closure({start_item})
    states = [I0]
    transitions = {}
    visited = {I0: 0}

    i = 0
    while i < len(states):
        state = states[i]
        symbols = {rhs[dot] for (lhs, rhs, dot) in state if dot < len(rhs)}
        for sym in symbols:
            g = goto(state, sym)
            if g:
                if g not in visited:
                    visited[g] = len(states)
                    states.append(g)
                transitions[(i, sym)] = visited[g]
        i += 1

    return states, transitions


# Example grammar
grammar = {
    'E': [['E', '+', 'T'], ['T']],
    'T': [['T', '*', 'F'], ['F']],
    'F': [['(', 'E', ')'], ['id']]
}

states, transitions = compute_lr0_items(grammar, 'E')

for i, state in enumerate(states):
    print(f"\nI{i}:")
    for (lhs, rhs, dot) in sorted(state):
        rhs_str = list(rhs)
        rhs_str.insert(dot, '•')
        print(f"  {lhs} -> {' '.join(rhs_str)}")

print("\nTransitions:")
for (state, sym), target in sorted(transitions.items()):
    print(f"  GOTO(I{state}, {sym}) = I{target}")
