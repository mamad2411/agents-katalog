---
name: gt3-backside-route-policy
description: Apply and validate GT3 backside routing policy in Innovus. Use when configuring CTS/PDN/signal layer usage, submitting GT3 consistency runs, diagnosing zero-backside-nets, or enforcing BPR-reserved-for-PDN constraints.
---

# GT3 Backside Route Policy

Apply this policy for GT3 experiments unless the task brief explicitly overrides it.

## Policy defaults
1. Keep CTS route on `M4/M5`.
2. Keep PDN on high layers (`BSPDN_HI` => `M6/M7`).
3. Reserve `BPR` for PDN.
4. Allow backside signal routing on `BM2/BM1` only (`index 1..2`).
5. Treat `BM2 -> BM1 -> M0 -> M1` as the current working signal-entry hypothesis until disproved by a topology-validity gate.
6. Do not assume direct `BM1 -> M1` connectivity without explicit tool or techlef evidence.

## Submit controlled run

```bash
ROOT=/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00
cd "$ROOT"

TASK_BRIEF=<task_brief_md> \
BACKSIDE_SIGNAL_NET_FILE=<net_list_txt> \
BACKSIDE_SIGNAL_NET_BOTTOM_INDEX=1 \
BACKSIDE_SIGNAL_NET_TOP_INDEX=2 \
bash scripts/debug/submit_gt3_route_rc_consistency.sh <design> <run_tag>
```

Monitor outputs:
- `slurm_logs/04_delay_modeling/<run_tag>.monitor.md`
- `slurm_logs/04_delay_modeling/<run_tag>.monitor.history.tsv`

## Post-run checks
1. Verify backside signal occupancy appears on BM layers.
2. Verify signal occupancy does not use BPR.
3. Verify CTS remains on `M4/M5` window.
4. Verify the run does not rely on an unproven shortcut such as direct `BM1-M1`.

Load `references/policy_checks.md` for quick command snippets.
