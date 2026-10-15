---
name: "android-coil-compose"
description: "Use Coil in Jetpack Compose with AsyncImage, painter variants, sizing, and accessible image loading patterns."
metadata:
  version: "0.1.0"
  category: "ui"
  tags: ["android", "compose", "coil", "images", "accessibility"]
  triggers:
    include: ["coil compose image loading", "asyncimage android compose", "rememberasyncimagepainter android", "compose image placeholder error android", "coil lazycolumn performance android"]
    exclude: ["retrofit only", "ui automator only", "room migration only"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "benchmarks/triggers.jsonl"]
---
# Android Coil Compose

## When To Use
- Use this skill when the request is about: coil compose image loading, asyncimage android compose, rememberasyncimagepainter android.
- Primary outcome: Use Coil in Jetpack Compose with `AsyncImage`, painter variants, sizing, and accessible image loading patterns.
- Reach for this skill when the work is specifically about image loading, placeholders, error states, sizing, or list performance in Compose.
- Read `references/patterns.md` for the `AsyncImage` vs painter vs subcomposition decision guide.
- Read `references/scenarios.md` for list-performance and screenshot-stable validation paths.
- Handoff skills when the scope expands:
- `android-compose-foundations`
- `android-compose-performance`

## Workflow
1. Identify whether the UI needs a simple image surface, low-level painter access, or custom slot-based loading states.
2. Prefer `AsyncImage` first, then drop down to painter APIs only when the component truly needs them.
3. Constrain size, placeholders, and content description so the image behavior is both performant and accessible; for painter APIs, supply an explicit size resolver when needed.
4. Check list rendering, state churn, and visual fallbacks before considering the implementation done, and confirm that remote data or decoder modules are actually present when the source type needs them.
5. Hand off general Compose layout or broader performance issues to the neighboring skills after the image pipeline is stable.

## Guardrails
- Prefer `AsyncImage` for most Compose surfaces.
- Keep image requests sized to the rendered UI surface when possible.
- Provide meaningful accessibility behavior: descriptive `contentDescription` for informative images, `null` for decorative ones.
- Avoid subcomposition-heavy image patterns in scroll-heavy lists unless the UX truly needs them.
- If you need painter state directly, remember that `rememberAsyncImagePainter` does not infer on-screen size by itself.

## Anti-Patterns
- Loading full-size remote assets into tiny list items.
- Using `SubcomposeAsyncImage` everywhere when a simple placeholder is enough.
- Treating image loading failures as silent no-ops with no error fallback.
- Forgetting accessibility semantics on actionable or informative images.

## Review Focus
- API choice: `AsyncImage`, `rememberAsyncImagePainter`, or `SubcomposeAsyncImage`.
- Correct sizing and request construction for the rendered surface.
- Remote-loading prerequisites such as the right Coil network modules.
- Stable placeholders and error states for lists, tests, and screenshots.

## Examples
### Happy path
- Scenario: Build the Compose fixture and verify a stable `AsyncImage` surface renders in the task board.
- Command: `bash skills/android-coil-compose/scripts/run_examples.sh`

### Edge case
- Scenario: Review a list cell where placeholders, sizing, and lazy-list performance all matter.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:testDebugUnitTest`

### Failure recovery
- Scenario: Re-check the image surface after a placeholder or error-state change using screenshot-friendly validation.
- Command: `cd examples/orbittasks-compose && ./gradlew verifyRoborazziDebug`

## Done Checklist
- `AsyncImage` is the default unless a lower-level painter API is justified.
- Sizing, placeholders, and error states are explicit.
- Accessibility behavior is intentional.
- List and screenshot behavior has been validated on the Compose fixture.

## Official References
- [https://coil-kt.github.io/coil/compose/](https://coil-kt.github.io/coil/compose/)
- [https://coil-kt.github.io/coil/image_requests/](https://coil-kt.github.io/coil/image_requests/)
- [https://coil-kt.github.io/coil/network/](https://coil-kt.github.io/coil/network/)
- [https://developer.android.com/develop/ui/compose/graphics/images/loading](https://developer.android.com/develop/ui/compose/graphics/images/loading)
- [https://developer.android.com/develop/ui/compose/accessibility](https://developer.android.com/develop/ui/compose/accessibility)
