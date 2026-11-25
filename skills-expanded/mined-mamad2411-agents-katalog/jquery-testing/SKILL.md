---
name: jquery-testing
description: Use when designing or implementing tests for jQuery code including DOM interaction tests, event simulation, AJAX mocking, and plugin behavior verification with QUnit or Jest.
---

# jQuery Testing

## Specialization

Design and implement expert-level tests for jQuery-based code covering DOM setup and teardown, event simulation, AJAX mocking, Deferred contract verification, and plugin lifecycle testing — using QUnit (jQuery's native framework) or Jest with jsdom.

## Trigger Conditions

- Writing unit or integration tests for jQuery DOM manipulation code.
- Testing jQuery event handlers — binding, delegation, and custom event payloads.
- Mocking or intercepting `$.ajax()` calls in tests.
- Verifying jQuery Deferred and Promise resolution contracts.
- Testing jQuery plugin initialization, option handling, method invocation, and destruction.
- Reviewing existing jQuery test suites for coverage gaps, false positives, or DOM isolation failures.
- Setting up a new test environment for a jQuery-based project.

## Scope Boundaries

In scope:

- QUnit test structure: `QUnit.module`, `QUnit.test`, `assert` methods, async tests.
- Jest + jsdom configuration for jQuery testing.
- DOM fixture setup and teardown patterns.
- Event simulation with `.trigger()` and native `dispatchEvent`.
- AJAX interception with `$.mockjax` or Jest's `fetch` / `XMLHttpRequest` mocks.
- Deferred contract testing: resolved, rejected, and always-called paths.
- Plugin lifecycle testing: init, update, method call, destroy.

Out of scope:

- End-to-end browser automation (Selenium, Playwright, Cypress).
- Performance benchmarking (see `jquery-performance`).
- Security testing (see `jquery-security`).

## Inputs

- Test target: module name, jQuery version, target functions or behaviors.
- Test framework preference: QUnit or Jest.
- DOM fixture complexity.
- AJAX endpoints to mock.
- Plugin public API surface.

## Required Outputs

- DOM fixture strategy with explicit setup and teardown.
- Event simulation tests that verify handler behavior and propagation control.
- AJAX mock configuration with success, error, and timeout scenarios.
- Deferred chain verification: `.done()`, `.fail()`, `.always()` are independently exercised.
- Plugin test suite: initialization, option override, public method calls, and destroy.
- Test isolation confirmation: no test leaves DOM state that affects subsequent tests.

## Test Environment Setup

### QUnit (Recommended for jQuery projects)

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://code.jquery.com/qunit/qunit-2.x.x.css">
</head>
<body>
  <div id="qunit"></div>
  <div id="qunit-fixture"></div>
  <script src="jquery.min.js"></script>
  <script src="https://code.jquery.com/qunit/qunit-2.x.x.js"></script>
  <script src="my-module.js"></script>
  <script src="my-module.test.js"></script>
</body>
</html>
```

- `#qunit-fixture` is automatically reset between tests — always place test HTML here.
- Use `QUnit.module('name', hooks)` with `beforeEach`/`afterEach` for setup and teardown.

### Jest + jsdom (for CI-first or Node-based projects)

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFiles: ['./test/setup.js']
};

// test/setup.js
const $ = require('jquery');
global.$ = global.jQuery = $;
```

- jsdom does not support all browser APIs — avoid testing CSS animations or computed styles with Jest.
- Use `document.body.innerHTML = ''` in `afterEach` to reset DOM state.

## Core Test Patterns

### DOM Fixture and Isolation

```javascript
// QUnit
QUnit.module('MyWidget', function(hooks) {
  hooks.beforeEach(function() {
    // #qunit-fixture is auto-cleared per test; append here
    $('#qunit-fixture').append('<div class="target"><button>Click</button></div>');
  });
  // No afterEach needed — QUnit clears #qunit-fixture automatically
});

// Jest
beforeEach(() => {
  document.body.innerHTML = '<div class="target"><button>Click</button></div>';
});
afterEach(() => {
  document.body.innerHTML = '';
});
```

### Event Simulation

```javascript
// Simulate a click and verify handler outcome
QUnit.test('click triggers state change', function(assert) {
  const $btn = $('#qunit-fixture .btn');
  $btn.trigger('click');
  assert.ok($btn.hasClass('active'), 'Button has active class after click');
});

