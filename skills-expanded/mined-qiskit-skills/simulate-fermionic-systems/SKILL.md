---
name: simulate-fermionic-systems
description: Guide for simulating fermionic systems (molecules, Hubbard/Anderson/impurity models, lattice fermions, any second-quantized Hamiltonian) on quantum computers with the qiskit-fermions package — building fermionic operators and circuits, choosing, comparing and implementing fermion-to-qubit encodings (Jordan-Wigner, ternary-tree, custom), transpiling fermionic circuits with fermionic-level optimizations (term grouping, Trotterization, orbital rotations), and verifying with ffsim. Use this skill whenever the user wants to put electrons or other fermions onto qubits, time-evolve or Trotterize a fermionic Hamiltonian, reduce Trotter depth, transpile an LUCJ/UCJ/UCC ansatz, compare or implement encodings, or compute ground-state energies with a quantum workflow (typically sample-based diagonalization) — even if they never mention qiskit-fermions and only say "mapping a Hamiltonian to qubits", "Jordan-Wigner", "second quantization in Qiskit", or "simulate this molecule on a quantum computer".
---

# Using qiskit-fermions

qiskit-fermions extends Qiskit with fermionic operators, mappers (fermion-to-qubit encodings) and
circuits. Its organizing idea: **keep the problem fermionic for as long as possible** and make the
encoding a late, explicit transpilation stage. Structure that is obvious in fermionic language
(term groups, single-particle rotations, Slater determinants) is invisible once everything is Pauli
strings, so the best optimizations happen *before* the encoding and carry over to every encoding.
**ffsim** simulates fermionic states and consumes this package's operators and circuits directly,
which is how you verify a pipeline before any qubit appears.

This skill holds judgment (what to decide, measure and check), not API recipes: those go stale,
while the guides are doctested. It is a guide, not a procedure; use the sections that match the task.

## Working with the user

Work in stages and end your turn when a decision belongs to the user, when the next step is
expensive (it multiplies work already done, scales with the full target instead of a small case, or
your own timings show it is slow), or when something surprised you. Do the cheap work first so the
stop carries findings, and end it with what you found, what is left, your recommendation and one
specific question. Never submit to hardware, or publish or share anything outside the working
directory, without an explicit go-ahead.

A request such as "don't stop to ask questions" or "report at the end" opts out of stops. Then
finish the work the request implies, including the checks you would otherwise offer, make a
labeled assumption wherever you would have asked, and put open questions after the results as
things the user may want next, not in place of them. A request too ambiguous to act on at all
(no system, goal or size to work with) is the exception: scope it and ask.

## Getting oriented in the installed version

**Use the version the user's environment already has**, and read the docs for that version. If
qiskit-fermions is not installed, install the latest release (`pip install "qiskit-fermions[ffsim]"`,
prebuilt wheels). Do not replace a development build with a release, and do not install one
yourself unless the user asks; it compiles a Rust extension from source. Add other packages when the
route calls for them (the SQD tooling, `qiskit-ibm-runtime`, etc), not up front. Never use or mix in
`qiskit-nature`: it is not actively developed and uses different conventions.

Have every script print the versions of `qiskit`, `qiskit-fermions` and `ffsim` at the top of its
output (a development build reports `0.4.0.dev0+<sha>`; keep the full string). The package restricts
Qiskit to a range that differs between releases, so check its requirements before you install or
upgrade Qiskit. ffsim needs the `[ffsim]` extra, which is not available on native Windows; if the
user hits that limit (fermionic simulation, exact checks), suggest the Windows Subsystem for Linux.
Building operators, mapping and transpiling work natively.

**Read the docs before writing code, and prefer the guides' recipes over improvising.** Each docs
site has an `llms.txt` index, and its pages are served as markdown with their code blocks intact;
use that, not a summarizing fetch tool, which drops the code. Pick the site from the installed
version:

- **The latest release:** the IBM Quantum Platform, starting from
  `https://quantum.cloud.ibm.com/llms.txt`. For this package, `/docs/addons/qiskit-fermions.md`
  (overview and guides) and `/docs/api/qiskit-fermions.md` (Python API; `qiskit-fermions-c.md` for
  the C API). For the other Qiskit addons a workflow might combine with it, `/docs/guides/addons.md`
  describes each addon and links to its docs. The platform keeps only the latest release's guides.
