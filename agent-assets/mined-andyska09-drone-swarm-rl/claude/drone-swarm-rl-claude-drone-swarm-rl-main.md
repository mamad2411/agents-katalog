# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Rules — every AI agent follows these, in every reply and every change

These rules are not optional. They come before your own defaults and before any skill's
instructions. If a rule seems to clash with what I ask, ask me before you act.

### Talking to me

- Start every message with `TARS:`.
- Write every reply in the [simple-english](.claude/output-styles/simple-english.md)
  output style.
- **Answer the question I asked, and nothing more.** Be short and direct.
- A question is not a sign that you were wrong. Do not re-analyse the plan, change your
  recommendations or rewrite your conclusions unless I tell you to. If something I said
  changes an earlier conclusion, say so in one line at the end, then stop and wait.
- When I give you new information, take it in and answer. Redo the analysis only if I
  ask for it.
- I am new to this field. Explain every term in plain words. When I ask what a term
  means, explain the idea, not the literature.

### Doing the work

- **Do only what I ask.** Do not add features, knobs, tests or metrics that I did not ask
  for. Suggest them in the chat instead.
- If one approach is clearly better, recommend it. If two are equally good, ask me.
  Always.
- Keep it simple. Simple means logic that is easy to follow, not few lines. Think first,
  then write the code.
- Keep diffs small. I want to read a change and know what it does.
- Everything stays under the repo root, `handoff.md` included. Scripts, probes and build
  artifacts go in `scratch/` (gitignored), never in `/tmp` or a session scratchpad.
- Unpublished papers under `research/papers/` stay local, and `CLAUDE.local.md` names
  them. Never commit one, never `git add -f` one, and never quote, summarise or name one
  in a tracked file, this one included.

### Code style

- Blunt, minimal code. No base classes, protocols or registries. One file per concern,
  readable top to bottom.
- Comments: as few as possible. Write one only where the code cannot say it itself: a
  constraint, a non-obvious reason, a trap. Never restate what the line does. One clear
  sentence beats three. No banner blocks, no section dividers.
- **Comments and docstrings say what the code does now.** No story and no claim about
  what the code does not do. No history and no sources in code: git keeps the history,
  and the notes keep the sources.
- Docstrings: a module gets a short one. A function gets one only if its contract is not
  obvious from its name and signature.

### For Codex

Edit only the named file. Do not run tests. Stop after the edit, summarize it, and wait
for approval before you touch another file. The only exception: I tell you to run wild.

## What this repository is

A research workspace for multi-robot / swarm RL. Our own code lives in `swarm/`;
`research/` holds notes, papers, and two vendored reference codebases we learn
from but do not edit.

**The deliverable is a JAX multirotor simulator** fast enough to train swarm
policies on thousands of parallel environments — written from scratch. What
it is for: **decentralized swarm interception** — N drones catching one agile
evader, each seeing only itself, its neighbours and the target, with no
communication between drones.

Two tasks run today: `circle_swap` (N drones on a circle swap to the opposite side
without touching) and `chase` (pursuers catch one evader with a net; its `default`
preset is the duel, one against one).

The work cycle for a task: write it in `swarm/envs/`, fly it with the cascade to
prove it is possible at all, train a policy with `run/train.py`, score both in the
same seat with `run/eval.py`, then watch it in `run/replay.py`.

The task ladder, the platform backlog, what is done, and every pass/fail gate
live in [research/notes/goals.local.md](research/notes/goals.local.md)
(gitignored, so a fresh clone does not have it). **Read it before planning work.**
Do not copy it here — this file goes stale, that one does not.

