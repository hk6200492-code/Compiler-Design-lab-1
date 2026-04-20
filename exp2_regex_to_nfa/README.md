# Experiment 2: Conversion from Regular Expression to NFA

## Aim
To write a Python program that converts a **Regular Expression** to an **NFA (Non-deterministic Finite Automaton)** using **Thompson's Construction** algorithm.

---

## Theory
Thompson's Construction builds an NFA from a regular expression by breaking it into sub-expressions and combining small NFA fragments using three fundamental operations:

| Operation       | Regex Notation | Description                               |
|-----------------|----------------|-------------------------------------------|
| **Literal**     | `a`            | Matches a single character                |
| **Concatenation**| `ab`          | NFA for `a` followed by NFA for `b`       |
| **Union**       | `a\|b`         | Either NFA for `a` OR NFA for `b`         |
| **Kleene Star** | `a*`           | Zero or more repetitions of NFA for `a`   |
| **One-or-more** | `a+`           | One or more repetitions of NFA for `a`    |

ε (epsilon) transitions are used to connect fragments without consuming input.

---

## Supported Syntax
| Symbol | Meaning            |
|--------|--------------------|
| `a-z`  | Literal characters |
| `\|`   | Union              |
| `*`    | Kleene star        |
| `+`    | One or more        |
| `()`   | Grouping           |

---

## Algorithm (Thompson's Construction)
1. **Literal `a`**: Create two states `s0` and `s1`, add transition `s0 --a--> s1`.
2. **Concatenation `AB`**: Connect accept state of A to start state of B via ε.
3. **Union `A|B`**: Create new start `s0` and accept `sf`; add ε from `s0` to start of A and B; add ε from accepts of A and B to `sf`.
4. **Star `A*`**: Create new start `s0` and accept `sf`; ε from `s0` to start of A and to `sf`; ε from accept of A back to start of A and to `sf`.
5. **Plus `A+`**: Like star but with at least one pass through A.

---

## How to Run

```bash
python regex_to_nfa.py
```

The program will:
- Run built-in test cases: `a|b`, `a*b`, `ab+`, `(a|b)*`, `a(b|c)*`
- Display the NFA transition table for each
- Prompt you to enter your own regular expression

---

## Sample Input / Output

**Input:** `a|b`

```
Regular Expression : a|b
Start State        : q4
Accept State       : q5
Total States       : 6

State     a               b               ε
--------------------------------------------------
q0        {q1}            ∅               ∅
q1        ∅               ∅               {q5}
q2        ∅               {q3}            ∅
q3        ∅               ∅               {q5}
q4        ∅               ∅               {q0, q2}
q5*       ∅               ∅               ∅
```

---

## Files
| File              | Description                          |
|-------------------|--------------------------------------|
| `regex_to_nfa.py` | Python implementation using Thompson's Construction |
| `README.md`       | This documentation file              |

---

## Result
The program successfully converts regular expressions to NFA transition tables using Thompson's Construction.
