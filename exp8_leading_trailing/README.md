# Experiment 8: Computation of LEADING and TRAILING

## Aim
To write a Python program to compute **LEADING** and **TRAILING** sets for each non-terminal in an operator grammar, and derive the **operator-precedence relations** (`<·`, `=·`, `>·`).

---

## Theory

**Operator-Precedence Parsing** works on **operator grammars** — grammars where no production has two adjacent non-terminals.

### LEADING Set
`LEADING(A)` = set of terminal symbols that can appear as the **leftmost terminal** in any string derived from `A`.

**Rule:** `a ∈ LEADING(A)` if:
- `A →* aγ`, OR
- `A →* Baγ` where `B` is a non-terminal

### TRAILING Set
`TRAILING(A)` = set of terminal symbols that can appear as the **rightmost terminal** in any string derived from `A`.

**Rule:** `a ∈ TRAILING(A)` if:
- `A →* γa`, OR
- `A →* γaB` where `B` is a non-terminal

---

## Operator-Precedence Relations

| Relation | Notation | Meaning |
|----------|----------|---------|
| Equal    | `a =· b` | `a` and `b` are at the same precedence level |
| Less     | `a <· b` | `a` has lower precedence than `b` |
| Greater  | `a >· b` | `a` has higher precedence than `b` |

**Derivation rules:**
- If `…aB…` appears in a production → `a <· LEADING(B)`
- If `…Ab…` appears in a production → `TRAILING(A) >· b`
- If `…aBb…` appears               → `a =· b`
- If `…ab…` appears                → `a =· b`

---

## Algorithm

1. Initialize `LEADING(A) = ∅` and `TRAILING(A) = ∅` for all non-terminals.
2. Scan each production to populate sets using the rules above.
3. Propagate sets iteratively until no changes occur.
4. Scan productions again to derive `<·`, `=·`, `>·` relations.
5. Display the precedence matrix.

---

## How to Run

```bash
python leading_trailing.py
```

The program processes two built-in grammars and then accepts interactive input.

### Interactive Input Format
```
E -> E+T | T
T -> T*F | F
F -> (E) | i
done
```

---

## Sample Output

```
Non-Terminal    LEADING                        TRAILING
───────────────────────────────────────────────────────────────────
E               { (, *, +, i }                 { ), *, +, i }
F               { (, i }                       { ), i }
T               { (, *, i }                    { ), *, i }

Operator Precedence Table
         (     )     *     +     i
────────────────────────────────────
     (        =·    <·    <·    <·
     )        >·    >·    >·
     *   <·   >·    >·    >·    <·
     +   <·   >·    <·    >·    <·
     i        >·    >·    >·
```

---

## Files
| File                   | Description                      |
|------------------------|----------------------------------|
| `leading_trailing.py`  | Python implementation            |
| `README.md`            | This documentation file          |

---

## Result
The program correctly computes LEADING and TRAILING sets and constructs the operator-precedence relation table for any valid operator grammar.
