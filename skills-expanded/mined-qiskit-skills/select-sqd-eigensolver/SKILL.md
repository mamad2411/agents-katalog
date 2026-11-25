---
name: select-sqd-eigensolver
description: >-
  Choose and integrate a solver for the diagonalization step of a sample-based quantum
  diagonalization (SQD) workflow — PySCF, Dice, SBD, or Fulqrum (which supplies the
  matrix-vector product, not an eigensolver). Use whenever the user runs /select-sqd-eigensolver
  or is deciding how to diagonalize in SQD, even if they name no solver: which SCI solver or
  sci_solver to pass to diagonalize_fermionic_hamiltonian; an SQD or configuration-recovery run
  that is too slow or out of memory; scaling past ~30 orbitals; RDMs for embedding or
  fragmentation; excited states or multiple roots; spin penalties or spin contamination; GPUs,
  MPI, mpirun or SPMD/collective launch; GDB or general non-product subspaces; swapping one
  solver for another; which eigensolver to pair with Fulqrum (scipy or PRIMME); the paper to
  cite or hosted documentation. Also use before telling the user whether a solver supports a
  capability. Not for circuit construction, sampling or other qiskit-addon-sqd steps that do not
  touch the solver.
---

# select-sqd-eigensolver

<!-- Before restructuring this skill or its registry, read EDITING_THIS_SKILL.md: it records why the design is shaped this way and which changes have already been tried and failed. -->

## What this skill is for

Helping a researcher understand their eigensolver options for the
diagonalization step of an SQD workflow, and what each option would cost them.

The goal is an informed choice, not a verdict. Often there is no solver that
does everything asked, and the useful answer is still a clear account of the
tradeoffs rather than "nothing fits."

At a high level, the conversation goes like this:

1. **What are they computing, and what do they need out of it?** System size,
   and whether they need RDMs, excited states, or spin control.
2. **What pushed them off PySCF?** Usually already answered by the time they
   ask — they hit a wall. Occasionally the answer is "nothing," and PySCF is
   still right.
3. **Which solvers address that, and what does each cost?** The substance.
   Prefer options that scale by changing execution mode over ones that need a
   different solver later.
4. **What hardware do they have?** If they have not said, give a preliminary
   answer across plausible ranges first, then ask.
5. **How does it install, and does that work where they are?** Including
   whether their install route actually delivers the capability they came for.

Steps 3 and 5 are where the registry earns its keep. Step 2 is nearly free and
saves a lot of wasted discussion.

## Assume this unless told otherwise

They are writing Python and using the SQD addon
(`qiskit-addon-sqd`), calling `diagonalize_fermionic_hamiltonian` with an
`sci_solver`. That is how nearly everyone arrives here, and assuming it avoids
asking about an implementation detail they may not have decided.

Revisit the assumption if they mention C++, a CLI workflow, or embedding a
solver in existing simulation code. Those are real cases and this skill covers
them, but they are the minority.

## Talking to the researcher

Readers span quantum chemists who have never run an MPI job and HPC people who
have never done electronic structure. Watch for cues and calibrate rather than
pitching everything at one level.

Roughly:

- **Safe for anyone doing SQD**: orbitals, determinants, subspace, Hamiltonian,
  ground state.
- **Expand on first use**: TPB and GDB, SCI, RDM, configuration recovery.
  One clause is enough — "a GDB subspace, meaning an arbitrary list of
  determinants rather than a product of alpha and beta lists."
- **Assume only with evidence they have been in the addon's code**:
  `sci_solver`, `ci_strings`, FCIDUMP, carryover, `SCIResult`.

Briefly defining a term costs almost nothing. Using an unexplained one can lose
the reader for the rest of the conversation.

### This skill's shorthand is not vocabulary to reuse

The compressed phrasing here exists to help you rank options. It is written for
you, not for the researcher, and handing it over verbatim reads as jargon they
have no context for. Say the substance in their terms instead:

