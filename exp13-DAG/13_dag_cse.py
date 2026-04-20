# Topic 13: Implementation of DAG (CSE Elimination)


class DAGNode:
    def __init__(self, op, left=None, right=None, value=None):
        self.op = op          # operator or 'leaf'
        self.left = left      # index of left child
        self.right = right    # index of right child
        self.value = value    # for leaf nodes: variable/constant name
        self.labels = set()   # variables that map to this node


class DAG:
    def __init__(self):
        self.nodes = []
        self.var_map = {}     # variable name -> node index
        self.node_map = {}    # (op, left_idx, right_idx) -> node index

    def get_or_create_leaf(self, val):
        if val in self.var_map:
            return self.var_map[val]
        node = DAGNode('leaf', value=val)
        node.labels.add(val)
        idx = len(self.nodes)
        self.nodes.append(node)
        self.var_map[val] = idx
        return idx

    def get_or_create_op(self, op, left, right):
        key = (op, left, right)
        if key in self.node_map:
            # CSE: reuse existing node — no new code needed!
            return self.node_map[key]
        node = DAGNode(op, left, right)
        idx = len(self.nodes)
        self.nodes.append(node)
        self.node_map[key] = idx
        return idx

    def process(self, instructions):
        """Process list of TAC instructions: 'x = y op z' or 'x = y'"""
        ops = ['+', '-', '*', '/']
        for instr in instructions:
            lhs, rhs = instr.replace(' ', '').split('=', 1)
            found_op = False
            for op in ops:
                if op in rhs:
                    y, z = rhs.split(op, 1)
                    nl = self.get_or_create_leaf(y)
                    nr = self.get_or_create_leaf(z)
                    ni = self.get_or_create_op(op, nl, nr)
                    self.nodes[ni].labels.add(lhs)
                    self.var_map[lhs] = ni
                    found_op = True
                    break
            if not found_op:
                ni = self.get_or_create_leaf(rhs)
                self.nodes[ni].labels.add(lhs)
                self.var_map[lhs] = ni

    def print_dag(self):
        print("DAG Nodes:")
        print(f"  {'Node':<6} {'Type':<8} {'Detail':<25} {'Labels'}")
        print("  " + "-" * 55)
        for i, n in enumerate(self.nodes):
            if n.op == 'leaf':
                detail = f"value='{n.value}'"
                print(f"  {i:<6} {'LEAF':<8} {detail:<25} {n.labels}")
            else:
                detail = f"({n.op}, node[{n.left}], node[{n.right}])"
                print(f"  {i:<6} {'OP':<8} {detail:<25} {n.labels}")

    def print_optimized_code(self):
        """Emit optimized code from DAG (one instruction per unique node)."""
        print("\nOptimized Code (CSE applied):")
        emitted = set()
        for i, n in enumerate(self.nodes):
            if n.op != 'leaf' and i not in emitted:
                label = next(iter(n.labels))
                l_node = self.nodes[n.left]
                r_node = self.nodes[n.right]
                lv = l_node.value if l_node.op == 'leaf' else f"node[{n.left}]"
                rv = r_node.value if r_node.op == 'leaf' else f"node[{n.right}]"
                print(f"  {label} = {lv} {n.op} {rv}   ; used by {n.labels}")
                emitted.add(i)


# Instructions with common subexpressions
instructions = [
    "t1 = b + c",
    "t2 = b + c",   # same as t1 -> CSE
    "t3 = t1 * d",
    "t4 = t2 * d",  # same as t3 -> CSE
    "a  = t3 - e",
]

print("Input Instructions:")
for ins in instructions:
    print(f"  {ins}")
print()

dag = DAG()
dag.process(instructions)
dag.print_dag()
dag.print_optimized_code()
