---
name: security-smart-contracts
description: >-
  Audit Solidity and EVM smart contracts, web3 protocols, and on-chain code.
  Use for smart contract review, Solidity or DeFi audit, proxy and
  upgradeability checks, invariant and property fuzzing design, oracle and
  price manipulation review, ERC-4337 or EIP-7702 account abstraction, Permit2
  and signature replay, L2 and cross-chain risk, and for running Slither,
  Aderyn, Echidna, Medusa, Halmos, or Foundry invariants. Skip it for
  off-chain application, cloud, container, or dependency security, for gas
  golfing, and for tokenomics or economic-design review with no security
  question attached.
---

# Smart contract security review

On-chain code is immutable by default, publicly readable, and adversarially
executed by anyone who can pay gas. Treat every deployed function as a hostile
entry point and every external call as a re-entry into your own state.

This skill is a four-phase procedure: reconnaissance, a two-pass sweep, deep
validation of each candidate, then a report. The phases are ordered because
each one narrows the next. Do not skip to reporting from tool output.

## The shared contract, restated

The `security-audit` skill in this plugin owns the long form of the severity
model, the evidence rules, and the report contract. The short version, which
binds this skill:

- **Every tool finding is a lead, not a finding.** Promote a lead only when a
  written attack path exists, with a `file:line` and named functions. Anything
  else is either discarded or tagged `theoretical`.
- **Evidence or silence.** Never claim a component, control, role, or data flow
  exists without a code reference. "Probably has a check somewhere" is not a
  finding and not a clearance.
- **Preflight, never assume.** Detect each tool before using it. If it is
  absent, print its install command and continue with agent-native reasoning
  rather than aborting the review.
- **Artifacts leave the working tree.** Scan output contains source excerpts
  and exploit steps. Write it to a directory outside the repository and never
  attach it to a pull request by default.
- **Exit codes are inconsistent across tools.** Handle them per tool and make
  every pipeline step non-fatal, so one analyzer's failure does not truncate
  the review.
- **Per-finding record:** identifier, title, severity, vulnerability class,
  `file:line`, affected contracts and functions, numbered attack path,
  preconditions, proof of concept or an explicit `theoretical` tag, impact,
  recommendation, and confidence.
- **Deduplicate by `(file, line, class)`** across every source, tool and human
  alike, and keep one merged record with the union of its corroboration.

## Phase 1: reconnaissance

Build a map before looking for bugs. A finding you cannot place in the value
flow is a finding you cannot rank.

1. Enumerate every `.sol` source under the project's source root and record the
   **pragma of each file**. Many defects are version-dependent — the arithmetic
   story, `PUSH0` availability, `transfer` gas semantics, and custom-error
   support all move with the compiler — so a per-file pragma table is not
   bookkeeping, it is an input to Phase 3.
2. Identify external dependencies: which library versions are vendored or
   installed, which are upgradeable, which are forks with local edits. A fork
   with edits is the highest-risk dependency shape there is; diff it.
3. Map privileged roles. For every role, record who holds it, what it can call,
   whether it can grant itself more, and whether it is behind a timelock.
4. Map value flows. For every asset, record how it enters, where it is
   accounted, who can move it, and how it leaves. Every deposit path must have
   a withdrawal path.
5. Record the trust assumptions the protocol states about oracles, sequencers,
   bridges, relayers, keepers, and governance. Phase 3 either confirms each one
   is enforced in code or turns it into a finding.
6. Run the Slither printers listed in `references/tooling.md` to accelerate
   steps 3 and 4. Treat printer output as a draft of your map, not the map.

## Phase 2: sweep

Two complementary passes. Run both. Neither alone is sufficient, and the
overlap between them is small.

### Pass A: syntactic

Grep for known trigger patterns and record every hit with its `file:line`.
This pass is deliberately dumb and deliberately over-inclusive; filtering is
Phase 3's job. Trigger set:

| Pattern | Suspected class |
| --- | --- |
| `delegatecall`, `callcode`, `assembly` | delegatecall, storage, arithmetic |
| `.call{value:`, `.send(`, `.transfer(` | reentrancy, unchecked calls, DoS |
| `tx.origin` | access control |
| `unchecked {`, downcasts such as `uint128(` | arithmetic |
| `block.timestamp`, `block.number`, `blockhash`, `prevrandao` | MEV, randomness, L2 |
| `ecrecover`, `EIP712`, `DOMAIN_SEPARATOR`, `permit(` | signatures |
| `initialize(`, `initializer`, `_disableInitializers` | upgradeability |
| `_authorizeUpgrade`, `upgradeTo`, `ERC1967` | upgradeability |
| `slot0(`, `getReserves(`, `latestRoundData(`, `getPrice` | oracles |
| `selfdestruct`, `create2`, `CREATE2` | access control, metamorphic code |
| `for (` over a storage or calldata array | DoS, gas griefing |
| `IERC20(...).transfer`, `.approve(`, absent `SafeERC20` | ERC-20 weirdness |
| `_safeMint`, `onERC721Received`, `onERC1155` | reentrancy via callbacks |
| `msg.value` inside a loop or `multicall` | `msg.value` replay |
| `payable(` fallback or `receive()` with logic | access control, DoS |

