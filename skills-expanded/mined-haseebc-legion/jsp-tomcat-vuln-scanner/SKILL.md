name: jsp_tomcat_vuln_scan
description: Detect security vulnerabilities in legacy Java web applications built with JSP/Servlets and deployed on Apache Tomcat. Use when the user asks to audit a JSP webapp, review WAR/exploded-webapp source for vulnerabilities, scan web.xml/context.xml/server.xml for Tomcat misconfiguration, hunt for in-memory/obfuscated Java webshells, check upload endpoints for unrestricted file upload, or pentest a Tomcat-hosted legacy Java app. Combines static source scanning with live misconfiguration probing (manager app exposure, Ghostcat, PUT-based JSP upload, TRACE). Authorized targets only.

# Legacy JSP / Apache Tomcat Vulnerability Scanner

> Adapts the agent-based "scan first, fix only after confirmation" workflow from Claude Code security-agent writeups to the JSP-on-Tomcat stack specifically: old-style Statement/JDBC concatenation, unescaped `<%= %>` output, `web.xml`/`server.xml` misconfiguration, and known Tomcat CVEs (Ghostcat, CVE-2017-12617) instead of Maven/Spring Boot dependency CVEs. Also incorporates real-world in-the-wild attacker TTPs — unauthenticated upload endpoints, Unicode-obfuscated/AES-encrypted in-memory webshells loaded via reflection, hidden credential-harvesting form fields, and server-side redirector exfiltration — documented in a case study of an actual legacy Tomcat 7 compromise (see `references/vuln_patterns.md` §12-16).

## Inputs
- **Static mode:** a path to JSP/Servlet source — an exploded WAR, `webapps/<app>/` directory, or a source checkout containing `.jsp`/`.java` files and `WEB-INF/{web.xml,lib/}`. No network access needed.
- **Live mode:** a base URL of a running Tomcat instance you are authorized to test, e.g. `https://target.tld:8443`. Makes real HTTP(S) requests.
- Use static mode when you have the codebase (most legacy-app audits); use live mode when you only have a deployed instance, or run both and cross-reference.

## Workflow

### Phase 1: Recon — fingerprint the stack
Before scanning, confirm this is actually a JSP/Tomcat target and note the version:
- Static: check `WEB-INF/lib` for Tomcat-bundled jars, `META-INF/MANIFEST.MF`, or a `RELEASE-NOTES`/`ServerInfo.properties` if the Tomcat install itself is in scope. Note the servlet-api version in `web.xml`'s `<web-app>` root element (`2.3`–`6.0`) — pre-3.0 (no annotations, XML-only routing) is a strong "legacy" signal.
- Live: `curl -sI https://target.tld/` and request a path guaranteed to 404 — legacy/unhardened Tomcat often leaks `Apache Tomcat/X.Y.Z` in the `Server` header or the default error page body.

Record the Tomcat version — cross-reference against `references/vuln_patterns.md`'s CVE table (Ghostcat, CVE-2017-12617, etc. are version-gated).

### Phase 2: Static source scan
```bash
scripts/jsp_scan.sh /path/to/webapp
```
Recursively greps every `.jsp`/`.jspx`/`.java` file for the classic legacy-JSP vulnerability idioms (raw `Statement` concatenation, `<%= request.getParameter(...) %>` echoed unescaped, `Runtime.exec`, path-traversal-prone `File`/stream constructors, XXE-prone parser factories, `ObjectInputStream`/`readObject`, hardcoded DB credentials), then separately checks `WEB-INF/{web.xml,context.xml}` and any `server.xml`/`tomcat-users.xml` in scope for the configuration issues in Phase 2b, and lists `WEB-INF/lib/*.jar` so you can spot known-vulnerable bundled libraries (old `commons-collections`, `struts2-core`, `log4j` 1.x/2.x<2.17).

It also runs the in-the-wild-derived checks from Phase 2c below in the same pass.

Output is grouped by category with `file:line` refs — treat every hit as a lead to manually confirm, not a confirmed finding (see Notes below).

