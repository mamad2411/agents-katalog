// Command: /fix-bug
// Description: Debug and fix issues systematically

You are debugging an issue in OrdnungsHub. Follow this systematic approach:

1. **Reproduce the Issue**
   - Get exact steps to reproduce
   - Identify affected components
   - Check logs for errors
   - Verify in test backend first

2. **Root Cause Analysis**
   - List 5-7 possible causes
   - Narrow down to 1-2 most likely
   - Add targeted logging to confirm
   - Use debugger if needed

3. **Implement Fix**
   - Write failing test that reproduces bug
   - Implement minimal fix
   - Ensure all existing tests pass
   - Add regression test

4. **Validation**
   - Test fix in isolation
   - Test in integrated environment
   - Check for side effects
   - Verify performance impact

Common debugging commands:
```bash
# Test backend for isolation
python test_backend.py

# Check Python errors
python -m pytest tests/ -v --tb=short

# Check JavaScript errors
npm run test -- --verbose

# Live logs
tail -f ordnungshub.log

# Reset state
rm ordnungshub.db && python -c "from src.backend.database import init_db; init_db()"
```

Remember:
- Don't just fix symptoms, fix root causes
- Add tests to prevent regression
- Document the fix for future reference
- Consider if similar bugs exist elsewhere
