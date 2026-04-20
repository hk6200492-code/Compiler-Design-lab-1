# Experiment 3: Conversion from NFA to DFA

## Aim
To write a Python program that converts an **NFA (Non-deterministic Finite Automaton)** with ε-transitions to a **DFA (Deterministic Finite Automaton)** using the **Subset Construction (Powerset)** algorithm.

---

## Theory

An NFA may have:
- Multiple transitions on the same symbol from one state
- ε (epsilon) transitions — moves without consuming input

A DFA has exactly one transition per symbol per state. Every NFA can be converted to an equivalent DFA.

### Key Concepts

| Concept | Description |
|---|---|
| **ε-closure(S)** | Set of all NFA states reachable from set S using only ε-transitions |
| **move(S, a)** | Set of NFA states reachable from set S on symbol `a` |
| **DFA State** | Each DFA state represents a **subset** of NFA states |
| **DFA Accept State** | Any DFA state that contains at least one NFA accept state |

---

## Algorithm (Subset Construction)

1. Compute `ε-closure({start_state})` — this is the DFA start state.
2. For each unmarked DFA state `T` and each input symbol `a`:
   - Compute `U = ε-closure(move(T, a))`
   - If `U` is not already a DFA state, add it as a new state
   - Add transition `T --a--> U`
3. Mark `T` as processed.
4. Repeat until no unmarked DFA states remain.
5. Any DFA state containing an NFA accept state is a DFA accept state.

---

## How to Run

```bash
python nfa_to_dfa.py
```

The program will:
- Convert two built-in NFA examples and display the DFA tables
- Simulate the DFA on sample input strings
- Allow you to define a custom NFA interactively

---

## Sample Input / Output

**NFA for `(a|b)*`:**
```
DFA Start State  : D0
DFA Accept States: ['D0', 'D1', 'D2']

State       a         b
---------------------------
D0*         D1        D2
D1*         D1        D2
D2*         D1        D2
```

**Simulation on `"ababba"`:**
```
ACCEPTED ✓
```

---

## Files
| File            | Description                                    |
|-----------------|------------------------------------------------|
| `nfa_to_dfa.py` | Python implementation of Subset Construction   |
| `README.md`     | This documentation file                        |

---

## Result
The program successfully converts any NFA (with ε-transitions) to an equivalent DFA and simulates it on input strings.
