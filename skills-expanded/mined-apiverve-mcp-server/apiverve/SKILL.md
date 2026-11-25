---
name: apiverve
description: Use APIVerve tools for live or validated data the model can't produce itself, such as IP and DNS lookups, email, phone and IBAN validation, exchange rates, SSL certificates, WHOIS, VIN decoding, weather and SEC filings.
---

# APIVerve

The APIVerve MCP server exposes one read-only tool per API (IPLookup, EmailValidator, ExchangeRate, SSLCertificateChecker, DNSLookup, VINDecoder and so on). The first call opens an APIVerve sign-in; the connection then uses that account's API key.

- Pick the most specific tool for the question rather than chaining general ones. Tool names match the API names on https://apiverve.com/marketplace.
- Every call costs credits (shown in each tool's description), so don't repeat a call whose result you already have.
- Results arrive as structured content; `null` fields mean "not available for this input or plan". Fields marked premium need a higher plan.
- Errors: 401 means the API key is invalid, 403 means the account is out of credits (not a bad key), 429 is a brief rate limit, so retry after a moment.
- Usage and plan are at https://dashboard.apiverve.com.
