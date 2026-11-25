# concurrency-review

Review async Python for the bugs that only surface under load: deadlocks,
unawaited coroutines, and blocking calls made inside the event loop.

When reviewing async code:

- Flag any call to a coroutine function that is missing `await` — it silently
  returns a coroutine object and the work never runs.
- Flag blocking I/O inside an `async def`: `requests`, `open()`, `time.sleep`,
  synchronous DB drivers. Recommend the async equivalent or
  `loop.run_in_executor`.
- Look for lock-ordering that can deadlock, and `asyncio.gather(...)` that drops
  exceptions without `return_exceptions=True` handling.
- Prefer structured concurrency (`asyncio.TaskGroup`) over bare `create_task`
  whose result and errors are never awaited.

Report the smallest reproducing scenario and the concrete fix, not just the
symptom.
