# 10 – Intermediate Code Gen: Postfix & Prefix

## Overview
This program converts **infix expressions** into **Postfix (RPN)** and
**Prefix (Polish Notation)** representations by first building an
**Abstract Syntax Tree (AST)** via a recursive descent parser, then
traversing the tree to produce each notation.

---

## Concepts Covered
- **Infix Notation**: Standard human-readable form — `(a + b) * c`
- **Postfix Notation (RPN)**: Operator comes *after* operands — `a b + c *`  
  Used in stack-based evaluation and many compilers.
- **Prefix Notation**: Operator comes *before* operands — `* + a b c`  
  Used in some functional languages and Lisp-style representations.
- **AST (Abstract Syntax Tree)**: Tree where internal nodes are operators and leaves are operands.
- **Recursive Descent Parser**: Parses expressions respecting precedence (`*` before `+`).

---

## How It Works
1. Tokenized infix expression is passed to the parser.
2. Parser builds an AST respecting operator precedence and parentheses.
3. `to_postfix()` traverses the AST in **Left → Right → Root** order.
4. `to_prefix()` traverses the AST in **Root → Left → Right** order.

---

## Example
```
Input   : (a + b) * (c - d)
Postfix : a b + c d - *
Prefix  : * + a b - c d
```

---

## How to Run
```bash
python3 10_postfix_prefix.py
```

## Dependencies
- Python 3.x (standard library only)

---

## Key Classes & Functions
| Name | Description |
|------|-------------|
| `ExprNode` | AST node with value, left child, right child |
| `parse_infix(tokens)` | Recursive descent parser — builds the AST |
| `to_postfix(node)` | Traverses AST to generate postfix string |
| `to_prefix(node)` | Traverses AST to generate prefix string |

---

## Traversal Order Summary
| Notation | Traversal |
|----------|-----------|
| Infix    | Left → Root → Right |
| Postfix  | Left → Right → Root |
| Prefix   | Root → Left → Right |
