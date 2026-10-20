---
name: face-value-only
skill_id: browser-skill:face-value-only
description: Getting into a sold out show at the price on the ticket
when_to_use:
  - intent_keywords: [sold out, resale, face value, scalper, spare ticket, waitlist, returns]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: face value returns, wait lists and official exchanges for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which seller is the official box office and which is resale for
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: chasing
    current_value: face value tickets for a sold out show
    fill_rule: say the show and the city
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [tickets, sold out, face value, resale, live music]
    related_skills: []
platforms: [macos]
---
# Face value only

## Purpose
A sold out show is rarely actually gone. This finds the returns, the official exchanges and the day-of releases, and names the price before anyone pays four times face for a listing that may not exist yet.

## Reads
- Search results for face value returns, wait lists and official exchanges for face value tickets for a sold out show.
- Search results for which seller is the official box office and which is resale for face value tickets for a sold out show.

## Lands in
- Goes to the platform's own return channel first. Short enough to act on straight away.

## Steps
1. Look up face value returns, wait lists and official exchanges for face value tickets for a sold out show.
2. Look up which seller is the official box office and which is resale for face value tickets for a sold out show.
3. Goes to the platform's own return channel first. DICE runs a wait list where a returned ticket sells for exactly what the first buyer paid, and Ticketmaster's Face Value Exchange caps resale at the price paid with no markup.

## Success criteria
- Goes to the platform's own return channel first. DICE runs a wait list where a returned ticket sells for exactly what the first buyer paid, and Ticketmaster's Face Value Exchange caps resale at the price paid with no markup.
- Knows the wait list is a promoter switch, not a platform feature. A sold out event with no wait list means the promoter turned it off, not that nothing came back.
- Sends the user to the box office on the day, since venues release production holds, unclaimed guest list and returns the day of the show, at face value and usually without the online service fee.
- Flags a listing that exists before the general sale has even happened as speculative. That seller does not hold a ticket and is betting on buying one later, which is how people end up with nothing at the door.
- Prices in the tier trap. Platforms that sell in releases resell a returned early bird ticket at the top tier price, so a ten dollar ticket can come back at thirty and still get called face value.
- Reads the all-in total, because US ticket sellers have been required to show fees up front since May 2025, and a page still hiding them until checkout is a reason to leave.

## Failure behavior
- If a page will not load, skip it and keep going.
- If there is no face value route at all, say so in one line and name the next show by the same artist or crew.

## Never
- Never sign in, buy, resell, refund or join a wait list.
- Never invent a price, an availability or a return policy.
- Never present a resale page as the official box office.

## Redaction
Omit query strings, account details, ticket orders, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
