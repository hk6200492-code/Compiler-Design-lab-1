# 15 – Storage Allocation: Static, Stack, and Heap

## Overview
This program simulates the three fundamental **storage allocation strategies**
used by compilers and runtime systems:

1. **Static Allocation** — fixed addresses at compile time.
2. **Stack Allocation** — dynamic activation records for function calls.
3. **Heap Allocation** — dynamic memory with explicit malloc/free.

---

## Concepts Covered

### 1. Static Allocation
Variables are assigned **fixed memory addresses** at compile time.
Used for global variables, static variables, and constants.

- Address is known before the program runs.
- No runtime overhead for allocation.
- Size must be known at compile time.

### 2. Stack Allocation
Memory is managed via a **stack of activation records** (stack frames).
Each function call pushes a frame; each return pops it.

An **activation record** contains:
- Local variables
- Parameters
- Return address
- Saved registers

The **Stack Pointer (SP)** tracks the top of the stack.
Allocation = increment SP. Deallocation = decrement SP (free entire frame).

### 3. Heap Allocation
Memory is allocated and freed **explicitly at runtime** in arbitrary order.
Used for dynamically-sized data structures (linked lists, trees, etc.).

This implementation uses a **first-fit** strategy:
- Scan free blocks from the start.
- Allocate the first block large enough.
- Split the block if there is leftover space.
- On `free()`, mark the block free and **coalesce** adjacent free blocks.

---

## Memory Layout (Example)
```
Address Range   Region     Description
─────────────────────────────────────────
1000 – 1024     Static     x, y, arr, flag
2000 – 2040     Stack      main frame, foo frame
3000 – 3256     Heap       dynamic allocations
```

---

## Sample Output
```
Static:
  1000  x     size=4   █
  1004  y     size=4   █
  1008  arr   size=16  ████

Stack:
  [main]  base=2000
    2000  argc
    2004  argv
  [foo]   base=2012
    2012  x

Heap:
  3000  size= 32  USED (node1)  ████
  3032  size= 64  USED (node2)  ████████
  3096  size=160  FREE          ░░░░░░░░
```

---

## How to Run
```bash
python3 15_storage_allocation.py
```

## Dependencies
- Python 3.x (standard library only)

---

## Key Classes
| Class | Method | Description |
|-------|--------|-------------|
| `StaticAllocator` | `allocate(name, size)` | Assigns next available static address |
| `StackAllocator` | `call(func, vars)` | Pushes a new activation record |
| `StackAllocator` | `ret()` | Pops the top frame, restores SP |
| `HeapAllocator` | `malloc(name, size)` | First-fit dynamic allocation |
| `HeapAllocator` | `free(name)` | Frees block and coalesces neighbours |

---

## Comparison Table
| Feature | Static | Stack | Heap |
|---------|--------|-------|------|
| When allocated | Compile time | Function call | Explicit `malloc` |
| When freed | Never (program lifetime) | Function return | Explicit `free` |
| Size known at? | Compile time | Compile time | Runtime |
| Fragmentation | None | None | Possible |
| Overhead | None | Very low | Higher |
| Use case | Globals, constants | Local vars, params | Dynamic structures |
