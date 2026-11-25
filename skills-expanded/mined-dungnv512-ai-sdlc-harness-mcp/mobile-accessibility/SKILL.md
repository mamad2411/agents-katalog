---
name: mobile-accessibility
description: Flutter accessibility implementation — Semantics widgets, MergeSemantics, TalkBack/VoiceOver testing, dynamic type clamping, reduced motion, WCAG 2.1 AA contrast, tap targets, focus order. MANDATORY TRIGGERS - "a11y", "accessibility", "semantics", "screen reader", "talkback", "voiceover", "dynamic type", "textscaler", "reduced motion", "wcag", "contrast", "tap target", "focus order".
allowed-tools: Read, Glob, Edit, Write
---

# Skill: mobile-accessibility

## When to use

Implementing a new screen or widget, reviewing an existing page for
accessibility compliance, or responding to a WCAG 2.1 AA audit finding.
This skill can also be triggered automatically by a golden-test workflow
that confirms each state has a Semantics snapshot.

---

## Inputs

- Widget or page being reviewed/built
- Feature slug
- Any accessibility audit finding text

---

## Steps

### 1. Semantics labels on interactive widgets

Every interactive widget that does not carry a text label visible to screen
readers must have a `Semantics` wrapper:

```dart
// Vote button — not just an icon
Semantics(
  label: t.post.voteUp,          // e.g. "Upvote post"
  hint: t.post.voteUpHint,       // e.g. "Double-tap to upvote"
  button: true,
  child: IconButton(
    icon: const Icon(Icons.arrow_upward),
    onPressed: _onUpvote,
  ),
),
```

Rules:
- `label` = what the element *is* (a short noun phrase).
- `hint` = what will *happen* (imperative, optional for obvious actions).
- `button: true` on tappable elements; `link: true` on navigation items;
  `header: true` on section headings.
- Do not duplicate text already present as visible text — the engine will
  concatenate them. Use `Semantics(label: '', child: ...)` to suppress a
  nested visual label that would double-announce.

### 2. MergeSemantics for card-level announcements

Composite cards (post cards, list-item cards) must announce as a single
node so screen readers read them as one coherent unit, not a stream of
fragments:

```dart
MergeSemantics(
  child: Column(
    children: [
      _AuthorRow(post: post),     // "@alice, 5 minutes ago"
      _PostBody(post: post),      // post text
      _PostActionBar(post: post), // vote/comment/repost row
    ],
  ),
)
```

The merged announcement should read approximately:
*"Post by @alice, 5 minutes ago, [body excerpt], 12 points, 3 comments"*

For elements *within* the merged group that should be silenced (decorative
dividers, icons redundant with label text), use `ExcludeSemantics`:

```dart
ExcludeSemantics(child: Divider()),
```

### 3. Dynamic type — clamp TextScaler

Always read `MediaQuery.textScalerOf(context)`. Numeric badges and
counters must clamp at 1.4–1.5x to prevent layout overflow while body
text scales freely:

```dart
// shared/extensions/text_scaler_x.dart
extension TextScalerX on TextScaler {
  /// Clamp for counter badges; body text uses the raw scaler.
  TextScaler get clamped => clamp(minScaleFactor: 1.0, maxScaleFactor: 1.4);
}
```

```dart
// Usage in a vote-count badge
MediaQuery(
  data: MediaQuery.of(context).copyWith(
    textScaler: MediaQuery.textScalerOf(context).clamped,
  ),
  child: Text(
    compactCount(post.netVote),
    style: Theme.of(context).textTheme.labelSmall,
  ),
),
```

Never set `textScaleFactor: 1.0` unconditionally — this disables the user's
accessibility setting entirely, which is a WCAG 2.1 AA failure.

Reference: [Flutter Accessibility](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility)

### 4. Reduced motion

Respect `MediaQuery.disableAnimations` and any in-app "reduce motion"
setting. Surface both through your app's lifecycle/theme manager. Wrap
any non-trivial animation:

```dart
final reduceMotion = MediaQuery.disableAnimationsOf(context)
    || context.read<ThemeCubit>().state.reduceMotion;

AnimatedSwitcher(
  duration: reduceMotion ? Duration.zero : Motion.med,
  child: _content,
)
```

Slide-in pills, Hero transitions, and list-scroll animations should all be
guarded by this flag. When reduced, use instant state swaps or simple
opacity fades of ≤ 120 ms.

