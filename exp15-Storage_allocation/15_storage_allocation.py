# Topic 15: Storage Allocation – Static, Stack, and Heap


# =============================================================
# STATIC ALLOCATION
# Fixed addresses assigned at compile time (global/static vars)
# =============================================================
class StaticAllocator:
    def __init__(self, base=1000):
        self.memory = {}       # name -> address
        self.sizes = {}        # name -> size
        self.address = base

    def allocate(self, name, size=4):
        if name in self.memory:
            raise ValueError(f"'{name}' already statically allocated.")
        self.memory[name] = self.address
        self.sizes[name] = size
        self.address += size
        return self.memory[name]

    def get_address(self, name):
        return self.memory.get(name, None)

    def display(self):
        print("┌─ Static Memory Layout ─────────────────────┐")
        for name, addr in self.memory.items():
            bar = '█' * (self.sizes[name] // 4)
            print(f"│  {addr:>5}  {name:<10} size={self.sizes[name]}  {bar}")
        print(f"└─ Next free: {self.address} ──────────────────────┘")


# =============================================================
# STACK ALLOCATION
# Activation records pushed/popped per function call
# =============================================================
class StackAllocator:
    def __init__(self, base=2000):
        self.sp = base
        self.base = base
        self.frames = []      # stack of (func_name, frame_base, var_offsets)
        self.call_log = []

    def call(self, func_name, local_vars: dict):
        """
        Push an activation record.
        local_vars: {var_name: size_in_bytes}
        """
        frame_base = self.sp
        var_offsets = {}
        for var, sz in local_vars.items():
            var_offsets[var] = self.sp
            self.sp += sz
        self.frames.append((func_name, frame_base, var_offsets))
        self.call_log.append(f"CALL {func_name:<10} frame_base={frame_base}  SP={self.sp}")

    def ret(self):
        """Pop the topmost activation record."""
        if not self.frames:
            raise RuntimeError("Stack underflow!")
        func_name, frame_base, _ = self.frames.pop()
        self.sp = frame_base
        self.call_log.append(f"RET  {func_name:<10} SP restored to {self.sp}")

    def display(self):
        print("┌─ Stack Frames ─────────────────────────────┐")
        for func, fbase, vars_ in self.frames:
            print(f"│  [{func}]  base={fbase}")
            for v, addr in vars_.items():
                print(f"│    {addr:>5}  {v}")
        print(f"│  SP = {self.sp}")
        print("└────────────────────────────────────────────┘")
        print("\nCall Log:")
        for entry in self.call_log:
            print(f"  {entry}")


# =============================================================
# HEAP ALLOCATION
# Dynamic memory – first-fit allocator with free/coalesce
# =============================================================
class HeapAllocator:
    def __init__(self, base=3000, total=256):
        # Each block: {'start': int, 'size': int, 'free': bool, 'name': str|None}
        self.blocks = [{'start': base, 'size': total, 'free': True, 'name': None}]
        self.allocations = {}   # name -> block index

    def malloc(self, name, size):
        """First-fit allocation."""
        for i, blk in enumerate(self.blocks):
            if blk['free'] and blk['size'] >= size:
                addr = blk['start']
                remainder = blk['size'] - size
                blk['size'] = size
                blk['free'] = False
                blk['name'] = name
                if remainder > 0:
                    new_blk = {'start': addr + size, 'size': remainder,
                               'free': True, 'name': None}
                    self.blocks.insert(i + 1, new_blk)
                self.allocations[name] = i
                print(f"  malloc({name!r:10}, {size:3}B) → address {addr}")
                return addr
        raise MemoryError(f"Heap: cannot allocate {size} bytes for '{name}'")

    def free(self, name):
        """Free a named allocation and coalesce adjacent free blocks."""
        if name not in self.allocations:
            raise KeyError(f"'{name}' not found in heap.")
        idx = self.allocations.pop(name)
        self.blocks[idx]['free'] = True
        self.blocks[idx]['name'] = None
        # Update indices after possible coalesce
        self._coalesce()
        print(f"  free({name!r})")

    def _coalesce(self):
        i = 0
        while i < len(self.blocks) - 1:
            if self.blocks[i]['free'] and self.blocks[i + 1]['free']:
                self.blocks[i]['size'] += self.blocks[i + 1]['size']
                del self.blocks[i + 1]
            else:
                i += 1
        # Rebuild allocations index map
        self.allocations = {
            blk['name']: i
            for i, blk in enumerate(self.blocks)
            if not blk['free']
        }

    def display(self):
        print("┌─ Heap Layout ──────────────────────────────┐")
        for blk in self.blocks:
            status = 'FREE' if blk['free'] else f"USED ({blk['name']})"
            bar = '░' * (blk['size'] // 8) if blk['free'] else '█' * (blk['size'] // 8)
            print(f"│  {blk['start']:>5}  size={blk['size']:>4}B  {status:<18} {bar}")
        print("└────────────────────────────────────────────┘")


# ── Demo ─────────────────────────────────────────────────────

print("=" * 50)
print("  STATIC ALLOCATION")
print("=" * 50)
static = StaticAllocator(base=1000)
static.allocate('x',   4)
static.allocate('y',   4)
static.allocate('arr', 16)
static.allocate('flag', 1)
static.display()

print("\n" + "=" * 50)
print("  STACK ALLOCATION")
print("=" * 50)
stack = StackAllocator(base=2000)
stack.call('main',  {'argc': 4, 'argv': 8})
stack.call('foo',   {'x': 4, 'y': 4, 'temp': 4})
stack.call('bar',   {'buf': 16})
stack.display()
print()
stack.ret()   # return from bar
stack.ret()   # return from foo
print("\nAfter returns:")
stack.display()

print("\n" + "=" * 50)
print("  HEAP ALLOCATION")
print("=" * 50)
heap = HeapAllocator(base=3000, total=256)
heap.malloc('node1', 32)
heap.malloc('node2', 64)
heap.malloc('node3', 16)
print()
heap.display()
print()
heap.free('node2')
heap.malloc('node4', 48)
print()
heap.display()
