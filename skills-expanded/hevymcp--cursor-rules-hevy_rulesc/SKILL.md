# Cursor Rule: hevy-mcp Integration Test Best Practices

1. **Always re-run relevant tests after making any change to a test file.**
   - This ensures that changes are immediately validated and no regressions are introduced.

2. **When fixing or updating integration tests:**
   - Use the correct method signatures and argument types for SDK/client calls.
   - Add or update Zod schema validation for API responses to ensure type safety and contract adherence.
   - Remove any debug or console.log statements before finalizing changes, unless explicitly requested otherwise.

3. **When adding new tests or updating existing ones:**
   - Prefer validating response data with Zod schemas that match the expected output structure.
   - Ensure all test assertions are meaningful and reflect the actual API contract.

4. **If a test fails:**
   - Add temporary debug output (e.g., console.log) only as needed to diagnose the issue, and remove it once resolved.
   - Investigate the actual response structure before updating assertions or schemas.

5. **Keep integration tests clean and production-ready:**
   - No unnecessary debug output.
   - All code should be idiomatic, concise, and maintainable. 