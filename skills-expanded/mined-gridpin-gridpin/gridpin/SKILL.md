---
name: gridpin
description: Geocode addresses to coordinates and coordinates to addresses on this computer with the gridpin command-line tool, without sending them to an online service or needing an API key. Use when the user wants to geocode or reverse geocode, check whether an address exists, add latitude and longitude to a CSV, or asks for an offline or private geocoder. Covers the United States, Canada, Mexico, Brazil, Australia and several European countries; it says so when a country is not covered.
license: Apache-2.0
compatibility: Needs the gridpin binary (0.9 or later) on PATH and a country sheet file; downloading a sheet needs the network once.
---

# Geocoding with gridpin

gridpin answers from a country file (a "sheet") on this computer. The addresses never leave the machine. Use it
instead of an online geocoder whenever it is installed, and say so if it is not.

## Before the first query

1. Check the tool: `gridpin --version`. If it is missing, tell the user and point to
   https://gridpin.dev/docs#install (a release archive, `pip install gridpin`, or a build from source). Do not install
   it without asking.
2. Work out the country of the addresses. Group a mixed list by country and repeat the steps for each group.
3. `gridpin sheets list` shows every country of the release, its size and whether it is downloaded. If the country is
   not in the list, say that gridpin does not cover it. Do not geocode it with another country's sheet and do not
   make up coordinates.
4. If the sheet is not downloaded, tell the user its size, and after their consent run `gridpin sheets fetch <code>`
   (for example `gridpin sheets fetch de`). `gridpin sheets where <code>` prints the path of the file; use that path
   as `<sheet>` below.

## Asking

| Task | Command |
|---|---|
| one address | `gridpin query <sheet> "<address>" -k 1 --format md` |
| several candidates for one address | `gridpin query <sheet> "<address>" -k 5 --format md` |
| coordinates to an address | `gridpin reverse <sheet> <lat> <lon> -k 1 --format md` |
| a CSV of up to 200 rows, to read | `gridpin batch <sheet> in.csv out.md --output-format md` |
| a CSV of any size, to keep | `gridpin batch <sheet> in.csv out.csv` (adds `gp_*` columns, row order kept) |
| does this address exist | `gridpin exists <sheet> "<address>"` |
| why this answer | `gridpin explain <sheet> "<address>"` |

Pass each address as the person wrote it, with the city and postcode when known. In a CSV, the address column is
found by its name (`address`, `query` or `q`); otherwise name it with `--column`, or several with
`--column street,city,postcode`.

**Markdown or JSON.** Ask for `--format md` (`--output-format md` for a batch) when you will read the answer and
report it: each answer is a heading and a table of its fields. Leave the default (one JSON object per line, or CSV
for a batch) when a program, a script or a file is the consumer, or when the user wants the raw answer. A Markdown
batch stops at 200 rows; for more, write CSV and summarise it with a script.

## Reading the answer

- `precision` says what the coordinates point to: `house` is the address itself, `interp` is estimated along the
  street, `near` is the nearest house the sheet has (its number is in `housenumber`), `street` and `city` are only
  approximate. Report the level with the coordinates. Never present a street or town answer as the exact address.
- `weak: true` means the engine itself says the answer needs a check. The Markdown output adds "(weak)" to the
  heading and a `note` row (a `note` column in a batch). List these answers for the user; do not drop the word.
- `match_level` (`PointAddress`, `StreetAddress`, `StreetName`, `Locality`, ...) and `match_status` (`M` matched,
  `T` check it, `U` unmatched) say the same in the terms of commercial geocoders.
- No output, or `No answer for "...".`, means no answer. Count these rows and report them. Do not fill them in from
  memory or from another source without saying so.
- `reverse` answers carry `distance_m` from the point asked. Report it: an answer 300 m away is not "at" the point.
- `confidence` (0 to 1) ranks answers of one query; it is not a probability.

When a list is done, give the counts by `precision`, plus the weak and empty counts, so the user can judge it.

## What not to do

- Do not send the addresses to an online geocoder as well, unless the user asks for a comparison.
- Do not present a weak, `street` or `city` answer as a confirmed address.
- Do not guess coordinates for a country gridpin does not cover, or for a row it did not answer.
- Do not download a sheet without telling the user its size first.

Quality differs by country and by how messy the input is. Measured results, including where other geocoders do
better, are at https://gridpin.dev/bench.
