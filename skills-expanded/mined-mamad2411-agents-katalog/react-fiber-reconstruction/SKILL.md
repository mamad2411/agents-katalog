---
name: react-fiber-reconstruction
description: Reconstruct React components from running websites without source access by using React Fiber metadata and DOM/CSS snapshots. Use for clone/recreate/reverse-engineer requests on production React UI, including props-to-HTML capture, type.toString extraction, structural and computed-style verification, stylesheet/font parity, dependency ordering, and fallbacks for animation or state-driven mismatches.
---

# React Fiber Reconstruction

Use this skill to rebuild or update React components from live pages with an evidence-first extraction flow, then enforce maintainable code standards before delivery.

## When To Use

- Reconstructing React UI from a running website when source code is unavailable.
- Rebuilding one or more production components with behavior and style parity requirements.
- Reverse-engineering component props/state from live runtime evidence.
- Updating existing component code to match captured runtime behavior without degrading maintainability.

## When Not To Use

- The target is not React-based and Fiber cannot be observed.

## Workflow

1. Confirm scope and permission.
- Verify the user is authorized to inspect and reproduce the target UI.
- Restrict extraction and output to approved components/assets.
- Define whether the task is `reconstruct new`, `patch existing`, or `hybrid`.

2. Capture runtime evidence from the page.
- Open the target route in a desktop browser context.
- Identify target DOM nodes and retrieve attached React Fiber nodes.
- Record per instance:
  - component identity key (in-memory `fiber.type` identity)
  - display name (`displayName` or `name`)
  - serializable props
  - rendered HTML snippet (`outerHTML`)
  - owner-chain path
  - `type.toString()` (when accessible)

3. Baseline existing code before writing updates.
- If code already exists, map capture groups to local files/components first.
- Record current API contract:
  - prop names/types/defaults
  - composition boundaries (leaf vs container)
  - styling system used (CSS modules, global CSS, CSS-in-JS, tokens)
- Mark what can be changed safely vs what must stay stable.

4. Capture state and interaction variants.
- Capture at least 3 meaningful variants when possible (default, active, submitted/open, disabled/loading, etc.).
- For each interaction, use deterministic assertion:
  - action
  - wait/confirm marker
  - post-action capture
- If scripted interactions do not mutate state reliably, infer behavior from `type.toString()` and document it.

5. Capture style and asset evidence.
- Capture computed styles for anchor nodes (container, title, subtitle, CTA cluster, controls).
- Capture active/inactive style deltas for stateful controls.
- Export relevant stylesheet responses and isolate rules for captured classnames/selectors.
- Record font stack and font-load status (`document.fonts.check(...)`) for key text nodes.

6. Group by component identity.
- Bucket captures by `fiber.type` identity.
- Keep grouped props/HTML examples together for each component.
- Preserve provenance for each capture (URL, timestamp, viewport).

7. Implement updates leaf-to-root.
- Update leaf components first; update containers only after leaf verification passes.
- Preserve stable public APIs unless parity requires a contract change.
- Require typed props, explicit defaults, deterministic rendering, and clear fallbacks.
- Keep behavior extraction separate from view primitives where possible.

8. Verify structure (render-and-diff loop).
- Render against captured fixtures.
- Normalize HTML before diffing.
- Feed focused mismatches back into patch iterations.
- Retry 3-5 rounds before fallback.

9. Verify visual parity.
- Compare computed-style snapshots between target and reconstructed components at anchor nodes.
- Verify typography and spacing (font family, weight, size, line height, letter spacing, max-width, gaps).
- Port captured stylesheet rules when broad visual drift exists.
- Re-check font loading; if failing, host needed fonts locally and re-verify.

10. Run maintainability gate before finalizing.
- Apply rules from `references/maintainable-code-update-guide.md`.
- Block merge for:
  - invalid interactive semantics (e.g., button nested inside anchor)
  - unstable list keys for dynamic collections
  - broken accessibility relationships and labels
  - prop/API breaking changes without migration note
- Prefer extraction-backed refactors over one-file monoliths.

11. Apply fallback for non-deterministic behavior.
- If mismatch is caused by animation timing, environment variance, or hidden internal state, freeze unstable sections as snapshot wrappers.
- Explicitly document unresolved deterministic gaps.

12. Assemble final output.
- Deliver reconstructed component code, required styles/assets, and verification artifacts.
- Include explicit limitations and residual risks.

## Capture Rules

- Prefer observed evidence over inferred behavior.
- Omit non-serializable values (functions, DOM nodes, symbols) and note omissions.
- Keep captures in one browser session when type identity stability matters.
- Use website-agnostic selector strategy in analysis (semantic anchors first, class hashes second).
- Keep raw logs for reruns and audits.

## Maintainable Update Rules

- Never paste extracted HTML/CSS blindly; map it into the project architecture.
- Keep business logic, state transitions, and rendering concerns separated.
- Keep tokens centralized; avoid duplicating `:root` variables across component CSS files.
- Favor semantic links/buttons for navigation and actions.
- Replace index keys with stable identifiers when list order/content can change.
- Write minimal comments only where intent is non-obvious.
- Keep changes small and composable; extract helper functions/hooks when component length grows significantly.

## Deliverables

- Reconstructed component files with typed interfaces.
- `verification-report.md` with fixture-level pass/fail.
- `style-parity-report.md` with key-node computed-style and typography checks.
- `limitations.md` for dynamic-state, animation, or environment caveats.
- `maintainability-report.md` with rule-by-rule pass/fail for updated files.

## References

- Read `references/fiber-capture-snippets.md` before runtime extraction.
- Read `references/style-parity-snippets.md` for computed-style/font/stylesheet parity checks.
- Read `references/chrome-devtools-mcp-playbook.md` for optimal DevTools MCP capture flow and pitfalls.
- Read `references/maintainable-code-update-guide.md` before final code edits.
- Use official React documentation and web search when React internals need confirmation.
