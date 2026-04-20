# Experiment 4: Elimination of Ambiguity, Left Recursion and Left Factoring

## Aim
To study ambiguity and implement the elimination of **Left Recursion** and **Left Factoring** from context-free grammars.

---

## Theory

### Ambiguity
A grammar is **ambiguous** if a string can have more than one parse tree (or leftmost derivation). Common causes include left recursion and common prefixes.

### Left Recursion
A production is **left-recursive** if it has the form:
```
A → Aα
```
This causes **infinite loops** in top-down (recursive-descent) parsers.

**Elimination:** Convert `A → Aα | β`  to:
```
A  → βA'
A' → αA' | ε
```

### Left Factoring
When two productions share a common prefix, the parser cannot decide which rule to apply:
```
A → αβ₁ | αβ₂
```
**Left Factoring** defers the decision:
```
A  → αA'
A' → β₁ | β₂
```

---

## Algorithm

### Eliminate Left Recursion
1. For each non-terminal `A`, split productions into:
   - **α-group**: bodies starting with `A`  (recursive)
   - **β-group**: bodies NOT starting with `A`
2. If α-group is non-empty, create new non-terminal `A'`:
   - `A  → βA'` for each β
   - `A' → αA' | ε` for each α

### Left Factoring
1. Group alternatives by their first character.
2. For each group with more than one alternative, find the **longest common prefix** `α`.
3. Replace the group with `αA'` and create new rule `A' → β₁ | β₂ | ...`
4. Repeat until no common prefixes remain.

---

## How to Run

```bash
python left_recursion_factoring.py
```

The program will:
- Process three built-in example grammars
- Show the grammar before and after each transformation
- Allow you to enter your own grammar interactively

### Interactive Input Format
```
E -> E+T | T
T -> T*F | F
F -> (E) | id
done
```

---

## Sample Input / Output

**Input:**
```
E -> E+T | T
T -> T*F | F
```

**After Eliminating Left Recursion:**
```
E  ->  TE'
E' ->  +TE' | ε
T  ->  FT'
T' ->  *FT' | ε
F  ->  (E) | id
```

---

## Files
| File                           | Description                    |
|--------------------------------|--------------------------------|
| `left_recursion_factoring.py`  | Python implementation          |
| `README.md`                    | This documentation file        |

---

## Result
The program successfully eliminates left recursion and applies left factoring to transform grammars into LL(1)-compatible form.
