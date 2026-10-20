---
name: lyra-nodejs
description: Node.js backend rules grounded in the single-threaded event loop. Use for Express, Fastify, NestJS, async pitfalls, streams, or worker threads.
compatibility: No tools required. Optional: lyra-tdd, lyra-clean-architecture, lyra-clean-code.
---

# lyra-nodejs

## What it does

Node.js is a single-threaded event loop with a libuv thread pool — every framework choice, async pattern, stream usage, and security posture flows from that fact. This skill derives sixteen tight rules from the mental model instead of handing you snippets to cargo-cult. Push business logic behind ports and test use cases with in-memory fakes; if a unit test needs to mock `pg` or `express`, the boundary is in the wrong place. Reach for it on new services, code reviews, or when an existing backend stalls, leaks, or crashes under load.

## The rules

### 1. Never block the event loop with CPU-bound sync work

A 200ms sync loop stalls every connected client for 200ms. Reach for the async variant of `pbkdf2`, `fs.readFile`, and large `JSON.parse` calls — let libuv handle them.

```typescript
// bad:  app.get('/hash', (req, res) => res.json(crypto.pbkdf2Sync(req.query.pw, salt, 1e5, 64, 'sha512')));
// good: app.get('/hash', async (req, res) => res.json(await pbkdf2(String(req.query.pw), salt, 1e5, 64, 'sha512')));
```

### 2. Reason about microtask vs macrotask ordering

`nextTick` > `Promise.then` > `setImmediate` > `setTimeout` > I/O. Recursive `nextTick` starves I/O; `setTimeout(0)` does not fire before a resolved promise.

```typescript
// bad:  setTimeout(() => log('A'), 0); Promise.resolve().then(() => log('B')); log('C'); // assumes C, A, B
// good: setImmediate(() => log('after I/O poll'));   // actual order above is C, B, A
```

### 3. Handle every promise rejection

Since Node 15, unhandled rejections terminate the process by default. Catch at the call site, and add a process-level safety net in bootstrap.

```typescript
// bad:  emailService.send(userId).then(() => log('sent'));   // rejection kills the process
// good: emailService.send(userId).then(() => log('sent')).catch((err) => log.error({ err }, 'email failed'));
//       process.on('unhandledRejection', (r) => { log.error({ r }, 'unhandled'); process.exit(1); });
```

### 4. Choose the framework by team scale and need, not by hype

Match the framework to the team and the workload — see the table below.

```typescript
// bad:  @Module({ controllers: [WebhookController], providers: [WebhookService] })   // NestJS for a 3-route webhook
// good: app.post('/webhook', async (req, reply) => { await queue.add(req.body); reply.code(202).send(); });
```

### 5. Use `Promise.all` for concurrent calls, `allSettled` when partial failure is OK

Sequential `await` in a loop turns N parallelizable calls into N round-trips. `Promise.all` rejects on first failure; `allSettled` collects them for bulk operations.

```typescript
// bad:  for (const id of ids) users.push(await db.user.findById(id));   // 50 sequential, 50× latency
// good: return Promise.all(ids.map((id) => db.user.findById(id)));       // 50 concurrent, ~1× latency
```

### 6. Centralize error handling — don't wrap every function in try/catch

Try/catch on every function swallows context and hides the real cause. Catch once at the handler boundary; let errors propagate with full stack traces.

```typescript
// bad:  async function getUser(id) { try { return await db.user.findById(id); } catch { return null; } }
// good: app.setErrorHandler((err, req, reply) => { log.error({ err }, 'failed'); reply.code(err.statusCode ?? 500).send({ error: err.message }); });
```

### 7. Stream payloads larger than ~1MB — never buffer entire bodies

Buffering a 2GB upload into a single `Buffer` exhausts heap under concurrent load. Streams process in chunks and keep memory flat.

```typescript
// bad:  const data = await fs.readFile(`/data/${id}`); res.send(data);
// good: createReadStream(`/data/${id}`).pipe(res);
```

### 8. Always handle stream errors and use `pipeline` for backpressure

Unhandled `error` events crash the process; manual `.pipe()` doesn't forward errors or clean up.

```typescript
// bad:  readStream.pipe(transformStream).pipe(writeStream);   // leak on failure
// good: await pipeline(createReadStream(input), createGzip(), createWriteStream(output));
```

### 9. Use `worker_threads` for CPU-bound work over ~100ms — never for I/O

The JS thread is single; CPU work blocks it. I/O is already parallel via libuv — moving it to a worker adds overhead with no benefit.