Also run the static analyzers here — Slither and Aderyn, per
`references/tooling.md`. Their output joins the same candidate list under the
same rule: lead, not finding.

### Pass B: semantic

Read for what does not grep. Budget the majority of Phase 2 here.

- **Cross-function and cross-contract reentrancy.** A guard on one function
  does not protect a second function that shares the same state. Follow every
  external call and ask which other entry point is reachable during it.
- **Missing access control on state-changing functions.** Enumerate every
  external and public function that writes storage, moves value, or changes a
  role, and name the modifier or explicit check that protects each. A blank
  cell is a candidate.
- **Inheritance and initialization order.** C3 linearization decides which
  implementation wins; constructor and initializer order decides which state is
  set. Check that every parent is initialized exactly once and in the right
  order, and that no override silently drops a base-class check.
- **Unchecked external calls.** A low-level call returns `(bool, bytes)` and a
  discarded `bool` is a silent failure. Check that the return value is used and
  that returndata is bounded.
- **Missing `initializer` on upgradeable contracts.** An `initialize()` without
  the modifier, or an implementation whose constructor omits
  `_disableInitializers()`, is a critical candidate on sight.
- **Invariants stated in comments or documentation but not enforced in code.**
  These convert directly into Phase 3 candidates and into the fuzzing
  properties in `references/invariants-and-fuzzing.md`.

Merge Pass A and Pass B into **one deduplicated candidate list**, each entry
carrying a `file:line` and a suspected class. Deduplicate by
`(file, line, class)`.

## Phase 3: deep validation

For each candidate, do the work that turns it into a finding or discards it:

1. Trace the full call chain from every external entry point that reaches it.
2. Follow the values of the relevant variables across contract boundaries,
   including through libraries, proxies, and callbacks.
3. Check every modifier and require on the path, and check what the path looks
   like when each one is satisfied by an attacker rather than a user.
4. Establish the preconditions an attacker needs, and whether they are
   reachable — capital is reachable via flash loan, ordering is reachable via
   MEV, and a "trusted" role is reachable if it is an EOA with no timelock.
5. Confirm or discard. Write the reason either way; a discarded candidate with
   a written reason is a durable review artifact.

### Rationalizations to reject

This list is the most valuable part of this skill. Each entry is a sentence
that ends analysis prematurely and is wrong often enough to be dangerous.

- **"The compiler is at least 0.8.0, so overflow is impossible."** Checked
  arithmetic covers ordinary expressions only. `unchecked` blocks, inline
  assembly, and **type downcasts** all still wrap silently — `uint128(x)` on an
  oversized `uint256` is a truncation, not a revert, at every compiler version.
- **"It uses OpenZeppelin, so it is safe."** The library is sound; the
  integration usually is not. The common defect is a custom function that
  forgot the modifier, an override that dropped a check, a hook used with the
  wrong assumptions, or a version whose behavior differs from the one the code
  was written against.
- **"That function is internal, so it is not reachable."** Internal functions
  are reached from external entry points and execute with the caller's context.
  Reachability is a property of the call graph, not of the visibility keyword.
  Enumerate the external callers before dismissing anything.
- **"No ETH is involved, so reentrancy does not apply."** ERC-721 `_safeMint`
  and `safeTransferFrom`, ERC-1155 single and batch safe transfers, and ERC-777
  `tokensToSend`/`tokensReceived` all hand control to a receiver. And
  **read-only reentrancy** needs no value transfer at all: a view function read
  mid-callback returns state that is momentarily inconsistent.
- **"It is upgradeable, so we can fix it later."** Upgradeability adds a
  vulnerability class rather than removing one. An `initialize()` without the
  `initializer` modifier is itself a critical finding, and a storage-layout
  collision cannot be fixed by the upgrade that causes it.
- **"The tool flagged it, so it is a finding."** And its inverse, **"the tools
  found nothing, so the code is clean."** A tool result is a lead until it has
  a written attack path; the absence of tool results says nothing about the
  business-logic and access-control classes that now dominate real losses.

