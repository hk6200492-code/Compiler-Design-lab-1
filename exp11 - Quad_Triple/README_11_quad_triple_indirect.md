# 11 – Intermediate Code Gen: Quadruple, Triple, Indirect Triple

## Overview
This program generates **Three-Address Code (TAC)** from an arithmetic expression
and represents it in three intermediate code formats:
**Quadruples**, **Triples**, and **Indirect Triples**.
These are the standard intermediate representations used inside compilers
between the front-end and back-end.

---

## Concepts Covered
- **Three-Address Code (TAC)**: Instructions of the form `x = y op z`, using temporaries.
- **Quadruple**: A 4-field record `(op, arg1, arg2, result)` — result is explicit.
- **Triple**: A 3-field record `(op, arg1, arg2)` — result identified by position index.
- **Indirect Triple**: A table of pointers into the triples table — enables reordering without renumbering.
- **Temporaries**: Compiler-generated variables (`t1`, `t2`, ...) to hold intermediate values.

---

## Format Comparison

| Format | Fields | Result Storage |
|--------|--------|----------------|
| Quadruple | `(op, arg1, arg2, result)` | Explicit named variable |
| Triple | `(op, arg1, arg2)` | Implicit — index number `(i)` |
| Indirect Triple | pointer → triple index | Separate indirection table |

---

## How It Works
1. Expression string is parsed recursively respecting operator precedence.
2. For each binary operation, a new temporary is created.
3. The same operation is simultaneously recorded in all three tables.

---

## Example
```
Expression: a + b * c - d

Quadruples:
  #    Op    Arg1     Arg2     Result
  0    *     b        c        t1
  1    +     a        t1       t2
  2    -     t2       d        t3

Triples:
  (0)  *     b        c
  (1)  +     a        (0)
  (2)  -     (1)      d

Indirect Triples:
  [0] -> (0)
  [1] -> (1)
  [2] -> (2)
```

---

## How to Run
```bash
python3 11_quad_triple_indirect.py
```

## Dependencies
- Python 3.x (standard library only)

---

## Key Class
| Method | Description |
|--------|-------------|
| `ICGGenerator.generate(expr)` | Parses expression and fills all three tables |
| `ICGGenerator.new_temp()` | Creates a new unique temporary variable |
| `ICGGenerator._eval(expr)` | Recursive expression evaluator / code emitter |
