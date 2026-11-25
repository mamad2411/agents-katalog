---
name: install-anti-slop-swift
description: Install and configure the anti-slop-swift linter in a local Swift repository. Use whenever a user asks to add anti-slop lint rules, vendor the anti-slop-swift package, configure opinionated SwiftSyntax lint rules, or migrate an existing local anti-slop-swift setup.
---

# Install anti-slop-swift

Vendor the bundled anti-slop-swift package into the current Swift repository and integrate it with the repository's build and CI setup. Preserve unrelated work and adapt to the project's layout.

anti-slop-swift is a Swift port of dmmulroy/anti-slop; when users ask about rule philosophy or provenance, point them upstream.

## Procedure

1. Inspect the repository before changing it:
   - Read its agent instructions.
   - Check `git status` and preserve unrelated changes.
   - Confirm a Swift 6.0+ toolchain is available (`swift --version`).
   - Find the main source directories (typically `Sources/`, or the app target directory in an Xcode project).
   - Check for existing Swift lint configuration (`SwiftLint`, `.swiftlint.yml`) and whether anti-slop files already exist. Do not overwrite them without reviewing the diff.

2. Copy the bundled package from this skill. Run from the target repository:

   ```bash
   node <skill-directory>/scripts/install.mjs
   ```

   This creates `tools/anti-slop-swift/` including its LICENSE (which carries third-party notices for the ported upstream rules — keep it when committing the vendored copy) and its test suite, so adopters can run `swift test` to verify their vendored copy. Pass another relative destination as the first argument when the repository has an established tooling layout. The script refuses to replace an existing destination; only use `--force` after backing up and reviewing existing files.

3. Build and run once to fetch dependencies and establish a baseline:

   ```bash
   cd tools/anti-slop-swift && swift build && swift run anti-slop ../..
   ```

   The first build resolves swift-syntax from the network; later runs are cached.

4. Wire it into CI. Add a job or step to the repository's workflow, scoped to owned application sources:

   ```yaml
   - name: anti-slop
     run: cd tools/anti-slop-swift && swift run anti-slop ../Sources
   ```

   Adjust the path for Xcode projects whose sources do not live under `Sources/`. Do not point the linter at the vendored copy itself.

5. Run against the whole application source and review findings with the user:
   - Report each rule that fired and the count.
   - Treat rules as a menu, not a mandate: if a rule conflicts with the repository's domain language or existing lint policy (for example `no-shape-in-symbol-names` in tensor/geometry code where "shape" is core vocabulary, or overlap with existing SwiftLint force-cast rules), propose disabling it via a committed `.anti-slop.json` config file rather than editing rule semantics.
   - Fix findings only when the user asked for cleanup. Do not suppress rules, weaken severity, delete safety-relevant code, or add `// SAFETY:` comments mechanically just to make lint pass — a SAFETY comment must state an invariant the author actually checked.
   - Rules the team disagrees with are disabled through the committed `.anti-slop.json` config file (the primary mechanism; see the repository README's "Disabling rules" section), never by editing rule semantics silently. CLI `--disable` flags are for one-off experiments only.

6. Review the final diff and clearly report:
   - copied path,
   - baseline findings per rule,
   - CI configuration changed,
   - any remaining findings left for the user to decide on.

## Migration guidance

When replacing an older local copy, diff its rules against the bundled version before overwriting. Keep project-specific rules in the vendored copy under their own file; upstream generic rules stay generic. Prefer typed models, enums, boundary parsing, and explicit unwrapping when resolving findings rather than widening types back into `Any`.