| Internal | What to actually say |
| --- | --- |
| `keyword-only` | "the addon will not forward that option, so bind it with `functools.partial` first" |
| `loop-contract` | "the recovery loop keeps one result per subspace, so extra roots have nowhere to go" |
| `type-mismatch` | "the interface takes alpha and beta lists, so it cannot express a flat determinant list at all" |
| maturity `partial` | "this works on some code paths and not others — here is which" |
| "scales by execution mode" | "you can move this from a laptop to the cluster by changing one argument, not by switching solvers" |

The same goes for "layer 3", "the addon layer", and the registry's field names.
Cite provenance — file, line, version, tracking link — because that is
checkable. Do not cite the registry's *schema*; the researcher does not know
what a cell is.

---

## Phase 1: Understand the problem before the machine

Check `$ARGUMENTS` first and extract whatever is already there. Do not ask for
something they have told you.

**Ask about the science first.** Keep hardware out of this message. The two
interact — a laptop constrains the science, and the science can rule out a
laptop — but asking together invites the researcher to quietly scale down their
problem to fit hardware they assume they are stuck with. Let them state the
problem they actually have.

What matters:

1. **The system** — roughly how many spatial orbitals and electrons, and
   whether the active space is likely to grow.
2. **What they need out of the diagonalization** — the energy alone, or also
   Reduced Density Matrices (RDMs) for embedding or fragmentation, excited states, or control over spin.
3. **What is going wrong now**, if anything. "Too slow" and "runs out of
   memory" point in different directions.

**If they lead with hardware, follow their lead.** Someone who opens with "I
have four A100s, what can I run" has told you something useful. Work from there
and fill in the science as you go.

**Then hardware, as its own question:** laptop, single workstation, a cluster
with MPI, GPUs and which vendor.

**If hardware is unstated, do not block on it.** Give a preliminary answer
across the plausible ranges — what you would suggest on a laptop, on one node,
on a cluster — and then ask. This is more useful than an empty question, and it
often prompts them to volunteer the constraint that actually matters.

## Phase 2: Read the registry

Read `registry.yaml` — the source of truth — and `capabilities.md` for
reasoning that does not fit in a cell.

Do not read `capabilities-table.md` — it is a generated export that can lag the
registry, and everything in it is in the two files above.

Ground claims in the registry rather than general knowledge about these
packages. The obvious answers are often wrong: a capability can be present in a
solver's C++ core and unreachable from Python, or present in Python and
unreachable through the addon's interface.

**Three layers.** Each cell may carry `engine`, `python`, and `addon` values,
and an omitted layer inherits from the one above. Read at the layer the
researcher will actually use — by default `addon`. Quoting an engine-layer
capability to someone working through the addon is the main way this skill
misleads.

**`blocked_by` says whether a gap is fixable**, which matters more than the
gap itself:

| `blocked_by` | Meaning | What to tell them |
| --- | --- | --- |
| `keyword-only` | option exists, the interface does not forward it | one line of `functools.partial` |
| `not-returned` | computed, then discarded | not reachable through the API |
| `not-wrapped` | in the engine, not the bindings | needs the engine directly |
| `type-mismatch` | the interface cannot express it | needs an upstream change |
| `loop-contract` | cannot survive the recovery loop | call the solver directly |

**`maturity` is how far a capability can be trusted**, separate from
`confidence`, which is how well this registry knows the fact. `verified` and
`supported` are safe to state plainly. `partial` means it works on some code
paths and not others — say so, and quote the `known_issues`, because a first
successful run proves little. `plumbing` means no reachable path; treat it as
absent.

**A bare `yes` means the latest release.** Prefer quoting a `since:` version,
which answers "will my install do this?" A cell marked `unreleased: true` is not
installable, so it cannot be the recommendation — but mention it when it is
precisely what they need, under its own heading, with the tracking link.

**Point at hosted documentation, and at the paper where there is one.** Each
solver carries a `docs` list of hosted pages, each with a `what` saying which
question that page answers — so link the page that addresses what they asked
rather than a landing page. Some entries carry a `stale` warning where the
upstream docs disagree with this registry; when you cite such a page, say what
it gets wrong, because the researcher will believe the official docs over you.

