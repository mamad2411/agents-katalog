---
name: audit-license-compliance
description: Audits open-source license compliance — resolves SPDX identifiers across the full transitive dependency tree (license-checker/scancode), classifies copyleft (GPL/AGPL/LGPL) exposure against the distribution model, enforces an allow/deny CI policy, and generates NOTICE/THIRD-PARTY attribution files.
when_to_use: Shipping a product/library or prepping a legal/procurement review and needing to clear OSS license obligations. Distinct from supply-chain-sbom-provenance (build integrity, SBOM signing, provenance), dependency-upgrade (version bumps), and publish-package-registry (the publish step).
---

## When to Use

Reach for this skill when the question is about **license obligations**, not which versions to ship or whether the build is tamper-proof:

- "Can we ship — does anything here have a GPL/AGPL problem?"
- "Generate the NOTICE / THIRD-PARTY-LICENSES file for the release."
- "Add a CI gate that fails the build on a forbidden license."
- "Legal/procurement needs the full list of dependencies and their licenses."
- "This transitive dep has no license / is dual-licensed — what do we do?"
- "We're going from internal SaaS to a downloadable binary — what changes?"

NOT this skill:
- Generating/signing an SBOM, provenance, or attestations → supply-chain-sbom-provenance (it lists *components*; this skill judges their *licenses*)
- Bumping a version or swapping a GPL dep for an alternative → dependency-upgrade
- The actual `npm publish` / `twine upload` step and its OIDC gate → publish-package-registry
- A design-level risk enumeration of the system → threat-model-stride

## Steps

1. **Scan the FULL transitive tree, not just direct deps — and pin the result to a manifest.** Direct deps are a tiny minority; copyleft almost always rides in transitively. Pick the resolver for the ecosystem and emit machine-readable output:

   ```bash
   # Node — license-checker-rseki (maintained fork) over the *production* tree only
   npx license-checker-rseki --production --json --out licenses.json
   # Python
   pip-licenses --format=json --with-license-file --with-urls > licenses.json
   # Rust
   cargo install cargo-deny && cargo deny list -f json > licenses.json
   # Go
   go install github.com/google/go-licenses@latest && go-licenses report ./... > licenses.csv
   # Ground truth when metadata lies — scans actual file headers/text
   pipx run scancode-toolkit scancode --license --json-pp scancode.json <vendored_dir>
   ```
   Scope to what you **distribute**: prod/runtime deps only. devDependencies, test, and build-only tooling are generally not distributed — exclude them (`--production`, `--omit=dev`) or you'll drown in false GPL hits from linters. When package metadata is missing or wrong, `scancode` reading the real LICENSE/headers is the tiebreaker, not the `package.json` `license` field.

