---
name: swiftui-native-component-design
description: Use when creating, designing, reviewing, or refactoring a reusable/custom SwiftUI view or component — especially one meant for a design-system module, a shared UI package, or anywhere multiple screens will call into it. Trigger on requests like "build a custom SwiftUI button/toggle/card/rating/badge component", "design an API for this view", "make this view reusable", "how should I structure this SwiftUI component's initializer", "add a custom style like ButtonStyle for my component", "review this SwiftUI component's API", or any request to make a SwiftUI view feel more "native" or consistent with Apple's own components. Also trigger when the user is deciding between a plain modifier, an environment value, and a custom ViewStyle for customizing a component — this skill has the decision process and ready-to-adapt code templates for all three. Do not wait for the user to say "design system" explicitly; any custom SwiftUI View intended for reuse across call sites qualifies.
---

# Designing Native-Feeling Reusable SwiftUI Views

## Why this matters

A custom SwiftUI component competes with Apple's own views for a developer's attention. When its API shape, naming, data flow, and customization story mirror system components (`Button`, `Label`, `ContentUnavailableView`, `ButtonStyle`), developers reuse the muscle memory they already have instead of learning something bespoke. That lowers the barrier to adoption and keeps a codebase's component surface coherent. This skill packages a design process — and copy-adaptable Swift code templates — for getting there.

Apply this process any time you are about to write (or review) a SwiftUI `View` meant to be called from more than one place. Work through it in order; each stage's decisions constrain the next one. Don't jump straight to typing an `init` — the API falls out naturally once the semantics and data flow are settled, and skipping ahead is exactly how you end up with a pile of boolean flags that need walking back later.

## Step 1 — Classify the component

Ask: does this component describe a **concept** (semantic), or does it already imply a **specific visual form** (prescriptive)?

- **Semantic** — like `Button` or `Toggle`. It represents an idea ("this can be tapped to perform an action", "this represents an enabled/disabled state") with no inherent look. A `Rating` control (pick a value in a range) is semantic: it could render as stars, a numeric readout, or a slider.
- **Prescriptive** — like a `BarChart` or a `Tag`/badge. Its visual form is part of what it *is*; customizing it means adjusting details (color, size), not swapping out its entire representation.

This classification is the fork in the road for Step 4 (customization): semantic components generally deserve a full custom-style protocol (like `ButtonStyle`); prescriptive components generally just need a few environment-value hooks. Don't build a whole style system for something whose shape will never change, and don't limit a genuinely semantic component to a couple of environment knobs.

If you're unsure, ask the user directly — the answer is usually obvious to whoever owns the design intent, and guessing wrong here means redoing Step 4 later.

## Step 2 — Model the semantics before the appearance

Before writing any view code, pin down what the component *represents* and which states are valid:

- Can the value be absent/empty? Are fractional or continuous values allowed, or only discrete ones? Does a range have a fixed lower bound? Can it be read-only/disabled?
- Make invalid states unrepresentable. If several values must always travel together or satisfy an invariant, introduce a dedicated model type instead of several loosely related parameters.
- Prefer a narrow, well-defined API to a falsely flexible one. An API that only supports whole-number values 1–5 and says so is better than one that silently misbehaves for other inputs.
- Name things the way Apple names things: `selection`, `value`, `label`, `content`, `isPresented`. Reusing this vocabulary means the *meaning* transfers, not just the word.

## Step 3 — Follow SwiftUI's data-flow and interaction conventions

