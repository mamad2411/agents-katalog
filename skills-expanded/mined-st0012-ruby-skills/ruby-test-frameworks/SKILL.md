---
name: ruby-test-frameworks
description: Use when writing or running tests in a Ruby project that uses minitest or test-unit. These frameworks have deceptively similar APIs with critical naming differences that cause NoMethodError at runtime. Consult this before writing assertions, running specific tests, or using setup/teardown lifecycle methods.
---

# Minitest vs Test-Unit Divergences

Only covers where minitest and test-unit diverge. If something isn't listed here, it works the same in both.

## Assertion Naming Mismatches

Using the wrong name causes `NoMethodError`.

| Concept | minitest | test-unit |
|---------|----------|-----------|
| Exception | `assert_raises` (plural) | `assert_raise` (singular) |
| Throw | `assert_throws` (plural) | `assert_throw` (singular) |
| Collection inclusion | `assert_includes` (plural) | `assert_include` (singular) |
| Path exists | `assert_path_exists` (with s) | `assert_path_exist` (no s) |
| Negation pattern | `refute_*` (e.g. `refute_nil`) | `assert_not_*` (e.g. `assert_not_nil`) |

test-unit aliases minitest names (`assert_raises`, `refute_*`, etc.), so minitest syntax works in test-unit but **not** vice versa.

## Assertions That Only Exist in One Framework

### test-unit only

| Method | Purpose |
|--------|---------|
| `assert_nothing_raised` | Passes if block doesn't raise (also added by Rails on top of minitest) |
| `assert_true` / `assert_false` | Checks for exactly `true` or `false` (not just truthy/falsy) |
| `assert_boolean` | Checks value is `true` or `false` |
| `assert_compare` | For `<`, `<=`, `>`, `>=` comparisons |
| `assert_raise_with_message` | Checks both exception class and message |
| `assert_raise_message` | Checks exception message only (any class) |
| `assert_raise_kind_of` | Checks exception via `kind_of?` instead of exact class |
| `assert_const_defined` / `assert_not_const_defined` | Check constant existence |
| `assert_alias_method` | Verify method aliasing |
| `assert_nothing_thrown` | Passes if block doesn't call `throw` |
| `assert_block` | Passes if block returns truthy |

### minitest only

| Method | Purpose |
|--------|---------|
| `assert_pattern` / `refute_pattern` | Ruby 3+ pattern matching (`in` expressions) |
| `assert_silent` | Passes if block produces no stdout/stderr |
| `assert_output` | Check stdout/stderr content |
| `capture_io` / `capture_subprocess_io` | Capture output for inspection |
| `skip_until(y, m, d, msg)` | Skip until a date, then fail as reminder |
| `fail_after(y, m, d, msg)` | Pass until a date, then fail as reminder |

### minitest 6 breaking change

`assert_equal(nil, value)` is a hard failure in minitest 6. Use `assert_nil(value)` instead. test-unit has no such restriction.

## Test Selection (CLI Flags)

| Operation | minitest | test-unit |
|-----------|----------|-----------|
| By name (exact) | `-n test_method_name` | `--name test_method_name` |
| By name (regex) | `-n /pattern/` | `--name "/pattern/"` |
| By name (rake) | `N=/pattern/ rake test` | N/A |
| By line number | `m test/file.rb:42` or `minitest test/file.rb:42` (v6) | `--location path.rb:LINE` |
| By line (Rails) | `bin/rails test test/file.rb:42` | N/A |
| Exclude by name | `-e /pattern/` | `--ignore-name /pattern/` |
| Exclude by class | N/A | `--ignore-testcase /pattern/` |
| Filter by class | N/A (use `-n /ClassName#/`) | `--testcase ClassName` |
| Filter by attribute | N/A | `--attribute "speed == :slow"` |
| Seed | `-s SEED` or `--seed SEED` | N/A (use `--order random`) |
| Stop on failure | N/A | `--stop-on-failure` |
| Execution order | Random by default | `--order alphabetic / random / defined` |
| Color | `-p` (pride) | `--color-scheme SCHEME` |