### Phase 2b: Config review (folded into the same script, but reason about it explicitly)
For each config file found, check against `references/vuln_patterns.md`'s config checklist: missing `<security-constraint>`, `listings=true` on the default servlet, `readonly=false` on the default servlet (enables PUT — see CVE-2017-12617), missing `<cookie-config><http-only>`/`<secure>`, `allowTrace="true"` on Connectors, weak/default `tomcat-users.xml` credentials, `crossContext="true"`.

### Phase 2c: In-memory webshell, upload, and exfiltration IOC checks (in-the-wild TTPs, see `references/vuln_patterns.md` §12-16)
The same `jsp_scan.sh` run also looks for the concrete attacker patterns from a documented legacy Tomcat 7 compromise, since these evade classic file-based/token-based scanning entirely:
- **Unrestricted upload endpoints** — `request.getPart(`, `Part.write(`, `ServletFileUpload`/`FileItem` usage without an obvious nearby extension/auth check (§12).
- **In-memory/obfuscated loaders** — `Cipher.getInstance("AES` co-occurring with `defineClass(`/`Method.invoke(`/`Class.forName(` in the same file, "magic method" (`equals()`/`hashCode()`/`toString()`) bodies containing `Runtime.exec`/`Cipher`/`defineClass`, and files with an abnormally high density of `\uXXXX` Unicode escapes (§13).
- **Hidden credential-harvesting fields** — `type="hidden"` or CSS-hidden inputs named like `cvv`/`card`/`expir` in JSP templates (§14).
- **Redirector/egress endpoints** — hardcoded external `new URL("https://...")`/`HttpURLConnection` destinations (§15).
- **Known decoy filenames** — `rd.jsp`, `error403.jsp`-style names, and stray `.sqm` files if scanning a live/exploded deployment rather than a clean source checkout (§16).

These are IOC-style leads, not proof — a hit here means "read this file closely," especially since some (e.g. `.sqm` files, decoy error-page names) are only meaningful when scanning an actual deployment directory rather than a version-controlled source tree.

### Phase 3: Live misconfiguration & known-CVE probing
```bash
scripts/tomcat_probe.sh -u https://target.tld:8443
```
Checks, non-destructively: exposed `/manager/html` and `/host-manager/html`, leftover default `/examples/` and `/docs/` webapps, direct `/WEB-INF/web.xml` access (source/config disclosure), allowed HTTP methods (`OPTIONS`) and a `TRACE` reflection test, `JSESSIONID` cookie flags, a stack-trace-disclosure probe, whether the AJP port (8009) is reachable (Ghostcat/CVE-2020-1938 — file read via AJP; flag for follow-up with a dedicated AJP tool, not exploited here), and whether `PUT` is accepted by the default servlet (CVE-2017-12617 precondition — the script tests with a harmless `.txt` file only; see `references/vuln_patterns.md` for why it deliberately does not attempt a `.jsp` PUT).

