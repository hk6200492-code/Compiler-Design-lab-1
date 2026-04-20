# Experiment 5: FIRST and FOLLOW Computation

## Aim
To write a Python program to compute **FIRST** and **FOLLOW** sets for all non-terminals of a given context-free grammar.

---

## Theory

FIRST and FOLLOW sets are essential for constructing predictive (LL(1)) parsers.

### FIRST Set
`FIRST(A)` = set of terminals that can appear as the **first symbol** of any string derived from `A`.

**Rules:**
- If `A → aα`, then `a ∈ FIRST(A)`
- If `A → ε`, then `ε ∈ FIRST(A)`
- If `A → Bα` and `ε ∈ FIRST(B)`, also add `FIRST(α)` to `FIRST(A)`

### FOLLOW Set
`FOLLOW(A)` = set of terminals that can appear **immediately after** `A` in some sentential form.

**Rules:**
- `$ ∈ FOLLOW(S)` where `S` is the start symbol
- If `A → αBβ`, then `FIRST(β) − {ε} ⊆ FOLLOW(B)`
- If `A → αBβ` and `ε ∈ FIRST(β)`, then `FOLLOW(A) ⊆ FOLLOW(B)`
- If `A → αB`, then `FOLLOW(A) ⊆ FOLLOW(B)`

---

## Algorithm

### FIRST
1. Initialize `FIRST(A) = ∅` for all non-terminals.
2. For each production `A → X₁X₂...Xₙ`:
   - Add `FIRST(X₁) − {ε}` to `FIRST(A)`
   - If `ε ∈ FIRST(X₁)`, also add `FIRST(X₂) − {ε}`, and so on
   - If all `Xᵢ` can derive ε, add `ε` to `FIRST(A)`
3. Repeat until no changes occur.

### FOLLOW
1. Initialize `FOLLOW(S) = {$}` for start symbol `S`.
2. For each production `A → αBβ`:
   - Add `FIRST(β) − {ε}` to `FOLLOW(B)`
   - If `ε ∈ FIRST(β)`, add `FOLLOW(A)` to `FOLLOW(B)`
3. Repeat until no changes occur.

---

## How to Run

```bash
python first_and_follow.py
```

The program processes three built-in grammars and also has an interactive mode.

### Interactive Input Format
```
E -> TR
R -> +TR | e
T -> FY
Y -> *FY | e
F -> (E) | i
done
```
> Use `e` to represent ε (epsilon).

---

## Sample Output

```
Non-Terminal    FIRST                               FOLLOW
───────────────────────────────────────────────────────────────────────────
E               { (, i }                            { $, ) }
F               { (, i }                            { $, ), *, + }
R               { +, ε }                            { $, ) }
T               { (, i }                            { $, ), + }
Y               { *, ε }                            { $, ), + }
```

---

## Files
| File                  | Description                      |
|-----------------------|----------------------------------|
| `first_and_follow.py` | Python implementation            |
| `README.md`           | This documentation file          |

---

## Result
The program correctly computes FIRST and FOLLOW sets for any context-free grammar, including those with ε-productions.