Where a solver has a `paper`, it is the citation the project itself asks for,
and `describes` says which design claims it is the source for. Mention it when
the researcher is choosing between approaches, writing something up, or asking
why a package is built the way it is.

**`role` and `not_an_eigensolver` say what the pieces actually are.** Several
of these are not single programs: Dice is a mature SHCI binary plus a
Python/addon bridge that drives it, and Fulqrum supplies the sparse
matrix-vector product while the caller brings the eigensolver. Read those
fields before describing a package, and when a capability is missing, say which
piece is missing it.

**`limits` is a size ceiling, and some are hard.** Check the researcher's
orbital count from Phase 1 against it before recommending anything. Quote the
block rather than a remembered figure, and keep its units — qubits and spatial
orbitals differ by a factor of two. A hard limit rejects the input; a
performance cliff only costs speed, where a fast packed path gives way to a
slower general one. So a workflow can run on CPU and fail outright on GPU at
unchanged size. Several ceilings are compile-time constants, so for a
borderline system say what controls the limit and suggest checking the
installed build.

## Phase 3: Build the tradeoff picture

This is the substance: an account of what each plausible option gives them and
what it takes away.

**Most people have already outgrown PySCF.** It is where the addon starts
everyone, so someone invoking this skill has usually hit its limits already and
recommending it back is mostly a non-answer. Put that in terms of their system
— what their orbital count costs in PySCF — rather than as a general claim
about the solver. Two exceptions worth watching for:

- Their constraints point there anyway — they need something trivially
  installable and their problem still fits.
- They came because of Windows. PySCF is the only solver here that runs there,
  and it needs `pyscf>=2.15.0` with `qiskit-addon-sqd>=0.14.1`. Older pins are
  why Windows SQD fails: before those releases there was no Windows wheel and
  the addon declared pyscf non-Windows, so the install came up without a
  solver. Recommend upgrading rather than switching solvers. SBD and Fulqrum do
  not run on Windows at all, so Windows plus a requirement only they satisfy
  means WSL, a Linux box, or a cluster.

**Dice has the highest barrier to entry.** The heaviest build in the set —
Boost from source, a Rust toolchain, x86_64 Ubuntu only — and RDMs that the
binary computes and the wrapper discards. So it is rarely where someone should
start.

**If someone does use Dice, point them at `main`, not a tag.** Installation is a
git checkout plus `build.sh` whichever commit they pick, so a tag buys none of
what tags usually buy — no tested wheel, no resolver guarantee — while the
latest tag predates the `solve_sci` entry point and `n_roots` that make Dice
usable with the addon at all. Check which they have before explaining
integration.

That is a statement about cost, not about speed. Dice is a mature SHCI code and
there are reports of it performing best on certain problems; this registry has
no benchmark data either way, so do not claim it is slower. If a researcher is
already set up for it, or their problem is one where it is known to do well,
that is a reason to use it — just be clear about what standing it up involves.

**Prefer solvers that scale by execution mode, not by replacement.** A
workflow that grows from a laptop to a cluster without changing solver is worth
a lot — no second integration, no second round of validation.

SBD is the clearest case: one install, with `device=` selecting `'cpu'`,
`'gpu'` (Thrust/CUDA, NVIDIA) or `'gpu-omp'` (OpenMP offload, NVIDIA or AMD)
per call, so it is really several execution routes behind one API rather than
one option among five. Fulqrum likewise has CPU and GPU paths over the same
operator construction, though the GPU path is unreleased today and narrower
than the CPU one.

Say this explicitly when recommending either — no cell in the feature matrix
expresses it, and it is often the strongest argument for a solver.

**Fulqrum is not an eigensolver, so recommending it means recommending two
things.** It builds the subspace Hamiltonian and implements the sparse
matrix-vector product; the caller supplies the eigensolver and iterates. Say
that when introducing it, both because calling it an eigensolver is wrong and
because it explains the rest of its column — multiple roots and general
subspace manipulation are free precisely because the eigensolver is not its
business. Integration is not the cost it once was: from `fulqrum>=0.5.0` the
package ships the addon adapter, so check `is_sci_solver_detail` before telling
anyone they have glue to write. That adapter returns the lowest root only.

