#!/usr/bin/env python3
"""Run test_all.py's nine group modules in parallel, in separate processes.

    python3 tests/run_parallel.py            # processes at once = CPU count
    python3 tests/run_parallel.py --jobs 2

The same tests as `python3 tests/test_all.py`, in the same modules; only the wall time changes.
Each module runs in its own interpreter with its own OUT directory (tests/out/<module>), because
the modules share output names (cap_mux.mp4 is written by three tests) and must not overwrite
each other's files. A module's output is printed whole when it finishes, never interleaved, and
the run fails if any module fails. The slowest modules start first so the longest one is not
left running alone at the end. The four largest modules run as two shards each (every other test
of the module, in its own process and OUT directory), so no one module sets the wall time.
"""
import argparse
import os
import re
import subprocess
import sys
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import test_all  # noqa: E402

# Seconds each module took serially on a 4-core Linux machine (2.17.2): the order to start them in.
ROUGH_SECONDS = {"test_picture": 600, "test_orchestration": 450, "test_analysis": 330, "test_editing": 300,
                 "test_delivery": 230, "test_cut_copy": 200, "test_audio": 160, "test_asr": 60, "test_accel": 40}
SHARDS = {"test_picture": 2, "test_orchestration": 2, "test_analysis": 2, "test_editing": 2}


def _flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _flatten(item)
        else:
            yield item


def run_shard(name: str, k: int, n: int) -> int:
    """Child mode: run every n-th test of module `name`, starting at k, in definition order."""
    tests = list(_flatten(unittest.defaultTestLoader.loadTestsFromName(name)))
    suite = unittest.TestSuite(t for i, t in enumerate(tests) if i % n == k)
    return 0 if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful() else 1


def run_job(job: "tuple", out_root: Path) -> "tuple":
    name, k, n = job
    label = name if n == 1 else f"{name}[{k + 1}/{n}]"
    out = out_root / (name.replace("test_", "") + ("" if n == 1 else f"_{k + 1}"))
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, OUT=str(out))
    cmd = ([sys.executable, "-m", "unittest", name] if n == 1
           else [sys.executable, str(Path(__file__).resolve()), "--shard", name, str(k), str(n)])
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=str(HERE), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, encoding="utf-8", errors="replace")
    return label, proc.returncode, time.time() - t0, proc.stdout


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--jobs", type=int, default=0, help="processes run at once (default: CPU count)")
    ap.add_argument("--shard", nargs=3, metavar=("MODULE", "K", "N"), help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.shard:
        return run_shard(args.shard[0], int(args.shard[1]), int(args.shard[2]))
    names = [m.__name__ for m in test_all.MODULES]
    work = sorted(((n, k, SHARDS.get(n, 1)) for n in names for k in range(SHARDS.get(n, 1))),
                  key=lambda j: -ROUGH_SECONDS.get(j[0], 0) / j[2])
    jobs = args.jobs or min(os.cpu_count() or 1, len(work))
    # absolute: the children run with cwd=tests/, so a relative OUT would mean a different place there
    out_root = Path(os.environ.get("OUT", HERE / "out")).resolve()
    t0 = time.time()
    failed, ran = [], 0
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for name, code, secs, output in pool.map(lambda j: run_job(j, out_root), work):
            last = output.strip().splitlines()[-1] if output.strip() else ""
            ran += sum(int(m) for m in re.findall(r"^Ran (\d+) tests?", output, flags=re.M))
            print(f"\n===== {name}: {'OK' if code == 0 else 'FAILED'} in {secs:.0f}s ({last}) =====")
            if code != 0:
                failed.append(name)
                print(output)
            else:
                print("\n".join(line for line in output.splitlines()[-3:]))
    print(f"\n{ran} tests, {len(names)} modules in {len(work)} processes, {jobs} at a time, {time.time() - t0:.0f}s wall; "
          + ("FAILED: " + ", ".join(failed) if failed else "all OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
