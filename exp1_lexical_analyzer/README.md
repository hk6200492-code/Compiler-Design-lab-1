# Experiment 1: Implementation of Lexical Analyzer

## Aim
To develop a lexical analyzer that identifies **identifiers**, **constants**, **comments**, **operators**, **keywords**, and **punctuation** from a given source code string.

---

## Theory
A **Lexical Analyzer** (also called a scanner or tokenizer) is the first phase of a compiler. It reads the source code character by character and groups them into meaningful sequences called **tokens**.

### Token Types Identified
| Token Type     | Examples                          |
|----------------|-----------------------------------|
| KEYWORD        | `int`, `float`, `while`, `return` |
| IDENTIFIER     | `main`, `count`, `x`              |
| INT_CONST      | `0`, `1`, `10`                    |
| FLOAT_CONST    | `3.14`, `1.0`                     |
| OPERATOR       | `+`, `-`, `*`, `==`, `++`         |
| PUNCTUATION    | `(`, `)`, `{`, `}`, `;`           |
| COMMENT        | `// ...` or `/* ... */`           |
| STRING_LITERAL | `"hello"`                         |
| UNKNOWN        | Any unrecognized character        |

---

## Algorithm
1. Start scanning the source string from left to right.
2. Skip whitespace characters (space, tab, newline).
3. Detect and skip single-line (`//`) and multi-line (`/* */`) comments.
4. If the current character starts an alphabetic sequence → extract the full word and classify as **KEYWORD** or **IDENTIFIER**.
5. If the current character is a digit → extract the full number and classify as **INT_CONST** or **FLOAT_CONST**.
6. Check for two-character operators (`==`, `!=`, `++`, etc.) before single-character operators.
7. Classify remaining characters as **OPERATOR**, **PUNCTUATION**, or **UNKNOWN**.
8. Print all collected tokens with their types.

---

## How to Run

```bash
python lexical_analyzer.py
```

The program will:
- Analyze a built-in sample C-like code snippet.
- Display all tokens in a formatted table.
- Prompt you to enter your own source code for analysis.

---

## Sample Input
```c
int main() {
    float x = a + 1;
    // single-line comment
    int count = 0;
    while (count < 10) {
        count++;
    }
    return 0;
}
```

## Sample Output
```
TOKEN TYPE           VALUE
---------------------------------------------
KEYWORD              int
IDENTIFIER           main
PUNCTUATION          (
PUNCTUATION          )
PUNCTUATION          {
KEYWORD              float
IDENTIFIER           x
OPERATOR             =
IDENTIFIER           a
OPERATOR             +
INT_CONST            1
PUNCTUATION          ;
COMMENT              // single-line comment
...
```

---

## Files
| File                  | Description                        |
|-----------------------|------------------------------------|
| `lexical_analyzer.py` | Python implementation of the lexer |
| `README.md`           | This documentation file            |

---

## Result
The program successfully tokenizes C-like source code and classifies each token into its appropriate category.