Two eigensolvers pair with it, and the choice is worth a sentence:

- **scipy** (`scipy.sparse.linalg.eigsh`) is already a hard dependency, so
  there is nothing to install. Every page of the hosted docs and both tutorials
  use it. The default suggestion.
- **PRIMME** is an optional dependency and generally performs better. It is
  what Fulqrum's own benchmarks use. This registry holds no head-to-head
  timing, so say it generally performs better and do not quote a speedup.

Both consume the same object, so switching is one line — worth saying, since
they can start on scipy and move to PRIMME if the diagonalization becomes the
bottleneck.

**If MPI is in play, say how the program gets launched.** Two incompatible
models, and getting this wrong wastes a cluster allocation: a solver that spawns
its own ranks runs under plain `python my_program.py` (Dice), while the
collective model needs `mpirun -n N python my_program.py` with
`diagonalize_fermionic_hamiltonian` called from every rank (SBD). Read
`execution_models` and the MPI section of `capabilities.md` for how each works.

The collective model is where the ecosystem is heading and what the upstream HPC
guide recommends, so say so when someone is choosing for a cluster and point
them at that guide. But do not oversell it: the default PySCF solver is not
distributed, so launching under MPI without a distributed solver gains
nothing.

**If they need a Jupyter notebook, the collective model is out.** Treat this as
a selection criterion. The kernel is one process started by the notebook server,
not by `mpirun`, so there is nothing to run collectively. Ask about notebooks
when someone mentions MPI and the answer is not already obvious, because it
eliminates an option that otherwise looks like the best one. Developing in a
notebook and running production under a batch script is a reasonable split.

**Some ranking considerations are judgment, not registry fact.** Read the
"Field reports" section of `capabilities.md`, which holds what researchers using
these solvers have said, kept apart from everything read out of source. It is
the only copy — deliberately, so the claims cannot drift — and each report
carries its own date and scope.

Let those steer which option you lead with. Do not restate them as capability
claims, and do not attach them to a solver's feature cells: a claim about what a
solver *does* needs a registry citation or it does not get made.

**Easier to install is better for most people.** Fewer moving parts, works on a
colleague's machine, survives an environment rebuild. Treat compiling as a real
cost and writing C++ as a larger one. Default to assuming they would rather do
neither, and relax that only on evidence — they mention a module system, a
toolchain, a cluster they administer, or having built this kind of thing before.

**Install cost is per-API, not per-solver.** Check the solver's `apis` block
before summarizing it, because quoting one route as "the" install cost misleads
anyone using another. SBD is the clear case: from Python it is an sdist, so pip
compiles the extension modules; from C++ it is header-only — an `INTERFACE`
CMake target, nothing to build or link — so integrating it into existing C++ is
far lighter than the Python figure implies. If you present a
comparison table, say which route each cell describes.

**Where two routes are otherwise comparable, prefer the reproducible one.** A
researcher who can hand a colleague a lockfile and get the same environment back
is better off than one who cannot, and that outlasts a marginal convenience at
install time.

### When the requirements cannot all be met

Two moves, in order.

**First, ask whether a requirement is softer than stated.** Researchers often
set options defensively. A `spin_sq` passed as insurance is not the same as one
passed because spin contamination was observed in results — and if it is
insurance, SBD becomes available and `S²` can be checked after the fact. Probe
once, specifically, without being tiresome about it.

**Then, whether or not it softens, give the closest options with their costs.**
Name what each one gives up and how much that actually hurts: recoverable by
parsing a file, or fatal to the science. "Nothing meets all three" is never the
whole answer, and on its own it is close to useless.

### Watch for failures that look like successes

Several capabilities here fail silently rather than raising. Check the
recommendation against these before presenting it:

- **SBD ignores `spin_sq`.** It is accepted for signature compatibility and
  discarded; the docstring says "unused by SBD." A workflow that passes it and
  swaps PySCF for SBD loses spin penalization with no error and exit code zero.
  Never let this pass unremarked.
