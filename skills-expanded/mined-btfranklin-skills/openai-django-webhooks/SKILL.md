---
name: openai-django-webhooks
description: >-
  Build or debug asynchronous OpenAI Responses API workflows in Django. Use this skill for background requests, signed webhooks, response correlation, persistence, and HTMX status polling. Do not use it for generic OpenAI calls, non-Django consumers, other webhook providers, or frontend-only polling.
---

# OpenAI Django Webhooks

## Workflow

1. Inspect the existing Django service, models, URLs, views, jobs, templates, and OpenAI client use. Preserve the established project conventions.
2. Define the lifecycle before you write code. Record the local record ID and the OpenAI response ID. Record the allowed states, terminal failures, duplicate-event behavior, and retry policy.
3. Read [the Django webhook flow reference](references/OPENAI_DJANGO_WEBHOOKS.md). It contains patterns for the service, callback, response extraction, and HTMX polling. Verify each code example against the current official documentation before you use it.
4. Assign each action to one component:
   - The request endpoint verifies the signature, records the delivery durably, enqueues work, and returns a `2xx` response promptly.
   - The worker retrieves the response and handles retryable processing failures.
   - The service layer owns idempotent state transitions and output persistence.
   - The status view authorizes each request and stops polling after every terminal state.
5. Validate signature failures and duplicate delivery. Validate events that are out of order or unknown. Validate retrieval failure, terminal response failure, successful completion, and polling termination. Report exact evidence during diagnosis. Do not infer a cause only from symptoms.

## Verify Current Information

Before implementation, use official OpenAI documentation to verify the current Responses API fields and webhook event structures. Also verify the SDK signature-verification helpers, retry behavior, and supported models. Record the documentation URL and access date in the plan or review. Check the current Django and HTMX documentation when behavior depends on their versions. Verify version-sensitive examples before you use them.
