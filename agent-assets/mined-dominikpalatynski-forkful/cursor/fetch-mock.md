---
alwaysApply: false
---
# Fetch Mocking: Best Practices & Scenarios

## Quick Reference

Use **dependency injection** to mock fetch in services that accept a `fetchImpl` parameter:

```typescript
const mockFetch = vi.fn();
const service = new ServiceClass(config, mockFetch);
```

---

## 5 Common Test Scenarios

### 1. Success Response (Happy Path)
```typescript
mockFetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ({ choices: [{ message: { content: JSON.stringify({ name: 'Recipe' }) } }] })
});

const result = await service.generate({ userMessage: 'test' });
expect(result.json).toEqual({ name: 'Recipe' });
```

### 2. HTTP Error (401 Unauthorized)
```typescript
mockFetch.mockResolvedValueOnce({
  ok: false,
  status: 401,
  statusText: 'Unauthorized',
  text: async () => 'Invalid API key'
});

await expect(service.generate({ userMessage: 'test' }))
  .rejects.toThrow(/HTTP 401/);
```

### 3. Network Timeout
```typescript
mockFetch.mockImplementationOnce(() => {
  const error = new DOMException('Aborted', 'AbortError');
  return Promise.reject(error);
});

await expect(service.generate({ userMessage: 'test' }))
  .rejects.toThrow(/timed out/);
```

### 4. Invalid JSON Response
```typescript
mockFetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ({
    choices: [{ message: { content: 'Not valid JSON {]' } }]
  })
});

await expect(service.generate({ userMessage: 'test' }))
  .rejects.toThrow(/not valid JSON/);
```

### 5. Schema Validation Failure
```typescript
mockFetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ({
    choices: [{ message: { content: JSON.stringify({ /* missing required field */ }) } }]
  })
});

await expect(service.generate({ userMessage: 'test' }))
  .rejects.toThrow(/does not match schema/);
```

---

## Best Practices

✅ **DO**
- Use `mockResolvedValueOnce()` for one-off calls
- Use `mockImplementation()` for complex logic
- Reset mocks with `vi.resetAllMocks()` in `beforeEach()`
- Verify calls: `expect(mockFetch).toHaveBeenCalledWith(...)`
- Test both success AND failure paths

❌ **DON'T**
- Call the real API during tests
- Forget to verify the mock was called
- Use `mockResolvedValue()` without resetting (persists between tests)
- Mock global `fetch` without cleanup

---

## Verify Request Details

```typescript
const callArgs = mockFetch.mock.calls[0];
const [url, options] = callArgs;

expect(url).toBe('https://openrouter.ai/api/v1/chat/completions');
expect(options.method).toBe('POST');
expect(options.headers['Authorization']).toBe('Bearer test-key');

// Verify request body
const body = JSON.parse(options.body);
expect(body.messages[0].role).toBe('system');
```
