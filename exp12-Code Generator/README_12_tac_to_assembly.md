# 12 – A Simple Code Generator (TAC → Assembly)

## Overview
This program implements a **simple code generator** that translates
**Three-Address Code (TAC)** into **assembly-like instructions**.
It includes a basic **register allocator** with a spill strategy,
modeling how a real compiler back-end maps variables to CPU registers.

---

## Concepts Covered
- **Code Generation**: Translating IR (TAC) into target machine instructions.
- **Register Descriptor**: Tracks which variable is currently held in each register.
- **Address Descriptor**: Tracks where each variable's value lives (register or memory).
- **Register Allocation**: Assigning variables to a limited set of registers.
- **Spilling**: When all registers are occupied, one is saved to memory to free it up.
- **LD / ST / MOV / ADD / SUB / MUL / DIV**: Simulated assembly instruction set.

---

## Instruction Set Used
| Instruction | Meaning |
|-------------|---------|
| `LD Rx, var` | Load variable from memory into register Rx |
| `ST var, Rx` | Store register Rx back to variable in memory |
| `MOV Rx, Ry` | Copy register Ry into Rx |
| `ADD Rx, Ry, Rz` | Rx = Ry + Rz |
| `SUB Rx, Ry, Rz` | Rx = Ry - Rz |
| `MUL Rx, Ry, Rz` | Rx = Ry * Rz |
| `DIV Rx, Ry, Rz` | Rx = Ry / Rz |

---

## How It Works
1. For each TAC instruction, determine registers for all operands.
2. Emit `LD` instructions to load operands into registers.
3. Emit the corresponding ALU instruction.
4. If registers are exhausted, spill a register (save to memory, reuse it).
5. At the end, store all live variables back to memory with `ST`.

---

## Example
```
TAC Input:
  t1 = b + c
  t2 = t1 * d
  a  = t2 - e

Generated Assembly:
  LD   R0, b
  LD   R1, c
  ADD  R2, R0, R1      ; t1 = b + c
  LD   R2, t1
  LD   R3, d
  MUL  R0, R2, R3      ; t2 = t1 * d
  ...
  ST   a, R0
```

---

## How to Run
```bash
python3 12_tac_to_assembly.py
```

## Dependencies
- Python 3.x (standard library only)

---

## Key Class
| Method | Description |
|--------|-------------|
| `SimpleCodeGen.get_reg(var)` | Returns a register for a variable, spilling if needed |
| `SimpleCodeGen.generate(tac)` | Processes TAC list and emits assembly instructions |
