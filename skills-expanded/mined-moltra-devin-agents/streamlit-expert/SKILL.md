---
name: streamlit-expert
description: Streamlit UI architecture, session state, and performance
argument-hint: "[files or scope]"
agent: streamlit-expert
triggers:
  - user
  - model
allowed-tools:
  - read
  - grep
  - glob
  - exec
permissions:
  allow:
    - Exec(true)
    - Exec(/bin/true)
    - Exec(/usr/bin/true)
    - Exec(cp *)
---
> **Note:** See `CONVENTIONS.md` for the sub-agent contract

Review Streamlit application focusing on:

1. **Session state management**
   - Proper initialization patterns
   - State persistence across reruns
   - State cleanup and memory management
   - Mutable vs. immutable state handling

2. **Caching strategy**
   - Appropriate use of @st.cache_data and @st.cache_resource
   - Cache invalidation patterns
   - Cache key design
   - Memory-efficient caching

3. **Performance optimization**
   - Minimizing unnecessary reruns
   - Efficient data loading
   - Lazy loading patterns
   - Callback function optimization

4. **UI/UX patterns**
   - Component organization
   - User input validation
   - Error handling and user feedback
   - Responsive design considerations

5. **Architecture patterns**
   - Separation of UI and business logic
   - Modular component design
   - Configuration management
   - Deployment readiness

## Review Scope
$ARGUMENTS

If no scope is provided, review Streamlit-related files in the current working directory.

## Common Issues to Check
- Improper session state initialization
- Missing cache decorators on expensive operations
- Unnecessary reruns causing performance issues
- Mutable state in cached functions
- Poor error handling in user interactions

## Output Format
Provide a structured report with:
- File paths and line numbers for each issue
- Severity levels (critical, warning, info)
- Streamlit best practice violations
- Performance improvement recommendations
- Code examples of correct patterns
- Priority-ordered action items