- **An older release or a development build:** `https://qiskit.github.io/qiskit-fermions/llms.txt`
  links to the index for each build it hosts (`dev/` is built from `main`; `stable/X.Y/` is a
  release series), and those indexes link to `.html.md` versions of the pages, guides and API
  reference alike. A dev build can be ahead of or behind the `dev/` docs. The platform also keeps
  the API reference of some superseded releases under a versioned path (for example
  `/docs/api/qiskit-fermions/0.2.md`, and `qiskit-fermions-c/0.2.md` for the C API); try it, and
  fall back to GitHub Pages if it does not exist. If neither has your version's guides (the earliest
  release has no GitHub Pages docs index), use the API reference you can reach and say that the
  guides for your version are unavailable, or recommend that the user upgrade.

If the docs and the installed code disagree, trust the installed code. A feature you read about may
be missing from your version (and the reverse); if the task needs a newer one, say so and offer the
upgrade instead of reimplementing it. Run an adapted recipe on a small case before scaling it up: a
guide's snippet is doctested, your adaptation of it is not.

## What the user is after

The goal determines the approach far more than the physical system does. If "simulate this
molecule" is ambiguous (dynamics or ground-state energy?), ask or state your assumption.

| Goal | Where to start |
|---|---|
| Ground-state or low-lying **eigenvalues** | Small enough for exact solving: use ffsim. Beyond that, default to sample-based diagonalization, preferring Hamiltonian-derived circuits (SKQD, SqDRIFT) over a fixed ansatz; say it is your default, and ask if you are unsure which variant fits. |
| **Time evolution**, Trotter circuits, resource estimates | Operator → `Evolution` gates → fermionic optimization → transpile. See "Circuit cost". |
| Transpile an **ansatz** from ffsim (LUCJ/UCJ/UCC) | Wrap it as a fermionic gate. Unlike ffsim's own Qiskit gates, which are specific to Jordan-Wigner, the wrapped gate can be lowered through any encoding with the synthesis plugins it needs, and gets the fermionic-level optimizations. |
| **Compare, design or implement encodings** | "Choosing an encoding" and "Implementing a custom encoding". |
| Just a **qubit operator** for another tool | Build the operator, call a mapper, simplify. |

## Building models and operators

- **All indices are 0-based**: modes, orbitals and the sites you create from them. Say which
  convention you assumed.
- Operator indices are fermionic modes. The current operator classes give a mode no spin of its
  own, but each class's documentation says what its indices mean, and that can change, so check it.
  A spinful system is a layout convention on top. The default is **block-spin** (alpha = modes
  `0..norb-1`, beta = `norb..2·norb-1`), which the integral constructors, ffsim's
  `nelec=(n_α, n_β)` and qiskit-addon-sqd assume.
- **Interleaved** ordering (orbital `p` ↦ modes `2p`, `2p+1`) is equally valid and changes the cost,
  not the physics: under Jordan-Wigner it keeps on-site interactions local but lengthens same-spin
  hops, and block-spin does the opposite, so measure it. Build the operator in that layout or
  relabel an existing one (check the permutation's direction on an asymmetric example), keep
  references, rotations and readout in the same layout, and convert at the boundary of tools that
  assume block-spin.
- Integral constructors take **lower-triangular packed**, **chemist's-notation** integrals.
- **Constants are explicit.** A core or nuclear-repulsion energy is an identity term you add when
  building from integrals, and solvers that take integrals return energies without it. Add it back,
  together with any spectator energy you treated classically.
- Normal-order and simplify, then set groups *after* the last operation that may reorder terms.
- `Evolution(num_modes, op, time)` is `exp(-i·time·op)`. ffsim simulates it exactly; it is
  Trotterized only on lowering.
- Measure at the **fermionic** level when your version supports it, so classical bit *i* reads
  mode *i* regardless of routing. Otherwise you must undo the final layout yourself.

## Validating at small size

Develop and verify on a miniature of anything too large to simulate exactly. Write the model and
circuit builders as functions of the size parameters, so the same code produces the correctness
check, the scaling study and the production run. Exact fermionic simulation costs
`C(norb, n_α)·C(norb, n_β)` amplitudes, far less than `2**(2·norb)`, so the miniature can be larger
than a qubit statevector would allow. Keep it faithful: the same Hamiltonian family, spin layout,
grouping and basis, and the target's qualitative features (symmetric or asymmetric placement,
sublattice structure).

