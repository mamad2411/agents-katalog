---
description: Testing conventions - test kinds, fakes vs mocks, naming, determinism
globs: tests/**
alwaysApply: false
---

# Testing conventions

## Which kind of test
- `tests/Unit/`: one class, no kernel, no DB. Domain, `FailoverDeliveryStrategy`, provider classification.
- `tests/Integration/`: `KernelTestCase` / `WebTestCase` against the real `app_test` MariaDB with
  `dama/doctrine-test-bundle` rolling back each test. Repositories, API, end-to-end pipeline (Messenger `async`
  is `in-memory://`; tests drain it on `delivery.bus` via `tests/Support/DeliveryPipeline` — never `sync://`).
- Prefer the cheapest kind that gives real evidence; do not integration-test what a unit test proves.

## Doubles
- Our own ports -> in-repo **fakes** (`FakeSmsProvider` with a mode, `InMemoryRecipientResolver`), never
  `createMock()` on our interfaces. Fakes are real classes under `src/.../Infrastructure/Provider/Fake/`.
- External HTTP -> `MockHttpClient` with scripted `MockResponse` (including thrown `TransportException`).
- Mail -> `MailerAssertionsTrait` on the `null://` transport. Time -> `Symfony\Component\Clock\MockClock`.

## Style
- Names describe behaviour: `test_it_fails_over_to_next_provider_on_transient_failure()`.
- Arrange / act / assert separated by a blank line; one behaviour per test; assert on outcome, not on
  call order. No `sleep()`, no real network, no random data without a seed.
- Builders for aggregates live in `tests/Support/` (e.g. `NotificationBuilder::aNotification()->withChannels(...)`).
- Every `WebTestCase` request is followed by `$this->assertResponseIsDocumented($client)` (trait
  `App\Tests\Support\OpenApiAssertions`). An undocumented status or extra/missing JSON field is a failing test.
- Every failure-semantics decision in `docs/DECISIONS.md` has exactly one test that encodes it; link the
  test in `docs/REQUIREMENTS_TRACE.md`.

```php
public function test_it_does_not_fail_over_when_outcome_is_unknown(): void
{
    $primary = FakeSmsProvider::withMode(FakeMode::Timeout);
    $secondary = FakeSmsProvider::withMode(FakeMode::Success);

    $result = $this->strategy->deliver($this->delivery, [$primary, $secondary]);

    self::assertSame(AttemptOutcome::Unknown, $result->lastOutcome());
    self::assertSame(0, $secondary->sentCount());
}
```

Run: `docker compose exec -T app vendor/bin/phpunit --filter <Name>`; full suite before a phase ends.
