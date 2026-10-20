---
name: kendo-ui-testing
description: Use when designing or implementing tests for Kendo UI components including mock DataSource, event simulation, widget lifecycle tests, and integration test strategy across jQuery, Angular, React, and Vue variants.
---

# Kendo UI Testing

## Specialization

Design and implement expert-level test suites for Kendo UI components covering widget initialization contracts, mock DataSource patterns, event simulation, method invocation verification, widget destruction, Kendo UI Validator testing, and framework-variant-specific testing strategies (QUnit for jQuery, Jasmine/Jest for Angular, Jest/React Testing Library for KendoReact).

## Trigger Conditions

- Writing unit tests for Kendo UI widget initialization and configuration.
- Mocking a DataSource to test widget behavior without a live server.
- Simulating user interaction with Kendo UI components (row selection, cell editing, dropdown selection, date picker navigation).
- Testing Kendo UI Validator rules including custom rules.
- Testing widget destruction and memory cleanup.
- Implementing integration tests that verify DataSource transport calls.
- A `kendo-ui-quality-gate` audit identifies missing test coverage.
- Introducing Kendo UI components to a project that has an existing test suite.

## Scope Boundaries

In scope:

- Widget initialization contract tests: options applied, DOM structure emitted correctly.
- Mock DataSource: local array DataSource as a server proxy, `transport.read` function override.
- Event simulation: programmatic `trigger()` and Kendo UI `trigger()` equivalents.
- Method invocation tests: `select()`, `value()`, `setDataSource()`, `refresh()`, `destroy()`.
- Validator testing: rule pass/fail, message content, `validate()` return value.
- Widget destruction: verify no leaked event handlers after `destroy()`.
- Framework-specific patterns: QUnit (jQuery), Jasmine (Angular), Jest + React Testing Library (KendoReact).

Out of scope:

- CI pipeline test execution configuration (see `kendo-ui-ci-integration`).
- Visual regression testing (covered separately by visual testing tools).
- Accessibility automated audit (see `kendo-ui-accessibility`).
- End-to-end browser tests beyond component-level interaction (use Playwright or Cypress skills).

## Inputs

- Widget(s) under test.
- Kendo UI version in use.
- Test framework in use: QUnit, Jasmine, Jest, or Mocha.
- DataSource type: local or remote (mock required for remote).
- Existing test coverage for the components (if any).

## Required Outputs

- Widget initialization test with option contract verification.
- Mock DataSource setup with local data covering edge cases (empty, single item, paginated).
- Event simulation test for each user-triggered event.
- Method invocation test covering the primary method surface.
- Validator rule tests: pass case, fail case, and custom rule case.
- Destruction test verifying no leaked handlers.
- Coverage gap list: untested widget behaviors.

## Core Patterns

### Mock DataSource (Local Array)

```javascript
// Use a local array DataSource to isolate widget behavior from network
function mockDataSource(data) {
    return new kendo.data.DataSource({
        data: data || [
            { id: 1, name: "Item A", status: "active" },
            { id: 2, name: "Item B", status: "inactive" }
        ],
        schema: {
            model: {
                id: "id",
                fields: {
                    id:     { type: "number" },
                    name:   { type: "string" },
                    status: { type: "string" }
                }
            }
        },
        pageSize: 10
    });
}
```

### QUnit Widget Initialization Test

```javascript
QUnit.module("Grid initialization", {
    beforeEach: function() {
        this.fixture = $("<div id='test-grid'></div>").appendTo("#qunit-fixture");
    },
    afterEach: function() {
        var grid = this.fixture.data("kendoGrid");
        if (grid) { grid.destroy(); }
    }
});

QUnit.test("renders correct number of rows", function(assert) {
    var done = assert.async();
    var ds = mockDataSource();

    this.fixture.kendoGrid({ dataSource: ds, columns: [{ field: "name" }] });
    var grid = this.fixture.data("kendoGrid");

    ds.one("change", function() {
        assert.equal(grid.tbody.find("tr").length, 2);
        done();
    });

    ds.read();
});
```

### Event Simulation

```javascript
QUnit.test("fires change event on row selection", function(assert) {
    var done = assert.async();
    var grid = this.fixture.kendoGrid({
        dataSource: mockDataSource(),
        selectable: "row"
    }).data("kendoGrid");

    grid.bind("change", function() {
        var selected = grid.select();
        assert.equal(selected.length, 1);
        done();
    });

    // Simulate row click
    grid.dataSource.one("change", function() {
        grid.tbody.find("tr:first").trigger("click");
    });
    grid.dataSource.read();
});
```

### Validator Rule Test

```javascript
QUnit.test("custom futureDate rule blocks past dates", function(assert) {
    var input = $("<input name='startDate' data-future-date-rule='true' />")
        .appendTo(this.fixture)
        .val("2020-01-01"); // past date

    var validator = this.fixture.kendoValidator({
        rules: {
            futureDate: function(input) {
                if (input.is("[data-future-date-rule]")) {
                    return kendo.parseDate(input.val()) > new Date();
                }
                return true;
            }
        }
    }).data("kendoValidator");

    assert.notOk(validator.validate(), "Validator should reject past date");
});
```

### Destruction Leak Test

```javascript
QUnit.test("destroy removes all event handlers", function(assert) {
    var handlerCalled = false;
    var grid = this.fixture.kendoGrid({ dataSource: mockDataSource() }).data("kendoGrid");

    grid.bind("dataBound", function() { handlerCalled = true; });
    grid.destroy();

    // Trigger dataBound manually — should not fire after destroy
    grid.trigger("dataBound");
    assert.notOk(handlerCalled, "Handler should not fire after destroy");
});
```

## Framework-Variant Testing Notes

| Framework | Preferred Test Runner | Key Considerations |
|---|---|---|
| Kendo UI for jQuery | QUnit | Use `#qunit-fixture` for DOM isolation; call `destroy()` in `afterEach` |
| KendoReact | Jest + React Testing Library | Use `@testing-library/react`; wrap in `KendoReactProvider` if theming is tested |
| Kendo UI for Angular | Jasmine + Angular TestBed | Import Kendo module in `TestBed`; use `fixture.detectChanges()` before assertions |
| Kendo UI for Vue | Jest + Vue Test Utils | Mount with `globalComponents` registration; use `wrapper.find()` for widget DOM |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | One initialization test with mock DataSource | Widget renders from local data; test passes |
| L2 Practical | Full event, method, and validation test suite for one widget | All primary interactions and edge cases covered |
| L3 Hardening | Destruction tests + DataSource transport mock + validator round-trip | No leaked handlers; transport mock intercepts all CRUD operations |
| L4 Expert | Cross-framework test strategy with shared mock fixtures | Mock DataSource reusable across QUnit/Jest; CI runs all suites |
