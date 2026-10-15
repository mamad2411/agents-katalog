---
name: inlens
description: Build, integrate, style, review, or debug InLens image magnifiers in React and Next.js. Use this skill whenever a task mentions InLens, @inlens/react, @inlens/next, @inlens/core, an RSC-safe image magnifier, or CSS-owned Lens, Panel, Tracker, and Magnified composition—even when the user has not explicitly asked to use InLens yet.
---

# InLens

Use InLens to create image magnifiers whose structure is server-compatible and whose presentation is
entirely consumer-owned.

## Workflow

1. Inspect the application before editing:
   - Identify React versus Next.js App Router.
   - Detect the package manager and existing InLens package/version.
   - Find the project's CSS convention and the component that owns the source image.
   - Prefer the installed package's types and README when they differ from this skill.
2. Choose the public package:
   - Use `@inlens/react` in React applications.
   - Use `@inlens/next` in Next.js App Router applications.
   - Use `@inlens/core` directly only for a custom runtime that needs the controller or geometry
     primitives without the compound React API.
3. Install with the project's existing package manager when needed.
4. Compose only the parts the design needs. Keep the composition in a Server Component unless the
   surrounding application behavior independently requires a client boundary.
5. Add consumer CSS for every visual decision. InLens deliberately ships no stylesheet.
6. Build and typecheck the affected application. Exercise pointer movement in a browser when browser
   testing is available.

Read [references/contract.md](references/contract.md) before writing or reviewing an InLens composition.
It contains the public component contract, geometry outputs, CSS recipe, and failure conditions.

## Design rules

- Treat `--inlens-*` custom properties as read-only runtime outputs. Never use them as configuration
  inputs or assign them in consumer code.
- Give Root and every rendered Lens or Panel measurable dimensions in CSS. A zero-sized surface remains
  idle by design.
- Let CSS own size, position, shape, overflow, visibility, transform, animation, and presentation.
  Avoid inline layout styles unless the user explicitly prefers inline styling.
- Use `data-inlens-state="idle|active"` to control interactive visibility. Keep the parts mounted.
- Do not add `"use client"` merely because InLens responds to pointers. Root already contains the one
  private client runtime.
- Keep `Image` and `Magnified` children as one consumer-owned React element. InLens renders those
  elements without cloning or modifying them.
- Give the source image meaningful alternative text. Magnified duplicates are normally decorative and
  should use `alt=""`.
- Ensure magnification is an enhancement: never make the Lens or Panel the only way to perceive
  information.
- Put `pointer-events: none` on visual overlays unless the requested interaction intentionally needs
  something else outside InLens.

## Composition choices

- Use Root + Image + Lens + Magnified for an on-image loupe.
- Use Root + Image + Panel + Magnified for an external preview.
- Add Tracker only when a Panel exists in the same initial Root subtree. Tracker represents the first
  owned Panel in DOM order.
- Lens and Panel can coexist. Each needs its own Magnified element.
- Nested Roots are supported; each part belongs to its closest Root.

## Review checklist

Before finishing, verify that:

- the import comes from the framework-appropriate package;
- public InLens components remain on the server side of the application's ownership boundary;
- the source, Lens, Panel, Tracker, and Magnified surface receive all required layout from consumer CSS;
- CSS applies the published translation and zoom variables;
- idle/active visibility does not unmount required parts;
- Tracker is never present without Panel;
- no application code writes reserved variables or relies on removed size, shape, position, or offset
  props;
- source and decorative-image alternative text are appropriate; and
- the affected production build and typecheck pass.
