---
name: mock-external-api
description: Builds a realistic mock of an external API for your tests, shaped from recorded or documented responses.
disable-model-invocation: true
---

Create a mock of this external API for tests: $ARGUMENTS

1. Find where the code calls the API (client module, SDK wrapper, fetch calls). List the endpoints, methods and fields the app actually uses.
2. Gather real shapes from, in order: fixtures or logs already in the repo, the provider's OpenAPI file or docs, and a sample response the user pastes. Do not call the live API and do not read credentials.
3. Pick the project's mocking tool (msw, nock, responses, WireMock, httpmock, vcr, Mockito) and build handlers there. Keep the mock in one folder with one file per endpoint group.
4. Cover: a success reply, an empty result, pagination, a 4xx validation error, a 429 with Retry-After, a 5xx, and a timeout. Use realistic ids and timestamps.
5. Add a contract test that checks each fixture against the schema (zod, JSON Schema or types) so drift is caught.
6. Replace one existing slow test to prove it works, then run the suite offline.

Report files created, scenarios covered and which fields were guessed rather than documented.