## Phase 4: report

Emit one record per confirmed finding, then a severity summary.

```markdown
### [SC-01] <title>

- Severity: High | Medium | Low | Informational
- Class: <OWASP SC id and name, or a named class from the inventory>
- Location: `src/Path.sol:142` (`Contract.functionName`)
- Also affects: <other file:line, if the same root cause>
- Attack path:
  1. <attacker action, with the concrete precondition>
  2. <state transition>
  3. <realized impact>
- Preconditions: <capital, role, ordering, external assumption>
- Proof of concept: `test/PoC.t.sol:test_...` — fails at <assertion>
  (or: `theoretical` — no PoC written, reason: ...)
- Impact: <what is lost, by whom, and bounded by what>
- Recommendation: <the specific change, not "add validation">
- Confidence: high | medium | low
- Corroboration: slither `<detector>`, aderyn `<detector>`, manual
```

Close with the summary table:

| Severity | Count | With PoC | Theoretical |
| --- | --- | --- | --- |
| High | | | |
| Medium | | | |
| Low | | | |
| Informational | | | |

## Severity rubric

Use the wording competitive-audit practitioners recognize, so a severity
travels between this report and a contest or a client review without
retranslation. This is the one place the plugin departs from the five-tier
ladder in `security-audit`: on-chain reviews have no Critical tier, because
direct loss of funds is already the top of the scale. When a finding has to be
reported alongside off-chain findings, map High here to Critical or High there
depending on whether the loss needs any precondition at all, and leave Medium,
Low, and Informational unchanged.

- **High** — assets can be **directly** stolen, lost, or compromised; or
  indirectly, via a valid attack path with no hand-waving. If a step in the
  path is "and then the admin makes a mistake" or "assuming an unrealistic
  market", it is not High.
- **Medium** — assets are not at direct risk, but a protocol function or its
  availability is impacted; or value leaks under a stated external assumption
  the protocol itself declares.
- **Low** — a real defect with negligible impact, or one requiring conditions
  outside any stated threat model.
- **Informational** — code quality, missing events, documentation drift. Keep
  these out of the severity table's decision-making and out of any gate.

Sherlock's denial-of-service rule, applied verbatim because it removes most
severity arguments: funds locked for **more than a week**, **or** availability
of time-sensitive functions impacted, is **Medium**; **both** together is
**High**.

Every High or Medium finding should carry a **failing Foundry
proof-of-concept test**, or be tagged explicitly as `theoretical`. A severity
without one of those two is not reportable. See
`references/invariants-and-fuzzing.md` for the harness patterns.

## Standards to work from

- **OWASP Smart Contract Top 10, 2026 edition** — `https://scs.owasp.org/sctop10/`.
  The current ranking, and the one to classify findings against:

  | ID | Class |
  | --- | --- |
  | SC01 | Access control vulnerabilities |
  | SC02 | Business logic vulnerabilities |
  | SC03 | Price oracle manipulation |
  | SC04 | Flash-loan-facilitated attacks |
  | SC05 | Lack of input validation |
  | SC06 | Unchecked external calls |
  | SC07 | Arithmetic errors (rounding and precision) |
  | SC08 | Reentrancy attacks |
  | SC09 | Integer overflow and underflow |
  | SC10 | Proxy and upgradeability vulnerabilities |

  **Access control is now #1 and reentrancy has fallen to #8.** Let the effort
  budget reflect that: the enumeration of every state-changing function and its
  guard is worth more review time than another pass over external calls.
- **Solodit checklist** — `https://solodit.cyfrin.io/checklist`, with the
  machine-readable source in `Cyfrin/audit-checklist`. Use it as the manual
  pass in the default pipeline; it is organized by the categories real audit
  reports use.
- **Building Secure Contracts** (Trail of Bits) — `https://secure-contracts.com`.
  Development guidance and the reference material for Echidna, Medusa, and
  Slither program analysis.
- **EEA EthTrust Security Levels v2**, 13 December 2023 —
  `https://entethalliance.org/specs/ethtrust-sl/v2/`. The formal successor to
  SWC, structured as testable requirements at three levels. A Version 3
  editor's draft is published at the unversioned URL; treat v2 as the citable
  release.
- **The SWC Registry is deprecated.** Cite an `SWC-xxx` identifier only when
  mapping a legacy report or an older tool's output. Do not use it as a live
  checklist.
- **DASP is dead** — the site is unreachable and its content dates from 2018.
  Do not cite it and do not use its top-ten ordering.

## Default pipeline

An ordered, copy-pasteable block for a Foundry repository. Every step is
non-fatal, and artifacts land **outside the working tree**.

