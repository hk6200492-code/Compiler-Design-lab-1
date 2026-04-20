# Topic 12: A Simple Code Generator (TAC → Assembly)


class SimpleCodeGen:
    def __init__(self):
        self.reg_desc = {}    # reg -> variable currently held
        self.addr_desc = {}   # var -> set of locations (register or 'MEM')
        self.registers = ['R0', 'R1', 'R2', 'R3']
        self.asm = []

    def get_reg(self, var):
        """Return a register for the given variable, loading if necessary."""
        # Already in a register?
        for reg, v in self.reg_desc.items():
            if v == var:
                return reg
        # Find a free register
        used = set(self.reg_desc.keys())
        for r in self.registers:
            if r not in used:
                self.reg_desc[r] = var
                self.addr_desc.setdefault(var, set()).add(r)
                return r
        # Spill R0 to make room
        spill = 'R0'
        old_var = self.reg_desc[spill]
        self.asm.append(f"  ST   {old_var}, {spill}       ; spill {old_var} to memory")
        self.addr_desc[old_var] = {'MEM'}
        self.reg_desc[spill] = var
        self.addr_desc.setdefault(var, set()).add(spill)
        return spill

    def generate(self, tac_instructions):
        """Generate assembly from a list of TAC instructions."""
        self.asm = ["; ===== Generated Assembly Code ====="]
        op_map = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}

        for instr in tac_instructions:
            self.asm.append(f"\n  ; TAC: {instr}")
            parts = instr.split()

            if len(parts) == 5 and parts[1] == '=':
                # x = y op z
                x, _, y, op, z = parts
                ry = self.get_reg(y)
                self.asm.append(f"  LD   {ry}, {y}")
                rz = self.get_reg(z)
                self.asm.append(f"  LD   {rz}, {z}")
                rx = self.get_reg(x)
                self.asm.append(f"  {op_map[op]:<4} {rx}, {ry}, {rz}")
                self.reg_desc[rx] = x
                self.addr_desc[x] = {rx}

            elif len(parts) == 3 and parts[1] == '=':
                # x = y  (simple copy)
                x, _, y = parts
                ry = self.get_reg(y)
                self.asm.append(f"  LD   {ry}, {y}")
                rx = self.get_reg(x)
                self.asm.append(f"  MOV  {rx}, {ry}")
                self.reg_desc[rx] = x
                self.addr_desc[x] = {rx}

        # Store all variables back to memory at end
        self.asm.append("\n  ; ---- Store live variables ----")
        for reg, var in self.reg_desc.items():
            self.asm.append(f"  ST   {var}, {reg}")

        return self.asm


# Example TAC program
tac = [
    "t1 = b + c",
    "t2 = t1 * d",
    "t3 = a - e",
    "a = t2 + t3",
]

print("Input TAC:")
for t in tac:
    print(f"  {t}")

print()
gen = SimpleCodeGen()
for line in gen.generate(tac):
    print(line)
