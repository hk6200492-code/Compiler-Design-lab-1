# Experiment 7: Shift-Reduce Parsing

## Aim
To write a Python program that implements a **Shift-Reduce Parser** — a bottom-up parsing technique used in LR parsers.

---

## Theory

**Shift-Reduce Parsing** is a bottom-up parsing strategy that reconstructs the parse tree from leaves to root by repeatedly applying two operations:

| Operation  | Description |
|------------|-------------|
| **Shift**  | Push the next input token onto the stack |
| **Reduce** | Replace the top of the stack matching a production's RHS with its LHS |

The parser **accepts** when the stack contains only the start symbol and the input is fully consumed.

### Example Grammar
```
E → E + E
E → E * E
E → ( E )
E → i
```

---

## Algorithm

1. Initialize stack with `$`, input pointer at first token.
2. **Repeat:**
   - Attempt to **Reduce**: scan grammar rules; if the stack top matches any RHS, pop those symbols and push the LHS.
   - If no reduction is possible, **Shift**: push the next input token.
   - If stack = `[$, S]` and input = `$` → **ACCEPT**.
   - If no shift or reduce is possible → **ERROR**.

---

## How to Run

```bash
python shift_reduce.py
```

The program will:
- Parse four built-in test strings with Example Grammar 1
- Parse a multi-char token example (`id + id * id`)
- Allow interactive grammar input and string parsing

---

## Sample Output for `i+i*i`

```
Stack                            Input                  Action
$                                i+i*i$                 Shift   'i'
$ i                              +i*i$                  Reduce  E → i
$ E                              +i*i$                  Shift   '+'
$ E +                            i*i$                   Shift   'i'
$ E + i                          *i$                    Reduce  E → i
$ E + E                          *i$                    Reduce  E → E+E
$ E                              *i$                    Shift   '*'
$ E *                            i$                     Shift   'i'
$ E * i                          $                      Reduce  E → i
$ E * E                          $                      Reduce  E → E*E
$ E                              $                      ACCEPT ✓
```

---

## Files
| File               | Description                      |
|--------------------|----------------------------------|
| `shift_reduce.py`  | Python implementation            |
| `README.md`        | This documentation file          |

---

## Notes
- Multi-character tokens (like `id`) should be space-separated in the input string: `id + id * id`
- The parser tries rules in order — order of grammar rules affects which reduction is chosen for ambiguous grammars.

---

## Result
The program successfully simulates shift-reduce parsing and prints a step-by-step trace showing every stack state, remaining input, and action taken.
