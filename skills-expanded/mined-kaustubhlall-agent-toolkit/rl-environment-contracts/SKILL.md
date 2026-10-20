---
name: rl-environment-contracts
description: Diagnose or change RL environment-to-learner contracts involving reset, wrappers, observations, actions, rewards, termination, bootstrap, collectors, replay, or multi-agent lifecycle; not general game or ML work.
---

# RL environment contracts

Use this skill when a user asks to debug, review, or change a reinforcement-learning environment or its learner adapter and the suspected failure concerns what crosses an environment, wrapper, vectorizer, collector, replay, or multi-agent boundary. Apply it to semantic errors such as incorrect terminal targets, episode leakage, misaligned transitions, malformed observation/action/reward data, or agent lifecycle mismatches. It does not apply to unrelated game logic, general ML advice, model architecture work, hyperparameter tuning, or performance optimization unless evidence localizes the issue to one of these contracts.

Keep the requested scope and the project’s existing acceptance criteria. First locate the actual transition path and relevant tests/manifests; distinguish a concrete contract defect from a policy that simply has not learned. Trace the affected fields end to end:

`reset → base env step → wrappers → vector/autoreset → collector → stored transition/replay → target or policy update`

Include every layer present; do not assume a Gymnasium, TorchRL, PettingZoo, or other API unless the code uses it. Check both the whole path and the narrow boundary where values change. In particular:

- Match declared and returned observation/action/reward/done structures, including shape, dtype, range, keys, and agent set where applicable.
- Establish episode semantics from the task definition before interpreting flags. A true MDP terminal has no bootstrap. An external cutoff of a continuing task may bootstrap from that episode’s final observation. A finite-horizon endpoint that belongs to the MDP is terminal; represent remaining time in the observation when needed for the Markov state. Never equate “truncated” with one universal bootstrap rule without checking task semantics.
- Distinguish the final observation of the ending episode from the reset observation of the next episode. Check the installed vector environment’s autoreset mode/version, wrappers, collector, and replay encoding; behavior differs across APIs and versions.
- Preserve declared reward aggregation and time-step semantics without dropping, duplicating or misaligning reward components. Observation, action, reward, terminal flags, final observation, episode identity and agent identity must remain paired through collection and replay. Do not sum per-agent rewards unless the contract specifies aggregation.
- For multi-agent environments, check live-agent membership, per-agent versus global rewards/terminations, simultaneous versus sequential action timing, reset and removal against the declared API. An atomic joint action produces its transition after the joint action completes; a sequential interface preserves its explicit substeps. Distinguish a newly terminated agent's legitimate final-step record from the next step's live-agent set and accepted actions.

Use a few hand-authored transitions with an independently calculated expected result before any long-running experiment. Prefer deterministic, tiny, offline fixtures and seed-matched comparisons. See [references/probes.md](references/probes.md) for optional probe designs. A fixture should fail clearly when the suspected field is corrupted; do not infer correctness from an episode return or a passing API checker alone.

Existing framework checkers may help when already available and compatible, but they are optional and do not replace checking wrappers, collectors, replay, learner targets, or project-specific invariants. They may reset, step, render, seed, or close an environment. Use only a disposable local instance; record those effects and read the installed-version documentation first. TorchRL’s `check_env_specs` is explicitly an offline check that can alter environment seeding, so never put it into a training script. Do not add a framework, schema, runner, helper, or adapter just to use this skill.

Start with synthetic fixtures or existing local checks. Do not initiate training, live game/client control, service queries, or frozen/holdout evaluation merely to use this skill. Existing authorization for the actual task still applies; choose the smallest useful check within it. Preserve project acceptance thresholds and evaluation boundaries. If an additional action requires new authorization or would consume a protected evaluation set, explain the concrete gap and obtain the needed decision before that action.

The source notes in [references/source.md](references/source.md) distinguish explicit upstream API behavior from this skill’s recommended workflow. Read [references/probes.md](references/probes.md) only when a concrete contract test needs to be designed.