minitest 6 renamed `-n` to `-i` (`--include`). `-n` still works as an alias but is planned for removal.

### Rails-specific flags (minitest underneath)

`bin/rails test` adds: `-b` (full backtrace), `-f` (fail-fast), `-d` (defer output), `--profile [N]` (slowest tests).

## Lifecycle Differences

### minitest

```
before_setup    (for frameworks like Rails)
  setup         (for test authors)
    after_setup
      [TEST]
    before_teardown
  teardown
after_teardown
```

No class-level hooks. No `cleanup`. For `before(:all)` / `after(:all)`, use the `minitest-hooks` gem.

### test-unit

```
startup           (class method, once before all tests)
  setup           (instance, before each test)
    [TEST]
  cleanup         (instance, only if test didn't raise)
  teardown        (instance, always runs, even if cleanup raised)
shutdown          (class method, once after all tests)
```

`startup`/`shutdown` have no minitest equivalent. `cleanup` runs after a passing test but before it's marked as passed — use it for verification like mock expectations. `teardown` always runs regardless of outcome — use it for resource release.

test-unit also supports registering multiple setup/teardown methods by symbol:

```ruby
setup :prepare_database, :prepare_cache
```

## Skip / Pending / Omit

| Concept | minitest | test-unit |
|---------|----------|-----------|
| Skip a test | `skip("reason")` | `omit("reason")` or `pend("reason")` |
| Conditional skip | `skip("reason") if condition` | `omit("reason") if condition` or `omit_if(condition, "reason")` / `omit_unless(condition, "reason")` |
| Output character | `S` | `O` (omit) or `P` (pend) |

**Critical difference**: test-unit's `pend` with a block **fails if the block passes**. This catches code that was fixed but still marked pending. minitest's `skip` is always unconditional.

```ruby
# test-unit: this FAILS if the bug gets fixed
pend("Bug #123") do
  assert_equal(42, buggy_method)  # if this passes, test fails
end

# minitest: no equivalent behavior
skip("Bug #123")  # always skips, no block form
```

## Output Format

| Aspect | minitest | test-unit |
|--------|----------|-----------|
| Progress | `.FES` | `.FEOPN` (adds Omit, Pending, Notification) |
| Summary | `N runs, N assertions, N failures, N errors, N skips` | `N tests, N assertions, N failures, N errors, N pendings, N omissions, N notifications` |
| Throughput | `runs/s, assertions/s` | `tests/s, assertions/s` |

## test-unit Exclusive Features

These have no minitest equivalent:

- **Data-driven tests**: `data("label", value)` method generates parameterized test runs
- **Priority system**: `priority :must` / `:important` / `:high` / `:normal` / `:low` / `:never` with probabilistic execution
- **Attributes**: Generic metadata on test methods, filterable via `--attribute`
- **`sub_test_case`**: Named nested test groups (minitest uses `describe` blocks in Spec mode)
- **`notify`**: Non-fatal informational messages shown as `N` in output
- **Test runners**: Console, Emacs, XML (minitest only has console with plugin system)
- **Config file**: `~/.test-unit.yml` for persistent settings

## Rails Context

Rails uses minitest, not test-unit. But Rails adds aliases and methods that blur the line:

**Aliases Rails defines on top of minitest:**

| Rails alias | Delegates to | Effect |
|-------------|-------------|--------|
| `assert_not_*` (12 methods) | `refute_*` | `assert_not_nil`, `assert_not_equal`, etc. all work in Rails |
| `assert_not` | `refute` | Base negation |
| `assert_raise` (singular) | `assert_raises` | Both singular and plural work in Rails |
| `assert_no_match` | `refute_match` | |

**Methods Rails adds (not in either framework):**

| Method | Purpose |
|--------|---------|
| `assert_nothing_raised` | Passes if block doesn't raise |
| `assert_difference` / `assert_no_difference` | Check numeric change after block |
| `assert_changes` / `assert_no_changes` | Check value change after block |

This means in Rails: `assert_not_nil`, `assert_raise`, and `assert_nothing_raised` all work — but they will **not** work if you move the test to plain minitest outside Rails.
