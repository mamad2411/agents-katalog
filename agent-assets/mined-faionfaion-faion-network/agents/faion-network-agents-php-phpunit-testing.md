# PHPUnit Testing Patterns

## Summary

**One-sentence:** Structure PHPUnit tests with strict isolation, factory-based fixtures, the Arrange-Act-Assert pattern, data providers for table tests, and dependency injection for mocks.

**One-paragraph:** PHPUnit is the standard PHP testing framework. Effective use requires: AAA test structure, factory-built fixtures (no shared state), data providers for parameterized tests, mock objects via constructor injection (not facade fakes), strict isolation (no test depends on order), and CI integration with --colors=never + --testdox + --coverage-xml. Pest is a wrapper that builds on PHPUnit; the rules carry over.

**Ефективно для:**

- Laravel / vanilla PHP проєкти з PHPUnit як test runner.
- TDD стайл — швидкі ізольовані тести без full bootstrap.
- Table-driven tests через #[DataProvider] для edge-case покриття.
- Pest-flavored projects — методологія повторюється.

## Applies If (ALL must hold)

- PHP 8.2+ project with composer + PHPUnit 11+ installed.
- Tests should run in CI on every push.
- Mocking is used (downstream HTTP / Stripe / S3 / DB).
- Team commits to maintaining the suite (not write-once-and-forget).

## Skip If (ANY kills it)

- Project standardized exclusively on Pest with no PHPUnit fallback — see pest-testing methodology.
- Integration-only test suite (Cypress / Playwright) — JS toolchain.
- Throwaway script.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Subject under test | PHP class with public methods | developer |
| Test bootstrap | phpunit.xml.dist + tests/bootstrap.php | repo |
| Factories | Laravel factories OR data-builder pattern | fixtures dir |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: aaa-structure, factory-no-shared-state, data-provider-table-tests, mocks-via-di, no-test-order-dependence | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-test` | sonnet | Templated test class. |
| `design-edge-cases` | opus | Identifying important cases is judgment-heavy. |
| `lint-shared-state` | haiku | Mechanical scan for static fixtures + setUp mutations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/OrderServiceTest.php` | PHPUnit test class with AAA + #[DataProvider] + constructor mocks |
| `templates/phpunit.xml` | PHPUnit config with random order + coverage clover output |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-phpunit-testing.py` | Validate the test artefact against the schema | Pre-commit + CI |

## Related

- [[php-laravel]]
- [[php-laravel-patterns]]
- [[ruby-rspec-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/OrderServiceTest.php`

```php
<?php

namespace Tests\Unit\Services;

use App\Models\Order;
use App\Models\OrderItem;
use App\Services\DiscountService;
use App\Services\OrderService;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;

final class OrderServiceTest extends TestCase
{
    private DiscountService&MockObject $discount;
    private OrderService $service;

    protected function setUp(): void
    {
        parent::setUp();
        $this->discount = $this->createMock(DiscountService::class);
        $this->service = new OrderService($this->discount);
    }

    #[DataProvider('totalCases')]
    public function test_calculates_total_for_various_baskets(array $items, int $discountCents, int $expectedCents): void
    {
        // Arrange
        $this->discount->method('apply')->willReturn($discountCents);

        // Act
        $total = $this->service->calculateTotal($items);

        // Assert
        self::assertSame($expectedCents, $total);
    }

    public static function totalCases(): array
    {
        return [
            'empty basket' => [[], 0, 0],
            'single item' => [[['cents' => 1000, 'qty' => 1]], 0, 1000],
            'multi-item with discount' => [[['cents' => 1000, 'qty' => 2], ['cents' => 500, 'qty' => 3]], 200, 3300],
        ];
    }
}
```
