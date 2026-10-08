# Development Rules

## Component Philosophy
- We're not building a full UI library - we're providing basic "looks good" UI components
- Fewer options, only options that look good
- Components should be simple and opinionated, not endlessly configurable
- Focus on the finest examples that demonstrate the component well

## Code Quality

### No `(as any)` Casts
**Rule**: If any component is calling `(this.region as any)` or similar casts, the API is wrong and needs to be fixed. `(as any)` is code smell and indicates missing public methods or improper encapsulation.

**Solution**: 
- Add proper public methods to expose needed functionality
- Use `@internal` JSDoc tags for methods that are internal but still need to be accessible to related classes (like `SectionReference`)
- Never use `(as any)` to bypass TypeScript's type system

**Example**:
```typescript
// ❌ BAD
const renderer = (this.region as any).renderer;
region._height -= amount;

// ✅ GOOD
const renderer = this.region.getRenderer();
region.decreaseHeight(amount);
```

