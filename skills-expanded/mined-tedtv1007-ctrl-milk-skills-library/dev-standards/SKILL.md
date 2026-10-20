# Development Standards & Quality Assurance
Description: Enforce high-quality development standards including Unit Tests and Component Security. E2E Tests are optional.

## 1. Workflow
Every feature implementation must follow this cycle:
1.  **Code**: Implement the feature.
2.  **Build**: Verify compilation (`dotnet build`).
3.  **Unit Test**: 
    -   Write unit tests for new Controllers/Services.
    -   Run `dotnet test` to ensure all pass.
4.  **Security Scan**:
    -   Run `dotnet list package --vulnerable`.
    -   Update any packages with known vulnerabilities.
5.  **E2E Test (Optional)**:
    -   **Run ONLY when explicitly requested.**
    -   May cause system instability if run automatically.

## 2. Checklist
- [ ] Code compiles without warnings/errors?
- [ ] Unit tests cover happy/sad paths?
- [ ] No vulnerable packages introduced?

## 3. Commands
-   **Build**: `dotnet build`
-   **Unit Test**: `dotnet test`
-   **Security**: `dotnet list package --vulnerable`
