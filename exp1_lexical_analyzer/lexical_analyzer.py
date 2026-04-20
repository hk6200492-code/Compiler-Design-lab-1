"""
Experiment 1: Implementation of Lexical Analyzer
Compiler Design Lab (18CSC304J)
SRM Institute of Science and Technology
"""


def lexical_analyzer(source_code: str):
    """
    Lexical Analyzer: tokenizes the given source code string.
    Identifies keywords, identifiers, operators, constants,
    punctuation, comments, and string literals.
    """

    keywords = {
        "auto", "break", "case", "char", "const", "continue", "default",
        "do", "double", "else", "enum", "extern", "float", "for", "goto",
        "if", "int", "long", "register", "return", "short", "signed",
        "sizeof", "static", "struct", "switch", "typedef", "union",
        "unsigned", "void", "volatile", "while"
    }

    operators   = set("+-*/%=<>!&|^~")
    punctuation = set("(){}[];,.")

    tokens = []
    i = 0
    n = len(source_code)

    while i < n:
        ch = source_code[i]

        # Whitespace
        if ch in " \t\n":
            i += 1
            continue

        # Single-line comment
        if source_code[i:i+2] == "//":
            j = i + 2
            while j < n and source_code[j] != "\n":
                j += 1
            tokens.append(("COMMENT", source_code[i:j]))
            i = j
            continue

        # Multi-line comment
        if source_code[i:i+2] == "/*":
            j = i + 2
            while j < n - 1 and source_code[j:j+2] != "*/":
                j += 1
            tokens.append(("COMMENT", source_code[i:j+2]))
            i = j + 2
            continue

        # String literal
        if ch == '"':
            j = i + 1
            while j < n and source_code[j] != '"':
                j += 1
            tokens.append(("STRING_LITERAL", source_code[i:j+1]))
            i = j + 1
            continue

        # Keywords and identifiers
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (source_code[j].isalnum() or source_code[j] == "_"):
                j += 1
            word = source_code[i:j]
            token_type = "KEYWORD" if word in keywords else "IDENTIFIER"
            tokens.append((token_type, word))
            i = j
            continue

        # Integer and float constants
        if ch.isdigit():
            j = i
            is_float = False
            while j < n and (source_code[j].isdigit() or source_code[j] == "."):
                if source_code[j] == ".":
                    is_float = True
                j += 1
            token_type = "FLOAT_CONST" if is_float else "INT_CONST"
            tokens.append((token_type, source_code[i:j]))
            i = j
            continue

        # Two-character operators
        two_char = source_code[i:i+2]
        if two_char in ("==", "!=", "<=", ">=", "++", "--", "&&", "||",
                        "+=", "-=", "*=", "/=", "->", "<<", ">>"):
            tokens.append(("OPERATOR", two_char))
            i += 2
            continue

        # Single-character operators
        if ch in operators:
            tokens.append(("OPERATOR", ch))
            i += 1
            continue

        # Punctuation
        if ch in punctuation:
            tokens.append(("PUNCTUATION", ch))
            i += 1
            continue

        # Unknown
        tokens.append(("UNKNOWN", ch))
        i += 1

    return tokens


def display_tokens(tokens):
    print(f"\n{'TOKEN TYPE':<20} VALUE")
    print("-" * 45)
    for token_type, value in tokens:
        print(f"{token_type:<20} {value}")
    print(f"\nTotal tokens: {len(tokens)}")


if __name__ == "__main__":
    sample_code = """
int main() {
    float x = a + 1;
    // single-line comment
    int count = 0;
    /* multi-line
       comment */
    while (count < 10) {
        count++;
    }
    return 0;
}
"""
    print("=" * 50)
    print("EXPERIMENT 1: LEXICAL ANALYZER")
    print("=" * 50)
    print("\nSource Code:")
    print(sample_code)

    tokens = lexical_analyzer(sample_code)
    display_tokens(tokens)

    # Interactive mode
    print("\n--- Interactive Mode ---")
    user_code = input("Enter source code to analyze (single line): ")
    if user_code.strip():
        t = lexical_analyzer(user_code)
        display_tokens(t)
