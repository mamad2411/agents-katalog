---
name: "Interactive Prototype Builder"
version: "1.0.0"
description: "Builds interactive prototypes with real data, navigation flows, and user interactions. Supports rapid iteration from concept to testable prototype."
author: "workspace"
activated: false
---

# Interactive Prototype Builder

Builds interactive prototypes with real data, navigation flows, and user interactions. Supports rapid iteration from concept to testable prototype.

## Decision Framework

### When to Apply
Use when: Rapid prototyping, user testing, concept validation, stakeholder demos

### When NOT to Apply
Don't use when: Production code (refactor after validation)

## Anti-Patterns

### 1. Prototype Becomes Production
Prototypes skip error handling, accessibility, and testing. Always refactor before shipping.

### 2. No Mock Data Strategy
```javascript
// BAD: Hardcoded values everywhere
const user = { name: 'John', email: 'john@example.com' };

// GOOD: Factory functions
const createMockUser = (overrides = {}) => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  ...overrides
});
```


## Trigger Phrases

- "Create prototype"
- "Quick mockup"
- "User testing"
- "Interactive demo"
- "Concept validation"

## Patterns

### Prototype Router
```javascript
const PrototypeApp = ({ screens }) => {
  const [currentScreen, setCurrentScreen] = useState('home');
  const [sharedState, setSharedState] = useState({});

  const Screen = screens[currentScreen];
  return (
    <Screen
      state={sharedState}
      setState={setSharedState}
      navigate={setCurrentScreen}
    />
  );
};
```

## Integration
- Works with: form-pattern-engine, component-lifecycle-manager

