# 14 – Global Data Flow Analysis (RD + Live Variables)

## Overview
This program implements two classic **global data flow analyses** that
operate over a **Control Flow Graph (CFG)**:

1. **Reaching Definitions (RD)** — a forward analysis.
2. **Live Variable Analysis (LV)** — a backward analysis.

Both use an **iterative fixed-point algorithm** that repeatedly updates
IN and OUT sets for each block until no further changes occur.

---

## Concepts Covered

### Control Flow Graph (CFG)
A directed graph where nodes are basic blocks and edges represent possible
control flow (branches, loops, fall-throughs).

### Reaching Definitions (Forward Analysis)
A definition `d: x = ...` **reaches** a point `p` if there exists a path
from `d` to `p` where `x` is not redefined along the way.

- **GEN[B]**: Definitions created in block B.
- **KILL[B]**: Definitions from other blocks that B overrides.
- **IN[B]** = ∪ OUT[predecessors]
- **OUT[B]** = GEN[B] ∪ (IN[B] − KILL[B])

### Live Variable Analysis (Backward Analysis)
A variable `x` is **live** at point `p` if its value may be used along
some path from `p` before being redefined.

- **USE[B]**: Variables used before being defined in B.
- **DEF[B]**: Variables defined in B.
- **OUT[B]** = ∪ IN[successors]
- **IN[B]** = USE[B] ∪ (OUT[B] − DEF[B])

---

## How It Works
1. Initialize all IN and OUT sets to empty.
2. Iterate over all blocks, recalculating IN and OUT using the equations above.
3. Repeat until a fixed point is reached (no set changes).
4. Print the final IN and OUT sets for each block.

---

## Example CFG
```
B1 → B2 → B3
     ↑_____|   (back edge — loop)
```

## Sample Output
```
Reaching Definitions:
  Block    IN                   OUT
  B1       {}                   {d1, d2}
  B2       {d1, d2}             {d2, d3}
  B3       {d2, d3}             {d2, d3, d4}

Live Variables:
  Block    IN                   OUT
  B1       {a, b, c}            {c, d}
  B2       {c, d, a, e}         {a, e}
  B3       {a, e}               {}
```

---

## How to Run
```bash
python3 14_data_flow_analysis.py
```

## Dependencies
- Python 3.x (standard library only)

---

## Key Functions
| Function | Type | Description |
|----------|------|-------------|
| `reaching_definitions(cfg, gen, kill)` | Forward | Computes RD_in, RD_out for each block |
| `live_variables(cfg, use, defn)` | Backward | Computes LV_in, LV_out for each block |
| `print_table(title, in_map, out_map)` | Utility | Displays results in a formatted table |

---

## Applications
- **Reaching Definitions** → used in constant propagation, ud-chains.
- **Live Variables** → used in register allocation, dead code elimination.
