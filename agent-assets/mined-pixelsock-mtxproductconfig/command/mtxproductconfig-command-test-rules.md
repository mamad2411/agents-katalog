---
name: test-rules
description: Test dynamic rules engine with validation scenarios
---

Execute comprehensive testing of the dynamic rules engine to ensure business logic correctness.

This command will:
1. Load and validate all rules from the Supabase rules table
2. Test rule priority and execution order
3. Validate if_this condition matching
4. Verify then_that action application
5. Test edge cases and error scenarios
6. Generate rule coverage report

Perfect for:
- After adding new rules to the database
- Before deploying configuration changes
- When debugging rule conflicts
- During QA validation cycles

Usage: `/test-rules [scope]`
       `/test-rules` (full test suite)
       `/test-rules priority` (priority conflicts only)
       `/test-rules coverage` (coverage report only)