---
name: doctor
description: Report whether the Svipall installation on this machine will actually work — build, browser, captcha models, ports, MCP wiring — and name the fix for anything that is wrong. Use when the user runs /svipall:doctor, asks whether Svipall is set up correctly, or when a Svipall tool behaves as if a browser or a model were missing.
---

# Check the Svipall installation

```bash
svipall doctor
```

One JSON object. Read it and answer in plain words; do not paste the JSON at somebody.

- `ok: true` → say it is ready, and name what it can do: which browser would run
  (`browser.in_use`, `browser.brand`) and which captcha models are compiled in
  (`models.embedded`).
- `ok: false` → for each entry in `problems[]`, give the `message` and then the `fix`, in the
  object's own words. They are written to be relayed.

**Command not found** is itself the answer: Svipall is not installed. Offer `/svipall:setup`.

Two things worth knowing before you interpret the result:

- `dashboard_port_busy` is usually a `svipall-mcp` that is already running. Say so rather than
  sending someone to change a port they do not need to change.
- `models.embedded` being empty is not cosmetic: image captchas go to the human dashboard instead
  of being answered. Which fix applies depends on `models.inference`. With it **true** the build can
  read a model and simply has none — a source build, typically — and `svipall models install`
  downloads them. With it **false** no file can help: that build was compiled without any `onnx-*`
  feature, and the answer is a build that carries them (on Linux the `-models` archive, or the
  container image). Say which of the two this is rather than offering both.

Then check the MCP side, which `doctor` cannot see from inside the binary: call `web_status`. If it
fails while `svipall doctor` succeeds, the binary is fine and the MCP registration is not —
`/svipall:setup` step 4 has the two ways to fix it.
