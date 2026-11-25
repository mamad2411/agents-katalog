---
name: use-map
description: >
  Addresses, routes and delivery order — the project's own map service. Load it when the owner says
  "show it on a map", "how far is it", "in what order should the courier drive", "find the address",
  or before you reach for Google Maps and a paid key. The thing nobody guesses from inside the guest
  layer: this exists, it costs nothing per call, and it answers with real road distances — but only
  for the region whose map was loaded, and loading one is a heavy background job that the owner
  starts, not you.
---

# use-map

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The door and the credential are in `use-data`. Unlike vectors and the knowledge base, **there is no
helper for maps in this project yet** — you call the door directly with `dataFetch`. Writing that
helper the first time you need it is welcome; writing a second address or a second key is not.

---

## 1. Four questions it answers

🔒 **The address is DOUBLED, and this is the trap that a cold run caught (2026-08-23).** The proxy
strips exactly `/service/<name>`, and this service carries a `/geo` prefix of its own — so the path
is `/service/geo/geo/<route>`. Written singly it reaches the service as `/geocode`, which does not
exist there, and the answer is an HTML `Cannot POST /geocode` — not a JSON error you would recognise.

```ts
await dataFetch("/service/geo/geo/optimize", { method: "POST", body: JSON.stringify({ coords }) })
```

The neighbours are not like this: the knowledge base answers at its root (`/service/rag/query`) and
channels too (`/service/channels/status`). Ask `/capabilities` for the prefixes, then check the
service's own route once — a 404 in HTML is what a wrong prefix looks like here.

All calls are server-side, through `dataFetch`.

| Route | Ask it | Answers |
|---|---|---|
| `/service/geo/geo/geocode` | `{ q: "street, house, city" }` | `{ lat, lon, name }` · 404 when not found |
| `/service/geo/geo/route` | `{ coords: [{lat,lon}, …] }` in YOUR order | `{ geometry, distanceKm, durationMin }` |
| `/service/geo/geo/matrix` | `{ coords: [...] }`, 2 or more | `{ distances, durations }` — N×N arrays, **metres and seconds** |
| `/service/geo/geo/optimize` | `{ coords: [...] }` | `{ order, geometry, totalKm, totalMin }` |

🔒 **THE UNITS DIFFER BETWEEN NEIGHBOURING ROUTES, and nothing warns you.** Measured live
2026-08-23, Eiffel Tower → Louvre: `route` answered `distanceKm: 4.29`, `durationMin: 10.5`, while
`matrix` answered `4303.9` and `632.1` **for the same pair** — metres and seconds, straight from the
routing engine. Read a matrix cell as kilometres and you are wrong by a factor of a thousand, in a
number that still looks plausible on a delivery screen.

```
matrix   → {"distances":[[0,4303.9],[4039.4,0]], "durations":[[0,632.1],[610.8,0]]}   // m, s
route    → {"geometry":…, "distanceKm":4.29, "durationMin":10.5}                      // km, min
optimize → {"order":[0,1,2], "geometry":…, "totalKm":6.79, "totalMin":17.19}           // km, min
```

🔒 **The matrix is NOT symmetric.** `4303.9` there against `4039.4` back — one-way streets are real.
Averaging the two directions, or reading one cell for both, quietly invents a road that does not exist.

*(This block exists because a cold acceptance run had to GUESS the units: the skill said only «raw
material for your own logic». A guess that lands on the right answer is still a guess.)*

🔒 **`route` keeps your order; `optimize` chooses one.** Sending points to `route` and calling the
result "the optimal delivery route" is the mistake this pair exists to prevent — it is the length of
the order you happened to pass.

## 2. 🔒 Real roads, not straight lines — and that is the point

Distances come from a routing engine over real road geometry, so a river without a bridge costs what
it really costs. A straight-line ("as the crow flies") calculation of your own is not a cheaper
approximation of this; it is a different number that will disagree with the driver.

Nothing here is billed per call: the engines run on this server. That is the argument against reaching
for a paid map API for distance work — the key, the quota and the invoice are the things you would be
adding, not the capability.

## 3. 🔒 It only knows the region that was loaded

The map data covers one region at a time — the one the owner provisioned. Ask for a route in another
country and the answer is an error, not a longer route.

```
GET /service/geo/geo/provision-status   → { state: "idle" | "downloading" | "processing" | … , region, step }
```

**`state` is a normal part of the product, not an exception.** While a region is being prepared, the
service answers with errors; a page that shows "the map is being prepared" is honest, a page that
shows a blank map is broken. Only one provisioning runs at a time — a second request gets `409`, with
the name of the region already being built.

🔒 **Starting a provisioning is the OWNER's action**, from the panel: it downloads and processes
several gigabytes and takes a long time. Do not trigger it from application code, and do not offer it
as a fix inside a page.

## 4. What the map service is not

- **Not a tile server for the picture.** These routes return numbers and geometry. Whatever draws the
  map in the browser is a separate decision (and a widget, `use-widgets` — with its own rule that the
  content must exist without JavaScript).
- **Not a geocoder for bulk imports.** It is a single service on the owner's machine; a thousand
  addresses at once will be slow and unkind. Geocode when a row is written, store `lat`/`lon` in the
  row, and never geocode the same address twice.
- **Not authoritative about addresses.** `geocode` returns the first match. For a form where a person
  types their own address, show them what was found and let them confirm — silently accepting the
  first match is how parcels go to the wrong street.

## 5. Before you call it done

1. `route` versus `optimize` chosen deliberately, and the step says which.
2. Coordinates stored on the row, not recomputed per render.
3. The "region not ready" and "address not found" paths exist in the product, in the user's language.
4. Tested with real points of the loaded region — a route between two invented coordinates proves
   nothing about the map the owner actually has.
