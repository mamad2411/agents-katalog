---
name: checkin-validator
description: "Validates honesty of /sprint:checkin claims by cross-checking against tool history. Detects fake claims (claiming step done without evidence), fake tests (assertions don't match test cases), and circular mocks. Used after each /sprint:checkin invocation."
---

# Checkin Validator

Проверяет искренность checkin'ов - не врёт ли executor.

## Когда применять

- После каждого `/sprint:checkin`
- Сразу как только checkin invoked
- Output: WARNING (не BLOCK) если checkin looks dishonest

## Why warn, not block

LLM agents не perfectly реliable judges. False positive blocks из-за heuristics будут frustrating. So:
- WARN executor and user
- Log в `.sprints/active/honesty-warnings.log`
- SE reviewer learns about warnings и applies extra scrutiny

В extreme cases (clearly dishonest): SE reviewer может flag и trigger sprint review.

## Honesty checks

### Check 1: Action vs claim alignment

Compare checkin claim against recent tool history:

```python
def check_alignment(checkin_text, recent_tool_calls):
    keywords_in_checkin = extract_action_keywords(checkin_text)
    # e.g., "wrote test", "ran pydeps", "edited config"
    
    keywords_in_tools = extract_actions_from_tools(recent_tool_calls)
    # e.g., ['Write tests/test_auth.py', 'Bash pydeps src/']
    
    if keywords_in_checkin not_supported_by keywords_in_tools:
        return WARNING("Checkin claims X but tool history shows Y")
```

**Examples**:

WARN case:
```
Checkin: "Wrote test for user authentication"
Tool history (last 5 min): 
  - Edit src/auth.py
  - Bash python -c "..."
  - Read tests/test_auth.py

Warning: "Wrote test" claimed but no Edit/Write to test files. 
Last test file action was Read, not Write.
```

OK case:
```
Checkin: "Wrote test for user authentication"
Tool history:
  - Edit tests/test_auth.py (added test_user_login_success function)
  - Bash pytest tests/test_auth.py

✓ Aligned: test file modified, test runner invoked.
```

### Check 2: Evidence claims

If checkin uses `--evidence=<file>`:

```python
def check_evidence(evidence_path):
    if not file_exists(evidence_path):
        return WARNING(f"Evidence file does not exist: {evidence_path}")
    if file_size(evidence_path) == 0:
        return WARNING(f"Evidence file is empty: {evidence_path}")
    if was_modified_recently(evidence_path, within_minutes=5):
        return OK
    else:
        return WARNING(f"Evidence file not modified recently. "
                       f"Last modification: {get_mtime(evidence_path)}")
```

### Check 3: Test claims with no test execution

If checkin claims "test passing" or "tests pass":

```python
def check_test_claim(checkin_text, recent_tool_calls):
    if 'test' in checkin_text.lower() and 'pass' in checkin_text.lower():
        recent_test_runs = find_test_runs(recent_tool_calls)
        if not recent_test_runs:
            return WARNING("Test pass claimed but no test runner invoked recently")
        
        # Check exit codes
        for test_run in recent_test_runs:
            if test_run.exit_code != 0:
                return WARNING(f"Test pass claimed but recent test run "
                               f"{test_run.command} returned exit code {test_run.exit_code}")
        
        return OK
```

### Check 4: Fake test detection (heuristic)

If checkin like "wrote test for X" - read the new/modified test:

```python
def detect_fake_test_patterns(test_content):
    flags = []
    
    # Pattern 1: assert True / assert 1 == 1
    if re.search(r'assert\s+(True|1\s*==\s*1)\b', test_content):
        flags.append("Test contains trivial 'assert True' - likely fake")
    
    # Pattern 2: empty test body
    if re.search(r'def test_\w+\([^)]*\):\s*pass\s*$', test_content, re.MULTILINE):
        flags.append("Test body is just 'pass' - empty test")
    
    # Pattern 3: only setup, no asserts
    if has_test_func_without_assert(test_content):
        flags.append("Test function has no assertions")
    
    # Pattern 4: mock returns X, asserts X
    # mock_func.return_value = 42
    # assert mock_func() == 42  <- circular
    if has_circular_mock(test_content):
        flags.append("Possibly circular mock - mocks return value, asserts the return value")
    
    return flags
```

These are **heuristics**, не perfect. WARN, не block.

### Check 5: Time tracking sanity

```python
def check_time_sanity(checkin):
    last_checkin = get_last_checkin()
    elapsed = checkin.timestamp - last_checkin.timestamp
    
    if elapsed < timedelta(seconds=10):
        return WARNING("Checkins too rapid - possible burst without actual work")
    
    if elapsed > timedelta(hours=1):
        return WARNING(f"Long gap since last checkin ({elapsed}). "
                       f"Either long work without intermediate checkins "
                       f"(should split) or session paused.")
    
    return OK
```

## Workflow

After `/sprint:checkin "<step text>"`:

### 1. Read context

- Last 5-10 tool calls from `tool-history.log`
- Current active task
- Recent file modifications

### 2. Run all checks

```python
warnings = []
warnings.extend(check_alignment(checkin_text, recent_tools))
warnings.extend(check_evidence(checkin.evidence) if checkin.evidence else [])
warnings.extend(check_test_claim(checkin_text, recent_tools))

# Fake test detection only if "wrote test" type claim
if is_test_writing_checkin(checkin_text):
    test_files = get_recently_modified_test_files()
    for test_file in test_files:
        warnings.extend(detect_fake_test_patterns(read(test_file)))

warnings.extend(check_time_sanity(checkin))
```

### 3. Output

If warnings:
- Log to `.sprints/active/honesty-warnings.log`
- Display to user (and executor) with specific concerns
- Не block work continues

```
Honesty check warnings for checkin "Wrote test for password hashing":

⚠ Test contains 'assert True' pattern in tests/test_auth.py:42
  Suggestion: Replace with actual assertion checking the bcrypt hash format

⚠ No test runner invocation in recent tool history
  Suggestion: Run pytest to verify test actually works

(These are heuristic warnings, не blocking. SE reviewer will review tests later.)
```

If no warnings:
- Silent (don't spam OK messages)
- Internal log "checkin verified" for audit

### 4. SE review handoff

All warnings accumulate в honesty-warnings.log. When SE review runs:
- Review reads warnings
- Pays extra attention to flagged areas
- Validates manually

## Output

`.sprints/active/honesty-warnings.log` (append mode)
- Per warning: timestamp, task, checkin text, warning details

`.sprints/active/_state.json`:
- `honesty_warnings_count: N`
- Used for retrospective metrics

## False positives

Heuristics can be wrong:
- Test framework with unusual structure → looks like missing asserts
- Generated tests → fake pattern false positive
- Tool history can be incomplete (some tools don't log)

So: warnings, not blocks. Executor can ignore false positives.

If pattern persistent (same task multiple warnings):
- SE reviewer escalates
- Possible block via SE review FAIL verdict

## Limitations (honest acknowledgment)

This skill **cannot** detect:
- Sophisticated fake tests that look real
- Subtle assertion mismatches  
- Circular logic disguised in helper functions
- Tests that test wrong scenario

For those: layered defense через SE review (with extended test review prompt) and optional mutation testing.

This skill: best-effort heuristic detection, structural checks.
