---
name: routeros-api
description: Programmatic access to MikroTik RouterOS 7 through the REST API (HTTPS and JSON under /rest) and the binary API (TCP 8728 and 8729 sentences). Covers enabling www-ssl with a certificate, least-privilege users and groups (read, write, api, rest-api policies), the method-to-command mapping (GET print, PUT add, PATCH set, DELETE remove, POST any command), .proplist and .query, ids, values as strings, the 60-second request limit and per-user serialization, running scripts and exports, the sentence, word and query syntax of the binary API, tags, listen and cancel, login methods and error traps, plus a REST command-line helper script. Use when an external tool, dashboard, automation or AI agent must read or change a RouterOS device remotely.
---

# RouterOS API and REST API

Two interfaces expose the same console menus, parameters and permissions as the CLI (the CLI reference describes them): the **REST API**
(JSON over HTTPS, easiest from any language) and the binary **API** (persistent TCP connection with sentences, supports `listen` streams and tags).

## Least privilege first

Give every client its own user in its own group. Never hand an `admin` password to an automation or an AI assistant; give it a read-only user and add write
access only for actions it truly needs.

```ros
/user/group/add name=rest-read policy=read,api,rest-api
/user/add name=monitoring group=rest-read password="use-a-long-random-password" address=192.168.88.10/32
```

- REST needs both `api` and `rest-api`, plus `read` to read, `write` to change, `test` for ping, `ftp` to write or read files (export), `sensitive` to include secrets in an export.
  `/user/group/add` revokes everything not listed; `/user/group/set` changes only what it lists (`policy=!write`). Binary API users need the `api` policy.
- Restrict the transport: `/ip/service/set www-ssl available-from=192.168.88.0/24`, `/ip/service/webserver/set rest-plain=no` (REST over HTTP then answers 403), and
  keep the default firewall that drops non-LAN access; reach remote routers through a VPN (`routeros-vpn`, `routeros-firewall`). Basic authentication sends
  credentials on every request, so use HTTPS only.

## REST API

Enable HTTPS with a certificate (without one `www-ssl` offers only anonymous ciphers that clients refuse):

```ros
/certificate/add name=rest-ca common-name=rest-ca key-usage=key-cert-sign,crl-sign days-valid=3650
/certificate/sign rest-ca
:delay 3s
/certificate/add name=rest-https common-name=192.168.88.1 subject-alt-name=IP:192.168.88.1 days-valid=365
/certificate/sign rest-https ca=rest-ca
:delay 3s
/certificate/export-certificate rest-ca file-name=rest-ca
/ip/service/set www-ssl certificate=rest-https disabled=no tls-version=only-1.2
```

Copy `rest-ca.crt` to the client and trust it. Address the router exactly as the certificate names it. For a public name use Let's Encrypt (`routeros-certificates`).

| Method | Console command | Success |
| --- | --- | --- |
| GET | print | 200, record or list |
| PUT | add | 201, new record, `Location` header |
| PATCH | set | 200, changed record |
| DELETE | remove | 204, empty body |
| POST | any command (`/rest/<path>/<command>`) | 200, the command reply |

```bash
curl --cacert rest-ca.crt -u monitoring -G https://192.168.88.1/rest/ip/address -d .proplist=.id,address,interface
curl --cacert rest-ca.crt -u admin -X PUT https://192.168.88.1/rest/ip/address -H "Content-Type: application/json" \
     --data '{"address":"192.168.99.1/24","interface":"guest"}'
curl --cacert rest-ca.crt -u admin -X PATCH "https://192.168.88.1/rest/ip/address/*18" -H "Content-Type: application/json" --data '{"comment":"guest"}'
curl --cacert rest-ca.crt -u admin -X POST https://192.168.88.1/rest/system/identity/set -H "Content-Type: application/json" --data '{"name":"branch-1"}'
```

- Send `Content-Type: application/json` on PUT, PATCH and POST (else 415). A menu without records (`/system/identity`, `/ip/dns`) returns one object and is changed with POST to `set`;
  PATCH works on records only. Several records at once: POST `set` with `{".id":"*12,*13","comment":"x"}`.
- Ids start with `*`; quote such URLs and send the asterisk as is (`%2A` is not decoded). Names work as ids where records have names (`/rest/interface/ether1`). Encode other reserved
  characters (`%20`, `%2F` for a slash in a file name).
- Query parameters on GET filter by exact value (`-d type=ether -d running=true`) and `.proplist` selects properties. For other conditions POST to `print` with `{".query":["type=ether","type=vlan","#|!"],".proplist":"name,type"}`
  (API query words without `?`). `{"count-only":""}` returns `{"ret":"N"}`. `{"oid":""}` returns SNMP OIDs.
