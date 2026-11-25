# Global Project Rules: AbrechozeiraApp

This project follows strict guidelines for Architecture, Frontend Design, and Angular development.

## 🏛️ Architecture & Decision Making
- **Simplicity First**: Start simple and add complexity only when proven necessary.
- **Trade-offs**: Every significant architectural decision must have a documented rationale or ADR.
- **Requirements Driven**: Architecture must be driven by requirements and identified constraints.

## 🎨 Frontend Design & Aesthetics
- **Intentional Aesthetics**: Avoid generic layout patterns. Every interface must have a clear aesthetic stance (e.g., luxury minimal, industrial utilitarian).
- **Typography & Color**: Use CSS variables exclusively. Avoid system defaults like Inter or Roboto for display elements.
- **Visual Memorability**: Every page should have at least one memorable design element.
- **Cohesive Restraint**: No random decoration; every flouris must serve the aesthetic thesis.

## 🅰️ Angular Development (v20+)
- **Modern Patterns**: Use Signals for fine-grained reactivity and local state. Use Standalone components exclusively.
- **Dependency Injection**: Favor the `inject()` function over constructor injection for cleaner, more modular code.
- **Change Detection**: Use `ChangeDetectionStrategy.OnPush` combined with Signals to optimize performance.
- **Reactive Forms**: Implement forms with proper validation and loading state feedback.

## 🏗️ UI Patterns
- **Loading States**: Show loading/skeleton indicators ONLY when there is no data to display.
- **Error Handling**: Never swallow errors. Always surface failures to the user via UI components (toasts, error screens).
- **Control Flow**: Use modern `@if`, `@for`, and `@defer` syntax for conditional rendering and performance optimization.
- **Button States**: Always disable triggers during async operations and show visual feedback (spinners).

---

> [!NOTE]
> These rules are derived from the following project skills:
> - `@frontend-design`
> - `@architecture`
> - `@angular`
> - `@angular-ui-patterns`
