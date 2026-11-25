---
name: forgeax-engine-performance
description: >-
  Evidence-driven ForgeAX CPU and GPU optimization. Use when diagnosing slow
  frames, GC or physics costs, reducing submission or shader work, replaying a
  captured frame as a GPU benchmark, comparing benchmarks, or adding techniques.
---

# forgeax-engine-performance

Identify the expensive owner, remove redundant work at its actual change
frequency, and verify the requested workload. Follow the checkout's
[delivery and rendering gates](../../AGENTS.md).

This Engine entrypoint owns the reusable action rules below. Detailed methods,
counterexamples and dated measurements stay in the linked Harness references;
raw captures stay outside source. Integrate later experience into the applicable
rule here as well as its evidence reference.

## Numeric allocation ownership

Choose storage by the last reader. Inspect existing arena/pool use at the hot
owner before introducing another allocator; preserve persistent semantic facts.

| Numeric storage lifetime | Prefer | Qualification |
| --- | --- | --- |
| Synchronous temporary work inside `update` / `run` | `world.frameArena.alloc(ctor, count)`; group contiguous standalone runs with `world.withFrameArena` | Initialize reused lanes; consume every view before the outer scope closes, including fixed catch-up ticks and command drains |
| System-owned state reused across frames | `world.buffers.alloc/view/resize/release` over the existing ECS BufferPool | Bind release to the actual plugin owner; reacquire views after resize; independent readers use once-only leases |
| Suspended, transported, published or submitted work | Existing publication/page/device owner; an owned-buffer lease where its reader contract permits | Arena views cannot cross await, yield, timers, transfer, snapshots or GPU completion; a lease pins storage but does not freeze its values |
| A few scalar reads or tiny fixed temporaries | Existing numeric probes, explicit output storage or a small factory | Compare the complete owner before adding scope, handle, view or Result work |
| Pure synchronous numerical work without a World | Caller-owned output storage or bounded private invocation scratch | Reentry owns separate scratch; decide retained-output admission before copying an escaping result; measure cold and densely changing calls |

Arena allocation reuses backing bytes but still constructs a TypedArray view and
Result on every request. BufferPool reuse also retains capacity and metadata.
Measure both backing allocations and JS object allocation; replacing many tiny
arrays with many arena requests does not establish an allocation win. Prefer a
single phase-local numeric window with indexed offsets when the consumer permits
it. Use existing output-writing Math APIs instead of allocating a result first.
For fixed invocation-private scratch without a World, several matrix/vector views
can share one non-overlapping backing allocated by the factory. Create those views
once, initialize every required lane, and keep reentry storage independent.
Compare backing count, view count and cold retained metadata separately: packing
backings does not remove view objects or prove lower warm allocation. Escaping
outputs still require independent storage. Reading each view's buffer proves
ArrayBuffer identities, not native allocator calls; measure actual factory
construction separately without that diagnostic inside the hot measurement.
Several views of one escaping output may share its independently owned backing
when their ranges are disjoint. Preserve each view's logical length, signed zero,
held-output independence and final-reader lifetime; this still creates every view.

Guard arena lifetime at each actual system invocation; a manual scope wrapper
alone does not prevent a suspended system from escaping reset. Scope adapters
return expected domain failures through `Result`, preserving retryability. Include
cumulative multi-view/pass demand in admission controls. For allocate/fill/copy
stages, pass explicit output windows, account for nonzero offsets, and consume
before scope close. Normalize a finished accumulator in place when its old values
have no remaining reader.