A miniature establishes **correctness**. It does not settle which choice is cheaper, because that
is a statement about scaling and a ranking that holds at the miniature can invert as the system
grows (see "Circuit cost"). For molecules, scaling down is not one size parameter: a miniature is a
smaller active space, a smaller basis or a different molecule, and the number of two-body terms
grows steeply with the orbital count, so read its cost ranking as indicative only.

Check once for exactly decoupled parts, but expect none in many problems. They can exist only when
the interaction touches few orbitals (an impurity model, say): modes outside the span of
`{h^k e_i}` for the interacting orbitals `i` are free spectators you can diagonalize and fill
classically. Degenerate levels of `h` (symmetric lattices or placements) are where they hide, since
an arbitrary `eigh` basis inside a level obscures them. Report the result either way.

**The checks.** Each isolates a different class of bug; choose those that apply, do the cheap ones
before your first stop, and offer the rest there:

- **Hamiltonian**: the lowest eigenvalue in the `(norb, nelec)` sector against an independent
  reference (PySCF FCI in the original basis, a closed form, the non-interacting limit). Off by
  exactly a constant: a dropped constant. Anything else: integral packing, notation or spin layout.
- **Target state**: `⟨S²⟩`, particle sector and the gap to the next state; do not assume a singlet.
- **Reference state** (Krylov and sampling methods): its overlap with the exact ground state. A
  closed-shell reference can never reach an open-shell ground state, since evolution conserves `S²`.
- **State preparation, on its own**: before any evolution, evaluate the occupation operators on the
  prepared state and compare them with the occupations you intended. This isolates the preparation
  and its readout from the evolution, so a wrong Fock state or readout is not hidden behind a
  Trotter error, and it is the check that exposes an encoding in which bits are not occupations.
- **Fermionic circuit vs the exact propagator**: isolates the *fermionic* Trotter error, independent
  of the encoding.
- **Qubit circuit vs fermionic simulation**, unrouted: differences are qubit-side product-formula
  error; watch them converge. Compare *measured* circuits by outcome distribution, not phase.
- **Bitstring order on a circuit that actually routes**: check that a known, asymmetric determinant
  comes back in the expected order. A circuit without two-qubit gates is never permuted.
- **The whole pipeline, noiselessly**: sample the fermionic circuits with ffsim and run the solver
  on the miniature against the exact energy before building on it. Sampling the *transpiled*
  circuit too is the last step before hardware, where bit-order bugs show; offer it at your stop,
  or run it if the user opted out of stops.

## Choosing the single-particle basis

A unitary change of single-particle basis leaves the spectrum untouched but changes which terms
appear, how local they are, and how *sparse* the states of interest are in the computational basis.
For **sampling-based methods** a ground state spread over thousands of determinants in one basis can
sit on a few dozen in another, and sampling works only in the sparse one. Look for the basis that
diagonalizes the dominant non-interacting part (the bath block of an impurity model, momentum modes
of a translation-invariant lattice, natural or Hartree-Fock orbitals of a molecule), keeping the
interacting orbitals local. Rotate the integrals *and* the reference, **measure the sparsity** at
small size (determinants for 99% of the weight, in both bases) before committing, and hand the
solver the integrals in that same basis. The basis also decides which terms are cheap: one that
delocalizes an on-site interaction turns one cheap term into many. It fixes the structure of the
one-body part as well: a rotated basis typically makes it dense, which is the case where the
orbital-rotation route pays off (see "One-body evolution"), and the rotation into that basis is
itself an orbital rotation.

## Circuit cost

**Every structural choice (basis, one-body route, grouping, encoding, device) is a measurement, not
an assertion, and the cost that matters is how it scales.** First reason about the scaling from the
structure (Pauli weight grows with mode distance under Jordan-Wigner, a star graph needs a number of
edge colors that grows with the number of modes, a local encoding is size independent), then
measure the alternatives at several sizes, including the target if a full-size transpile is
feasible. If it is not, fit the trend from the sizes you can run and say it is an extrapolation.
Report 2q-gate count, 2q depth and the Trotter error where it applies, then explain the trend from
the structure (which terms are long, how the interaction graph meets the device); a table without
that is not a justification. Compare like with like: lower every variant to the same basis gate
set, optimization level and seed, and state the basis next to each number (one Givens gate is two
CZs, so an unlowered all-to-all count beside CZ-basis device counts understates the ideal by about
2x and invents a routing penalty).

