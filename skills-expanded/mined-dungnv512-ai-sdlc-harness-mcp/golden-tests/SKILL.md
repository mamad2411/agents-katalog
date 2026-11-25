---
name: golden-tests
description: Alchemist golden-image tests for Flutter widgets - device sizes, themes, states, CI determinism. MANDATORY TRIGGERS - "golden", "goldens", "alchemist", "snapshot test", "visual regression", "pixel diff".
allowed-tools: Read, Glob, Write, Edit, Bash
---

# Skill: golden-tests

## When to use

Adding or changing a public widget. Updating the theme. Diff in a
golden image showed up in CI.

## Setup

`test/alchemist_config.dart`:

```dart
return AlchemistConfig(
  platformGoldensConfig: PlatformGoldensConfig(enabled: false),
  ciGoldensConfig: const CiGoldensConfig(enabled: true),
  theme: AppTheme.light, // and a dark variant test
);
```

## Pattern

```dart
@Tags(['golden'])
void main() {
  goldenTest(
    'PostCard renders all states',
    fileName: 'post_card_states',
    builder: () => GoldenTestGroup(
      columns: 2,
      children: [
        GoldenTestScenario(name: 'default', child: PostCard(post: _post())),
        GoldenTestScenario(name: 'loading', child: const PostCard.skeleton()),
        GoldenTestScenario(name: 'long text', child: PostCard(post: _longPost())),
        GoldenTestScenario(name: 'rtl', child: Directionality(textDirection: TextDirection.rtl, child: PostCard(post: _post()))),
      ],
    ),
  );
}
```

## Rules

- One golden file per state matrix, two device sizes (small phone +
  tablet).
- Use **deterministic** fixtures — fixed dates, fixed avatars
  (committed PNGs under `test/fixtures/`).
- Never call `--update-goldens` blindly in CI. Update locally,
  attach diff screenshots to PR, then re-run.
- Goldens live under `test/features/<slug>/golden/`.

## CI

`flutter test --tags golden`. Compares against committed PNGs; PR
fails on diff > 0 pixels.

## See also

- `design-system` (stories source the golden matrix)