### Phase 4: Manual verification / exploitation (not automated)
Static-scan hits and live-probe flags are leads, not proof. For each:
- SQLi hits → confirm with `sql-injection-tester` skill's probe script against the specific parameter.
- XSS hits → confirm the output actually reaches the browser unescaped (view source / trigger with a benign marker string, not a live `<script>` payload, until scope confirms it's fine).
- PUT/readonly=false findings → only attempt an actual `.jsp` webshell upload if the engagement scope explicitly authorizes RCE proof, and clean up the uploaded file immediately after.
- AJP/Ghostcat → verify with a dedicated PoC/NSE script (`nmap --script ajp-request` or a maintained Ghostcat PoC), since crafting raw AJP packets is out of scope for this skill's bash tooling.
- Upload-endpoint hits (§12) → confirm there's genuinely no auth/extension/magic-byte check by reading the handler method in full, not just the `getPart`/`FileItem` line.
- In-memory loader / obfuscation hits (§13) → don't try to decrypt or execute a suspected payload as part of a "confirm the finding" step; treat any `Cipher`+reflection co-occurrence or dense `\uXXXX` file as confirmed-enough to report and escalate, since safely detonating an unknown loader is out of scope for source review.
- Hidden-field hits (§14) → diff the JSP against version control / a known-good backup rather than trying to decide "is this legitimate" from the regex hit alone.
- Redirector/egress hits (§15) → confirm the destination host against the application's documented external integrations before flagging as malicious; plenty of legitimate apps call out to a payment gateway or webhook.

### Phase 5: Report
Map confirmed findings to OWASP Top 10 / CWE and, where relevant, the MITRE ATT&CK mapping (both in `references/vuln_patterns.md`) and give a PASS/WARN/BLOCK-style severity call per finding, plus the specific remediation (parameterized queries, `<c:out escapeXml="true">`, disabling external entities, upgrading the bundled library, tightening `web.xml`, adding upload validation/egress controls).

## Notes / tips
- **This is a legacy-stack skill on purpose.** Modern Spring Boot / Jakarta EE apps have their own idioms (JPA, `@RestController`, dependency-managed BOMs) — point Maven/Gradle dependency-CVE questions elsewhere. This skill assumes raw JDBC, scriptlet-heavy JSP, `web.xml`-based config, and a standalone Tomcat, which is exactly the profile of most still-running "legacy" Java web apps.
- **Grep-based static scanning is a heuristic, not proof.** A `Statement` + `+` hit next to a hardcoded string isn't necessarily injectable if the concatenated part never touches user input three lines up — read the surrounding method, don't just count regex hits.
- **Bundled-library CVEs matter as much as custom code.** A legacy app with a 2013-era `commons-collections-3.1.jar` in `WEB-INF/lib` is an insecure-deserialization RCE waiting for any `ObjectInputStream.readObject()` call in the app or a container-level gadget chain (ysoserial) — flag the jar even if you find no obvious `readObject` call yourself.
- **Don't leave a webshell behind.** If a PUT-based JSP upload is confirmed as part of an authorized RCE proof, delete it immediately and note the exact filename/timestamp in the report.
- **No CVE required.** A real documented compromise of a legacy Tomcat 7/Java 7 deployment went from unauthenticated upload to credential harvesting to C2 callback using nothing but insecure-by-default behavior — no zero-day, no CVE. Don't let "the version isn't in the CVE table" stand in for "this is fine"; architectural weaknesses (permissive upload, no egress control, no reflective-loading detection) are often the whole story.
- **Static scanning has a real blind spot here.** Unicode-escaped source and AES-encrypted-until-runtime payloads are specifically designed to defeat token-based grep/SAST — a clean `jsp_scan.sh` run is evidence of absence only for the patterns it knows to look for, not proof the app is clean. Pair static scanning with the IOC checks in Phase 2c, and note that in-memory-only artifacts may require host-level/JVM-level analysis (heap dump, Java Agent instrumentation) to catch what source review alone cannot.
- **Prevention checklist** (for reports): parameterized queries/`PreparedStatement` everywhere, `<c:out escapeXml="true">`/`StringEscapeUtils` on all reflected output, disable external entities on every `DocumentBuilderFactory`/`SAXParserFactory`/`XMLInputFactory`, remove `/examples`, `/docs`, `/manager` from production, set `readonly=true` and disable `listings` on the default servlet, set `<cookie-config><http-only>true</http-only><secure>true</secure></cookie-config>` in `web.xml`, keep Tomcat and every `WEB-INF/lib` jar patched, prefer upgrading off scriptlet-style JSP toward JSTL/EL with auto-escaping where the app can tolerate the change, require auth + extension/magic-byte allowlisting on every upload endpoint with storage outside the servable webroot, add egress filtering so the app tier can't call out to arbitrary hosts, and — for high-risk legacy targets — consider a Java Agent/RASP to catch reflective class loading and crypto-plus-reflection combinations that static analysis will miss.

Adapts the scan/fix/verify agent workflow described in "Use of Claude Code Agents in Mitigating Application Vulnerabilities" (mchathuranga4, Medium) to the legacy JSP-on-Tomcat stack, and incorporates real-world attacker TTPs and remediation guidance from "From Foothold to Callback: Memory-Resident Payloads and Architectural Weaknesses in a Legacy Java Platform" (Chaudhary, Cadinouche, Chiapponi, Demazeau — Amadeus IT Group).
