---
name: new-screen
description: Scaffold a new screen using EdgeScaffold + ContentHeader + the persistent-chrome / omnibox-spine conventions. Triggered when adding a new screen / route.
---

# /new-screen — scaffold a screen

## Steps

1. Create `lib/features/<feature>/<name>_screen.dart` with the template
   below
2. Register the route in `lib/app/router.dart` (see `new-route` skill)
3. Wire any navigation into it via `context.push` (never `go` for
   drill-in — see `push-not-go`)
4. Add an `OmniboxEntry` for it in `lib/features/omnibox/omnibox_catalog.dart`
   so users can find it by typing
5. If it's worth a golden test, add `test/golden/<name>_test.dart`
   (see `golden-test` skill)

## Template

```dart
import 'package:differentworld/shared/widgets/content_header.dart';
import 'package:differentworld/shared/widgets/edge_scaffold.dart';
import 'package:differentworld/shared/widgets/empty_state.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class FooScreen extends ConsumerWidget {
  const FooScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Replace with the actual data source — Drift stream provider.
    final dataAsync = ref.watch(/* yourProvider */);

    return EdgeScaffold(
      // Drill-in by default (showBack: true). Set false for home pages
      // where the hamburger should appear in the top-left instead.
      // backFallbackRoute: '/parent',  // only if reachable from a deep link
      actions: const [
        // Screen-level actions go in the top-right glass pill.
        // EdgeScaffold publishes these to routeChromeProvider; AppShell
        // paints them in the persistent chrome layer ABOVE the page
        // transitions.
        // SyncStatusIndicator(),
        // IconButton(icon: Icon(Icons.edit_outlined), onPressed: ...),
      ],
      body: dataAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (_, _) => const EmptyState(
          icon: Icons.error_outline,
          title: 'Could not load',
        ),
        data: (items) {
          if (items.isEmpty) {
            return const EmptyState(
              icon: Icons.inbox_outlined,
              title: 'Nothing here yet',
              message: 'Sentence explaining what would go here and how.',
              // action: FilledButton.icon(...),
            );
          }
          return ListView.builder(
            // No bottom padding for the bar — AppShell already adds
            // 76 dp under widget.child for the persistent omnibox.
            // Add bottom padding here ONLY if you have a FAB stacked
            // ABOVE the bar (rare).
            padding: const EdgeInsets.symmetric(vertical: 8),
            itemCount: items.length + 1,
            itemBuilder: (_, i) {
              if (i == 0) {
                return const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 16),
                  child: ContentHeader(
                    title: 'Foo',
                    subtitle: 'optional',
                  ),
                );
              }
              return /* tile for items[i - 1] */;
            },
          );
        },
      ),
      // floatingActionButton: FloatingActionButton.extended(...),
      // ↑ Avoid if possible. The right pattern is PrimaryActionButton
      // in EdgeScaffold.actions; FABs occupy the same thumb-zone as
      // the omnibox bar.
    );
  }
}
```

## What you get for free from AppShell

- **Bottom omnibox composer bar** — already there, sits above the
  keyboard, auto-hidden in kid mode.
- **Top-left chrome** — back arrow (when `showBack: true`) or
  hamburger (when `showBack: false` + signed in). Both stay anchored
  during route transitions.
- **Top-right action pill** — fed from `EdgeScaffold.actions`.
- **76 dp bottom inset** on widget.child so content doesn't render
  under the omnibox bar.

## Checklist for new screens

- [ ] Uses `EdgeScaffold`, not raw `Scaffold + AppBar`
- [ ] Title via `ContentHeader` inside scrollable content
- [ ] All four UX states (loading / empty / error / data)
- [ ] No manual 76 dp bottom padding — AppShell adds it
- [ ] All drill-in nav uses `context.push`
- [ ] Haptic feedback on primary taps
- [ ] List uses `ListView.builder` for variable-length lists
- [ ] OmniboxEntry added so the screen is discoverable
- [ ] (Optional) golden test added — see `golden-test`
