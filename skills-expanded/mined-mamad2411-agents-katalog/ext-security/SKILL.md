---
name: ext-security
description: Extension security specialist. Owns threat model for content-script injection, CSP, message validation across origins, secret handling, and supply-chain risk. Auto-invoked for any content-script, page-world, or cross-origin messaging code.
---

# Browser Extension Security

An extension straddles trusted and hostile contexts: content scripts read
attacker-controlled pages, and message handlers receive attacker-controlled
messages. Every boundary crossing needs a validator.

## When to reach for this

- Writing content scripts, page-world injection, or any `onMessage` /
  `onMessageExternal` handler
- Deciding where tokens and secrets live, or setting CSP for extension pages
- Adding third-party libraries or new remote endpoints to the extension
- A host-permission broadening just expanded what injected code can reach

## Principles

1. **Isolated world by default.** Inject into the page world (`world: "MAIN"`)
   only when you must touch the page's own JS state, with a written
   justification — and treat everything read there as attacker-controlled.
2. **Check `sender` on every message.** External: verify `sender.id` /
   `sender.origin` against an allowlist and constrain the surface with
   `externally_connectable` in the manifest. Internal: a message from your own
   content script is still untrusted — the script runs inside a hostile page.
3. **Schema-validate before dispatch.** JSON-shaped is not validated. Parse
   against an explicit schema, dispatch through a command allowlist, and never
   let a message field decide privilege ("isAdmin: true" from a content script).
4. **Secrets never sit in `storage.local` in clear.** It is plaintext on disk
   and readable by anything with debugger access. Prefer `chrome.storage.session`
   (in-memory, cleared on browser exit, hidden from content scripts by default)
   for tokens; long-lived credentials belong on your backend, not in the bundle.
5. **MV3 CSP bans remote code.** Extension pages default to
   `script-src 'self'; object-src 'self'` and cannot be loosened to remote
   origins — bundle dependencies, no CDN `<script>`, no `eval`/`new Function`.
6. **Pin and audit dependencies.** Extensions are prime supply-chain targets
   (store takeovers routinely arrive via a compromised dependency or buyer):
   lockfile committed, exact versions, diff review on every bump.

## Message-handler validation skeleton

```ts
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  // 1. Provenance: same extension; gate privileged commands on surface.
  if (sender.id !== chrome.runtime.id) return; // drop silently, no reply
  const fromContentScript = sender.tab !== undefined; // hostile-page context

  // 2. Shape: validate before touching any field.
  const parsed = MessageSchema.safeParse(msg); // zod or equivalent
  if (!parsed.success) return;

  // 3. Allowlisted dispatch — no dynamic property access off msg.type,
  //    and privileged commands rejected when fromContentScript.
  const handler = HANDLERS[parsed.data.type];
  if (!handler || (handler.privileged && fromContentScript)) return;
  handler.run(parsed.data).then(sendResponse);
  return true; // keep the channel open for the async response
});
```

## Pitfalls

- `externally_connectable` left undeclared — the default leaves you connectable
  by *any other extension* via `onMessageExternal`
- API keys shipped in the bundle — extension source is user-visible and scraped
  at scale; keys belong behind your own backend
- `innerHTML` with page-derived strings in popup/options pages — XSS in the
  privileged context inherits every API the extension holds
- Treating shadow DOM as a security boundary — it isolates styles, not access
- Validating only external messages while internal handlers trust content-script
  input wholesale
- Wide host permissions plus a compromised dependency = the worst-case audit
  finding; scope and supply chain multiply each other

---
*Related: `ext-permissions` (scoping what's exposed), `ext-native-messaging`
(the native-host trust boundary), `ext-ux` (security-dialog copy),
`security-checklist` (OWASP self-check, severity rating) · domain agent:
`ext-architect` · output/ADR format: `playbook-conventions`*
