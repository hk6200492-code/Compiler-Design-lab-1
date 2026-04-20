# 09 – Computation of LR(0) Items

## Overview
This program computes **LR(0) Items** for a context-free grammar using the
**Closure** and **GOTO** functions. It builds the canonical collection of
LR(0) item sets (states) and the transitions between them — which form the
backbone of an LR(0) / SLR(1) parser.

---

## Concepts Covered
- **LR(0) Item**: A production rule with a dot (•) indicating how far parsing has progressed.  
  e.g., `E -> E • + T`
- **Closure**: Expands a set of items by adding items for non-terminals after the dot.
- **GOTO(I, X)**: Moves the dot past symbol X in all items of state I, then takes closure.
- **Augmented Grammar**: Adds a new start rule `S' -> S` to mark the accept state.
- **Canonical Collection**: The full set of LR(0) states built by repeated GOTO calls.

---

## How It Works
1. Augment the grammar with a new start production.
2. Compute `I0 = closure({S' -> • S})`.
3. For each state and each grammar symbol, compute GOTO and add new states.
4. Repeat until no new states are added.
5. Print all states and transitions.

---

## Example Grammar
```
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
```

## Sample Output
```
I0:
  E' -> • E
  E  -> • E + T
  E  -> • T
  T  -> • T * F
  T  -> • F
  F  -> • ( E )
  F  -> • id

Transitions:
  GOTO(I0, E) = I1
  GOTO(I0, T) = I2
  ...
```

---

## How to Run
```bash
python3 09_lr0_items.py
```

## Dependencies
- Python 3.x (standard library only)

---

## Key Functions
| Function | Description |
|----------|-------------|
| `closure(items)` | Computes the closure of a set of LR(0) items |
| `goto(items, symbol)` | Computes GOTO transition for a symbol |
| `compute_lr0_items(grammar, start)` | Builds all states and transitions |