- **Immutable input** for values the component only reads.
- **`Binding`** when the component mutates state the *caller* owns — a binding is a promise that data flows back out, not just a convenient way to pass a value in.
- **Internal `@State`** only for state the component itself owns. Keep this separate from the component's public semantic state — e.g. a star being currently pressed/hovered/animating is transient visual state and should stay internal (or flow through a style's configuration), while the selected rating is public API.
- Prefer **composition over flag proliferation**. Parameters like `showsIcon`, `isCompact`, `usesBorder` combine combinatorially into unclear states. Dedicated initializers, child-view slots (`@ViewBuilder`), modifiers, and styles scale better and give you **progressive disclosure**: a short, obvious call site for the common case, with specialized use cases still reachable.
- Keep the component's own type declaration scannable. When a component needs a small supporting type — an enum of variants, a `Status`-like case set, a nested configuration struct — define it in its own `extension` next to the component rather than inline inside the struct body. Someone skimming the type should find its stored properties, `init`, and `body` without wading through unrelated declarations first.
- Prefer real controls over raw gestures. A `Button` participates in keyboard interaction, focus, `disabled` state, and accessibility for free — `onTapGesture` does not. Reach for the system control whenever an interaction matches one.
- Accessibility is part of the component's API, not an afterthought applied to whatever the final layout happens to produce. Expose an appropriate label, value, role, and actions (e.g. an adjustable action for a value-picking control) so assistive technology doesn't have to reconstruct meaning from rendered children.
- Respect the environment values that affect this component's semantics or presentation — commonly `isEnabled`, `controlSize`, `dynamicTypeSize`, `layoutDirection`, `tint`, `accessibilityReduceMotion`, `accessibilityDifferentiateWithoutColor`. Don't cargo-cult all of them — read the ones that actually matter for what this component does.
- Define precedence and stick to it. A common, predictable rule: an explicit modifier at the call site overrides an environment default; a style is responsible for its own visual details. Whatever you choose, apply it consistently so behavior doesn't surprise callers.
- Preserve view identity — avoid unnecessary type erasure (`AnyView`) and large structural changes, since SwiftUI uses identity to retain state and drive animations/transitions correctly. Type erasure is a legitimate tool at a *deliberate, local* boundary (see Step 4's style resolution pattern) — it shouldn't be the default way you plug two pieces together.
- For components with a public/module API, remember initializers, generic constraints, defaults, and overloads become hard to change once other code depends on them — decide extension points deliberately rather than postponing that decision.
- Plan to preview/test the component across its meaningful states, both color schemes, a couple of Dynamic Type sizes, layout direction, and localization. This routinely surfaces API assumptions before they calcify.

## Step 4 — Design the initializer

Read `references/initializers.md` for full worked examples (a `Card` container view and a `Tag` leaf view) — adapt the *pattern*, not the exact type/parameter names, to what the user is building.

The short version:

- **Container views** (accept child `View`s): start with the most flexible initializer — `@ViewBuilder` slots for every child-view region, e.g. `header`/`content`. Then layer *focused* convenience initializers as constrained extensions (`extension Card where Header == Image`) for common shapes, without narrowing the general-purpose base initializer. `ContentUnavailableView` is a good system reference for this pattern.
- **Leaf/non-container views**: keep the initializer as short as the common case allows, and mirror an analogous system view's argument order and labels (e.g. a `Tag(_:systemImage:)` mirroring `Label(_:systemImage:)`). Prefer `LocalizedStringResource` over `String` for user-visible text (gets String Catalog support for free), and `ImageResource` over an asset-name string for type-safe image lookups. Use `Binding` whenever the view mutates data passed into it.

## Step 5 — Design the customization API

This is where Step 1's classification pays off.

- **Semantic component needing fundamentally different visual representations** → build a custom view style, following the shape of `ButtonStyle`/`LabelStyle`. Read `references/view-styles.md` for the full pattern (configuration struct, `DynamicProperty`-conforming style protocol, resolver view, `@Entry` environment registration, `View` modifier, static factory extensions like `.star`/`.numeric`) worked through a complete `Rating`/`RatingStyle` example — adapt names to the component at hand.
- **Prescriptive component needing only focused appearance adjustments** → add one or more `@Entry` environment values (often typed as a broad protocol like `ShapeStyle` rather than a concrete type, so callers can pass a `Color`, gradient, or material interchangeably), a `View` extension setter modifier, and a sensible internal fallback when unset. Read `references/environment-customization.md` for the full pattern worked through a `Tag`/`tagBackgroundStyle` example.

Don't build the style-protocol machinery for a component that's actually prescriptive — it's a lot of ceremony (configuration type, `DynamicProperty` resolver, environment registration) for something that will only ever need a couple of environment knobs. Conversely, don't limit a genuinely semantic component to environment values only — callers won't be able to swap in a fundamentally different visual representation without forking the component.

## Applying this as a review checklist

When reviewing an existing component instead of designing a new one, walk the same five steps as questions:

- Is this semantic or prescriptive — and does its current customization approach (style vs. environment vs. neither) match that?
- Are invalid states representable? Is the naming aligned with Apple's vocabulary?
- Is `Binding` used only where the component mutates caller-owned state? Is transient visual state kept out of the public API? Are there boolean flags that should be initializers, slots, or styles instead?
- Does it use real controls where one exists? Does it expose accessibility label/value/role/actions? Does it read the environment values relevant to its behavior?
- Is precedence between defaults/environment/modifiers/styles defined and consistent? Is `AnyView` used only at deliberate boundaries?
- Does the initializer follow the container/leaf pattern from Step 4, with a flexible base and focused convenience overloads?

Call out concrete file/line findings the same way you would for any other code review — this checklist is a lens, not a replacement for reading the component's actual code.

## Reference files

- `references/initializers.md` — container view (`Card`) and leaf view (`Tag`) initializer patterns, with the `ContentUnavailableView` system reference.
- `references/view-styles.md` — full custom `ViewStyle`-protocol pattern (`RatingStyleConfiguration`, `RatingStyle`, resolver view, `@Entry`, static factories) for semantic components.
- `references/environment-customization.md` — environment-value customization pattern (`tagBackgroundStyle`) for prescriptive components.

Load the relevant reference file(s) once you know which patterns apply — don't load all three for a component that only needs the leaf-view initializer pattern, for instance.