2. **Classify each license by risk against YOUR distribution model — this is the whole audit.** The same license is fine or fatal depending on how you ship. Decide the model first, then read the table left-to-right:

   | License class | Examples | SaaS (network only) | Distributed binary / app | Library you publish |
   |---|---|---|---|---|
   | Permissive | MIT, BSD-2/3, ISC, Apache-2.0, Unlicense, 0BSD | ✅ allow | ✅ allow (must keep NOTICE) | ✅ allow |
   | Weak copyleft (file) | MPL-2.0, EPL-2.0, CDDL | ✅ allow | ⚠️ allow if unmodified & file-isolated | ⚠️ review |
   | Weak copyleft (lib) | LGPL-2.1/3.0 | ✅ allow | ⚠️ **dynamic** link only; static link triggers relink obligation | ⚠️ review |
   | Strong copyleft | GPL-2.0, GPL-3.0 | ✅ allow (no conveying) | ❌ **deny** — forces whole-program source disclosure | ❌ deny |
   | Network copyleft | **AGPL-3.0** | ❌ **deny** — network use = conveying, source must be offered to users | ❌ deny | ❌ deny |
   | Notice-heavy / patent | Apache-2.0, BSD-4-Clause | ✅ (track NOTICE/patent grant) | ⚠️ BSD-4 advertising clause incompatible w/ GPL | ⚠️ review |
   | Non-OSS / source-available | SSPL, BUSL-1.1, Elastic-2.0, CC-BY-NC, "Commons Clause" | ❌ deny (not OSI; usage-restricted) | ❌ deny | ❌ deny |
   | Public domain / unclear | WTFPL, "UNLICENSED", no license | ❌ deny pending manual review | ❌ deny pending review | ❌ deny |

   The trap most teams miss: **AGPL bites SaaS** (where GPL does not, because you never "convey" a binary), and **LGPL/GPL bite distributed binaries** (where they're harmless on a server). Set the model once; don't hand-wave it as "it depends."

3. **Encode the policy as allow / deny / review with SPDX IDs and gate CI on it.** A human-readable table isn't enforcement. Use one tool to both classify and fail the build. `cargo-deny`-style config (mirror the shape in `license-checker --failOn` or an `oss-review-toolkit`/`fossa`/`trivy` policy):

   ```toml
   # deny.toml — explicit allowlist; everything unlisted is a hard failure
   [licenses]
   allow = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0"]
   confidence-threshold = 0.9          # below this, treat as unknown → fail

   # exceptions: this one crate is allowed despite the policy, with a reason on record
   [[licenses.exceptions]]
   crate = "ring"
   allow = ["OpenSSL"]                 # rationale: leaf TLS dep, OpenSSL terms cleared by legal 2026-05
   ```
   ```bash
   # CI gate — non-zero exit blocks the merge. Run on every PR.
   cargo deny check licenses
   # Node equivalent (allowlist must match deny.toml above):
   npx license-checker-rseki --production --onlyAllow \
     "MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC;MPL-2.0" --excludePrivatePackages
   ```
   Default posture is **allowlist, deny-by-default**: an unknown/unparseable license fails closed, so a newly added denied or no-license dep cannot merge silently. Route genuinely-ambiguous cases to a `review` bucket that fails CI with a "needs legal sign-off" message rather than auto-allowing.

4. **Resolve dual-licensed and missing-license deps explicitly — never let the tool pick for you.** SPDX `OR` means *you choose* (e.g. `(MIT OR Apache-2.0)` → pick the one in your allowlist and record the choice). SPDX `AND` means *both apply* (you must satisfy every obligation). For a dep with **no license**, default-deny: open an issue, contact the maintainer, or remove it — "no license" means all-rights-reserved, not free. Pin every resolution and exception in `deny.toml`/policy with a one-line rationale so the next audit doesn't relitigate it.

5. **Generate NOTICE / THIRD-PARTY-LICENSES attribution from the same scan.** Permissive licenses (MIT/BSD/Apache) require you to reproduce their copyright + license text in distributed artifacts; Apache-2.0 also requires propagating any upstream `NOTICE`. Auto-generate, don't hand-maintain:

   ```bash
   npx oss-attribution-generator ./   # → oss-attribution/attribution.txt
   # or: license-checker-rseki --production --customPath fields.json --files THIRD-PARTY-LICENSES/
   pip-licenses --format=plain-vertical --with-license-file --no-license-path \
     --output-file THIRD-PARTY-LICENSES.txt
   go-licenses save ./... --save_path=THIRD-PARTY-LICENSES/
   ```
   Ship `THIRD-PARTY-LICENSES.txt` (or `NOTICE`) inside the artifact — in the package tarball, the container image, the app's "Licenses" screen, or `/licenses`. Regenerate it in CI from the locked tree and **diff against the committed copy** so a new dep can't slip in without its attribution.

6. **Wire both gates into one CI job.** Policy check (step 3) + attribution drift check (step 5) run on every PR and on the release tag. Fail the build if a denied/unknown license appears OR the generated NOTICE differs from the committed one. This is what makes the audit durable instead of a one-time spreadsheet.

## Common Errors

- **Scanning direct deps only.** The GPL/AGPL almost always arrives 3 levels deep. Always resolve the full transitive tree (`--production` flattens it).
- **Including devDependencies in the distributed verdict.** A GPL linter or test runner isn't distributed and isn't a violation — it just floods the report and gets the gate disabled. Scope to runtime/prod.
- **Trusting the package `license` field over the actual files.** Metadata is frequently wrong, stale, or `SEE LICENSE IN ...`. When it matters, let `scancode` read the real LICENSE/headers; that's ground truth.
- **Treating AGPL like GPL for a SaaS.** AGPL's network clause means serving it over HTTP *is* conveying — source must be offered to every user. Deny AGPL even when GPL would be fine for your server-only model.
- **Static-linking an LGPL library into a shipped binary.** That triggers the relink obligation (users must be able to swap the lib). Dynamic-link it, or treat it as deny for static builds.
- **Auto-picking a side of a dual license silently.** `(GPL-2.0 OR MIT)` is only safe because *you* elect MIT — record the election. If the tool defaulted to GPL, you may have manufactured an obligation that didn't exist.
- **"No license" read as permissive.** Absence of a license = all rights reserved = you have no grant to use it. Default-deny and resolve, don't ship.
- **Allowlist that fails *open* on unknowns.** A typo SPDX id or low-confidence match must fail the build, not pass. Set `confidence-threshold` and deny-by-default.
- **Hand-maintaining NOTICE.** It drifts the moment a transitive dep changes. Generate it from the lockfile in CI and diff against the committed copy.
- **Confusing source-available with open-source.** SSPL/BUSL/Elastic-2.0/"Commons Clause" are usage-restricted and not OSI-approved — deny them unless legal explicitly cleared the specific use.

## Verify

1. **Coverage:** The scan output lists *transitive* deps, not just the handful in `package.json`/`Cargo.toml`. Spot-check a known deep dep appears with a license.
2. **Policy gate fires (positive control):** Add a dep with a denied license (e.g. a GPL-3.0 package) on a throwaway branch → CI **fails** with a message naming the dep and its license. Revert.
3. **Unknown fails closed:** Point the scanner at a dep with a stripped/garbled license → it is reported as unknown and the gate **fails**, not passes.
4. **Distribution-model correctness:** Re-run classification under the other model (flip SaaS↔distributed) and confirm AGPL/LGPL/GPL verdicts change as the table predicts — proves the model is actually driving the verdict, not hardcoded.
5. **Attribution completeness:** Every distributed (prod) dependency in the lockfile appears in `THIRD-PARTY-LICENSES`/`NOTICE` with its license text. Count of attributed deps == count of distributed deps; no entry is empty.
6. **Attribution drift gate:** Add a prod dep without regenerating → CI's NOTICE-diff check **fails**. Regenerate → it passes and the new dep+license is present.
7. **Dual/missing resolved:** No dep is left with an unresolved `OR` expression or empty license; each exception in the policy has a written rationale.

Done = the scan covers the full transitive prod tree, CI blocks a newly added denied-license **and** an unknown-license dep (verified by positive controls), every distributed dependency is listed with its license in the committed NOTICE, and the NOTICE-drift gate fails when that list goes stale.
