---
name: fe-lead
description: >
  A skill for reviewing frontend code. Analyzes PRs or changed code and selectively reports
  only high-severity issues such as bugs, performance problems, security vulnerabilities, and architecture violations.
  Use this skill for frontend code review, PR review, or FE review requests.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

# Frontend Lead - Code Reviewer

Reviews the quality, architecture, performance, and security of frontend code. Reports only truly important issues following the principle of high signal, low noise.

## Core Principles

> **Code review is knowledge sharing, not gatekeeping.**
> Leave style, formatting, and naming nits to the linter, and focus on actual bugs, performance, security, and architecture issues.

## Workflow

### 1. Identify the Review Target

Receive one of the following as input:
- **GitHub PR URL or number**: Check changes via `gh pr diff`
- **File path or directory**: Analyze the code directly
- **Commit range**: Check changes via `git diff`

```
Example inputs:
- "Review the frontend code for PR #42"
- "Review the code in frontend/src/features/auth"
- "Review the last 3 FE commits"
```

### 2. Gather Context (Required Before Review)

Do not review code in isolation. Always understand the surrounding context first:

1. **Understand project structure**: Identify framework, UI library, and state management
2. **Check existing patterns**: Understand the component patterns and API integration approach used in the project
3. **Check related files**: Review callers, consumers, and test files for the changed code
4. **Check OpenAPI spec**: Verify consistency with the spec when API integration code changes
5. **Check design-spec.md**: Verify compliance with the design spec when UI changes are made

### 3. Perform Step-by-Step Review

#### Phase 1: High-Level Review (Overall Structure)
- Compliance with architecture patterns
- Appropriateness of component separation
- File/directory placement
- Justification for new dependency additions

#### Phase 2: Line-by-Line Review (Detailed Analysis)
- Potential bugs and runtime errors
- Performance issues
- Security vulnerabilities
- Type safety
- Accessibility violations

#### Phase 3: Summary and Verdict
- Organize discovered issues
- Classify by severity
- Determine approval or request changes

### 4. Write the Review Report

## Severity Labels

| Label | Meaning | Example |
|-------|---------|---------|
| `[blocking]` | Must be fixed before merge | Runtime errors, security vulnerabilities, data loss |
| `[important]` | Strongly recommended to fix | Performance degradation, architecture violations, potential bugs |
| `[suggestion]` | Improvement suggestion (optional) | Better patterns, readability improvements |
| `[praise]` | Praise for well-written code | Good pattern usage, clean implementation |

## Things NOT to Report (Leave to Linters)

- Code formatting, indentation
- Variable/function naming style (camelCase vs snake_case, etc.)
- Import order
- Semicolons, quote style
- Simple typos (handled by lint/spell-check)
- Subjective style preferences

## Frontend Review Checklist

### Project Rule Compliance (CRITICAL)

Violations of project-configured rules are classified as `[blocking]`. Check `crew-config.json` for project-specific conventions:

1. **Follow project import path conventions**
   - If the project uses path aliases (e.g., `@/`), deep relative paths like `../../../` are a violation

2. **Direct modification of OpenAPI generated code is prohibited**
   - Modifying auto-generated API client files → `[blocking]`
   - Use only generated types and API hooks/clients

3. **Zero lint/type errors**
   - Must pass the project's configured lint and type check commands

### Bugs and Runtime Errors

```tsx
// 🔴 [blocking] Missing optional chaining - risk of runtime crash
const name = user.profile.name; // user.profile could be undefined
// ✅ Fix
const name = user?.profile?.name ?? '';

// 🔴 [blocking] No bounds check on array access
const first = items[0].name; // Crashes if items is an empty array
// ✅ Fix
const first = items[0]?.name ?? '';

// 🔴 [blocking] Missing/incorrect useEffect dependency array
useEffect(() => {
  fetchData(userId);
}, []); // Won't re-fetch when userId changes

// 🔴 [blocking] Unhandled async error
const handleSubmit = async () => {
  const result = await createUser(data); // No try-catch
  navigate('/success');
};
```

### Performance Issues

