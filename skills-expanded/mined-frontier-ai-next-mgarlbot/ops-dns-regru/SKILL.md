---
name: ops_dns_regru
description: Point a subdomain to IPv4 via REG.API 2 (zone/get_resource_records, zone/add_alias); credentials from REGRU_* in the environment
triggers: [regru, reg.ru, dns, subdomain, a record, zone, nss, рег.ру, поддомен, зона]
tools: [shell]
platform: all
---

## REG.API 2 — documented calls only

Official docs: [REG.API 2](https://www.reg.ru/reseller/api2doc).

Zone base URL: ``${REGRU_API_BASE_URL}/api/regru2/zone/<function>`` (default host `https://api.reg.ru`).

Bot process credentials (exported from settings into ``os.environ``): ``REGRU_API_USERNAME``, ``REGRU_API_PASSWORD``, optional ``REGRU_DNS_ZONE`` (apex zone, e.g. `example.ru`).

**Do not** print the password or full API responses to the user; log-level summaries with `result` / `error_text` only.

### Prerequisite

The domain must use REG.RU nameservers (`ns1.reg.ru` / `ns2.reg.ru`), otherwise the API returns ``DOMAIN_IS_NOT_USE_REGRU_NSS``.

### 1) List current records

POST `Content-Type: application/x-www-form-urlencoded`, fields `input_format=json`, `input_data` = **one-line** JSON string (per docs). Zone examples include `username` / `password` **inside** `input_data`.

Build JSON with Python (avoids password showing up in `ps` from inline flags — use env only):

```bash
REGRU_ZONE="${REGRU_DNS_ZONE:?set REGRU_DNS_ZONE}"
INPUT_DATA="$(REGRU_ZONE="$REGRU_ZONE" python3 -c '
import json, os
z = os.environ["REGRU_ZONE"]
print(json.dumps({
  "username": os.environ["REGRU_API_USERNAME"],
  "password": os.environ["REGRU_API_PASSWORD"],
  "domains": [{"dname": z}],
  "output_content_type": "json",
}))
')"
curl -sS -X POST "${REGRU_API_BASE_URL}/api/regru2/zone/get_resource_records" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "input_format=json" \
  --data-urlencode "input_data=${INPUT_DATA}"
```

### 2) Add A (IPv4) for a subdomain — `zone/add_alias`

Parameters (doc §9.2): `domains` — list of `{dname}`, shared `subdomain` label without the zone (`www`, `api`, or `@` for apex), `ipaddr`.

Example: subdomain `app` → IP `203.0.113.10`:

```bash
REGRU_ZONE="${REGRU_DNS_ZONE:?set REGRU_DNS_ZONE}"
export SUB="${SUBDOMAIN:-app}"
export IP="${TARGET_IPV4:?set TARGET_IPV4}"
INPUT_DATA="$(REGRU_ZONE="$REGRU_ZONE" python3 -c '
import json, os
z, sub, ip = os.environ["REGRU_ZONE"], os.environ["SUB"], os.environ["IP"]
print(json.dumps({
  "username": os.environ["REGRU_API_USERNAME"],
  "password": os.environ["REGRU_API_PASSWORD"],
  "domains": [{"dname": z}],
  "subdomain": sub,
  "ipaddr": ip,
  "output_content_type": "json",
}))
')"
curl -sS -X POST "${REGRU_API_BASE_URL}/api/regru2/zone/add_alias" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "input_format=json" \
  --data-urlencode "input_data=${INPUT_DATA}"
```

If the user gives only an FQDN (`app.example.ru`), split: `dname=example.ru`, `subdomain=app`.

### 3) Idempotency

Before `add_alias`, prefer `get_resource_records`: if an **A** with the right `content` and `subname` already exists, do not duplicate (or use documented update flows if the IP must change).

### Test API endpoint

If the account has a separate test endpoint (doc §2.5), set `REGRU_API_BASE_URL` accordingly in `.env`.
