# Topic 14: Global Data Flow Analysis (Reaching Definitions + Live Variables)


def reaching_definitions(cfg, gen, kill):
    """
    Compute Reaching Definitions for each block.

    cfg  : dict { block_id -> [successor block_ids] }
    gen  : dict { block_id -> set of definitions generated }
    kill : dict { block_id -> set of definitions killed }

    Returns RD_in, RD_out for each block.
    """
    RD_in  = {b: set() for b in cfg}
    RD_out = {b: set() for b in cfg}

    iteration = 0
    changed = True
    while changed:
        changed = False
        iteration += 1
        for b in cfg:
            # IN[b] = union of OUT[p] for all predecessors p
            preds = [p for p, succs in cfg.items() if b in succs]
            RD_in[b] = set().union(*(RD_out[p] for p in preds)) if preds else set()
            # OUT[b] = GEN[b] ∪ (IN[b] - KILL[b])
            new_out = gen[b] | (RD_in[b] - kill[b])
            if new_out != RD_out[b]:
                RD_out[b] = new_out
                changed = True

    print(f"  Converged in {iteration} iteration(s).")
    return RD_in, RD_out


def live_variables(cfg, use, defn):
    """
    Compute Live Variables for each block (backward analysis).

    cfg  : dict { block_id -> [successor block_ids] }
    use  : dict { block_id -> set of variables used before defined }
    defn : dict { block_id -> set of variables defined }

    Returns LV_in, LV_out for each block.
    """
    LV_in  = {b: set() for b in cfg}
    LV_out = {b: set() for b in cfg}

    iteration = 0
    changed = True
    while changed:
        changed = False
        iteration += 1
        for b in cfg:
            # OUT[b] = union of IN[s] for all successors s
            LV_out[b] = set().union(*(LV_in[s] for s in cfg[b])) if cfg[b] else set()
            # IN[b] = USE[b] ∪ (OUT[b] - DEF[b])
            new_in = use[b] | (LV_out[b] - defn[b])
            if new_in != LV_in[b]:
                LV_in[b] = new_in
                changed = True

    print(f"  Converged in {iteration} iteration(s).")
    return LV_in, LV_out


def print_table(title, in_map, out_map):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    print(f"  {'Block':<8} {'IN':<25} {'OUT'}")
    print(f"  {'-'*50}")
    for b in sorted(in_map):
        print(f"  {b:<8} {str(sorted(in_map[b])):<25} {sorted(out_map[b])}")


# -------------------------------------------------------
# Example CFG:
#
#   B1 --> B2 --> B3
#          ^       |
#          |_______|  (back edge: loop)
# -------------------------------------------------------

cfg = {
    'B1': ['B2'],
    'B2': ['B3', 'B1'],   # B2 loops back to B1
    'B3': []
}

print("Control Flow Graph:")
for b, succs in cfg.items():
    print(f"  {b} -> {succs}")

# --- Reaching Definitions ---
# Definitions: d1 (B1 defines a), d2 (B1 defines b),
#              d3 (B2 defines a), d4 (B3 defines c)
gen_rd  = {'B1': {'d1', 'd2'}, 'B2': {'d3'},       'B3': {'d4'}}
kill_rd = {'B1': {'d3'},       'B2': {'d1'},        'B3': set()}

print("\nReaching Definitions:")
print(f"  GEN  = {gen_rd}")
print(f"  KILL = {kill_rd}")
rd_in, rd_out = reaching_definitions(cfg, gen_rd, kill_rd)
print_table("Reaching Definitions Results", rd_in, rd_out)

# --- Live Variables ---
use_lv  = {'B1': {'a', 'b'}, 'B2': {'c', 'd'}, 'B3': {'a', 'e'}}
def_lv  = {'B1': {'c'},      'B2': {'a', 'b'}, 'B3': {'f'}}

print("\nLive Variables:")
print(f"  USE = {use_lv}")
print(f"  DEF = {def_lv}")
lv_in, lv_out = live_variables(cfg, use_lv, def_lv)
print_table("Live Variables Results", lv_in, lv_out)
