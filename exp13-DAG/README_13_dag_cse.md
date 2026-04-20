# 13 – Implementation of DAG (CSE Elimination)

## Overview
This program implements a **Directed Acyclic Graph (DAG)** for a basic block
to detect and eliminate **Common Subexpressions (CSE)**.
Instead of recomputing the same expression multiple times, the DAG reuses
existing nodes, producing optimized intermediate code.

---

## Concepts Covered
- **DAG (Directed Acyclic Graph)**: A graph representation of a basic block where
  each unique computation appears exactly once as a node.
- **CSE (Common Subexpression Elimination)**: An optimization that replaces
  repeated computations with references to a single previously computed result.
- **Leaf Node**: Represents an operand (variable or constant).
- **Interior Node**: Represents an operation `(op, left_child, right_child)`.
- **Node Labels**: Each node tracks all variable names that hold its value.

---

## How It Works
1. For each TAC instruction `x = y op z`:
   - Get or create leaf nodes for `y` and `z`.
   - Check if a node `(op, node_y, node_z)` already exists.
     - **If yes** → reuse it (CSE found!), just add `x` as a label.
     - **If no** → create a new interior node.
2. Print the DAG showing which variables map to the same node.
3. Emit optimized code — one instruction per unique interior node.

---

## Example
```
Input:
  t1 = b + c
  t2 = b + c    ← same as t1 (CSE!)
  t3 = t1 * d
  t4 = t2 * d   ← same as t3 (CSE!)
  a  = t3 - e

DAG Output:
  Node 0: LEAF 'b'
  Node 1: LEAF 'c'
  Node 2: OP (+, node[0], node[1])  labels = {t1, t2}   ← merged!
  Node 3: LEAF 'd'
  Node 4: OP (*, node[2], node[3])  labels = {t3, t4}   ← merged!
  Node 5: LEAF 'e'
  Node 6: OP (-, node[4], node[5])  labels = {a}

Optimized Code:
  t1 = b + c        ; used by {t1, t2}
  t3 = t1 * d       ; used by {t3, t4}
  a  = t3 - e
```
4 instructions reduced to 3 — redundant computations eliminated.

---

## How to Run
```bash
python3 13_dag_cse.py
```

## Dependencies
- Python 3.x (standard library only)

---

## Key Class
| Method | Description |
|--------|-------------|
| `DAG.get_or_create_leaf(val)` | Returns existing or new leaf node for a variable |
| `DAG.get_or_create_op(op, l, r)` | Reuses existing node if same op+children exist (CSE) |
| `DAG.process(instructions)` | Builds the DAG from a list of TAC instructions |
| `DAG.print_optimized_code()` | Emits one instruction per unique DAG node |
