---
name: obscured-site
description: Minimize browser-delivered implementation and apply the default obscuring pass when building or updating a website or static web app. Balance exposure against loading and interaction costs. Supports static build output; does not authorize deployment or unrelated security work.
---

# Obscured site

This skill depends on a separate obscuring build pass that initializes a site policy,
transforms static output, writes a private manifest, verifies output, and checks a
deployed URL. Set `OBSCURE_REPO` in [config.example](../config.example), then read
that dependency's README, review notes, and maintained status before integration.
Integrating a site does not require restarting research.

## Minimize what the browser receives

Minimize real application code delivered to the browser before obscuring it,
subject to the site's loading, interaction and availability requirements. Inspect
the actual build and import graph: remove unused code and dependencies, prefer
static HTML/CSS for static content, and hydrate only the parts needing interaction.
Avoid shipping a framework runtime solely to render otherwise static content.

Within the authorized scope, keep server-suitable implementations off the client
and return only the results the product needs, using the selected-function routes
below where appropriate. Keep immediate input handling, animation and other
latency-sensitive behavior local when server round trips would harm the experience.
Assess cold starts, network latency, caching and offline needs before moving work.
Code splitting and lazy loading can reduce initial delivery; they do not keep
publicly fetchable code private. Browser-decrypted modules and bytecode are still
delivered implementations.

Compare before/after real JavaScript bytes, added decoy bytes and compressed
transfer sizes separately. Measure cold/warm startup and representative interactions
under comparable conditions, including added requests and server round trips;
label automation overhead and measurement limits. Choose the smallest exposed
implementation that meets the site's measured performance needs. Record the
reason for meaningful client-side logic that remains. Preserve the decoy policy
below; minimizing application code does not silently waive its budgets or opt-outs.

## Audit comments and public source

Check repository visibility and intended publication before writing explanatory
comments. Keep private design notes, security analysis, internal paths and hints
identifying real versus decoy logic outside public source. Public comments should
contain only the rationale needed by their intended readers; respect explicitly
requested public documentation and open-source goals.

Inspect the actual served HTML, JavaScript, CSS and SVG, including inline and
embedded source such as shaders. Use syntax-aware production transforms to remove
nonessential explanatory comments, preserving required license notices and framework
hydration markers. Verify the result with parsers or appropriate format checks;
an unsupported format is an unverified surface. Build-time stripping does not hide
comments in a public repository, its published history or other published copies.
Check those publication surfaces separately within the authorized scope. Comment
removal reduces disclosure of intent; it does not make delivered logic secret.

## Integrate and verify

Run `obscure init`, choose public/private mode and meaningful sensitive strings,
then build and verify the actual output against its private manifest. Preserve the
visitor experience, accessibility, legal pages and the site's explicit opt-outs.
Opt-outs require a written config reason. For frameworks without static output,
test an appropriate integration before claiming this pattern applies.

Keep source, public output, gated content and private manifests confined and
separate. Follow the repo's symlink, regular-file and quarantine rules. Never put
secrets or private analysis in browser output. Run this pass before precompression;
compressed source sidecars bypass protection and are rejected. Disable inline
source maps upstream. Missing or obsolete manifest evidence requires a rebuild,
not weaker verification.

Use `obscure check-url` against the intended deployed copy when rollout is
already authorized. It verifies inventoried HTML, JavaScript and CSS, parsed HTML
asset references, and the unmapped static JavaScript import/re-export graph,
including query variants. Only matching HTML/module bytes may extend discovery.
Read the README's coverage limits: import maps, dynamic imports, runtime DOM
changes and other routes are not a complete browser trace. A changing `<base>`
fails explicitly because the checker does not emulate CSP/parser timing.
Verify actual behavior through the authorized browser integration and preserve a
rollback before rollout. Local checks alone do not establish deployed behavior.

Every build records a new seed. `--seed <32 hex characters>` reproduces the same
inputs and policy; `--watermark <label>` is publicly readable, so use generic text.
The ruling of 2026-10-10 keeps AI crawlers allowed: the pass reduces exposed
implementation without making crawler exclusion its goal. Keep existing llms.txt
and deliver the same pages to bots and people. Decoy pages use the fixed claim-free copy, noindex and robots Disallow;
honeypot links appear only in private mode. These directives do not guarantee
that a URL never appears in search results.

## Protect important implementations

Use the dependency's selected-function routes:

- Keep server-suitable logic in an explicitly authorized server registry outside
  the browser import graph. Validate inputs, authorize the caller and return only
  the result the product needs; use `validateResult` to check the serialized shape.
  Outputs remain an inference channel. Account/request-owned parameters must come
  from a trusted workflow; preserve inputs users legitimately choose.
- For supported pure functions that must run locally, use opt-in bytecode and
  verify behavior. Unsupported selections must fail rather than fall back to plain code.
- Deliver private self-contained modules through the existing authorized AES-GCM
  path when appropriate. Browser-delivered code, bytecode and decrypted content
  remain recoverable. Single use describes a delivery nonce, not permanent secrecy.

These are per-site integration choices, not automatic migrations of working logic.
The server recipes do not supply login, provisioning or transaction isolation.

## Decoys and performance

Retain the requested substantial, varied fake code mixed through the same
scrambling pass as eligible application code. Use the existing seeded `decoyCode`
budgets; inspect skipped scripts and verify generated code survives the final
build. Separate decoy pages or a few token stubs do not satisfy this requirement.
Record real/added bytes and compressed transfer size; measure startup and
interaction costs for the site. Decoys must have no network, storage or other
externally visible side effects. Reductions or opt-outs require a written reason.

For selected virtualized functions, retain the bounded semantic variant pools and
encoded routing. Check genuine behavior and observable decoy divergence on the
actual input domain, including output types, numeric boundaries and invariants.
Private analysis stays private; no public truth labels or fixed genuine slot.

Keep current mode defaults and recorded budgets. More encryption, padding or
false members is not demonstrated protection. The dependency's current evidence includes exact fresh-agent
recovery, cheap repairs and isolated false completions; it does not establish
reliable persistent deception. Experimental source hints and alternate pools stay
in benchmarks until matched evidence supports promotion.

## When explicitly improving the defenses

Use the dependency's testing-a-proposed-layer and persistent-false-discovery methods.
Start with representation-appropriate extraction, padding removal, voting,
boundary/history probes and source repair. Carry counterexamples into deeper
layers and run the dependency's minimum-counterexample-cover
control: sequential first-found failures can exaggerate semantic depth.

Only then run fresh matched analysts with frozen artifacts, public interfaces,
seeds, budgets and execution-accounting rules. Capture candidate bytes and explicit
completion/confidence claims before hidden grading. Wrong completion is evidence;
a decoded fake, admitted uncertainty or tool ERROR is not. Include a working
positive control and report successful recovery alongside failures. Measure
compressed bytes and execution costs before promoting an increase in strength.

Use the dependency's checkpoint capture from before inspection. `save-checked` retains candidate, exact public interface,
preflight result and hash-bound receipt; include public executions in accounting.
It supports the closed scalar evaluator. Structured ledger inputs still use
capture-only `save` with separately recorded grading: do not silently run arbitrary
candidate JavaScript in a VM as a substitute. Local timestamps and self-reported
execution ledgers are not tamper-proof or complete accounting.

A skill or local template grants no deploy, production install, DNS/cache or
credential authority. Use the existing per-site authority.