For SKQD and SqDRIFT, the sampling parameters scale the cost too, separately from system size: the
Krylov dimension and time step set the circuit depth in SKQD, and the number of circuits in the
ensemble (and the total evolution time) set it in SqDRIFT. Report cost against them as well.

### Term order and grouping

The cost of a Trotterized evolution depends on the Pauli weight of the mapped terms, how they meet
the device connectivity, and the **order** in which they are exponentiated, which is easy to
overlook. Exponentials of commuting terms reorder freely; grouping commuting terms on disjoint modes
lets their rotations run in parallel, which can cut 2q depth a lot at identical gate count and
accuracy. Reordering non-commuting terms changes the Trotter error and may change depth. Qiskit
synthesizes a `PauliEvolutionGate` in the order it receives the terms, and a mapper's raw output
order is arbitrary, so the default pipeline will not find a parallel-friendly order.

qiskit-fermions exposes that freedom at the fermionic level: **term groups** (Hermitian, term +
h.c. together, and internally commuting where possible), **fermionic Trotterization** (a
fermion-to-fermion synthesis method that turns one `Evolution` into a product of smaller
`Evolution` gates, one per group, which later stages can schedule, merge and route), and
**group-wise mapping** (one gate with each group's Pauli terms kept adjacent; under ternary-tree
encodings this is also what keeps particle number exact).

Traps: the fermion-to-fermion stage rewrites only the gates it is configured for, so any other
`Evolution` is mapped whole (check the circuit after that stage); an operator without groups is
split term by term into possibly non-Hermitian factors, which fails late; simplifying after
group-wise mapping re-sorts the terms.

### One-body evolution

`exp(-i t H₁)` for a quadratic `H₁ = Σ h_pq a†_p a_q` is an **orbital rotation** by
`U = expm(-i t h)`: exact. When you have a dense one-body operator that you would otherwise pass to
`Evolution`, build an `OrbitalRotation` from it instead. It is synthesized back into
nearest-neighbor `Evolution` gates, but the fermionic passes still merge consecutive rotations and
fuse a Fock state followed by a rotation into one Slater-determinant preparation, which pays off
across a whole circuit. With a diagonal `H₂` (on-site interactions), `half(H₂) · OrbitalRotation ·
half(H₂)` is a natural second-order step.

Dense or long-range one-body terms (molecular orbitals, rotated bases, a bath coupled to every mode)
favor the rotation by a large factor: the graph of `h` is a star or dense graph that needs many
edge colors, so the Pauli route serializes. Short-range hopping in a good mode order (a 1D chain)
can favor grouped `Evolution`s of commuting bond sets. That graph is a property of the basis you
chose (see "Choosing the single-particle basis"), so decide the two together and compare the routes
in the basis you will actually use, across sizes as described under "Circuit cost".

How a rotation lowers depends on the pipeline. Under Jordan-Wigner in the preset, a hop between
adjacent qubits becomes one native two-qubit rotation, which is exact. Elsewhere (another encoding,
a pipeline you assemble yourself, rotations on modes that are not adjacent in the qubit order, as
in an interleaved layout) the generic qubit-side product formula applies, with a Trotter error that
shrinks as you add repetitions or raise the order. Verify any such pipeline against the fermionic
simulation.

### Choosing an encoding

Jordan-Wigner is *one* encoding the package provides, with a ready-made transpiler preset; the
fermionic circuit assumes none, so choose on purpose. Lower Pauli weight of the Hamiltonian does not
imply a cheaper circuit, and mapped term counts are not a useful proxy. Mode ordering is part of the
choice. Compare relatively, since absolute gate counts move between Qiskit versions.

1. **State the requirements first.** Sampling workflows need measured bitstrings that map directly
   onto the basis the Hamiltonian is projected into, which is why Jordan-Wigner with block-spin is
   the established practice (see that section). A gate without a plugin for an encoding rules it out
   for circuits that use it; the plugins registered in your version decide this. If a requirement
   settles the choice, say whether it is a tooling limit or current practice.
