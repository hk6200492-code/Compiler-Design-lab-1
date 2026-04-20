# Experiment 6: Construction of Predictive Parsing Table (LL(1))

## Aim
To write a Python program that constructs an **LL(1) Predictive Parsing Table** and simulates parsing of an input string using stack-based LL(1) parsing.

---

## Theory

A **Predictive Parser** is a top-down parser that can predict which production to use by looking at the current input symbol — without backtracking.

An **LL(1)** grammar means:
- **L** — scans input Left to right
- **L** — produces Leftmost derivation
- **1** — uses 1 symbol of lookahead

### Parsing Table Construction
For each production `A → α`:
1. For each terminal `a ∈ FIRST(α)`, add `A → α` to `M[A, a]`
2. If `ε ∈ FIRST(α)`, for each terminal `b ∈ FOLLOW(A)`, add `A → α` to `M[A, b]`

### Stack-Based Parsing Algorithm
```
Push $ and start symbol onto stack
Repeat:
  top = stack top,  current = next input token
  if top == current == $  → ACCEPT
  if top == current       → Pop stack, advance input (MATCH)
  if top is non-terminal  → Replace top with M[top, current] (reversed)
  else                    → ERROR
```

---

## How to Run

```bash
python predictive_parsing.py
```

> **Note:** This file imports `first_and_follow.py` from Experiment 5.  
> Make sure both files are in the same folder, or copy `first_and_follow.py` here.

---

## Grammar Used
```
E  → TR
R  → +TR | ε
T  → FY
Y  → *FY | ε
F  → (E) | i
```

---

## Sample Parsing Table
```
NT          $       (       )       *       +       i
E                   E→TR                            E→TR
R           R→ε             R→ε             R→+TR
T                   T→FY                            T→FY
Y           Y→ε             Y→ε    Y→*FY    Y→ε
F                   F→(E)                           F→i
```

---

## Sample Trace for `i+i*i`
```
Stack                Input                  Action
E$                   i+i*i$                 E → TR
TR$                  i+i*i$                 T → FY
FYR$                 i+i*i$                 F → i
iYR$                 i+i*i$                 Match 'i'
YR$                  +i*i$                  Y → ε
R$                   +i*i$                  R → +TR
...
$                    $                      ACCEPT ✓
```

---

## Files
| File                    | Description                           |
|-------------------------|---------------------------------------|
| `predictive_parsing.py` | LL(1) table construction and parsing  |
| `README.md`             | This documentation file               |

> Also requires `first_and_follow.py` from **Experiment 5**.

---

## Result
The program successfully builds the LL(1) parsing table and correctly accepts or rejects input strings with a step-by-step parsing trace.