```typescript
// bad:  app.post('/hash-batch', (req, res) => res.json(req.body.items.map(slowHashSync)));   // 5s stall
// good: const pool = new Piscina({ filename: new URL('./hash-worker.js', import.meta.url) });
//       app.post('/hash-batch', async (req, res) => res.json(await Promise.all(req.body.items.map((i) => pool.run(i)))));
```

### 10. Use connection pooling — never open a connection per request

Opening a DB connection costs 50–200ms. Per-request connections add that latency every call and exhaust the DB's connection limit under load.

```typescript
// bad:  const client = new pg.Client({ connectionString }); await client.connect(); /* ... */ await client.end();
// good: const pool = new pg.Pool({ connectionString, max: 20 }); const r = await pool.query('SELECT * FROM users');
```

### 11. Use parameterized queries — never string-concatenate SQL

String concatenation in SQL is injection, even on "internal-only" endpoints.

```typescript
// bad:  await pool.query(`SELECT * FROM users WHERE name = '${req.query.name}'`);   // '; DROP TABLE users; --'
// good: await pool.query('SELECT * FROM users WHERE name = $1', [req.query.name]);
```

### 12. Validate and sanitize all input with a schema — never trust `req.body`

Every client field is adversarial. Schema validation at the boundary is your first defense against injection, prototype pollution, and type coercion.

```typescript
// bad:  await db.user.create({ email: req.body.email, role: req.body.role });   // role = 'admin' from anonymous
// good: const S = z.object({ email: z.string().email(), role: z.enum(['member', 'viewer']).default('member') });
//       const parsed = S.safeParse(req.body); if (!parsed.success) return res.status(400).json(parsed.error.flatten());
```

### 13. Manage secrets via env vars and a secrets manager — never hardcode

Hardcoded secrets leak via git history, logs, and bundles. Load from env at startup, fail fast if missing, and use a secrets manager in prod.

```typescript
// bad:  const stripeKey = 'sk_live_51234567890abcdef';   // forever in git history
// good: const stripeKey = requiredEnv('STRIPE_SECRET_KEY');   // throws at boot if unset
```

### 14. Keep dependencies lean and harden HTTP — audit, headers, CORS, rate-limit

Every dependency is attack surface: `npm audit` in CI, pin majors (never `latest`), dedupe, drop unused. Default responses leak info — use `helmet`, an explicit CORS allowlist (never `*` in prod), and rate-limit auth.

```typescript
// bad:  app.use(cors());   // origin: '*'
// good: app.use(helmet()); app.use(cors({ origin: ['https://app.example.com'], credentials: true }));
//       app.use('/auth/login', rateLimit({ windowMs: 15 * 60 * 1000, max: 10 }));
```

### 15. Enable compression, set cache headers, and use all CPU cores

Three low-effort wins: gzip/brotli saves 60–80% bandwidth, `Cache-Control` + `ETag` skips redundant work, and clustering runs one process per core.

```typescript
// bad:  app.get('/api/products', async (req, res) => res.json(await db.product.findAll()));   // one core, no cache
// good: if (cluster.isPrimary) { for (let i = 0; i < availableParallelism(); i++) cluster.fork(); } else {
//         app.use(compression()); app.get('/api/products', async (req, res) => { res.set('Cache-Control', 'public, max-age=60'); res.json(await db.product.findAll()); }); app.listen(3000); }
```

### 16. Keep business logic out of route handlers

Handlers are outer adapters; business logic belongs in framework-agnostic use cases that depend on ports, not PrismaClient.

```typescript
// bad:  app.post('/orders', async (req, res) => { const item = await db.product.findById(req.body.productId); if (item.stock < req.body.qty) return res.status(400).send('out of stock'); await db.order.create({ ...req.body }); res.status(201).send('created'); });
// good: app.post('/orders', async (req, res) => res.status(201).json(await createOrder.execute(req.body)));
```

## Framework selection

| Framework   | Choose when                                                          | Avoid when                                                 |
| ----------- | -------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Express** | Existing apps, simple prototypes, ≤ 20 routes                        | New perf-sensitive projects, large teams needing structure |
| **Fastify** | New APIs where throughput matters, JSON-heavy, schema-first          | Small teams who don't want ceremony, heavy DI needed       |
| **NestJS**  | Enterprise, ≥ 3 devs, complex domain needing DI, Java/C# backgrounds | Simple CRUD, prototypes, solo projects                     |

---

_Part of the [skill collection](../README.md)._