Physics and control-stack reference: [ctu-mrs/mrs_multirotor_simulator](https://github.com/ctu-mrs/mrs_multirotor_simulator)
— `multirotor_model.hpp` (state + ODE) and `uav_system.hpp` (the six-controller
cascade). We reimplement it in JAX; we do not wrap the C++.


## swarm/ — our simulator

Every command below needs the `conda run -n drone-swarm` prefix. Pins in
`requirements.txt` (jax 0.11.1, flax 0.12.9, numpy 2.5.2, matplotlib 3.11.2,
pytest 9.1.1).

Run `pytest tests/`, never bare `pytest`, because other folders hold tests too.

```bash
pytest tests/test_control.py                           # one file
pytest tests/test_dynamics.py -k tumble                # one test
python run/train.py --task circle_swap --preset pair --steps 5e6  # PPO -> runs/<name>/
python run/train.py --task circle_swap --preset pair --set gamma=0.99  # any TrainConfig field
python run/train.py --task chase --preset default --set gamma=0.99 --set generations=13 --steps 1.4e9  # pools
python run/train.py --resume runs/<name>               # a pool run, from its unfinished phase, in its recorded env
python run/matrix.py runs/<name>                       # every pursuer against every evader
python run/eval.py runs/<name>                         # -> runs/<name>/evals/latest/
python run/eval.py runs/<name> --seat drone cascade   # the cascade in one role's seat
python run/replay.py                                   # serve + open the 3D viewer
python run/plot.py runs/<name>/evals/latest            # time plots of one episode
bash tools/mrs_golden/build.sh      # regenerate tests/golden/ from the C++
python3 tools/metacentrum/submit.py --walltime 1:00:00 -- --task chase --preset default --set generations=13 --steps 1.4e9  # on MetaCentrum: tools/metacentrum/metacentrum.md. 1 h is enough for a 1.4e9 pool run: always give --walltime 1:00:00
```

Presets: `circle_swap` has `pair` and `circle8`; `chase` has `default`, `open`, `small` and `nemecek`. `train.py`
stops unless it gets both `--task` and `--preset`. A preset picks env
values only — hyperparameters live in `learn/config.py` and are overridden with
`--set`.

- `sim/dynamics.py` — `Params`/`State` as `flax.struct.dataclass`,
  `step(state, throttle, params, dt)` with `throttle ∈ [0,1]⁴`. RK4 over the 18
  rigid-body states, then re-orthonormalize, then the exponential motor lag.
- `sim/control.py` — the cascade, read top to bottom in the order it runs:
  `position -> velocity -> acceleration -> attitude -> rate -> mixer`, plus
  `cascade_step` which chains all six. PID state is carried explicitly in
  `PIDState`; only the heading branch exists, not MRS's heading-rate branch.
- `sim/guidance.py` — the hand-written opponents for chase: FRPN, APF and the flown
  paths. Each one gives a world acceleration, and `learn/seats.py` turns it into a
  CTBR action.
- `envs/` — one file per task (`circle_swap.py`, `chase.py`), each with
  `reset`, `step`, `get_obs`, `reference`, `compute_reward`, `RewardConfig`,
  `EnvParams` and `PRESETS`. Plain functions, no gymnax; auto-reset belongs to the
  trainer. `__init__.py` holds the shared `Obs` layout, `flat`, `take`,
  `make(task, preset)` and **the env contract every task file must meet** — read it
  before writing a task. Every task carries a drone axis, `N = 1` included, and each
  has a note beside it in `research/notes/task_<name>.md`.
- **`envs/core.py` holds everything the tasks share**: `Common` (the `EnvParams`
  fields every task has, which each task's `EnvParams` inherits), `fly` (the rate
  loop and the plant for one policy step), `own_obs`/`target_obs`/`others`,
  `spawn`, `hits`, `is_dead`, and the CTBR action conversion. A task file holds only
  what makes that task different. Do not copy a helper into a task file.
- **No task names a drone by number.** `roles` is static, so a task reads its own
  index arrays from it — see `chase._sides`. That is what lets a longer `roles`
  add more pursuers with no other change.
- **Every task uses the same observation shape**: `Obs(own, others, others_mask,
  target, scene)`. `own` is body-frame velocity, `R`, `omega`, height, and the
  distance to the arena wall ahead, behind, left and right. `others` holds
  the K nearest drones, whatever their role — body-frame offset, body-frame
  velocity, and a 0/1 flag saying whether that drone shares my role, so a teammate
  and an opponent are told apart by a number, not by sitting in different blocks.
  `target` is the body-frame offset to a goal point, and a task with no goal point
  gives it width 0 — `chase` does. `others_mask` is a 0/1 column, and `flat` zeroes
  the masked rows before it concatenates, so an empty seat becomes zeros and never
  changes the vector width. `scene` is the critic's input: the whole game. Add a
  task, not a new obs format.
- The reward is a per-step cost, not a bonus: `-policy_dt * (distance + spin + …)`
  with a one-off crash penalty. `circle_swap` adds a proximity cost and an upright
  term. **`chase` keeps three words apart and never mixes them**: `fail` is leaving
  the box through the ground, a wall or the ceiling (in the `open` preset only the
  ground, and the evader pays `outside` per second instead), `collPP` is a pursuer hitting a
  pursuer (both end the episode), and `collPE` is a pursuer hitting the evader, which
  costs per step and does not end it. `collPP` and `collPE` are Gavin's names, used
  for the `RewardConfig` field, the function and the `info` key alike. The outcomes
  split a `fail` into `crash` (the ground, or a broken state) and `OOB` (a wall or
  the ceiling). **This reward parks the drone 0.2-0.6 m short of the goal** — the open
  problem, with the fixes other papers use, is at the end of
  [research/notes/archive/task_a_to_b.md](research/notes/archive/task_a_to_b.md).
- **`EnvParams.roles` is the field everything hangs off.** It is
  `pytree_node=False`; its length is the drone count, and `role_slices` in
  `learn/ppo.py` turns each distinct name in it into its own set of weights.
- `learn/` — our PPO. `ppo.py` (`Actor`, `Critic` and `make`, one compiled update),
  `vecenv.py` (vmap, auto-reset, normalization), `runner.py` (the update loop, run
  directory, checkpoints, wandb), `config.py` (hyperparameters), `evaluate.py`
  (fixed eval seeds, mean actions, no auto-reset), `seats.py` (who flies a seat: a
  network, the cascade, FRPN, APF or a path; eval and training share it), `pool.py`
  (chase against pools of frozen opponents: generations, phases, Hedge, pool files,
  resume). `ppo.py`, `vecenv.py` and `runner.py` know nothing about drones: they take
  an env *module* and one network per role. `seats.py` and `pool.py` know chase.
- **Every role is its own learner.** One `TrainState` per role, so gradient
  clipping, Adam state, the adaptive lr, advantage scaling and reward scaling never
  mix two sides of a game. `cfg.generations` above 0 trains chase with pools, one side
  at a time — the design is in [research/notes/AMSPBH.md](research/notes/AMSPBH.md).
- **Eval writes into the run it measures**, at `runs/<run>/evals/<name>/`:
  `eval.json` (summary + checkpoint + seeds + commit), `episodes.npz` (per-episode
  arrays), `trajectory.npz` (the first 8 episodes, full state + action), `header.json`
  (task, preset, arena, roles — the viewer never imports the env). Eval holds the
  scene frozen once an episode ends; the env does not, because with `N = 1` the
  episode ends the same step and the trainer resets it.
- `tools/viewer/index.html` — one file, three.js from a CDN, no build step. Parses
  the `.npz` in JS (`np.savez` writes a *stored* zip, so no inflate library).
  `run/replay.py` serves the repo and lists every eval at `/evals.json`, so the
  viewer opens with a dropdown; dragging the files onto the page still works.
- `sim/` is written for **one drone**. Both the drone axis and the parallel-env axis
  are `jax.vmap` at the env boundary. No Python branches on array values, no
  `.item()`, no value-dependent shapes — `test_vmap_matches_python_loop` enforces it.
- Every design decision for the simulator and for what all tasks share, every
  deviation, and every "revisit later" lives in
  [research/notes/choices.md](research/notes/choices.md). A task's own settings live
  in its task note, and pool training in `AMSPBH.md`. **Read it before changing the
  physics, and update it when a decision changes.**
- `conftest.py` turns on `jax_enable_x64` because the C++
is double precision.
- One deliberate deviation from the C++, patched by `tools/mrs_golden/transpose.diff`:
MRS re-orthonormalizes as `R·L⁻¹`, which is not orthonormal and drifts ~3e-3 off
SO(3); we use `R·L⁻ᵀ`. Hover is not a gate — it is an equilibrium, so a
transposed allocation matrix or a missing `ω × Jω` sails through it. Only
`tumble` and `spin_down` exercise the torque path.

## Tests — what each one gates

| file | gate |
|---|---|
| `test_dynamics.py` | the plant against the goldens |
| `test_control.py` | the cascade against the goldens |
| `test_env.py` | the cascade flies a lone drone across the circle; `chase` scales with `roles`, one catch pays every pursuer, a net on another pursuer kills both, and after a failure only the survivor bootstraps |
| `test_learn.py` | it learns, the same seed gives the same numbers, and a frozen role does not move |
| `test_runner.py` | a run says what produced it and resumes |
| `test_pool.py` | the Hedge weights follow eq. 12, and a resume in the middle of a generation keeps its pool |
| `test_eval.py` | the cascade in both chase seats scores its baseline number |

## research/ and the reference code

- `notes/` — working notes, Czech is fine. `goals.local.md` (GITIGNORED) holds
  the task ladder and the gates. `choices.md` holds the shared design decisions.
  `task_<name>.md` is one note per task. `archive/` holds the notes about removed
  code; `archive/task_a_to_b.md` ends with the open reward question, with the reward
  and observation terms every reference paper uses. `comparisons.md` puts our
  observation and reward beside the reference works. `lit_review.md` sorts the
  papers by milestone, and `lit_review_tunnel.md` is the reading list for the tunnel
  task. `learning/` are explainers, `experiments/` holds one run log per training
  setup.
- `code_sources/` (GITIGNORED) — reference code, **not ours**:
  `mrs_multirotor_simulator/` (the C++ we reimplement), `PPO_example/` (the
  supervisor's JAX PPO), `quad-swarm-rl/` (PyTorch swarm, upstream clone).
- **Papers: grep the transcript, don't open the PDF.** Every PDF has a
  `pdftotext -layout` transcript as a sibling `.md`; open the PDF only for
  figures. [bibliography_index.md](research/papers/bibliography_index.md) is the
  entry point — a tracked table of paper → files → one-line summary. Add a row
  whenever a PDF is added, and generate its transcript with
  `pdftotext -layout <file>.pdf <file>.md`.
- Only the PDFs are gitignored. Transcripts and `bibliography_index.md` are
  tracked, so a fresh clone can grep every paper without the binaries.
- The unpublished papers (see Rules) are excluded through `.git/info/exclude`, which is
  itself untracked, so no tracked file names them. Add an index row only for a paper
  that is publicly published.
- `quad-swarm-rl` is a **live clone with its own `.git` and an `origin` pointing at
  the upstream GitHub repo**. Never commit or push from inside it. Treat every
  `code_sources/` tree as a read-only reference unless the user says otherwise.

## PPO_example — JAX learner (the baseline we build on)

Has its own [CLAUDE.md](research/code_sources/PPO_example/CLAUDE.md), which is
authoritative when working inside that directory. Read it plus its `README.md`,
`ppo/train.py`, `envs/interceptor2d.py` — the whole thing is ~1,000 lines.

PureJaxRL-style PPO where the entire training loop is a single XLA program.
`ppo/train.py` (ActorCritic + `make_train`), `ppo/wrappers.py`, `ppo/config.py`
(every hyperparameter), `envs/interceptor2d.py` (env + reward + `PRESETS`),
`run/{train,eval,plot}.py` (CLI → `runs/<preset>_s<seed>/`), `cluster/` (RCI SLURM).

```bash
# PPO_example/CLAUDE.md names a conda env `agiflight`; it does NOT exist here.
# Use `conda run -n drone-swarm`.
python tests/test_smoke.py     # ~15 s, THE GATE: env checks + a learning gate
python run/train.py --steps 3e6 --num-envs 256 --num-steps 64 --num-minibatches 8   # CPU
python run/train.py            # GPU defaults: 4096 envs, 50M steps
python run/eval.py runs/straight_s0
python run/plot.py runs/straight_s0
```

Smoke tests must be green before any change is called done and before any GPU
job. Writing a new env: follow the contract in
[envs/README.md](research/code_sources/PPO_example/envs/README.md) — gymnax-style
`flax.struct` state with identical dtypes from `reset_env`/`step_env`, static
params as `pytree_node=False`, `info` carrying `terminated`/`truncated`/
`terminal_obs`, and all values chosen in `PRESETS`, never in `run/`.

The traps that repo already paid for: `env.step` auto-resets on done (log
terminal data *before* it, or use `step_env`); obs-normalization stats are part
of the policy and live in `params.pkl`; timeout is truncation (bootstrap V),
capture/miss are terminals; small batch + `ent_coef=0.01` makes entropy blow up
(keep ≥2048 envs on GPU). Cluster gotchas are in `cluster/README.md` — deploy
source by git only, verify `git log -1` on the cluster after every pull, and
`pip install --user` without `--no-deps` shadows the container's CUDA jax.

## quad-swarm-rl — PyTorch swarm reference (attention)

Separate stack, separate env: Python ≥3.11, `pip install -e .` (numpy 1.26,
torch 2.5, sample-factory, numba, gym/gymnasium). Two halves:

- `gym_art/quadrotor_multi/` — the simulator: `quadrotor_dynamics.py`,
  `quadrotor_multi.py` (the multi-agent env), `collisions/`, `obstacles/`,
  `aerodynamics/` (downwash), and `scenarios/` — one file per task
  (`static_same_goal`, `swarm_vs_swarm`, `mix`, …), each subclassing
  `scenarios/base.py`. Numba-accelerated hot paths (`--quads_use_numba`).
- `swarm_rl/` — the training glue on top of Sample Factory APPO:
  `models/quad_multi_model.py` + `models/attention_layer.py` (the neighbor
  encoder — this is the "swarming with attention" piece we want),
  `env_wrappers/reward_shaping.py`, `runs/` (Sample Factory launcher scripts
  = experiment configs), `sim2real/` (PyTorch → C for Crazyflie firmware).

```bash
bash train.sh                                    # baseline multi-drone APPO run
python -m sample_factory.launcher.run --run=swarm_rl.runs.single_quad.single_quad \
    --max_parallel=4 --pause_between=1 --experiments_per_gpu=1 --num_gpus=4
python -m swarm_rl.enjoy --algo=APPO --env=quadrotor_multi --quads_render=True \
    --train_dir=... --experiment=... --quads_view_mode topdown
./run_tests.sh                                   # = python -m unittest (all tests)
python -m unittest gym_art.quadrotor_multi.tests.test_multi_env   # single test module
tensorboard --logdir=./                          # from the experiment folder
```

Key training flags to recognise: `--quads_mode` (scenario), `--quads_obs_repr`,
`--quads_neighbor_encoder_type=attention`, `--quads_neighbor_visible_num`,
`--quads_use_obstacles`, `--quads_use_downwash`, `--replay_buffer_sample_prob`.

## Shell traps

- **Bare `python` is not on PATH.** Every command goes through
  `conda run -n drone-swarm`.
- **`conda run` swallows stdout.** If you need to read the output, use
  `conda run --no-capture-output -n drone-swarm python ...`. Without the flag a
  script that prints fine in a terminal returns nothing here.
- **There is no `CONTEXT.md` and no `CONTEXT-MAP.md`.** A skill that asks for one
  will not find it. The ubiquitous language lives in this file and in
  `research/notes/task_<name>.md`.