```bash
OUT="${TMPDIR:-/tmp}/sc-audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"
REPO_URL="https://github.com/ORG/REPO"          # for --markdown-root
EXCL="lib/|test/|script/|mock/"

# 1. Recon
{ forge --version; slither --version; aderyn --version; } 2>&1 | tee "$OUT/versions.txt"
find . -name '*.sol' -not -path './lib/*' | xargs grep -H '^pragma solidity' \
  > "$OUT/pragmas.txt" || true
forge build --sizes > "$OUT/build.txt" 2>&1 || true
slither . --print human-summary,contract-summary,vars-and-auth,entry-points,not-pausable \
  > "$OUT/recon.txt" 2>&1 || true

# 2. Static analysis (run both; they disagree usefully)
slither . --checklist --markdown-root "$REPO_URL/blob/$(git rev-parse HEAD)/" \
  --filter-paths "$EXCL" --exclude-dependencies > "$OUT/slither.md" 2>&1 || true
slither . --json "$OUT/slither.json" --sarif "$OUT/slither.sarif" --fail-none || true
aderyn . -x lib,test,script -o "$OUT/aderyn.json" || true
aderyn . -x lib,test,script -o "$OUT/aderyn.md"   || true
solhint 'src/**/*.sol' -f sarif > "$OUT/solhint.sarif" 2>/dev/null || true

# 3. Proxy and storage checks (only when a proxy exists)
slither-check-upgradeability . ContractV1 --new-contract-name ContractV2 \
  > "$OUT/upgradeability.txt" 2>&1 || true
slither-read-storage . --contract-name Contract > "$OUT/storage.txt" 2>&1 || true

# 4. Tests and coverage
forge test -vv > "$OUT/tests.txt" 2>&1 || true
forge coverage --report lcov --report-file "$OUT/lcov.info" \
  --no-match-coverage "(test|script|mock)" --ir-minimum > "$OUT/coverage.txt" 2>&1 || true

# 5. Invariants and property fuzzing
FOUNDRY_PROFILE=invariant forge test --match-test invariant_ -vv \
  > "$OUT/invariants.txt" 2>&1 || true
echidna . --contract InvariantHarness --test-mode assertion \
  --corpus-dir "$OUT/echidna-corpus" > "$OUT/echidna.txt" 2>&1 || true
medusa fuzz --target-contracts InvariantHarness \
  --corpus-dir "$OUT/medusa-corpus" > "$OUT/medusa.txt" 2>&1 || true

# 6. Symbolic and formal, best effort only
halmos --function check_ --solver-timeout-assertion 0 > "$OUT/halmos.txt" 2>&1 || true
hevm test > "$OUT/hevm.txt" 2>&1 || true

# 7. Manual pass — the part no step above performs
echo "Solodit checklist + OWASP SC Top 10 2026 + the class inventory" \
  > "$OUT/manual-pass.md"
```

Replace `Contract`, `ContractV1`, `ContractV2`, `InvariantHarness`, and
`REPO_URL` with the project's own names; nothing else is project-specific.

### Triage rules

- **Suppress `lib/`, `test/`, `script/`, and `mock/` everywhere**, in every
  tool, using that tool's own path filter. A finding inside a dependency
  belongs to the dependency review, not this one.
- **Deduplicate across Slither and Aderyn by `(file, line, class)`.** Keep one
  record whose corroboration field lists both detectors. Agreement raises
  confidence; it does not create a second finding.
- **Promote a lead to a finding only** with a written attack path plus a
  failing Foundry proof of concept, or an explicit `theoretical` tag.
- Suppress `reentrancy-benign` and `reentrancy-events` by default; they are
  usually non-issues and they crowd out the signal.
- Keep Solhint's output entirely out of the findings report. It is a style
  gate, not an audit input.

## References in this skill

| File | Contents |
| --- | --- |
| `references/vulnerability-classes.md` | The 2026 class inventory: what each class is, how to spot it, what to check |
| `references/tooling.md` | Install, invocation, output format, and false-positive character for every tool |
| `references/invariants-and-fuzzing.md` | Foundry invariants, the six invariant families, `crytic/properties`, Echidna, Medusa |
| `references/operations.md` | Upgrade safety, verification, keys and governance, monitoring, incident response, non-EVM |

## When not to use this skill

- Off-chain application, API, cloud, container, or dependency security — those
  belong to the other skills in this plugin.
- Gas optimization, tokenomics, or economic-design review with no security
  question attached.
- Non-EVM chains beyond the short pointers in `references/operations.md`.
- A request to attack or scan a contract the user does not own or is not
  authorized to review.