- **Replies encode every value as a string** (`"true"`, `"7"`). Requests may send strings, numbers or booleans. A flag without value is an empty string (`"once":""`); the console's unnamed argument is `numbers`.
- Errors: `{"error":404,"message":"Not Found"}`, `400` with `detail` (for example `Session closed`), `401`, `403`. A PATCH by a user without `write` fails with 400.
- **60-second limit:** the router ends longer requests. Bound commands: `ping` with `count`, monitor commands with `once`, `bandwidth-test` with a short `duration`. Longer jobs: `POST /rest/execute`
  with `{"script":"..."}` (returns a job id; add `"as-string":""` to wait for the output) and let the job write its result to the log or a file.
- **Requests of one user run one at a time**, in order; different users run in parallel. A client that gives up does not stop the command on the router. Use separate users for a dashboard and for automation,
  keep connections alive, and keep replies small with `.proplist`.
- No CORS: browsers cannot call the router directly (OPTIONS gets 503). Put a backend in between.
- Useful calls: run a stored script `POST /rest/system/script/run {".id":"daily-report"}`; export `POST /rest/export {"file":"backup"}` then read chunks with `POST /rest/file/read` (32768 bytes
  per request, `offset` increments) and `DELETE /rest/file/backup.rsc`; block an address with a timeout `PUT /rest/ip/firewall/address-list` (plus a raw-table drop rule); move a rule `POST .../move {".id":"*9","destination":"*C"}`;
  discover commands with `POST /rest/console/inspect`.

### Helper script

`scripts/rest_call.py` is a standard-library REST client. The password comes from `ROUTEROS_PASSWORD` (or a prompt), never from arguments.

```bash
export ROUTEROS_PASSWORD='...'
python scripts/rest_call.py --host 192.168.88.1 --user monitoring --ca rest-ca.crt GET /system/resource --query .proplist=board-name,cpu-load
python scripts/rest_call.py --host 192.168.88.1 --user admin --ca rest-ca.crt PUT /ip/firewall/address-list --data '{"list":"blocked","address":"203.0.113.45","timeout":"1d"}'
```

It prints JSON, exits 1 on an HTTP error (body on stderr), 3 on connection or certificate problems, 2 on bad usage. `--insecure` and `--plain-http` exist for lab use and print warnings.

## Binary API

Enable `/ip/service set api disabled=no` (TCP 8728) or use `api-ssl` (8729, needs a certificate). A client sends **sentences**: a command word, attribute words and a zero-length
word; the router answers with `!re` (data), `!done`, `!trap` (error with `message` and sometimes `category`), `!empty` or `!fatal` (connection closes).

- A word is a length-prefixed string. Lengths up to 0x7F use 1 byte, then 2, 3, 4 bytes, and `0xF0` plus four bytes; first bytes >= 0xF8 are reserved. A sentence without the terminating
  empty word is never evaluated.
- Command words start with `/` and use slashes instead of spaces (`/interface/vlan/remove`). Attributes are `=name=value` (the value may contain `=` or be empty), API attributes start with `.` (`.tag=`), queries with `?`.
- Login: `/login` with `=name=` and `=password=`; `!done` means success, `!trap` `invalid user name or password` otherwise. Accounts in the old password format use challenge-response (`=ret=` answered
  with `=response=00` plus MD5 hex); the Python 3 example implements both and includes a test vector.
- `print` has no `where`: use query words, evaluated on a stack in order (`?type=ether`, `?type=vlan`, `?#|`, `?<name=x`, `?>name=x`, `?name`, `?-name`; no regular expressions). `=.proplist=a,b`
  limits properties (omitting it can be slow for file contents and counters). `set` needs the `=.id=` (internal number or name); there is no query form, so print ids first.
- `.tag=N` lets several commands run at once and tags every reply; `/cancel` (optionally `=tag=N`) stops them. `listen` streams `!re` on changes (`=.dead=true` when an item disappears) until cancelled.
- `getall` is an alias of `print`; the `oid` properties are exposed as `<name>.oid` via `.proplist`.

## Where to look

| Need | Open |
| --- | --- |
| REST: HTTPS, users, filters, `.query`, limits, automation recipes, dashboards and AI assistants | `references/guides/developer-guides/rest-api.md` |
| Binary API: words, queries, login, tags, errors, examples | `references/guides/developer-guides/api.md` |
| Working client (sockets, login both methods) | `references/guides/developer-guides/api/python3-example.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-scripting` (what runs on the router), `routeros-users-aaa` (users, groups, policies), `routeros-certificates`, `routeros-system-utilities` (services,
`fetch` as a REST client), `routeros-management-tools`, `routeros-firewall` (limiting the web service).
