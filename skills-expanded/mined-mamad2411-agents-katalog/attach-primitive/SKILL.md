---
name: attach-primitive
description: Contract and invariants for `attach*` composition primitives, the side-effectful building blocks composed inside workspace builders. Also covers when to use `create*` (pure construction).
---

# Attach Primitives

Every persistence, sync, materializer, and binding in `packages/workspace` (plus session-shaped primitives in `packages/cli`) follows one shape. Match the invariants exactly.

## Naming

| Prefix     | Meaning                                                                                                                      |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `attach*`  | Side-effectful. Registers observers, destroy listeners, or subscription state. Return shape is free: fixed surface *or* chainable builder, both are `attach*`. |
| `create*`  | Pure construction. No listeners, no subscriptions, no destroy registration at call time. Cache constructors qualify, e.g. `createFileContentDocs` returns a `createDisposableCache` result; nothing attaches until `.open(id)` is called. |

Both return plain objects. The distinction is **what happens at call time**, not what the return value looks like. A chainable builder with `.table()/.kv()` that registers `table.observe(...)` is still `attach*`; chainability is a return-shape concern, orthogonal to naming.

## The shape

```ts
export function attachX(subject: TSubject, opts: XOptions): XAttachment;
```

**One rule.** The first argument is the subject being modified. The subject is almost always a `Y.Doc`. In the rare case where a primitive operates on an existing attachment rather than a ydoc, the subject is that attachment.

Examples of the common form:

```ts
attachIndexedDb(ydoc)                   // Y.Doc subject
attachSqlite(ydoc, { filePath })
attachSync(ydoc, { url, getToken })
attachBroadcastChannel(ydoc)
attachEncryption(ydoc, { encryptionKeys })
attachTable(ydoc, name, def)            // Y.Doc subject + slot key + def
attachTables(ydoc, defs)
attachKv(ydoc, defs)
attachAwareness(ydoc, defs)
attachRichText(ydoc) / attachPlainText(ydoc) / attachTimeline(ydoc)
```

**Chainable return is allowed** when per-entity configuration is incremental. Materializers follow the same `attachX(ydoc, opts)` shape — the builder registers specific table/kv references via `.table(ref, cfg)`:

```ts
attachMarkdownMaterializer(ydoc, { dir, waitFor })
  .table(tables.files, {
    filename: slugFilename('title'),
    // Most real tables store body content in a separate Y.Doc (via
    // createDisposableCache), so toMarkdown / fromMarkdown are typically
    // bespoke callbacks; no sugar helper can abstract the async
    // open/await/dispose cycle usefully.
    toMarkdown: async (row) => {
      using doc = fileContentDocs.open(row.id);
      await doc.whenReady;
      return { frontmatter: { id: row.id, name: row.name }, body: doc.content.read() };
    },
  })
  .kv(kv);

attachSqliteMaterializer(ydoc, { db, waitFor })
  .table(tables.posts, { fts: ['title'] });
```

Passing `tables.files` directly (rather than a string name) mirrors y-prosemirror / y-codemirror — take the specific shared resource, not a bag plus a lookup key. The materializer reads `table.name` and `table.definition` off the reference internally. All `.table()` / `.kv()` registrations must happen synchronously after construction; calls after `whenFlushed` resolves throw.

## The one exception — non-ydoc subject