Reference: [WCAG 2.1 §2.3.3 Animation from Interactions](https://www.w3.org/TR/WCAG21/#animation-from-interactions)

### 5. Color contrast

WCAG 2.1 AA requires:
- Body text (< 18pt / < 14pt bold): 4.5:1 contrast ratio
- Large text (≥ 18pt / ≥ 14pt bold): 3:1 contrast ratio
- UI component states (focused border, icon-only buttons): 3:1

Keep a `SemanticColors` (or equivalent) token set pre-validated against
every theme variant you ship (light, dark, and any additional themes). Do
not introduce raw `Color(0x...)` values outside `design_system/` — use a
token.

Verify with the `checkAccessibilityGuideline` flutter_test matcher in
golden tests:

```dart
testWidgets('PostCard meets contrast requirements', (tester) async {
  await tester.pumpWidget(pumpApp(const PostCard(post: mockPost)));
  await expectLater(
    find.byType(PostCard),
    meetsGuideline(textContrastGuideline),
  );
  await expectLater(
    find.byType(PostCard),
    meetsGuideline(iOSTapTargetGuideline),
  );
});
```

References: [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/), [Apple HIG Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Material 3 Accessibility](https://m3.material.io/foundations/accessible-design/overview)

### 6. Tap target sizes

- iOS HIG minimum: 44×44 pt logical pixels.
- Material 3 minimum: 48×48 dp logical pixels.
- Recommended project-wide standard: **48×48 dp** everywhere (satisfies both).

When a visual element is smaller than 48 dp, wrap with `SizedBox` or use
the `minimumSize` constraint on `ButtonStyle`:

```dart
IconButton(
  constraints: const BoxConstraints.tightFor(width: 48, height: 48),
  icon: const Icon(Icons.bookmark_outline),
  onPressed: _onBookmark,
)
```

Verify with `iOSTapTargetGuideline` in widget tests (see §5 snippet above).

### 7. Focus order

Use `FocusTraversalGroup` with `OrderedTraversalPolicy` wherever the visual
order differs from the logical focus order. Critical surfaces:

- Composer/editor forms: text field → attachment/metadata chips → media
  picker → language → char counter → submit.
- Login form: email → password → sign-in button → "Forgot password" link.
- Card action bar: vote up → vote down → comment → repost → share.

```dart
FocusTraversalGroup(
  policy: OrderedTraversalPolicy(),
  child: Column(
    children: [
      FocusTraversalOrder(order: const NumericFocusOrder(1), child: _emailField),
      FocusTraversalOrder(order: const NumericFocusOrder(2), child: _passwordField),
      FocusTraversalOrder(order: const NumericFocusOrder(3), child: _submitButton),
    ],
  ),
)
```

Test with:
```dart
await tester.testTextInput.receiveAction(TextInputAction.next);
expect(FocusScope.of(tester.element(find.byType(TextField).last)).hasFocus, isTrue);
```

### 8. Live regions for dynamic content

Vote counts and unread badge counts update silently while the user is on
screen. Announce changes to screen readers with `SemanticsProperties.liveRegion`:

```dart
Semantics(
  liveRegion: true,
  label: t.post.votesCount(post.netVote),
  child: Text(compactCount(post.netVote)),
)
```

Use sparingly — too many live regions create noise.

### 9. TalkBack / VoiceOver testing recipes

**Android TalkBack:**
1. Enable: Settings → Accessibility → TalkBack.
2. Navigate with swipe-right (next element), swipe-left (previous),
   double-tap (activate).
3. Check: every interactive element announces label; no duplicate
   announcements; scroll positions make sense.
4. Test the primary list: each card should be one TalkBack stop that reads
   the merged semantics label.

**iOS VoiceOver:**
1. Enable: Settings → Accessibility → VoiceOver, or triple-click side button.
2. Navigate with single-swipe right/left; activate with double-tap.
3. Use the Rotor (two-finger rotate) to check headings, links, and form fields.
4. Test focus order on the composer/editor screen.

If your app ships in multiple locales, also test TalkBack/VoiceOver with
each supported locale's TTS engine — some fonts and TTS engines handle
diacritics, tone marks, or non-Latin scripts inconsistently, so verify
rendering and pronunciation for every locale you support.

### 10. Per-PR accessibility checklist

Before marking a PR ready:

- [ ] Every new interactive widget has a `Semantics` label.
- [ ] Card-level widgets use `MergeSemantics`.
- [ ] Dynamic content (counters, badges) uses `liveRegion: true` where needed.
- [ ] No hard-coded text size (all via `TextTheme` tokens).
- [ ] `textScaler` tested up to 1.5x — no overflow, no clipped labels.
- [ ] `disableAnimations` path verified — no crash or invisible state.
- [ ] Tap targets ≥ 48 dp — verified with `iOSTapTargetGuideline` test.
- [ ] Contrast ratio ≥ 4.5:1 body — verified with `textContrastGuideline`.
- [ ] Focus order matches reading order for the new screen.

---

## Output

For each new screen or widget:
- `Semantics` wrapper on every interactive element
- `MergeSemantics` on composite cards
- Widget test with `meetsGuideline(textContrastGuideline)` and
  `meetsGuideline(iOSTapTargetGuideline)`
- Accessibility checklist ticked in PR body

---

## Anti-patterns

- `Semantics(label: widget.text)` on a `Text` widget — the text is already
  the semantic label; wrapping doubles the announcement.
- `ExcludeSemantics` on the entire action bar of a post card — buttons
  inside merged semantics should still be individually reachable when the
  user double-taps into the group.
- `MediaQuery.textScaleFactor` (deprecated) — use `MediaQuery.textScalerOf`.
- Hardcoded font sizes (`style: TextStyle(fontSize: 16)`) — always use
  `Theme.of(context).textTheme.*`.
- Setting `Semantics(enabled: false)` on a tappable widget — makes it
  invisible to screen readers. Use `ExcludeSemantics` for decorative elements only.

---

## See also

- `.claude/skills/device-matrix/SKILL.md` — textScaler matrix in goldens
- your project's mobile standards doc — tap target and contrast standards