2. **Otherwise pick candidates with a stated reason each**, always including Jordan-Wigner in a good
   mode order as the baseline.
3. **Reason about each one's scaling, then measure on the real target** at several sizes (see
   "Circuit cost"), and report proxies (Pauli weight) separately, never as the deciding number.
4. **Explain the outcome in the physics of the problem.**

What the library has today:

- **Jordan-Wigner**: occupation = bit, the most plugin support, cheap nearest-neighbor hopping in a
  good ordering, expensive long-range terms.
- **Ternary trees** (the mapper framework; Jordan-Wigner, parity, balanced and Bravyi-Kitaev
  encodings are all instances, see the mappers guide): shorter worst-case single-operator weight
  ([Jiang et al.](https://arxiv.org/abs/1910.10746) prove the balanced tree optimal), which is not a
  cheaper Trotter step. Fock states stay basis states but bits are parities of occupations, so
  readout and state preparation need the parity relation: read the supports of each `n_j` off the
  mapper and solve the small linear system over GF(2). Trees fitted to a device, Hamiltonian or
  state are a search problem, for example [Bonsai](https://arxiv.org/abs/2212.09731),
  [Treespilation](https://arxiv.org/abs/2403.03992) and [HATT](https://arxiv.org/abs/2409.02010).
- **Local (ancilla) encodings** such as flow sets, with constant-depth Trotter layers on lattices at
  the cost of extra qubits and a code space (see the 1D and 2D Fermi-Hubbard guides, and
  [Gandon et al.](https://arxiv.org/abs/2512.11418) for flow sets).

Jordan-Wigner is hard to beat for 1D and small 2D lattices in a good ordering (see
[Cade et al.](https://arxiv.org/abs/1912.06007) and the ordering study of
[Hartnett et al.](https://arxiv.org/abs/2605.04025)); real wins come from geometry-aware encodings
or measurement-side savings. Treat claims in papers as proxy-only unless they report compiled 2q
count and depth on a connectivity: for example, the weight advantage of Bravyi-Kitaev is reported to
vanish once routing is included ([Esposito et al.](https://arxiv.org/abs/2608.25024)).

### Implementing a custom encoding

Check the library and the ternary-tree framework first, since many encodings are trees, and say so
if one covers the request.

1. **Write down the contract**: which operator types the mapper accepts, whether Fock states stay
   basis states and how occupations read back, whether extra qubits define a code space (and its
   stabilizers), and what it needs from the layout.
2. **Build the mapper from the images of the generators** with the framework's helpers, not by
   transforming whole operators. If the generator images satisfy the canonical anticommutation
   relations, the mapper is correct for every operator built from them. For a tree, describe the
   tree and let the framework compile it once.
3. **Validate at small size**, with asymmetric examples (symmetric ones hide index and direction
   mistakes):
   - the anticommutation relations of the images (the real correctness condition);
   - the mapped number operators land on the expected qubits and occupations round-trip through the
     readout (the check that catches a wrong mode-to-qubit assignment, which no spectrum can see);
   - a hopping and an interaction term map to what you derive by hand;
   - one qubit per mode: the spectrum equals Jordan-Wigner's. This is necessary only, because it is
     invariant under any unitary and passes a permuted layout;
   - extra qubits: project onto the code space and compare that spectrum with multiplicities.

   These show a valid encoding, not that it is the one the user named; offer to confirm that
   against another package's implementation or a hand-written construction.
4. **Wire it into the pipeline.** With the fermion-to-fermion stage in front, orbital rotations and
   the rotation part of a Slater-determinant preparation become `Evolution` gates and go through
   your mapper. What still needs its own synthesis plugin is state initialization (also the
   Fock-state part of a Slater preparation) and measurement; an unregistered gate raises. Write the
   plugin, restrict the circuit to gates that have one, or prepare the state at the qubit level.
   Make sure the layout matches the qubit meaning your mapper assumes, and map group-wise.
5. **Compare against Jordan-Wigner on the target**, and explain the result whether it wins or not.

### Choosing a device

If the user has not fixed a device, **transpile to more than one connectivity** and recommend from
the numbers: at least one square-lattice and one heavy-hex backend (the fake backends of
`qiskit-ibm-runtime` have both; check which exist), plus all-to-all as the lower bound. Under
block-spin Jordan-Wigner, a Givens network plus on-site interactions forms a ladder, which a square
lattice embeds without SWAPs; heavy-hex pays for routing. Routing overhead depends on how the
interaction graph fits the coupling map, so check a device conclusion at the target size and not
only on a miniature. **Fake backends carry no real error rates**, so they compare structural cost
only; defer fidelity and queue to live calibration data. Take the backend as a script parameter.

## Sample-based diagonalization (SQD, SKQD, SqDRIFT)

For eigenvalues beyond exact reach, the established quantum-centric route is **sample-based quantum
diagonalization** via `qiskit-addon-sqd`: sample bitstrings from a circuit, read each as a Slater
determinant, and diagonalize classically in the sampled subspace. The solver side belongs to the SQD
tooling; this section covers what qiskit-fermions contributes.

**Prefer circuits derived from the Hamiltonian.** SKQD
([Yu et al.](https://arxiv.org/abs/2501.09702); Krylov time-evolution circuits) and SqDRIFT
([Piccinelli et al.](https://arxiv.org/abs/2508.02578); randomized qDRIFT circuits from a grouped
Hamiltonian, after [Campbell](https://arxiv.org/abs/1811.08017)) tie the sampled subspace to the
problem. A fixed ansatz such as LUCJ ([Robledo-Moreno et al.](https://arxiv.org/abs/2405.05068))
does not: recent studies find that shallow LUCJ circuits sample few configurations beyond the
reference determinant, that random configurations plus configuration recovery can match hardware
results ([Vaquero-Sabater et al.](https://arxiv.org/abs/2605.23697)), and that random
initialization of the ansatz is about as good as a coupled-cluster one
([Jones et al.](https://arxiv.org/abs/2606.14933)). The good results come from noisy device samples
plus configuration recovery in the post-processing, not from chemistry in the ansatz. So steer
toward SKQD or SqDRIFT when the user has not chosen a circuit. If they ask for LUCJ, build it and
say what its results rest on; a noiseless simulation will not reproduce the noisy-device behavior.

**What the encoding must provide**: measured bitstrings that map directly onto the basis the
Hamiltonian is projected into, in a form that configuration recovery and the per-spin
particle-number checks can reason about. Jordan-Wigner with block-spin provides this: each bit is
one orbital occupation, so a bit flip corrupts one occupation, and the tooling expects raw
occupations in the alpha/beta layout. Under a ternary tree, bits are parities of occupations and one
flip scrambles several. Jordan-Wigner is the established choice, not a theorem: an encoding that
preserves locality and still reads out occupation-basis bitstrings would meet the same need. If the
user wants one, build it as a custom encoding and compare it against Jordan-Wigner.

**Hand off.** If a skill covering qiskit-addon-sqd is available, invoke it for everything
downstream (variant, solver settings, configuration recovery, hardware execution) and install what
it asks for. Pass it `norb`, `nelec`, the integrals the circuits were built in (full 4-index,
chemist's notation) and the constant, the counts, and what validation found about the target state
(`⟨S²⟩`, near-degeneracies). Without one, follow the SKQD guide's diagonalization step and point the
user to the qiskit-addon-sqd docs (`https://quantum.cloud.ibm.com/docs/addons/qiskit-addon-sqd.md`)
rather than inventing solver settings. The SQD energy is a variational upper bound; compare it
against the exact (small) or a classical (large) reference.

## Reporting

Report so the user can check and act on it: the package versions; the assumptions you made (index
convention, which route you chose and why); what was verified, how, and against what, and what was
not (list anything left as *proposed next*, with what it would show); for each structural choice,
the measured comparison, how it scales, and its explanation (a choice settled by a requirement needs
no comparison, but name the requirement); and classical baselines named honestly ("beyond
brute-force checking", never "quantum advantage"). When an exact reference is cheap, say so: the
problem is then solvable classically, and the report should state what a quantum run would still
add, and for a reduction the size that is left for it. For a hardware script, give the exact command
(the user starts it) and save the raw counts so post-processing can be redone.