// Verify stopPropagation
QUnit.test('inner click does not bubble to outer', function(assert) {
  let outerFired = false;
  $('#qunit-fixture .outer').on('click', function() { outerFired = true; });
  $('#qunit-fixture .inner').trigger('click'); // inner handler calls stopPropagation
  assert.notOk(outerFired, 'Outer handler did not fire');
});
```

- Use `.trigger()` for jQuery event simulation — it fires both jQuery handlers and native handlers.
- Use `dispatchEvent` with a `CustomEvent` when testing code that uses native `addEventListener`.

### AJAX Mocking with $.mockjax

```javascript
// Install: npm install jquery-mockjax
$.mockjax({
  url: '/api/users',
  responseTime: 0,
  responseText: [{ id: 1, name: 'Alice' }]
});

QUnit.test('loads users on init', function(assert) {
  const done = assert.async();
  loadUsers().done(function(users) {
    assert.equal(users.length, 1);
    assert.equal(users[0].name, 'Alice');
    done();
  });
});

// Teardown
QUnit.module('AJAX tests', {
  afterEach: function() { $.mockjax.clear(); }
});
```

- Always call `$.mockjax.clear()` in `afterEach` — uncleaned mocks leak across tests.
- Test error and timeout paths explicitly:
  ```javascript
  $.mockjax({ url: '/api/fail', status: 500 });
  $.mockjax({ url: '/api/timeout', isTimeout: true });
  ```

### Deferred Contract Testing

```javascript
QUnit.test('resolves with correct data', function(assert) {
  const done = assert.async();
  const deferred = $.Deferred();

  let doneValue, failCalled = false, alwaysCalled = false;

  deferred
    .done(function(val) { doneValue = val; })
    .fail(function() { failCalled = true; })
    .always(function() { alwaysCalled = true; });

  deferred.resolve('expected');

  assert.equal(doneValue, 'expected', '.done called with resolved value');
  assert.notOk(failCalled, '.fail not called on resolve');
  assert.ok(alwaysCalled, '.always called');
  done();
});
```

- Always test the rejection path independently.
- Verify `.always()` fires on both resolution and rejection.

### Plugin Testing

```javascript
QUnit.module('$.fn.myPlugin', function(hooks) {
  hooks.beforeEach(function() {
    $('#qunit-fixture').append('<div class="widget"></div>');
  });

  QUnit.test('initializes without error', function(assert) {
    assert.expect(1);
    assert.doesNotThrow(function() {
      $('.widget').myPlugin({ option1: 'value' });
    });
  });

  QUnit.test('stores instance in data cache', function(assert) {
    $('.widget').myPlugin();
    assert.ok($.data($('.widget')[0], 'myPlugin'), 'instance stored in data');
  });

  QUnit.test('destroy removes data and unbinds events', function(assert) {
    $('.widget').myPlugin();
    const instance = $.data($('.widget')[0], 'myPlugin');
    instance.destroy();
    assert.notOk($.data($('.widget')[0], 'myPlugin'), 'data cleared after destroy');
  });
});
```

## Workflow

1. Choose test framework: QUnit for browser-native projects; Jest + jsdom for Node-based CI.
2. Set up DOM fixture isolation (`#qunit-fixture` or `beforeEach`/`afterEach` reset).
3. Write event simulation tests that verify handler outcomes and propagation.
4. Configure AJAX mocks for all endpoints under test — include error and timeout scenarios.
5. Write Deferred contract tests: resolved, rejected, and always paths independently.
6. Write plugin lifecycle tests: init, option update, method call, and destroy.
7. Verify test isolation: confirm no test leaves residual DOM or mock state.

## Done Criteria

- Every test uses `#qunit-fixture` or equivalent DOM reset.
- AJAX mocks are cleared in `afterEach`.
- Deferred `.done()`, `.fail()`, and `.always()` are each independently tested.
- Plugin destroy test verifies event unbinding and data removal.
- No test relies on execution order for correctness.

## References

- [QUnit Docs](https://qunitjs.com)
- [QUnit API Reference](https://api.qunitjs.com)
- [jQuery Mockjax](https://github.com/jakerella/jquery-mockjax)
- [Jest jsdom Environment](https://jestjs.io/docs/configuration#testenvironment-string)
- [jQuery API: .trigger()](https://api.jquery.com/trigger/)
- [jQuery API: Deferred Object](https://api.jquery.com/category/deferred-object/)
- [jQuery Learn: Testing with QUnit](https://learn.jquery.com/code-organization/unit-testing/)