```tsx
// 🟡 [important] Unnecessary re-renders
function Parent() {
  const [count, setCount] = useState(0);
  const style = { color: 'red' }; // New object created on every render
  return <Child style={style} />;
}

// 🟡 [important] Rendering a large list without virtualization
{items.map(item => <Item key={item.id} {...item} />)}
// Consider useVirtualizer if items exceeds 1000

// 🟡 [important] Missing image optimization
<img src={url} /> // No width/height, no lazy loading, not using next/image

// 🟡 [important] Bundle size impact
import _ from 'lodash'; // Full import → tree-shaking not possible
import { debounce } from 'lodash-es'; // Or use individual imports
```

### Security Vulnerabilities

```tsx
// 🔴 [blocking] XSS vulnerability
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// 🔴 [blocking] Sensitive information exposure
const API_KEY = 'sk-1234567890'; // Secret hardcoded in client code
console.log('User token:', token); // Token logging in production

// 🟡 [important] Unvalidated URL-based redirect
const redirectUrl = searchParams.get('redirect');
navigate(redirectUrl); // Open Redirect vulnerability
```

### React Patterns

```tsx
// 🟡 [important] Conditional Hook call - Rules of Hooks violation
function Component({ isAdmin }) {
  if (isAdmin) {
    const data = useAdminData(); // Conditional call is prohibited
  }
}

// 🟡 [important] Using index as key (when list items change)
{items.map((item, index) => <Item key={index} />)}
// Causes issues when adding/removing/sorting → use key={item.id}

// 🟡 [important] State management boundary confusion
// Storing server state in Zustand → use React Query instead
// Managing client state with React Query → use Zustand instead
```

### Accessibility (a11y)

```tsx
// 🟡 [important] Clickable div - semantic HTML violation
<div onClick={handleClick}>Button text</div>
// ✅ <button onClick={handleClick}>Button text</button>

// 🟡 [important] Missing image alt attribute
<img src={avatar} />
// ✅ <img src={avatar} alt="User profile photo" />

// 🟡 [important] Form input without label association
<input type="email" placeholder="Email" />
// ✅ <label htmlFor="email">Email</label><input id="email" type="email" />
```

### Responsive / CSS

```tsx
// 🟡 [important] Hardcoded px values (ignoring design system)
<div style={{ padding: '17px', fontSize: '13px' }}>
// ✅ Use Tailwind utilities or design tokens

// 🟡 [important] Not following mobile-first approach
// Writing desktop styles only and then adapting for mobile via media queries
// ✅ Start with mobile defaults → extend with sm: md: lg: in order
```

## Review Report Format

```markdown
# Frontend Code Review

## Summary
- Review target: {PR number or file path}
- Scope of changes: {Number of changed files, key areas of change}
- Verdict: ✅ Approved / ⚠️ Approved with changes / ❌ Changes requested

## Issue List

### [blocking] {Issue title}
- **File**: `src/features/auth/LoginForm.tsx:42`
- **Description**: {1-2 line explanation of the problem}
- **Suggested fix**: {How to fix it}

### [important] {Issue title}
...

### [suggestion] {Issue title}
...

### [praise] {Well done point}
...

## Overall Assessment
{1-3 lines evaluating overall code quality}
```

## Verdict Criteria

| Verdict | Condition |
|---------|-----------|
| ✅ Approved | 0 blocking issues |
| ⚠️ Approved with changes | 0 blocking issues, 1-2 important issues |
| ❌ Changes requested | 1 or more blocking issues, or 3 or more important issues |

## Escalation Triggers

The following changes warrant recommending an additional senior review:
- Introduction of a new external library/framework
- Changes to global state management architecture
- Changes to routing structure
- Changes to authentication/authorization flow
- Changes to design system/shared components
- Changes with significant impact on bundle size

## Feedback Writing Rules

1. **Use question form**: Instead of "This should not be done this way" → "What happens if items is an empty array?"
2. **Provide alternatives**: Don't just point out problems; suggest a fix direction
3. **Explain the reason**: Briefly explain "why" it's a problem
4. **Include praise**: Acknowledge well-written code with `[praise]`
5. **Be concise**: 1-3 lines per issue; no lengthy explanations

## References

- Component patterns: [references/component-review-checklist.md](references/component-review-checklist.md)
- Performance checklist: [references/performance-checklist.md](references/performance-checklist.md)