Compare complete factory and arena/pool owners under warm reuse, changing sizes,
spike/drain/trim, overlapping readers and failed admission. Record copy/zero work,
CPU, backing allocations, JS views/Results, retained capacity and metadata using
cold `world.memoryStats()` snapshots alongside allocation and retained-heap evidence. Repeated
large allocate/release must not leak slot metadata after backing retirement. Read
the [ECS memory contract](../../packages/ecs/README.md#numeric-memory-services)
for scope, lease, budget and trim behavior.
For short inline ECS arrays already copied into pose/matrix scratch, use the
read capability's output-copy route instead of creating a typed row view first.
Resolve the current row on every read; test growth, migration, stale identities,
output offsets and overlapping conversion. Variable pool fields still need their
live slot lookup. Compare sparse, dense, idle and catch-up complete owners before
claiming whole-Worker savings.
Replacing one vector read with a length lookup and per-element World reads can
repeat entity, schema and column resolution. Measure that complete changing
caller. A private bulk-copy window avoids repeated resolution but copies every
lane even when scalar comparison could exit early; qualify the actual channel
mix and whole-game throughput before retaining either replacement.

When retained snapshots show duplicated compiler facts, first prove a strong
route from the live publication. Share equal detached immutable subtrees at that
existing admission owner, preserving every variant and full validation. Keep
the structural pool temporary and publication-local; measure cold CPU and loading
memory alongside the after-GC floor. Snapshot node counts include VM/native nodes
and are distinct from application object counts or dominator-retained bytes.
For repeated borrows of one physical allocation, validate once and retain its
current typed window with that allocation. Invalidate after successful resize,
not failed admission, and drop the owner cache on retirement. Keep independent
completion capabilities and detached release callbacks; recycling a public lease
would let an old callback release a newer tenant. Compare overlapping readers,
periodic/dense resize and cold allocate/retire, not just warm acquisition.
Keep invalid or zero-length slots from growing a view-cache index needlessly.
Count the additional live headers and JS index storage separately from numeric
metadata and backing bytes. Prove released windows collect while the World stays
alive; a lower warm rate alone cannot justify a retained-storage regression.

A fixed scalar-format codec can own a finite conversion window independent of
World capacity when only numbers escape and the operation is synchronous and
callback-free. Derive conversion from the existing native type metadata; retain
ordinary typed accesses for shared no-tear semantics, foreign buffers and exceptional
indices/alignment/detachment. This is fixed codec metadata, not workload storage.
Qualify full World reads, writes, growth, migration, relationships, cold retirement
and released-backing/World collection; preserve public transient views. Keep a
positive allocation control and a maintained complete-owner gate. A warm scalar
loop alone does not qualify the lifecycle or persistent floor.

## Drive the optimization

For slow dev startup, separate product-DDC warmth from a new browser and runtime.
Use the DevKit workspace-timing request records and actual watcher snapshot spans
to attribute first-frame waiting. Request durations overlap; compare their
critical path and real scan counts before claiming a startup or GPU improvement.
For warm backend preparation, separate full integrity serialization from file
waits and count actual HTTP encodings by content. Batch bounded callback-free
scalar JSON through the existing serializer and keep HTTP encoder concurrency
bounded by both tasks and input bytes. Share accepted immutable artifact bodies
only within their publication; prefer an existing smaller backing and discard
the temporary content index before serving. Preserve canonical digests, MIME,
head/source fences and the compression format/level; do not add a parallel cache.
Confirm the active host's watcher configuration first: the live DevKit host owns
source observation and disables Pack's independent watcher. Collect the existing
Worker load timeline and progress before attributing a long first-frame interval
to module delivery or GPU work. A pending Catalog fetch can be server-side CPU.
If wire-table encoding dominates, preserve shared publication identity through
scope projection so complete output closures are validated and serialized once.
Qualify complete wire bytes, scoped locators, source paths and a real game start;
a faster isolated encoder does not establish a full startup result.

A movement route must clear obstacles by the full character footprint, including
feedback delay and turn overshoot. Keep height/corridor guards; save the last state
and partial trajectory when they reject a capture. Preserve its earlier windows
as rejected evidence rather than assembling a successful subset. Tightening route or cadence
starts a new workload cohort: keep old raw evidence and do not claim numerical
whole-game gains across protocols. Derive report descriptions from the protocol
authority instead of copying an old movement label. Sampled allocation stacks
mapped only to an ancestor do not identify the exact owner; inspect unmapped
library/native callees before editing that mapped caller.
Input remains held while an inspection reply travels. Test both fresh and stale
replies with elapsed transport delay, record that delay, and keep every spatial,
height and travel check on actual samples. Steering prediction is not measured
motion evidence; freeze its selected speed and input policy with the workload.
If asset admission fails before profiling, preserve its named startup stage and
failed scene. Diagnose startup separately without retrying generation inside the
collector or extending its deadline. After a healthy fresh owner and unchanged
payload are verified, restart the complete capture cohort; never combine its
successful predecessor windows with a later count or census. An unreproduced
registration stall remains an unproven cause, not a repaired producer.
Verify inferred V8 names against the actual generated call location: a class name
can identify its iterator method rather than its constructor. Do not add a query
cache when the live Query is already retained. A synchronous complete internal
walk can use the existing borrowed `Query.forEach` cursor when rows never escape;
retain public independent iterators, nested-read isolation and failure closure.

1. Wait for the full build command's successful terminal, then freeze source/build
   and native payload identity, scene, backend, Workers,
   quality and actions. Preserve original failures. A content/profile/ABI change
   needs a fresh baseline. Unexplained rendering follows
   [RHI Debug](../forgeax-engine-rhi-debug/SKILL.md).
2. Attribute the actual expensive population before editing. Separate ordinary
   completion throughput, intrusive profiling and private diagnostic controls.
   Name removable work and a counterexample that could falsify the change.
3. List a bounded batch of attributed opportunities before editing. Implement
   every selected point before the joint build, regressions and game capture;
   avoid a broad test/profile cycle after each point. Apply the ownership and
   hot-path rules below. Measure the complete replacement
   owner, including key construction, validation, allocation, retained storage,
   publication, uploads and retirement where affected.
4. Validate semantic controls, then compare preselected matched windows. Report
   implementation proof, helper results, whole-Worker results and unfinished
   targets separately. Batch verified owner changes before another broad run.

Treat nonempty native payload checks as presence evidence only. If source-key
provenance is absent, preserve the old bytes and hydrate through the pinned
producer before build/freeze. Keep fidelity oracles unchanged and start a fresh
native cohort when payload bytes change.

For sustained-motion GC work, retain the actual moving game as the acceptance
workload. Owner controls must change poses and joints on every call and include
dense updates plus mixed content changes. A moving scene does not by itself prove
that an optimization lowers the changing data's cost; report that path separately
from static-input reuse. Preserve completed throughput and frame-time tails while
reducing allocation and natural GC. Lower B/s at lower throughput is insufficient.
A real hot-path hit and lower Node or profiled allocation do not establish a
natural GC gain. Reject a candidate whose whole-game GC stays unchanged or whose
throughput falls; keep all measurements and restore the prior runtime bytes.

Iterator names in an allocation trace are attribution under that instrumentation,
not proof of ordinary object counts or GC cost. Check the deployed V8 version's
tracking path before interpreting it; full allocation tracking can disable inline
allocation. Observe warmed real workloads separately without heap tracking,
sampling, forced GC or Debugger activation. Native GC boundary counters establish
realm-wide allocation, not which function caused it. Preserve caller semantics
and require a complete-owner counterfactual before replacing traversal syntax.

For natural GC timing, omit `disabled-by-default-v8.gc_stats`: it enables a full
heap object census during major collection. Reject owned-window
`V8.GC_OBJECT_DUMP_STATISTICS` or `V8.GC_Objects_Stats` events, including scopes
crossing a boundary; retain the contaminated trace as diagnostic evidence.
The separate `disabled-by-default-v8.gc` category carries GC boundary counters.
Native tracing still has observation cost; compare preselected interleaved
ordinary windows and never subtract object-census time to invent a natural pause.

When native service lookup is an actual allocation owner, remove unnecessary
resolution/diagnostic work in the pinned dependency policy before retaining a
service copy at every caller. A current native implementation can prove the
happy path; re-read that existing authority every time. Only an unintercepted
native event owner may skip event construction. Keep accessor diagnostics,
interception/veto, custom event owners, method caller tracing, isolation and
retirement/replacement live. Qualify fresh pnpm and Bun consumers from the source
patch and both locks, not by editing installed/cache payloads. Resolve test
tool executables from the owning package and verify their actual version: a root
shim can select another workspace version, and installing that browser does not
prove the consumer can launch its own pinned build. Compare hooked
controls as well as the ordinary route and preserve any slower-path tradeoff.

A GPU-bound frame is attributed from a capture first; see
[Optimize GPU frames from a capture](#optimize-gpu-frames-from-a-capture).

## Optimize GPU frames from a capture

When the frame is GPU-bound (presented-frame rate below target while CPU frame
time is within budget, and the GPU timestamp `union` at or above the frame
budget), use one captured frame as the GPU benchmark before editing shaders or
passes. The tape freezes the exact commands, resources and pass graph, so every
candidate is measured against the same work, without CPU, vsync, frame pacing
or publication-credit noise.

1. **Capture** a representative steady-state frame of the frozen scene with a
   recorder-enabled host (`dev start --rhi-capture true`, then `rhi capture`;
   see [RHI Debug capture](../forgeax-engine-rhi-debug/SKILL.md#game-cli-entry)).
   Skip warm-up frames and record the build identity with the tape; tapes stay
   outside source.
2. **Rank** passes: `forgeax rhi timing T.rhitape` prints whole-frame
   `union` p50 with its 95% interval, drift, the top passes and preflight
   checks (`--json` for every pass). Discard a run whose first line says
   `INVALID` (GPU busy before or after, quantized timestamps).
   `rhi summary --passes --json` names each pass's targets, draws and
   pipelines, so a cost maps to its owner.
3. **Size** each candidate before changing it. `--skip '<regex>'`,
   `--skip-passes` or `--skip-works` adds an interleaved ABBA variant whose
   paired delta and `significant` verdict estimate what removing that pass,
   draw or dispatch could save. `--isolate` reads one pass's own cost without
   neighbours, but isolated sums are an upper bound. Work on the largest
   removable cost first; add `--ci-ms 0.05` for small deltas.
4. **Re-capture** with the changed build at the same scene state and run
   `forgeax rhi timing after.rhitape --compare before.rhitape`: both tapes
   replay interleaved, and the paired union delta comes with a verdict and
   per-pass deltas. Check the image with `rhi read` or same-tick screenshots.
5. **Confirm live.** Only live, frame-level evidence reports a gain: presented
   frames per second (not rAF callbacks; with frames in flight rAF keeps firing
   while frames wait for a credit), live timestamp `union`, and renderer-level
   feature toggles, all in a quiet machine slot with an idle GPU. A bench
   `fps_mean` taken from rAF intervals is not presented frames: the r2 base read
   56 rAF fps while it submitted 39.3 frames/s.

Replay and live measure different things:

| Question | Replay (capture) | Live (running game) |
| --- | --- | --- |
| Which pass dominates, and how much could removing it save? | Rank and paired skip delta | Renderer feature toggle |
| Shader-level feature cost (light count, shader variants, sampling in consumers) | Not replayable: a skipped shadow raster still leaves shadow sampling in the main pass | Toggle the feature |
| Cross-frame overlap, cache state, pacing | Absent: each replay resets and runs alone | Included |
| Absolute ms against the frame budget | No: compare variants inside one run | Yes |

On Apple and other tile-based GPUs pass timestamps overlap: quote `union`, never
the per-pass sum. Any idle gap between replays lets the GPU clock fall, so
replay restores state with GPU copies and submits replays back to back. On
r2-searchlight (Apple M4 Pro, Metal through Dawn), the old re-upload path read
union p50 23 ms with a 4.6–5.1 ms stddev and a slow drift; steady pipelined
replay reads 11.3 ms with a 0.2 ms stddev and no drift, against 17.2 ms
(stddev 2.3 ms) live. Replay is lower than live because it runs at a
sustained clock: compare replay with replay, never replay ms with live ms.
Paired skip deltas then resolve to about ±0.05 ms: shadow raster 2.89 ms,
bloom 0.50 ms, FXAA 0.24 ms (live `shadows=0` saves 3.4 ms; bloom and FXAA
live toggles stay within live noise). Details:
[replay GPU benchmark](../../packages/rhi-debug/README.md#replay-gpu-benchmark).

## Choose the producer before adding reuse

| Observed repeated work | Action | Correctness boundary |
| --- | --- | --- |
| A partial query builds a complete publication and discards most fields | Produce the required value directly through shared validation, as with Fog-only selection | Keep validation/getter order, independent last-known-good values and detached old results |
| Fixed parameters are uploaded every frame | Initialize them with each physical resource; update only dynamic fields | Boot, per-view creation and recovery replacements all initialize; preserve error propagation and capture bootstrap |
| Stable view composition or Feature resource names are reconstructed per consumer | Keep source membership, roles and scoped name routes with their existing view/Feature owner; adopt frame leases and resource values separately | Publish actual relationship changes through ordinary ECS versions; hold prior frame results independently and keep raw borrowed declarations live |
| An incremental residual roster is expanded into dense frame arrays | Consume fixed slot membership directly and apply publication/availability changes to its readable subset | Ranked access, removed/reused slots, missing publication, held frames and full fallback after lost journal history |
| Every shadow pass rebuilds fixed physical ABI dependencies before a GPU-cache hit | Publish the fixed binding route from the physical PipelineState producer; observe only its actual growing/replaced slots and reuse the existing cache leaf | Prove fixed-field ownership at construction; include layout, conditional ABI resources and recovery root; borrowed states and copied owners retain ordinary live reads |
| Several consumers reconstruct the same admitted fact | Publish it once from the existing producer or commit | Prove that owner survives the relevant frames and owns every dependency |
| A stable entity/resource relationship is projected again each frame | Keep compact numeric membership and shared immutable values with the existing phase; apply its changed membership | Slot/generation reuse, removal, held old frames, current accepted versions/scopes and live borrowed/custom inputs |
| Temporary numerical storage | Use bounded scratch or explicit acquire/use/finally-release | Reentry needs independent storage; clear references on release and detach escaped results |
| A few closed immutable definitions | Share finite definitions or producer-owned derived values | Keep borrowed mutable/custom inputs live; shallow freeze and readonly types do not prove deep ownership |
| A proposed result cache | Measure actual owner identities, complete logical inputs and reuse distance during stationary and changing work | Admit a singleton or bounded FIFO only for a small stable working set with a cheap complete key and clear lifetime |

For repeated program serialization, detach immutable metadata at the actual native
receive boundary and preserve its fixed shape through schema rebinding. Prove all
relevant groups through own data properties and deep, dense plain JSON; a numeric
value ownership flag, shallow freeze, accessor or sparse array is insufficient.
Keep shared facts/serialized strings per fixed snapshot and Pass, not per entity.
A memoized miss may keep using the ordinary live route even after later freezing;
only a positive immutable proof permits reuse. An existing available-admission
proof can retain its immutable producer observations instead of a parallel field
roster. Compare every current identity, rejection, deformation and dispatch fact
before reusing a complete contributor. Copy the roster at admission, preserve
held proofs, and recapture borrowed or rejected inputs. Include capture, canonicalization,
rebind, dense metadata replacement and borrowed controls in complete-owner measures.
A warm saving can carry a small cold update penalty; preserve and report both.
An observed component version can change without changing any selected row. When
the existing StateProjection reports neither selected indices nor membership
changes, keep its admitted collection and accept the empty candidate only after
success. Independent consumers such as moving audio sources/listeners still run;
selected pose writes, removal and failed updates retain ordinary retry behavior.
When building a filtered projection, append into one owner output instead of making
one temporary []/[row] per input for flatMap. Preserve header/getter observation
order before traversal as well as row order and absence/rejection behavior.
When a projection immediately unpacks a temporary input envelope, pass the actual
source owner and capture its required primitive observations once. Defer identity
arrays and serialization until membership is known; preserve the prior identity
observation order before borrowed material/getter reads and keep missing-input
diagnostics. Include ignored passes and all changing/borrowed owner controls.

A public iterator is an independent completion capability, not reusable scratch.
Move traversal logic to its prototype and bind callbacks on demand when complete
owner measurements support it. Preserve detached callback calls, stable function
identity, early-close/no-commit, stale-close isolation and held result/span values.
Do not revive a returned cursor or pool escaped facades to improve an empty loop.
Qualify empty, dense, changed, partial and cold owners with a positive sampler
control; an iterator microbenchmark does not establish whole-Worker savings.
Independent commit/validation candidates can share prototype logic and bind only
requested callbacks. Preserve detached calls, callback identity, stale-token
rejection, held component facts and the documented borrowed-index lifetime.
Compare quiet, changing, discarded, held and cold candidates; reduced closure
allocation can carry a CPU cost.
Within a native recording whose shader owners are already captured, reuse its
existing dependency envelope only after matching current physical inputs.
Keep custom/raw reads live and discard the envelope with that invocation.

For internal `FrameList` cursors, the explicit contract permits one private step
object per walk. Keep captured row values independent, close permanently after
return/failure, release input references and publish cached rows only after full
exhaustion. This permission does not extend to public ECS query results/spans.
For a complete synchronous `forEach`, consume already admitted numeric membership
directly when this removes nested cursor wrappers. Preserve custom iterator lookup,
receiver and close semantics, nested walks and callback failure; only a completed
walk may publish traversal state. Include partial, cold and repeated consumers.
Use an invocation stamp on an existing traversal cache entry instead of filling
another Set for hot rows; preserve cold-path cycle detection and measure the
additional retained field as well as the avoided collection work.

Keep unique immutable visibility facts at the extraction producer, then let
Feature frames share that snapshot when no additional reports change its meaning.
Do not rebuild a copy and dedup Set every frame for inactive rows. Borrowed arrays,
getters and custom additions remain live; shallow freeze alone is no ownership
proof. Include producer capture and cold/periodic changes in the complete-owner
comparison, and avoid argument expansion for unbounded entity populations.

Clearing reused small Maps/Sets can cost more CPU than fresh collections while
leaving sampled allocation unchanged. Do not infer backing reuse from wrapper
reuse. Prefer removing a duplicate producer envelope, comparing admitted fields
before materialization, or packing a large synchronous index workspace into one
arena span. Return structured allocation failures through the scope and prove a
warm backing plateau, held output independence and smaller-demand recovery.
Keep preparation/settlement admission closed to callback reentry before reusing
private state; old candidates remain once-only capabilities.
For a numeric traversal stack, clearing a JS Array's length can discard backing
capacity. Track the active range separately when measurements support it, and
trim through the existing structure lifecycle. Test deep/shallow walks, cycles
and drain; reference-valued tails still need clearing. A short-lived read cache
can stamp one retained entry table instead of growing a new Map each generation.
Preserve missed-generation expiry and immutable public values; include extra
stamp records, cold replacement, partial readers and scan CPU in the comparison.

Keep numerical membership with its admitted view when the complete binning inputs
are unchanged; refresh unrelated light payloads independently. Capture numeric
dependencies rather than retaining an old frame bag, validate budgets before hits,
and replace the fact only after successful computation. Preserve old outputs on
change, failure and disposal. Prove the actual pipeline and configuration producer:
a borrowed frozen copy is not the owned default. Compare stable, periodic, dense
and cold work, including output backing separately from sampled JS. A cache can
remove backing churn while adding cold metadata. Inspect disabled profiling too:
per-item callbacks can allocate lexical environments even without an active timer.
Use a direct shared numeric kernel for ordinary execution and preserve the
instrumented path's phase order and exact output.

Carry a fixed value fact from the actual material producer through its existing
resource, then pass that fact to phase-local consumers. A global identity lookup
on every ownership query can slow borrowed inputs; prefer direct owner evidence
at the caller. Keep live readiness, proxy/getter behavior and old accepted
versions independent of the current proof. Include receive/adoption cost, one
material, many materials, continuous changes and borrowed controls; warm short
CPU cases sufficiently and preserve the original caller in the baseline.
Trace the actual receive/schema-rebinding chain: an intermediate copy can lose
a producer proof before its consumer. Preserve fixed value ownership across
metadata-only derivations and exact-snapshot adoption while keeping public aliases
borrowed. Keep the fact with the existing resource authority instead of copying,
freezing or registering every derived snapshot again. Include continuous-rebinding
CPU: extra proof maintenance can cost more despite lower allocation.
A snapshot fact must outlive its latest mutable resource owner. Preserve it in
the existing identity authority, independently of the owner's current version;
qualify multiple holders, rejected candidates, exact-snapshot clones and fresh
copies. Keep borrowed entries cheap instead of adding metadata to every input.

Keep a prepared plan's fixed material/class slot projection with that actual
producer capture. Let its first consumer supply the ordinary index instead of
building another index before consumption; keep current accepted values and World
scopes in each recording. Borrowed arrays and mixed CPU/GPU demand retain their
ordinary live merge. Measure stable, periodically replaced and continuously
replaced plans: a retained index can save steady work while adding cold cost.

Separate cold Scene identity/content columns from pose/version columns so a pose
edit does not copy static relations. Protect matrix windows returned even before
a pending page is captured; a later write or slot reuse cannot overwrite an old
observation. Include real copied bytes, old-root/old-window controls and complete
owner CPU in the comparison. A numeric copy reduction alone does not prove that
the complete renderer scales independently of its retained row population.

Keep retained source identity separate from requested raster work. An empty GPU
eligibility list does not itself imply CPU fallback: hidden and zero-instance
sources need neither lane. Fix the membership producer and use the same demand
predicate for receipts, diagnostic summaries and presentation. Keep real visible
resource failures observable. Qualify hide/show, zero/nonzero transitions, held
old rosters and actual Renderer N/K controls; a counter-only fix cannot remove
unnecessary traversal.
Profile diagnostic consumers as well as rendering. A warning that never fires
can repeatedly scan every inactive row. Keep ordered demand membership with the
captured source root and consume it directly; do not infer demand through custom
projections. Bail out disabled diagnostics before reading rows, after cheaper
light/latch guards. Include lit, dense-change, cold and borrowed controls so
producer maintenance and small-path regressions stay visible. Full exports of N
records still cost O(N); report them separately from ordinary draw work.
Resolve bounded diagnostic identities through the producer's captured immutable
index when it already supplies that fact; do not eagerly scan N rows for a
64-sample quota that may never fill. Preserve held roots and address generations.
A borrowed array can change without changing identity, and a custom projection
can change membership facts. Count and sample their current rows in one coherent
observation instead of adding a second correctness scan. Compare the complete
producer/record/query path, including sparse late candidates, actual pose edits,
explicit queries and custom inputs; keep GPU and whole-game qualification separate.
Forward diagnostic field selection to the owner before producing large
inventories, rather than only selecting before cloning or serialization. Scalar
status/capability reads must not build per-entity material, instance or LOD
exports. Omitted selection keeps the full detached result; qualify empty and
explicit full selections, old observations and cross-Worker cloning. Keep
diagnostic retention/export side effects independent of output selection.

A small matrix window can retain a complete old numeric page. Repeated lane edits
can leave the current row cache holding many old page buffers even after external
readers close. Measure unique reachable backing through actual current outputs,
including cold, rotating edits, held roots and drain. Split independently changing
numeric storage into smaller immutable chunks when that reduces copying and
retention; count extra chunk/view metadata, dense-write CPU and JS allocations too.
Clear removed observations from the current copied page while preserving old
roots. Chunking reduces the retained unit; it does not establish explicit page
leases or authorize recycling storage still visible to automatic readers.

Treat bulk disposal separately from per-row removal. Clearing one authority can
leave derived hierarchy maps, numerical bounds columns, staging arrays and journal
capacity retained by the still reachable owner. Drive the actual bounds/cache
consumers before spike/dispose tests. Return discarded history to cold capacity,
keep cursor positions monotonic so old evidence cannot become current again, and
verify old captured values independently of lazy wrapper identity after disposal.
Count remaining cold owner storage; an empty row root does not prove zero backing.
Inspect strong heap paths when retired Worlds survive a completed lifecycle.
Closures created in one function can share a lexical environment: a returned
callback may retain `previous` even when only a sibling cache predicate reads it.
Create escaping products in a separate scope with their actual admitted data;
keep old held products valid and prove replaced unheld products collect. Exclude
WeakMap ephemeron-value edges from a purported strong retaining path, and repeat
with data-only observation copies before attributing retention to the owner.

Keep full byte/DataView windows with a persistent numeric table's actual physical
backing; use offsets for row writes, clearing and queue uploads. Refresh views only
when that backing changes and verify nonzero source offsets through real payload
assertions. CPU table retirement follows the last synchronous reader, independently
of held GPU versions. Reject update/commit reentry, defer CPU release through an
active queue call, and fault-inject disposal at create/upload/retire boundaries
before adopting growth. Include held versions and repeated grow/dispose cycles.

Read only the allocation columns a hot consumer needs instead of materializing a
complete row view. Keep full detached views for real whole-row observations.
Traverse existing publication groups in their original order instead of copying
their full population into an intermediate array; build membership indexes directly
without mapped temporary key arrays. Qualify sparse pose, content, instance-only
and dense-change paths, including zero addresses and independently held versions.

Measure retained products through their next consumer, including serialization.
Fewer object allocations can still make a native graph-key path much slower when
the produced object representation changes. Keep borrowed getter/toJSON semantics
live and retain cold and changing controls. A plain-object sensitivity probe does
not justify shipping a shared mutable product or a custom serializer; withdraw a
cache whose complete-path CPU cost outweighs the allocation saving.

Share fixed stage facts and synchronous finalizer functions at their installation
owner. Pass the exact preparation and accepted work into the runner instead of
capturing them in new callbacks or retargeting a shared frame context. Reordering
must replace event facts without changing held frames. Keep producer contexts and
native-plan capabilities fresh; test throwing submit/abort/source callbacks,
sibling cleanup, retry and queue-fenced retirement. Compare accepted, aborted and
changing complete-owner paths before claiming a normal-frame CPU gain.

A small record pool can reduce bytes while increasing CPU through lookup and
field clearing. For graph callbacks that only consume the resolved encoder,
frame and resource resolver, use `encodeDirect` to remove the argument record.
Keep the context form for callbacks that need that record, preserve bound
receivers, and measure the complete graph owner with ordinary CPU separate from
allocation sampling. Guard retained frame-resource state before invoking imported
resolvers as well as before pass encoding; recursive resolution can otherwise
overwrite the active frame before the existing execution guard runs. No helper result establishes a whole-Worker improvement.

For derived World facts, record dependencies from the actual read queries and
reuse StateProjection for candidate membership, additions, removals and generation
replacement. Optional absence and required pose joins are inputs too. Keep
resource values, time dependence, asset admission and routed failures explicit.
Separate independent light content from a moving camera at the existing source
owner, retaining per-view shadow/culling work with its actual consumer. Propagate
successful nested component/global/pose inputs on both cache hits and misses;
child time dependence and routed failures invalidate the parent. Restore the
parent after failed extraction, and keep foreign-World or unobserved child reads
conservative. Compare static and densely edited complete publications. Arbitrary extractors
retain conservative behavior until their complete read route is owned. Numeric
publication ranges can feed canonical rows within admission without per-row
matrix copies; return detached deltas rather than borrowed packet windows.

Compare incoming numerical columns with canonical values before hydrating row
observations or staging per-identity work. A previously staged operation owns its
current value: do not compare a later span only with the old columns. Read a
borrowed source window once, leave missing-row windows unread, and preserve source
offsets, parity, strict numeric equality, duplicate edits and removal/recreation.
For large validated transform-only admission, stage numeric source coordinates in
arena chunks and share the owner's existing commit-local slot index instead of
creating full per-row pending records or another N-sized index. Admit all chunks
before canonical writes, clear touched indices on denial, and keep sticky parity
through duplicate/reverting edits. Keep borrowed getters on their ordinary route.
Measure small selected inputs too: scope, view and Result overhead can outweigh
the removed records, so retain tiny ordinary staging when evidence supports it.

Measure complete admission with full unchanged/partly changed input and selected/
fully changing controls. Work on an incoming N-row payload still scales with that
payload; this does not prove N-independent maintenance or whole-game savings.

A hot call count does not imply a large working set; a long-lived object does
not imply stable values. Avoid one cache per entity/material, pose-history FIFOs,
output signatures that cost as much as the avoided work, and new age/version/
dependency scanners added solely to reduce allocation. Keep existing GPU caches,
resource leases, intrinsic invalidation and recovery with their current owners.
Do not attach metadata to foreign or frozen inputs.

## Select the numeric hot path

Use the implemented [ECS contract](../../packages/ecs/README.md#physical-numeric-batches)
and [Math contract](../../packages/math/README.md); retain queries at their actual
World/system lifetime, with reentry and replacement handled by that owner.

| Work | Prefer | Preserve |
| --- | --- | --- |
| Read-only, non-temporal numeric selection, including sparse/optional data | Prepared `query.batches()` and columns resolved once per batch | Real ranges use physical `start, end)`; indexed selections use `rows[0..count)`; test optional absence at the batch boundary |
| Dense required-component numeric writes | Existing spans/shared numeric kernels | Declared writes, version publication, structural fences and shared-kernel eligibility |
| Tiny selection or known entity | Existing numeric `worldRead` probes | Optional membership, numeric representation and bounds; fragmented one-row tables may favor probes over batches |
| Incremental derived output | Existing changed Query/StateProjection | Reconcile complete dependencies, membership, removals and recovery; changed rows alone cannot replace a full aggregate |
| Managed strings or coherent public declarations | Existing semantic snapshot path | String decoding and detached value semantics |

Batches reject write, changed and added descriptors; use their existing write/
temporal paths. Keep entity windows, column lookup and field positioning
outside inner loops.
For repeated span preparation, retain the latest complete physical column window
at the column owner, including its actual backing, range and managed field type.
Keep shape records fresh where callers can replace fields; retain frozen managed
readers with their original bound storage, own enumeration and detached-call
behavior. Partial changed-row windows must not evict the complete-table route.
Replacement/growth must drop the old route instead of retargeting held readers.
Measure the full query traversal and numerical work, not a cached getter alone.

Do not gather sparse rows into copied dense columns or add a row-wrapper class.
Do not expand optional fields into every component combination. Borrow columns
only through the valid batch/span lifetime. Structural callbacks and suspended
iteration retain their original checks and temporal cursor semantics.

Require output storage for output-writing Math APIs. Returning that same output,
or an independent boolean/status, is supported; factories remain explicit
allocation sites. Preserve precision, aliasing and result lifetime; measure
internal temporaries too. `?? 0` does not allocate;
use direct indexed values after proving bounds, and retain meaningful absence
handling. Do not trade clarity for many callbacks to eliminate a small fixed
traversal cost without a complete-owner CPU/allocation win.

Engine implementation uses the fast paths enforced by
`pnpm check:ecs-iteration`, `pnpm check:required-output` and
`pnpm check:foundation-allocations`; apps/templates retain their gameplay APIs.
These finite gates do not prove every caller is optimal or zero-allocation.

## Remove CPU preparation and collection work

| Owner or population | Apply this rule | Counterexample/control |
| --- | --- | --- |
| Exact nearest-geometry queries | Visit nearer conservative bounds first and tighten the existing exact minimum before farther siblings | Exhaustive distances from both ends and on the surface, bounded actual triangle reads, identical complete motion reports and whole-owner cold/query CPU |
| Native-only material test production | Use the existing backend target, file-owned bounded cooker and package-local program codec; retain validated byte views until real wire encoding | Portable producer parity, complete consumed artifacts, fresh Registry/device state, current and held material values, native pixels and complete ordinary-owner timing |

| Serialized keys inside a sort comparator | Serialize each captured full tuple once when ordering is needed, sort by that exact string, then serialize the original ordered tuples | Preserve the singleton direct path, locale comparison, stable ties, escaping, undefined lanes, detached old identities and live changed inputs; measure the complete admission owner |
| Composite/string keys | Reuse existing numeric slots or producer identity before inventing another registry | Slot reuse/generation, realm transfer, collision equality and full key construction cost |
| Packed numeric/spatial keys | Validate integer ranges and exact decoding; preserve the original quantization | Safe-integer overflow, 32-bit coercion, negative/fractional coordinates and traversal order |
| Tiny/sparse lookup fanout | Use existing inline-first or singleton representations only where their limited API fits | Stored undefined, SameValueZero, insertion order, iteration-time changes and actual overflow fanout |
| Duplicate membership collections | Remove the second index only when an existing owner already proves uniqueness | Every insertion, lookup, flush and reacquisition; aliases/barriers keep command order |
| Empty publication classification rosters | Omit temporary membership Sets until their source roster is nonempty | Preserve nonempty Set semantics, overlapping categories, create/update/recreate order, reset and retry behavior |
| Private native Map copies on immutable page paths | Compare native `forEach` copying with iterable construction to avoid per-entry iterator products; initialize one private page object before publication | Borrowed/custom Maps keep their iterator contract. Preserve insertion order, held roots, reference counts and every allocation/write/retirement rollback; qualify sparse and dense complete owners, not a Map microbenchmark |
| Per-instance methods/accessors and temporary result arrays | Share functions/accessor descriptors or consume ordered facts directly when the contract permits | Callback receiver, lazy/own/enumerable getter behavior, ordering, throws, fact count and Object.is distinctions |
| Many lazy rows select the same immutable source digest | Bind the shared detached getter directly to its existing fragment owner; keep canonical lazy selection weakly keyed there instead of retaining an intermediate wrapper | Preserve lazy source identity, own enumerable getters, foreign receivers and publication isolation; hold one row/getter then release it to test unrelated-source collection; count weak-index metadata and cold CPU as well as removed objects |
| A batch closure captures many optional columns | Move selection to shared functions and read only present component inputs; resolve admitted numeric columns once per live batch and defer unused temporary views | Existing views can still incur lease/schema lookup on every read. Preserve validation order, migration, reentry and detached outputs; count batch-cache headers and measure one-row, absent and dense costs |
| Private computed numerical scratch is copied through a generic iterable snapshot route | Copy its indexed lanes directly into the final owned immutable snapshot | Prove the actual private producer; preserve public borrowed/custom iterable semantics, signed zero, held outputs and reentry; escaping snapshots cannot use a frame arena |
| Current-state candidates rebuild component change facts | Share frozen full/empty declarations and retain at most the last equal partial roster per projection | Preserve declaration order, held facts and independent candidate completion capabilities. Keep quiet/full fast paths and compare rotating partial sets, discard, cold construction and the added retained array |
| Lazy collections consumed more than once | Keep numeric membership with its existing owner and traverse through explicit bounded cursors; remove nested generator result allocation | Fixed membership, independent walks, early return, held row values and ordinary public iterator result lifetime; measure the complete traversal |
| Column shapes repeatedly enumerate immutable field Maps | Traverse the existing ordered component vocabulary and its stored sidecar names | Preserve keys/order, managed readers, fixed strides, fresh carriers, growth and partial spans; measure complete narrow/wide queries |
| A compiled owner repeatedly walks fixed Map/Set membership | Compare compilation-owned ordered traversal while keeping resource values and independent capabilities live | Include added retained arrays, rebuild/retirement cost, insertion order and resolver reentry; warm JIT may already elide ordinary iterator records |
| Frame/record construction | Keep mutable internal records at their actual owner lifetime and publish detached immutable results; qualify the final object shape | Held snapshots, asynchronous completion facts, physical replacement, callback reentry and symbol/optional fields; sharing accessors must preserve enumeration and laziness |
| Systems with no deferred structural work | Declare `commands: 'none'` at registration so the scheduler omits the transaction | Default command buffers keep fresh invocation identity; denial, replacement, reentry, predecessor flush and poisoning remain correct |
| Fixed/variable schedule partitioning | Borrow numeric windows of the compiled order; allocate selection membership only after topology replacement, and create command ledgers only for deferred work | Mid-frame registration keeps captured membership in the rebuilt order; predecessor flush, abort and command identity remain intact |
| Per-frame cache-domain rotation | Retain hot weak entries at their Mesh/resource owner and rebuild against actual distinct reads | Cold, sparse, unread and replaced domains retire; include retained capacity and lookup CPU |
| Reusable private ledgers | Reuse pending/accepted cells with bounded numeric generations; detach callbacks from mutable work domains | Commit, rejection, clear and held callbacks preserve exact facts without retaining retired resources |
| Transaction rollback | Journal this transaction's fresh additions when that is the existing invariant | Retain snapshots for arbitrary replacement/removal; abort/retry and completion leases still protect accepted resources |
| Context service lookup inside simulation | Resolve the injected service at plugin activation and retain it for that Fiber lifetime | Unload/reinstall and dependency invalidation; no global service cache |
| A collection whose count changes every frame (spawned/retired members) reallocates GPU Scene rows, direct instance buffers, bind groups or bounds hierarchies | Reserve through the shared `dynamicCapacity`/`shouldShrinkCapacity` policy at each owner; a count change inside the reservation resizes in place, keeps addresses, buffers and bind groups, and clears only the released tail | First publication stays exact; growth past the reservation and large shrinks still reallocate; retained rows keep their temporal history and diff-only uploads; the uniform fallback keeps its fixed array |
| A full re-derive walks the same rows in separate validate, copy and reduce passes | Fuse the passes per leaf node and use branch-free `Math.min`/`Math.max` folds; build identity columns with a loop and memoize their uniqueness proof | Measure on scattered real data: a compare-and-store branch mispredicts there and loses to the shared fold; keep invalid-row and NaN rejection |

A cache hit can still allocate its optional-input or diagnostic collections.
Cold template/value ledgers can be admitted together only when construction is
actually requested; a pose-only candidate need not own every full-row Map.
Prove the active control changes a material/row rather than writing the same
value, and count both fewer held-candidate Maps and the cold workspace/header
cost. Compare full preparation, transfer, acceptance/discard and recycling.
Read the same live flags in their original order, then build names/descriptors
only in the miss or failure branch that consumes them. Keep finite numeric slots
already owned by the cache. Include shared hits, ordinary hits, periodic recovery
and cold descriptor production; a function-level heap attribution alone does not
prove its final resource cache is missing.

A small fixed restriction must not enumerate a much larger member universe.
Retain source-derived membership bounds with the immutable query and traverse the
smaller valid domain; nested restrictions can pass their bound without computing
an eager intersection. Preserve sorted order and member multiplicity, deduplicate
restriction keys where membership is boolean, and cache exact counts only with
that fixed owner. Prove attempted membership checks follow K, test both operand
orders, and separate required output/tree lookups from whole-population maintenance.

Adopt borrowed key cursors only for intrinsic fixed numerical roots. Preserve the
ordinary result lifetime of public Set iterators and keep arbitrary input iterables
on their live path. Each walk owns independent traversal state; break/throw closes
inner cursors. Empty borrowed walks can share immutable termination. Fuse nested
cursor bookkeeping before adding a pool and measure the complete sparse consumer.
Do not infer a win from fewer generator calls. Intrusive iterator records need not
survive ordinary JIT optimization: replacing a Set loop with `forEach` can add
a callback/context and increase complete-owner allocation. Returning an array from a previously
uniform generator route can make the caller polymorphic and increase per-member
iteration allocation. Compare the complete consumer before accepting it; a private
reused-result cursor must still preserve independent walks and early return. Warm
short CPU cases through tiering before comparing steady execution, and retain cold
and partial-range costs separately. An unchanged-path control that shifts by
the same factor prevents attributing a process-wide CPU ratio. Repeat with adjacent
alternating complete-owner CPU blocks after tiering, alongside fresh-process
allocation comparisons.
Keep cold capture state at the membership-cache miss instead of enlarging every
hot frame cursor. Extra fixed fields can erase the avoided iterator objects when
several consumers reread one frame. Compare one/many rosters and repeated reads;
publish captured membership only after full exhaustion and drop it on failure.

Clearing an array's length can discard its backing even when the wrapper is
retained. At a quiet immutable output owner, retain a second ledger's capacity only
when both ledgers reference the exact detached entries already held by the current
root. Clear candidate/retired entries on change, failure, shrink and disposal. Do
not retain borrowed source rows to save capacity. Compare the full output walk and
address consumer with sparse/dense changes, duplicate/reorder controls and repeated
spike/drain; removing quiet writes through an extra per-entry branch can slow the
changing path more than retaining a bounded second ledger.

Index invalidation by the complete consumer dependency domain. A binding's
coverage may follow a peer execution with the same material/group, World, Mesh
and draw; checking only the exact binding misses changes, while rechecking every
batch scales with unrelated work. Maintain the adjacency with existing source
batch diffs and prune retired routes. A fixed source roster does not prove its
consumer selection's routes are immutable: admit that evidence separately at
the actual producer, and keep complete re-judgment for borrowed selections.
For a retained available coverage proof, compare every input to identity and
rejection, including current deformation, fragment selection and owner/device
generations. Retain already consumed private primitive rows rather than another
roster. Keep custom/borrowed contributors and unavailable diagnostics on the
ordinary path. Measure dense publication replacement as well as unchanged and
periodic populations; proof bookkeeping and freezing can make the dense path
more expensive.

Static stock read-only Query declarations can retain one Query per World. Own
their frozen declarations, record the full input vocabulary on every hit, retry
creation failures and let ordinary ECS iteration resolve current membership.
Consult the ECS owner's active-cursor probe before reuse; nested callbacks need
an independent Query until the outer cursor closes, including on a throw.
Do not share temporal cursors or erase optional-absence and joined-component
dependencies. Remove per-call fallback arrays from dependency recording only
after complete extraction controls pass.
Count attempted checks as well as changed outputs: a zero-write result can still hide a complete scan.

A copy-on-write page pool can duplicate backing when automatic immutable row
observations must detach their numeric values before reuse. Account for those
escaped values and explicit root-edge bookkeeping in the complete replacement
owner. Passing last-reader tests is necessary but does not establish a memory or
CPU win. Migrate internal consumers to scoped numeric rows/deltas before enabling
physical page reuse; preserve automatic public observations separately. Reject
an otherwise-correct pool when total backing or CPU grows.

When reconciling persistent membership, submit only actual membership flips. A
row publication that changes pose or contents can leave membership unchanged;
filter those no-op writes before copying bitmap pages or building an edit batch.
Keep real entry/removal, availability recovery and held-frame controls.

Array `push` may reuse capacity; `splice` produces a result array. Reusing a
Map/Set wrapper does not prove clear/refill reuses its backing storage. Inspect
and measure actual operations rather than banning syntax by name.
Once a complete producer traversal admitted a fixed binding sequence, answer a
rank lookup directly from that sequence instead of constructing a generator and
consuming one result. Preserve the cold merge, partial/range semantics, order,
slot recycling and held-frame controls. Qualify the full query/traversal/read
owner under steady and dense Pass adoption.

Publish the final accepted projection directly when an intermediate roster adds
no independent semantics. Keep per-view visibility/culling separate from shared
preparation, and preserve the accepted-work selection across producer callbacks.
For VFX, share immutable code/layout while each Player retains independent
buffers, seed, ticks and feedback. Retained effects must keep their own complete
material/mesh/texture closure through replacement, abort, ACK and retirement.

Ordered compute dispatches may share one physical pass when the producer owns
predicate semantics and no required copy, timing or resource boundary intervenes.
Declare the full resource union and keep each kernel's pipeline/bindings explicit.
Retain separate passes for custom predicates unless explicitly admitted. Verify
indirect readback, Skin overflow ordering, real pixels and GPU timestamps; fewer
pass API calls alone do not establish less shader work or lower frame time. Physical
pass changes also change per-pass query instrumentation. Compare an equal-write,
same-scope control before attributing GPU timing changes; keep every cold/steady
window and unresolved asynchronous readback visible.

Steady-frame CPU in a many-static-light scene is mostly rebuilt-but-unchanged
snapshots. Key a per-entity cache on the component mutation epochs (and refuse
it for interpolated or volatile inputs), return the identical object, and let
downstream equality checks short-circuit on identity. In a 120-lamp scene this
removed the extraction self time and halved deep-compare time (about 0.3 ms per
frame). Memoize a pure per-frame collector (cameras) on mutation epoch, structure
epoch and Time/FixedTime phase. Judge CPU by interleaved profiles: identical
builds varied 5.4-9.3 ms per frame, so read per-function self time, not totals.

## Reduce GPU work through its existing contract

| Work | Move/remove at this boundary | Verify |
| --- | --- | --- |
| Material-constant math such as UV coefficients | Existing cook/upload-derived ABI | f32 rounding, schema offsets and direct/Scene/rigid/skinned shader agreement; fragment-dependent math stays in the shader |
| Overlapping shader neighborhoods | Share actual lane integer coordinates before deriving conservative cache footprints and lossless row summaries | Cover f32 phase boundaries and non-power-of-two extents with a direct-texture GPU oracle; preserve center/row-major ties, invalid vetoes, background/farthest witnesses and uniform barriers. Measure rejected regions and matched live Renderer windows after separate-device replay; see the [TSR iteration |
| Static feature choice and unused resources | Compiler active graph/static switches | Program, macros, parameter layout, bindings and startup sources agree; animated values remain data updates |
| Counter-only telemetry copies full member/indirect capacity | Size the persistent producer's storage, graph imports and copies from its declared demand | Keep default detailed readback, original-frame fences, pending-map skips and replacement cleanup |
| Loading-only program/source ownership | Existing successful preparation/admission transition | Fresh source invalidates correctly; cold first-use cost, failure and recovery remain observable |
| Local smoke or sparse screen contribution | Existing view/composite footprint | Jitter, upsampling, filter/AA support, borders and temporal history; compare pixels and actual raster work |
| Scene batching or exact vertex welding | Authoring/publication owner | Count CPU rows, retained geometry, topology candidates and executed draws separately; weld complete attributes while preserving primitive/material/corner order |
| Shadow preparation/retention | Existing scene, view and physical-resource owners | Caster content at unchanged bounds, light/material changes, per-view frusta, receiver/filter/bias guard bands and new graph/device resources |
| Repeated GPU test startup | Reuse initialized renderer/device preparation across fresh World and asset owners | Actual native request budgets, lease/target cleanup, separate constrained/publication/cold-temporal hosts, fresh replay falsifiers and unchanged frames/pixels; see [CI workload budgets](../../scripts/ci/README.md#native-fixture-workload-budgets) |
| Repeated test readback allocation and per-texel assertion calls | Reuse unmapped staging storage at the harness lifetime; aggregate exact predicate failures | Preserve every readback, frame and pixel predicate, copy owned bytes before unmapping, replace storage on extent/device changes, and reject restored allocations or corrupted finite/coverage samples |
| GPU test replay prefixes | Project existing FrameModel metadata and batch actual selected-work reads | Exact pixel/parameter/depth bytes and provenance, original frame windows, independent falsifier devices and actual native submission budgets |
| GPU snapshot and reference assertions | Compare complete payloads through the shared byte helper; use explicit identity oracles for references | Preserve all bytes, metadata, provenance and negative controls; qualify the real matcher work guard and full native gate through [CI payload work](../../scripts/ci/README.md#native-payload-and-startup-work) |
| Material program wire keys | Encode the complete canonical artifact byte view alongside unchanged JSON metadata | Real enumeration and serializer work gates, differing bytes under identical claims, subviews, metadata collisions and real source/decode/adoption; see [Pack transport](../../packages/pack/README.md#shared-material-program-transport) |
| Material fixture cooking | Declare storage WebGPU or storage WebGPU with rays only for fixtures with that actual backend contract | Full selected-program byte/selection parity, both eligible ray/Card contexts, distinct producer identities, actual output-context guards and unchanged portable/constrained/fallback owners; normalize numeric views once after publication digests and wire encoding |
| Gzip capture transport | Use the package-owned native codec in Node and portable codec in browsers/Workers | Preserve complete payload bytes, stored-payload digests, corruption failures and real replay; qualify conditional packaging and the actual Node codec-call budget before complete timing |

Fewer shader operations or taps are hypotheses until the actual backend shows
both acceptable pixels and lower GPU cost. Measured on Apple M4 Pro at 1080p (r2-searchlight, main pass
about 11 ms): removing ambient IBL sampling from the Standard fs gave no gain at
full resolution (only about -0.6 ms at half resolution), and `discard`-ing the
last (transparent) pass's depth/stencil store gave no change in union or main
p50. Gating a never-taken `discard` behind an override made main 2.7-2.9 ms
slower, while removing every discard from the opaque program at compile time
halved main on the heaviest shot (see the Metal fs row below), so verify every
shader trim on the real backend. Policy: a surface discard that is reachable in the shader must be absent
from the source, not folded. On Apple TBDR a reachable discard disables
hidden-surface removal, and an override-folded `if (false)` is not a reliable
substitute: Tint lowers the default `standardSurfaceDiscards` override to
`if (false)` in the MSL, and one earlier experiment that deleted the LOD coverage
and view clipping calls from fs_opaque left Searchlight's frozen-camera main pass
within noise (7.80/7.93/7.85 ms with versus 7.79/7.82/7.65 ms without, 3
interleaved perf-slot pairs), so that experiment does not prove the folded form
is free. Express each discard as a compile-time `#if AXIS == true` variant axis
(ALPHA_MASK, LOD_DITHER, CLIPPING_PLANES), default the new axes to false at
boot, and never rely on `if (false)`. Keep the axis three-state (none / clip /
lod+clip) so rows are cut rather than added, and still verify every trim on the
real backend. Replacing the white fallback irradiance sample
with a constant 1.0 made main about 0.5 ms slower (3-round medians 7.70 vs
8.17 ms), so it was reverted.

Do not turn native async hashing into synchronous JS hashing on first use. Replacing
the shader manifest's `crypto.subtle` digest check with lazy per-source JS sha256
(`@noble/hashes`) made Searchlight's first acquire 0.9-1.1 s slower (1624/1720/1726 ms
to 2491/2727/2875 ms, about 1046 ms of the profile in the verifier; 11372 fragments,
25.4 MB, 5752 sources). Integrity checks are off the critical path when native and
async, so keep them that way and measure first acquire end to end. Resolution, cascade count, distance,
filters and quality changes start a different comparison profile.

## Specialize shader code at compile time

| Rule | Why | Measured (r2-searchlight, M4 Pro, 1080p) |
| --- | --- | --- |
| Remove a disabled `discard` from source with a preprocessor variant (`#ifdef`); never leave it behind `if (false)`, an override or a uniform. Default opaque programs ship with zero `discard_fragment` in the backend dump | Tint lowers overrides to literal branches that Metal keeps. A reachable discard costs the whole pipeline hidden-surface removal on TBDR GPUs and early-Z on mobile forward paths, so remove it even when one desktop ablation is within noise | Removing the two never-taken surface discards: heaviest shot main 16.6 -> 8.5 ms. View-clip/LOD `if (false)` discards ablated only -0.1 ms on desktop and were removed anyway. Default fs_opaque dumps: 0 discards; whole dump 38 -> 17, all in pipelines that use them |
| Make alpha test a material-selected compile-time variant (`ALPHA_MASK`: alphaCutoff > 0 or alphaHash). Each variant keeps only the discard its material or scene actually uses: cutoff, hash, clipping planes, or LOD dither only when cross-fade is enabled (UE mobile leaves `AllowDitheredLODTransition` off) | An unused discard in a shared fs is paid by every opaque pixel; a cutout material should not silently carry LOD-dither code | Candidate: full-run submit 58.6 -> 60.0, gap p95 -2.0 ms, gputiming union -2.6 to -3.6 ms; t600/t1800 checksums unchanged |
| Put every new axis into the one rule table, [variant-permutation-rules.ts](../../packages/shader/src/variant-permutation-rules.ts) (UE `ShouldCompilePermutation`): one rule per combination the runtime cannot request, with its reason and a unit test. Merge related switches into one axis instead of adding independent ones. Keep the 512 MB sdk-seed heap and 128 MiB publication gates fixed | Each `#pragma variant_axis` multiplies the published matrix and its resident memory | Two independent discard axes (LOD x clipping) quadrupled the rows and the publication build ran out of a 4 GB heap; one merged axis with 3 combinations published at 121.0/121.9 MB. Rule-table prune: 5747 -> 3299 rows, 143.9 -> 121.3 MB. `DIRECTIONAL_SHADOW_SIMPLE`: 3715 rows / 149.85 MB unpruned, 3395 rows / 129.35 MB pruned |
| Select an opt-in specialization (`DIRECTIONAL_SHADOW_SIMPLE`: one cascade, no blend, pcf-vogel, no constant-bias camera) only from config that proves the general path computes the same result. Request sites check `isSupportedVariantKey` and fall back to the general variant; until the specialized pipeline is compiled, draw with the prewarmed general one under a pixel-equality assertion, and count fallback frames | A specialization missing from boot prewarm compiles on first use and blocks the frame | Missing prewarm: a CI browser shard waited 12 frames and captured an empty picture. SIMPLE: 1-light cell union 10.21 -> 9.05 ms (90% of the ablation ceiling), no-light 8.29 -> 7.55 ms, fs_main MSL 261 -> 240 KB |
| Write the packaged shader container as ASCII JSON (escape non-Latin-1 characters, including those in WGSL comments) | One non-Latin-1 character makes V8 hold the whole decoded text as a two-byte string | About 175 such characters doubled the 130M-character container text to about 234 MB; ASCII brought it to 128 MB and the text+container peak from 402 to 280 MB, passing the Node 22 512 MB seed gate |

Order the cheap checks before an exclusive perf slot:

1. **Check how UE does it first** (where the Harness knowledge base is installed,
   permutation filtering, `DITHERED_LOD_TRANSITION`, mobile `EnvBRDFApprox`
   and PSO precaching each answered a design question that override-based
   attempts had failed; the 64002 override recovered 0% of the receiver gain.
2. **Dump the backend source** (Dawn `dump_shaders` for MSL) and grep for the
   removed symbols (`discard_fragment`, `_pickCascadeLayer`, PCSS) before
   queueing any run. Code still present in the dump will not get faster.
3. **Find the direction with frozen-camera short runs** (`freezeAt` freezes the
   camera and simulation; about 6 s per shot) on the heaviest, a typical and a
   spike shot; run the full interleaved A/B only for a kept change. Freezing
   tick 620 against 1850 placed the spike's extra 5.66 ms of main in shadow
   receiving (1.56 ms with `shadows=0`). Put all cells in one perf job and
   rebuild only the changed packages.
4. **Subtract only comparable cells.** A cell that reaches the display cap
   leaves the GPU idle and downclocked: `shadows=0` read union 13.66 ms against
   12.17 ms at base. Use a reference that runs the same program variant: zero
   lights selects a smaller cluster variant, so the r2 light rows use one light.
   `gputiming=1` itself costs frames (57.0 against 60.00 submit/s).

Fresh Skin wrappers and recycled pages do not establish unchanged pose content.
Preserve the current conservative Skin-task demand path. A logical retained
result cannot initialize a replacement physical GPU resource.

## Preserve scheduling, physics and delayed work

| Symptom | Next action | Invariant |
| --- | --- | --- |
| Long completed-picture interval | Join exact World/device/frame tasks, submissions, completions and valid thread clocks | Task wall, thread CPU, notification delay and GPU duration are distinct; preserve unknown gaps and right-censored tails |
| Idle Host and missed native animation callbacks | Compare Window/Worker native frame providers and compositor begin-frame/drop events before changing publication credit | Prefer an existing Worker and Host channel over a dedicated clock Worker; measure each candidate because a busy Render Worker can miss native callbacks. A Worker clock is requested native pacing, never a timer or synthetic completion. Preserve owning-Window time/input, visibility, cancellation and disposal; count its additional Worker/messages/heap. Qualify sustained moving gameplay after removing diagnostic overrides; keep browser versions separate |
| Render backpressure and catch-up bursts | Reduce work holding existing publication credit | Admission precedes input/World mutation; keep each admitted update's ordered effects, fixed delta and dropped-time policy |
| Native CPU/allocation grows during GPU completion | Split actual thread CPU at draw/completion and separately census provider event pumping | Keep operations/pixels and raw regressions; diagnostic scheduler overrides do not become production or browser gains |
| Native physics pressure | Restore the same snapshot; compare actual phases, shapes, compound leaves, active contacts and steps | Native-only replay excludes controllers/publication; compare poses, velocities, sleep and events; contact suppression changes behavior |
| Default callback/event overhead | Keep filtering native when no JS hook is needed; decode only required contacts | Custom callbacks, sensors, collision response and unmanaged/unknown pair handling remain correct |
| Destruction slows after input stops | Keep one World through warmup, real sustained impacts and the stopped-input tail; trace support, fracture, admission and publication queues | Track oldest age and produced/completed work at every queue; a bounded queue or completed counter alone does not prove convergence |

Keep broad terrain/fragment wake bounds and visual-only changes distinct at their
actual producer. Avoid whole-queue copying before a budgeted traversal's first
yield. Disabling collision, damage, effects, shadows or publication is a
sensitivity control, not an equivalent-work optimization.

## Qualify allocation and performance evidence

Keep two explicit comparisons: original unoptimized source versus all retained
changes for cumulative benefit, and the previous accepted source versus the new
batch for incremental admission. Rejecting one batch does not erase prior gains.
Rebuild both cumulative sides with their own lockfile and dependency patches;
freeze common native/assets/workload inputs and verify loaded payloads before and
after capture. Report allocation rate, completed throughput, GC thread CPU, pause
wall time and worst pauses separately. Lower bytes or GC CPU alone do not prove
preserved FPS or shorter pauses; retain all serial comparison windows.

For every allocation round, list Engine and Render separately: total allocation
events and bytes, top source/function rows with count and byte shares, and an
explicit other/unknown remainder. Select a shared row set for both distributions;
include count-heavy rows even when they allocate few bytes. Rows plus remainder
must conserve both totals. Include window duration, completed work and
per-frame normalization using each realm's actual completion counter; World
completion is not Renderer completion. Report ordinary throughput, sampled byte rates,
intrusive event tracing and after-GC census in separate tables; never combine
their populations or call sampling records object counts. For retained storage,
list snapshot object/type counts and self bytes separately from allocation churn.
Observe browser presentation through `forgeax:frame-completed`, rather than only
raw Worker messages: split Render completion can use a dedicated MessagePort.
Require a positive ready-frame control before interpreting a counter or its absence.
Unavailable counts stay unmeasured, with the missing capture identified.
State whether capture changes source files, injects runtime listeners or controls,
enables sampling/tracking, or pauses/forces GC. Profiler-off throughput can still
include real-input drivers, inspection and frame observers. Profiled byte rates
are estimates under that diagnostic workload, not exact uninstrumented rates.
Keep calibration before the measured counter baseline; report remaining profiler
and control overhead rather than subtracting an assumed constant.
A lower intrusive event/frame count or private-owner byte cost does not establish
a lower whole-Worker byte rate. When those populations disagree, replay the full
before-source under the same collector and restore the measured candidate bytes;
retain all windows and report throughput, per-frame bytes and cold metadata cost.
An intermediate package-success line can precede declaration and shader-profile
work; probes overlapping those stages remain rejected. For a before-source replay,
seal the quiescent verified candidate outputs first. Restore the exact source and
output bytes in `finally`, then verify the complete measured manifest and generated
input receipts. Archived successful build bytes can support a same-protocol retry;
they do not turn an incomplete moving capture into a qualified comparison.
Switch only differing source/build bytes, or use separate frozen checkouts.
Rewriting equal build trees can wake filesystem observers; record host activity
and keep build/restoration work outside performance windows. An incomplete
recovery cohort cannot borrow successful windows from its predecessor.

| Evidence | Required accounting |
| --- | --- |
| Allocation churn versus retained storage | Measure rate, promotion, after-GC floor and peak separately; their product is not a GC equation. Include TypedArray backing stores, retained pool capacity and duplicate object graphs |
| A scaling gain with a small current-scene effect | Report both populations and the marginal benefit from the new retained baseline; accept an explicit storage/update tradeoff for the selected objective without claiming CPU, GC or FPS improvement |
| Source attribution | Authenticate actual loaded JS and both map levels; count direct/ancestor/unresolved bytes once. An ancestor is not the exact allocation expression |
| JIT-sensitive allocation probe | Warm the real target, include collected objects and an escaping positive control; name the target URL/function when a marker can inline away; retain orphan bytes as unknown |
| Small effects/noisy runs | Preselect windows and order, retain all repetitions and work counts; a minimum or a local variability cutoff cannot redefine the requested budget |
| CPU and GPU clocks | Thread CPU differs from wall time; GPU interval sums, unions and envelopes differ from each other and from completed presentation |
| Ready/complete/capture state | Validate the actual readiness owner and receipt/fence; a successful draw call or queue wait alone does not establish a ready picture |
| Procedural asset actions in a measured scene | Require the selected producer's successful status and expected artifact identity before freezing the workload; UI presence and zero console errors do not prove generation succeeded or that a preserved old asset is equivalent |
| Frozen source/native inputs | Verify the full payload identity even for a README-only input change; identical JS wrappers do not prove identical WASM/native bytes |
| Backend commands and bundle replay | Count virtual preparation/matching separately from native execution; one bundle call can follow many source command checks |
| CI placement costs | Use complete file/owner timings, including skipped-file process overhead; interrupted work supplies no completion sample. Preserve the full roster, assertions and deadlines; a scheduling estimate requires complete final-head CI acceptance |
| Selected coverage evidence | Apply the actual project wrapper's exclusions and type mode before deriving membership; verify the intended cases in the result JSON before claiming qualification |
| Sampled test attribution | Check actual operation and phase durations before choosing an owner; keep intrusive probes separate from complete ordinary windows and compare full outputs after conservative predicate rejection |
| Private instrumentation or CPU stub | Separate diagnosis from ordinary acceptance; Node/Null/stub results do not establish browser/native GPU timing or FPS |
| Vsync-capped FPS | A capped mean near the display rate hides headroom. Report GPU union headroom (1000 / union p50 ms) together with credit-blocked frames (submit/s versus rAF under the 2-frame credit), plus main-thread busy ms/frame from a CPU profile. Do not use uncapped Chrome (`--disable-gpu-vsync --disable-frame-rate-limit`) as a headroom measure: the compositor and idle rAFs then compete for the GPU and a WebGPU build can get slower (measured 57.8 capped vs 43 uncapped submit/s on the same build) |
| Apple GPU pass attribution | Attribute with per-pass GPU timestamps (union p50 and per-pass ms/frame) plus the diagnostic render ablation (`?forgeax-render-ablation=`: shadow raster, shadow sampling, local-light fraction, post, render scale) at a pinned resolution. Read the serial critical path (pre-main shadows/culls, then main, then post), not the pass sum. An ablation changes pixels and only localizes cost; it is never a shipped setting |
| Fragment-shader variants on a very large fs (Metal) | Judge any WGSL change to a multi-thousand-line fs by live main-pass ms in an exclusive perf slot, never by "removes work". Tint does not fold overrides: it emits a constant `if (false)` branch, so the discard stays reachable to the Metal compiler and the GPU. On Apple TBDR any reachable `discard` costs the whole pipeline its hidden-surface removal, even when no fragment ever takes it. Alpha test must therefore be a compile-time variant (`#if ALPHA_MASK == true`, selected by the material: alphaCutoff > 0 or alphaHash); an override or uniform branch does not count. Measured (r2-searchlight, M4 Pro, 1080p): a1 gated alpha test behind override 64001 and kept the alpha-hash discard, so main got slower (+2.7 ms, submit 57.6 -> 51.7); d12 removed both discards from the opaque program and the heaviest shot went from main 16.6 to 8.5 ms (submit 41.3 -> 58.1, full run 58.8 -> 60.0). Dump the MSL and confirm `discard_fragment` is gone from the opaque variant. The same holds for shadow-receiver code: WGSL override branches do not remove code in Metal (a 64002 override that folded PCSS, the cascade pick and the variance body recovered 0% of the gain), so specialise the receiver with a source-level variant (`DIRECTIONAL_SHADOW_SIMPLE`, opt-in, chosen only from the shadow config: one cascade, no blend, pcf-vogel, no constant-bias camera) and check the MSL has no `_pickCascadeLayer` or PCSS body before queueing any perf run |
| Cross-build replay deltas | Capture both builds at the same deterministic tick with every readback/indirect buffer seeded from the capture. A different unseeded-readback count makes the delta invalid. If replay and live disagree in sign, live decides |
| Shared or loaded host | Record load before and after each run, gate starts on a load ceiling and interleave before/after builds; a run that the host stalled is noise for both builds, not a regression or a gain |
| Node microbenchmarks of a hot loop | Use the real data distribution (scattered transforms, real counts); a uniform synthetic input can reverse a branch-versus-fold decision. Confirm every kept change in the real game profile |

An implausible zero in a known allocating owner is unmeasured, not a saving.
Retain the raw profile and verify samples beyond the warmup ordinal, attribution
coverage and a positive control. If a sampling interval/setup changes during
recovery, rerun both sides as a new matched helper cohort; keep rejected results.

A queue fake retaining synchronous upload input must copy its exact byte window
before scratch reuse. Keep byte assertions and separately verify real GPU
readback. When moving uploads to creation, validate capture bootstrap and fresh
replay as well as live pixels. Removing allocation from one owner does not prove
lower whole-Worker allocation, a smaller retained heap, or a solved runtime target.

## Select detailed methods and evidence

| Need | Reference |
| --- | --- |
| Baseline admission, clocks, cold input identity and batch comparison | Measurement |
| Completed gaps, native task joins and publication backpressure | Slow frames |
| Keys, fanout, rollback, VFX and producer/publication boundaries | CPU preparation |
| Heap attribution, scratch, ECS, outputs and ownership counterexamples | GC |
| Static contracts, uniform-derived math and cold resource ownership | Materials and shaders |
| Coverage, filtering and retained shadow correctness | Shadows |
| Native phases, contact complexity and replay | Physics |
| Support/publication queues and stopped-input tails | Destruction |
| Few stable logical values and finite immutable producer definitions | Working-set case |
| Direct Fog production, resource-owned shadow initialization and measurement limits | Fog/shadow case |
| Allocation ownership and lifecycle controls | game-3d allocation case |
| Cache regressions, cold ownership and Native completion attribution | Regression repair case |
| Capture adapters and analytical tools | Toolbox |

The tools below read local artifacts and use Node built-ins. They do not launch a
browser, acquire a GPU lease, build Engine, or qualify a delivery gate.

| Tool | Input and useful result |
| --- | --- |
| [analyze_cpu_profile.mjs](scripts/analyze_cpu_profile.mjs) | CDP/V8 profile; sampled self/inclusive time, recursion-safe symbol totals and unobserved interval |
| [analyze_cpu_windows.mjs](scripts/analyze_cpu_windows.mjs) | Existing ordinary CPU capture, clock anchors and frame receipts; separate same-capture LIVE/gap windows with coverage, identity and reordered-sample audit |
| [summarize_gpu_timing.mjs](scripts/summarize_gpu_timing.mjs) | Engine GPU observations; semantic pass costs, completeness, interval union and timestamp envelope |
| [analyze_gpu_timeline.mjs](scripts/analyze_gpu_timeline.mjs) | Existing GPU observations and same-report completion receipts; semantic interval overlap, measured envelopes and missing source population |
| [analyze_heap_profile.mjs](scripts/analyze_heap_profile.mjs) | SamplingHeapProfile; conserved direct/ancestor/unresolved byte partitions and source owner distribution |
| [symbolize_heap_profile.mjs](scripts/symbolize_heap_profile.mjs) | Captured script digests and frozen hidden maps; source locations authenticated to the selected profile |
| [compare_heap_profiles.mjs](scripts/compare_heap_profiles.mjs) | Two retained or two churn heap profiles with symbols; before/after bytes per package, file, function and unresolved frame |
| [heap_snapshot_census.mjs](scripts/heap_snapshot_census.mjs) | Existing V8 heap snapshot; conserved node counts and self bytes by type/name, separate from allocation events and dominator retention |
| [allocation_trace.mjs](scripts/allocation_trace.mjs) | Tracked V8 snapshots; same-tracker cumulative self-event/byte deltas and conserved function distributions, including later-collected and VM events |
| [summarize_game3d_allocations.mjs](scripts/summarize_game3d_allocations.mjs) | Complete moving/count/census reports; authenticates raw artifact digests, joins realms by name and emits conserved count/byte tables with independent completion denominators |
| [capture_game3d_counts.mjs](scripts/capture_game3d_counts.mjs) | Intrusive public `project play` adapter; each real Worker validates known live/collected witnesses before a bounded moving allocation-trace window |
| [capture_game3d_allocations.mjs](scripts/capture_game3d_allocations.mjs) | Public `project play` adapter; three ordinary and three collected-object sampling windows with bounded real WASD travel and completed-frame evidence |
| [game3d_motion.mjs](scripts/game3d_motion.mjs) | Fixed-target real-input motion with position feedback, finite XYZ/height/range checks, travel evidence and input release on every exit |
| [game3d_workload.mjs](scripts/game3d_workload.mjs) | Actual runtime vase producer admission and unchanged publication/parameters/geometry receipts; rejects preserved old meshes after terminal generation failure |
| [capture_game3d_retained.mjs](scripts/capture_game3d_retained.mjs) | Intrusive public `project play` adapter; real motion, actual App pause/drain, serial Worker forced-GC snapshots, then healthy completed-frame recovery |
| [allocation_probe.mjs](scripts/allocation_probe.mjs) | Node unit-test helper; sampled bytes per call of a warmed function, to keep a removed allocation removed |
| [summarize_native_gc.mjs](scripts/summarize_native_gc.mjs) | Owned-thread native trace; Minor/Major/finalization durations and bounded allocation/promotion counters |
| [compare_samples.mjs](scripts/compare_samples.mjs) | Raw sample arrays plus selected workload identity; matched descriptive statistics or explicit mismatch |

For moving `game-3d` allocation captures, set `FORGEAX_ALLOCATION_OUTPUT` to a
new absolute directory outside source, then run `forgeax project play
<absolute-path-to-capture_game3d_allocations.mjs> --root templates/game-3d
--backend hardware --headless true --require-ui --viewports 1280x720
--timeout-ms 240000 --json`. The adapter consumes the ordinary owner page;
freeze and verify built/native payloads separately before and after capture.
Pause the actual App and drain submitted frames before intrusive debugger/source
archiving; require unchanged completions, then resume and warm ordinary work.
Keep production frame deadlines intact and preserve any timeout/failure picture.
Changing this collector setup starts a fresh baseline, even with the same motion.
The motion helper follows fixed targets in the stock empty corridor using actual
position and camera-yaw feedback. Validate finite XYZ, grounded height and spatial
bounds after every observation; release held keys on failure. Horizontal travel
alone accepts a character falling beyond the platform and invalidates visible-scene
comparisons. Keep every failed route; a changed motion protocol needs a new matched
baseline, including a full-duration run and visual end check.
Observe non-bubbling canvas completion events in capture phase and require ready
receipts before sampling. Do not substitute held input for motion proof: inspect each window's travel,
health, Worker identities and ready-frame rate. Keep every repetition and failed
capture. Rate bounds cover asynchronous sampler boundaries, not statistical
confidence. Count orphan samples in total bytes with unknown owners; sampling
records cannot establish temporary object counts. Run retained census and
allocation-event tracking separately from ordinary throughput.

For a retained census, substitute `capture_game3d_retained.mjs` in the same play
command and set `FORGEAX_RETAINED_OUTPUT`. The diagnostic resolves the real App
binding through DevTools closure scopes; unavailable scope inspection is a failed
capture, never permission to fabricate a pause. Require zero in-flight work,
unchanged completed frames throughout both snapshots, and healthy resumed
completion. Forced GC and snapshot wall time are intrusive controls. They do not
measure natural GC pauses, ordinary peaks or moving allocation rates. Archive
screenshots immediately and authenticate their producer digests because public
play reuses its per-script output path.

For event counts, substitute `capture_game3d_counts.mjs` and set
`FORGEAX_TRACE_OUTPUT`. Validate each actual runtime with known live objects,
forced collection and unchanged cumulative source counters. VM metadata may add
events at the same function; do not demand logical-object equality or infer
cumulative types from surviving trace IDs. Sum trace-node self counters once;
function starts and ancestor attribution are not exact allocation expressions.
Tracking changes execution and excludes external/GPU backing, so its event/byte
totals cannot establish ordinary allocation rates or the moving budget.

Run an entrypoint with `--help`; Toolbox owns arguments,
exit meanings and capture adapters. Use private output paths and retain raw
inputs. These summaries establish their stated analytical boundary only.

Keep reusable decisions in this Engine entrypoint; add detailed method and
counterexample evidence to the existing topic, and dated results to one scoped
case using Contributing. Remove superseded guidance. Preserve raw failures privately and retain useful
counterexamples; do not promote one run's numbers, host paths, quality settings
or an unimplemented prototype into a universal rule.

When animation times are externally sampled, zero playback speed does not permit
skipping pose evaluation. Retain events, normalization and target updates while
avoiding unchanged clock writes; verify paused, wrapping and externally edited
targets through the same animation owner.

For fixed-input material builds, capture WGSL records and their complete path
namespace through the existing Pack source fence, then pass an explicit
`captureMaterialSourceSnapshot` result to the material cooker. Never apply this
lifetime to live/default callers. Transport DDC admission requires the product
cache's producer checks and an explicit pure, sink-free policy identity; cached
dependency topology may order work but cannot admit or skip publication.