- **Dice discards RDMs.** The binary computes them and writes files; the
  wrapper returns only occupancies and leaves `SCIResult.rdm1`/`rdm2` unset,
  then deletes the temp directory by default.
- **The addon forwards no keyword arguments.** `sci_solver` is called with five
  positional arguments, so every solver option — `spin_sq`, `n_roots`,
  `mpirun_options`, `sbd_config`, `device_config` — is silently absent unless
  bound with `functools.partial` first.
- **Excited states do not survive the recovery loop**, which keeps one result
  per subspace and returns a single best `SCIResult`.
- **SBD's `gpu-omp` size check aborts with exit status zero.** Over its
  compile-time cap the run prints a diagnostic and stops, but a batch script or
  `subprocess.check_call` sees success. Tell anyone sizing a `gpu-omp` run to
  check the output rather than the exit code. On NVIDIA, `device='gpu'`
  (Thrust) has no such cap.
- **A GPU install may not have GPU support.** See Phase 4.

Report these even when they do not change the recommendation. The researcher
cannot discover them from a successful run.

## Phase 4: Install route, and what it actually delivers

Treat this as part of the recommendation, not an afterthought — it can decide
the choice.

Two separate questions:

- **Does `pip install` compile?** Being on PyPI does not settle it. Only PySCF
  ships wheels across its supported platforms, Windows included since 2.15.0.
  `sbd-eigensolver` and `fulqrum` are sdist-only, so pip invokes a compiler.
  Read `pypi_install`, not `pypi`.
- **Do they need conda-forge?** Only PySCF and the addon itself are there
  today. `sbd-eigensolver` and `fulqrum` both have recipes under review, as
  does PRIMME, so check before assuming a source build is still required.

**Capability can depend on the channel, not just the code.** This is easy to
get wrong and worth checking whenever GPU support is part of why they are
choosing a solver. The known case: SBD's NVIDIA Thrust backend needs `nvc++`
from the NVIDIA HPC SDK, which conda-forge does not package — it has
`cuda-nvcc` but no `nvhpc`. So an SBD installed from conda-forge cannot have
that backend, while the same version built from source on a machine with NVHPC
can. Tell them what their route delivers, not what the code supports.

For a source build, say what varies by machine where the registry records it —
`sbd-eigensolver`'s available backends depend on the toolchain the build finds,
so the same command gives different GPU support on different hosts.

**If recommending a conda-forge install**, and only then, pixi is worth a
sentence: it gives a per-project environment with a lockfile, so the install is
reproducible rather than a snapshot of whatever solved that day. Do not raise
pixi otherwise — not for someone happily using pip, and not merely because they
mentioned conda.

## Phase 5: Check before you commit to it

If a `verified` cell is load-bearing, confirm it holds in the version the
researcher actually has, which may differ from the registry's baseline. Where a
cell has `since:`, compare it against their installed version — a capability
added in 1.7.1 is absent from their 1.6.0 install, and that is likelier than the
registry being wrong.

If a load-bearing cell is `unverified`, say what you would check rather than
asserting it.

## Phase 6: What to tell them

Shape this to the conversation rather than filling in a form. A researcher who
asked one narrow question deserves a short answer, not six headings.

Cover what is relevant:

- **The options and their tradeoffs.** Usually two or three, each with what it
  gives and what it costs. Cite the registry cell or note behind each claim,
  and state the `maturity` of anything not `supported` or `verified`.
- **What you would do**, if they want a recommendation, with the reasoning
  visible so they can disagree productively.
- **Silent-failure warnings** for anything in the recommendation. One sentence
  each.
- **How to install it and what that route delivers**, including the actual
  command and whether it needs a compiler.
- **Integration**, concretely: the `sci_solver` argument and any
  `functools.partial` needed to bind options.
- **Unreleased work**, when something they need exists but has not shipped —
  separately labeled, with the tracking link, never folded into the main
  recommendation as though it were installable.
- **Where to read more** — the hosted page that answers what they asked, and
  the paper when the project has one. Flag any page whose contents this
  registry contradicts.
- **What rests on unverified cells**, and what to check.

If hardware is still unknown, give the answer across ranges and say which
question would narrow it.