When a primitive modifies a sibling attachment and the coordination is cross-package (so it can't be a method on the coordinator), it's a top-level function with the attachment as first arg:

```ts
attachSessionUnlock(encryption, { sessions, serverUrl, waitFor })
```

This is rare — one example in the whole codebase. It lives in `@epicenter/cli` and operates on an `EncryptionAttachment` defined in `@epicenter/workspace`; making it a method on the workspace type would couple packages backwards, so it stays a top-level function.

If the primitive is in-package with its coordinator, prefer method-on-coordinator (below) over a top-level `attachX(attachment, opts)`.

## Coordinator pattern (the encryption case)

When one attachment registers additional sibling attachments into itself, it owns the method surface:

```ts
const encryption = attachEncryption(ydoc, { encryptionKeys });
const tables = encryption.attachTables(defs);      // method on coordinator
const kv = encryption.attachKv(defs);
```

vs. the top-level form that would read:

```ts
const tables = attachEncryptedTables(ydoc, encryption, defs);   // ← not used; coordinator owns this
```

The method form says "use the encryption's attach-tables" directly. Preferred when the coordinator and its siblings live in the same package.

## Invariants

1. **Synchronous return.** Construction never awaits. Startup work goes into semantic `when*` promises on the returned object. Genuine async teardown exposes a `whenDisposed` promise field resolved from the `ydoc.destroy()` cascade.
2. **Teardown hooked to the subject's lifecycle.**
   - Y.Doc subject: `ydoc.once('destroy', ...)`. Never expose a `.destroy()` method on the attachment.
   - Attachment subject: use the subject attachment's disposal signal; or no teardown if there are no listeners.
   - Chainable builders (materializers): `[Symbol.dispose]()` method on the builder, unsubscribes observers.
3. **Idempotent cleanup.** If the underlying library also registers a destroy handler (like `y-indexeddb`), your handler must be safe to run alongside it.
4. **Plain data returned.** The attachment is a record of promises, functions, and occasionally mutable state. No ES classes, no getters that lazy-init.
5. **No id option on ydoc-bound primitives.** `ydoc.guid` is the identity — read it off the doc.
6. **Barrier naming is semantic, not mechanical.** Pick the name that describes the actual event:
   - `whenLoaded` — local state replayed into the ydoc (IDB, SQLite)
   - `whenConnected` — remote transport up + first exchange done (sync)
   - `whenChecked` — configuration action settled (session-unlock — resolves even if nothing was applied)
   - `whenFlushed` — initial side-effect pass done (materializer)
   - `whenReady` — bundle-level aggregate only; not on individual attachments

## Composition inside a workspace builder

Primitives compose inside a build closure:

```ts
const cache = createDisposableCache((id: string) => {
  const ydoc       = new Y.Doc({ guid: id, gc: false });
  const encryption = attachEncryption(ydoc, { encryptionKeys });
  const tables     = encryption.attachTables(schema);     // coordinator method
  const idb        = attachIndexedDb(ydoc);
  const unlock     = attachSessionUnlock(encryption, {          // non-ydoc subject
    sessions, serverUrl, waitFor: idb.whenLoaded,
  });
  const sync       = attachSync(ydoc, {
    url, getToken,
    waitFor: Promise.all([idb.whenLoaded, unlock.whenChecked]),
  });
  const markdown   = attachMarkdownMaterializer(ydoc, {           // chainable return
    dir, waitFor: sync.whenConnected,
  }).table(tables.posts, { filename: slugFilename('title') });

  return {
    ydoc, tables, encryption, idb, sync, markdown,
    whenReady: Promise.all([idb.whenLoaded, unlock.whenChecked, sync.whenConnected]),
    async wipe() {
      ydoc.destroy();
      await sync.whenDisposed;
      await idb.whenDisposed;
      await idb.clearLocal();
    },
    [Symbol.dispose]() { ydoc.destroy(); },
  };
});

export const workspace = cache.open('my-app');
```

The bundle aggregates child `whenLoaded` / `whenConnected` / `whenChecked` into one `whenReady`. Browser bundles expose `wipe()` for reset flows that must dispose and delete local storage in the right order. Daemon bundles expose `[Symbol.asyncDispose]()` as the trigger and await attachment `whenDisposed` barriers before process exit.

## The `waitFor` convention

Primitives that perform a gated startup (sync, session-unlock) accept `waitFor?: Promise<unknown>` in their options. The primitive awaits it before taking its first action. This replaces the old extension-chain "init pipeline": sequencing is now explicit at the call site, visible in one file, with no hidden ordering.

Use it whenever a primitive's startup must follow another's. Examples:
- `attachSync` after local hydrate: `waitFor: idb.whenLoaded`
- `attachSessionUnlock` after hydrate (so stored keys don't clobber freshly-hydrated plaintext mid-replay): `waitFor: persistence.whenLoaded`
- `attachSync` after both hydrate AND unlock: `waitFor: Promise.all([idb.whenLoaded, unlock.whenChecked])`

## Anti-patterns

- **Don't revive `ExtensionContext` / `RawExtension` / `defineExtension`.** Those were deleted for a reason — the lifecycle framework added a registration indirection that primitives don't need.
- **Don't wrap attachments in a `createWorkspace().with(...)` chain.** Compose inline in the factory.
- **Don't expose `dispose()` on a ydoc-bound attachment.** Destroy the Y.Doc.
- **Don't duck-type an attachment.** If you need to brand it, use a `Symbol.for` marker. See `skills/typescript` — runtime shape-checking is a code smell.
- **Don't take an `id` on a ydoc-bound primitive.** Use `ydoc.guid`.
- **Don't use `createX` for a side-effectful primitive.** If it registers listeners, it's `attach*`.
- **Don't introduce `attachEncryptedX(ydoc, encryption, ...)` top-level exports.** Use `encryption.attachX(...)`: the coordinator owns its siblings.

## Reference implementations

- `packages/workspace/src/document/attach-indexed-db.ts` — the canonical 40-line example.
- `packages/workspace/src/document/attach-sync.ts` — network variant with `whenConnected` + `waitFor`.
- `packages/workspace/src/document/attach-encryption.ts` — state-owning coordinator; exposes `attachTable` / `attachTables` / `attachKv` as methods.
- `packages/cli/src/primitives/attach-session-unlock.ts` — non-ydoc subject (cross-package exception).
- `packages/workspace/src/document/materializer/markdown/materializer.ts` — chainable builder with `.table()/.kv()`.
- `apps/whispering/src/lib/client.ts`: full singleton composition.
