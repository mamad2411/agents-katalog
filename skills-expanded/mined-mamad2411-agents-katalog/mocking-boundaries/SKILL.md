---
name: mocking-boundaries
description: Mock at I/O and network boundaries only; never mock the unit under test; prefer fakes over deep mock chains
---

# Mocking Boundaries

Mocks are a tool for controlling dependencies you don't own, not a replacement for understanding the code you're testing. When tests mock the very thing they're testing, or build deep chains of `mockReturnValue` calls, they stop verifying behavior and start verifying that the test author's assumptions were internally consistent. That is not testing.

## Rules

- **Mock at the I/O boundary only.** Databases, HTTP clients, file system calls, third-party SDKs, and the system clock are the correct seam. Pure business logic that depends only on its arguments needs no mocking.
- **Never mock the unit under test.** If you are testing `OrderService`, do not mock `OrderService`. Mock the `PaymentGateway` it calls, not the service itself.
- **Prefer fakes over mock chains.** A `FakeUserRepository` that stores data in a `Map` is easier to read and maintain than `vi.fn().mockResolvedValueOnce(...)` scattered across ten tests. Fakes encode valid behavior; deep mock chains encode assumptions.
- **Mock at the module boundary, not the implementation detail.** Mock `emailClient.send`, not `nodemailer.createTransport().sendMail`. When the implementation changes, the test should not break.
- **Avoid mocking what you can inject.** If a class accepts a dependency in its constructor, pass a real or fake version in the test. Reaching past the constructor with `vi.spyOn` to swap an internal means the design needs an injection point, not a better mock.

## Examples

```ts
// BAD — mocks the unit under test; tests the mock, not the code
it('charges the user', async () => {
  const chargeUser = vi.fn().mockResolvedValue({ status: 'ok' })
  const result = await chargeUser({ userId: 1, amount: 50 })
  expect(result.status).toBe('ok') // only verifies the mock setup
})

// BAD — deep mock chain leaks implementation details
it('sends a welcome email', async () => {
  const transporter = { sendMail: vi.fn().mockResolvedValue({}) }
  vi.spyOn(nodemailer, 'createTransport').mockReturnValue(transporter)
  await sendWelcomeEmail('alice@example.com')
  expect(transporter.sendMail).toHaveBeenCalled()
})

// GOOD — fake replaces the I/O boundary; real service is tested
class FakeEmailClient implements EmailClient {
  sent: EmailMessage[] = []
  async send(msg: EmailMessage) { this.sent.push(msg) }
}

it('sends a welcome email to the registered address', async () => {
  const emailClient = new FakeEmailClient()
  const service = new UserService(emailClient)
  await service.register({ email: 'alice@example.com' })
  expect(emailClient.sent).toHaveLength(1)
  expect(emailClient.sent[0].to).toBe('alice@example.com')
})

// GOOD — HTTP boundary mocked with MSW or a fetch stub
it('returns user data from the API', async () => {
  server.use(
    http.get('/api/users/1', () => HttpResponse.json({ id: 1, name: 'Alice' }))
  )
  const user = await fetchUser(1)
  expect(user.name).toBe('Alice')
})
```
