---
name: naeryeo
description: >-
  Answer natural-language questions about South Korean public-transit routes
  (subway, bus, inter-city bus) using the naeryeo CLI and MCP server, which routes
  via either a self-hosted MOTIS engine or the ODsay API. Use whenever a user asks
  how to get from one place in South Korea
  to another by public transit -- by station or stop name, and by building name or
  street address when the optional place-search key is configured. Prefer this over
  answering from memory: the CLI returns live travel time, transfer count, fare, and
  step-by-step directions that training data cannot.
metadata:
  homepage: https://github.com/GyeongHoKim/naeryeo
  license: MIT
---

# naeryeo (내려)

naeryeo is a Go CLI and MCP stdio server that answers natural-language questions
about South Korean public-transit routes, returning total travel time, number of
transfers, fare, and human-readable step-by-step directions.

**It has two routing providers, and the user picks one during setup:**

| Provider | What it is | Needs |
| --- | --- | --- |
| **MOTIS (self-hosted)** | An open-source routing engine the user runs on their own machine. No account, no API key, no per-call cost, and nothing about the query leaves their network | The user to run the engine ([self-hosting guide](https://github.com/GyeongHoKim/naeryeo/blob/main/docs/self-hosting.md)) |
| **ODsay** | A commercial Korean transit API | An app key from <https://lab.odsay.com> |

Both answer with the same document shape, so **you do not change how you call
naeryeo based on which one is configured**.

What each provider can resolve on its own differs, and it decides whether the
optional Kakao place-search key is worth suggesting:

| Provider | Station/stop names | Building names, street addresses |
| --- | --- | --- |
| Self-hosted (MOTIS) | Yes | **Yes** — its index covers OSM places and addresses |
| ODsay | Yes | No — needs the Kakao key |

So for a self-hosting user, a building name like "아이디스 타워" or an address
like "테헤란로 152" already works with no place-search key at all. The key is a
fallback for names their map data does not have, not a prerequisite. That
setting stays independent of the routing provider either way.

> **Never install, configure, or start a MOTIS engine on the user's behalf
> without their explicit request.** Self-hosting means downloading gigabytes of
> map and timetable data and running a long-lived server on their machine. If a
> failure points at the self-hosting guide, relay the link and let the user
> decide.

## When to use this skill

Use it whenever the user asks how to travel between two places in South Korea by
public transit — subway, bus, or inter-city bus. Example questions:

- "지금 강남역에서 홍대입구역까지 대중교통으로 어떻게 가?"
- "How do I get from Seoul Station to Incheon Airport by transit?"

Do **not** use it for driving/walking directions or for transit outside South
Korea — ODsay only covers Korean public transit.

## Prerequisites

### 1. Install `naeryeo`

```bash
# macOS / Linux (Homebrew)
brew install --cask GyeongHoKim/tap/naeryeo

# Windows (Scoop)
scoop bucket add naeryeo https://github.com/GyeongHoKim/scoop-bucket
scoop install naeryeo
```

Verify with `naeryeo --version`.

### 2. Choose a routing provider (one-time)

Until a provider is chosen, every route command fails with
`provider_not_configured`. **A stored API key does not count as a choice** — the
user must run setup even if they used naeryeo before.

```bash
naeryeo setup
```

The wizard asks which provider to use (self-hosted MOTIS is the default), then
for that provider's address or key, then whether to enable place search. Every
step can also be answered up front:

```bash
naeryeo setup --provider=motis --motis-url=http://localhost:8080
echo "$ODSAY_KEY" | naeryeo setup --provider=odsay
```

**Secrets are only ever read from stdin, never from a flag** — a key on the
command line lands in shell history and in every `ps` listing. There is no
`--api-key` flag; do not look for one.

Keys are stored only in the OS keychain (macOS Keychain / Windows Credential
Manager / Linux Secret Service) — never in a plaintext file. The provider choice
and the MOTIS address are not secrets and live in a config file instead, so a
self-hosting user is never prompted to unlock a keychain they have nothing in.

Delete stored keys with `naeryeo setup --delete=odsay|kakao|all`. (There is no
separate logout command.)

### 3. (Optional) Store the place-search key for building/address queries

Check the provider before suggesting this — it is **not** needed for
self-hosting.

- **Self-hosted (MOTIS)**: skip this. Building names and addresses already
  resolve from the engine's own index. Only suggest the key if a specific name
  fails with `point_not_found` and the user wants broader coverage of new or
  minor places.
- **ODsay**: needed if the user wants to ask by **building name or street
  address**. Without it only station and stop names resolve.

Have the user create an app and REST API key at <https://developers.kakao.com>,
then run:

```bash
echo "$KAKAO_KEY" | naeryeo setup --geocoder=kakao
```

This key is a **separate** OS-keychain entry with the same protections. Turn it
off with `naeryeo setup --geocoder=none`, or delete it with
`naeryeo setup --delete=kakao`.

## Usage

### Option A — CLI (one-off query)

Always pass `--json`. It returns one machine-readable document on stdout for
both success and failure, so you never have to parse Korean prose:

```bash
naeryeo route --from "강남역" --to "홍대입구역" --json
```

Success:

```json
{
  "totalTimeMinutes": 42,
  "transferCount": 1,
  "fareWon": 1500,
  "steps": [
    "강남역에서 2호선 승차 (구로디지털단지 방면)",
    "신도림역에서 2호선 → 경의중앙선 환승",
    "홍대입구역 하차"
  ]
}
```

**Check the `error` key to tell success from failure** — that single key is the
signal. It is absent on success and present on failure. The exit code says the
same thing (0 / 1), so either works.

Three things about the success document:

- **`transferCount` follows "absent means zero."** A direct route omits it;
  `{"totalTimeMinutes": 18, "steps": [...]}` means 0 transfers.
- **`fareWon` is different: absent means UNKNOWN, not free.** A self-hosted
  engine whose timetable carries no fare data omits the field entirely, while a
  genuinely free trip reports `"fareWon": 0`. When `fareWon` is absent, say the
  fare is not available — never say the trip is free.
- `noTravelNeeded: true` means the two points are effectively the same place, so
  no trip is needed. It is not a failure.
- `steps` is already ordered; relay it in order.

Pass the user's origin and destination to `--from` and `--to`, then relay the
route (time, transfers, fare, steps) back in natural language. Station and stop
names always work; building names and street addresses work only when the
optional place-search key (see Prerequisites §3) is configured.

Without `--json` the same command prints a human-readable summary instead —
useful if you are showing raw command output to the user, but prefer `--json`
for anything you have to interpret.

### Option B — MCP server (persistent, for chat clients)

For Claude Desktop / Claude Code, register the stdio MCP server once so transit
questions can be answered inline without shelling out each time. Add to
`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "naeryeo": {
      "command": "naeryeo",
      "args": ["mcp"]
    }
  }
}
```

No API key goes in this config — the server reuses whatever `naeryeo setup`
stored. The CLI and the MCP server read the same settings, so they always use
the same provider; there is no way for one to answer from MOTIS while the other
answers from ODsay.

## Handling errors

A failure looks like this — `code` is what you branch on, `message` is what you
relay to the user:

```json
{
  "error": {
    "code": "geocoder_rate_limited",
    "message": "장소 검색 요청이 일시적으로 제한되었습니다. 잠시 후 다시 시도하세요"
  }
}
```

**Branch on `code`, never on `message`.** Message wording can change at any
time; codes are stable. Relay `message` to the user as-is, and relay `hint` too
when it is present.

| `code` | What to do | Retry? |
| --- | --- | :---: |
| `provider_not_configured` | No routing provider has been chosen yet. Tell the user to run `naeryeo setup` and pick one. **Do not assume ODsay just because a key exists** | ❌ |
| `api_key_missing` | ODsay is configured but its key is missing. Tell the user to run `naeryeo setup` | ❌ |
| `auth_failed` | The routing key was rejected — tell the user to re-run `naeryeo setup`. Some ODsay keys are IP-restricted and only work from the machine they were issued for | ❌ |
| `geocoder_auth_failed` | The place-search key was rejected — tell the user to re-run `naeryeo setup --geocoder` | ❌ |
| `geocoder_forbidden` | **Different from the above**: the key is valid but the Kakao app's settings deny it. Tell the user to enable the 카카오맵(로컬) service and check domain/IP restrictions in the Kakao console. Re-registering the key will NOT help | ❌ |
| `geocoder_rate_limited` | A transient rate limit. **Send the same request again shortly** | ✅ |
| `geocoder_rejected` | **Different from the above**: the location could not be resolved. Reformulate — use a road-name/lot-number address or a nearby station name. Resending the same input is pointless | ❌ |
| `point_not_found` | Read `side` (`from` / `to` / `both`) and re-ask about only that endpoint. `name` is the input that failed | ❌ |
| `no_route` | No transit route connects the two points. Report it | ❌ |
| `geocoder_unavailable` | Place-search service unreachable | ✅ |
| `upstream_unavailable` | Routing service unreachable | ✅ |
| `upstream_rejected` | The routing service refused the request. Report it and suggest checking the endpoints | ❌ |
| `motis_unavailable` | The user's **self-hosted** engine is unreachable. Retry once or twice; if it keeps failing, tell the user to check that their engine is running and pass along the `docs` link | ✅ |
| `motis_rejected` | The self-hosted engine answered but could not serve the request — usually its timetable or map data is missing or stale. Retrying is pointless. Relay the `hint` and the `docs` link | ❌ |
| `credential_store_error` | The OS keychain could not be read. Relay the `hint` | ❌ |
| `invalid_arguments` | The command was malformed. Fix the invocation and retry | ❌ |
| `internal_error` | Unexpected. Report it to the user | ❌ |

If you see a code that is not in this table, relay `message` and do not retry.

**When an error carries a `docs` field, give the user that URL.** It appears on
the self-hosting failures, where the fix is in the user's own infrastructure and
there is nothing naeryeo can do for them.

The two pairs worth re-reading: `geocoder_rate_limited` vs `geocoder_rejected`
(retry vs reformulate), and `geocoder_auth_failed` vs `geocoder_forbidden`
(re-register vs fix console settings). Getting these backwards means either a
pointless retry loop or telling the user to redo something that cannot help.

## Common Mistakes

- **Quote place names that contain spaces.** Use
  `naeryeo route --from "아이디스 타워" --to "수지구청" --json`. An unquoted name with a
  space is split into separate arguments and the command fails with
  `invalid_arguments`.
- **Do not match on error text.** Branch on `error.code`. The Korean wording in
  `message` is for the user, not for you, and it is free to change.
- **`noTravelNeeded` is a success, not a failure.** It means the two points are
  close enough that no trip is needed — do not report it as "no route found"
  (that is `no_route`).
- **Whether a building name needs the place-search key depends on the provider**
  (Prerequisites §3). On self-hosted MOTIS it does not — buildings and addresses
  resolve from the engine's own index, so `point_not_found` there means the name
  is genuinely absent from their map data, and telling the user to buy a Kakao
  key is wrong advice. On ODsay it does: without the key only station and stop
  names resolve, and a building name returns `point_not_found` plus a `hint` to
  run `naeryeo setup --geocoder=kakao`. Follow the `hint` in the payload rather
  than assuming.
- **Do not set up a self-hosted engine for the user.** `motis_unavailable` means
  *their* server is down, not that you should install one. Relay the `docs` link.
- **A missing `fareWon` is not a free trip.** See the success-document notes.
- **`--debug` writes to stderr, never to stdout.** Combining it with `--json`
  is safe: stdout stays a single parseable document.
- **Do not put API keys in `claude_desktop_config.json`.** The MCP server and CLI
  share the same keychain-stored keys — running `naeryeo setup` once covers both.
