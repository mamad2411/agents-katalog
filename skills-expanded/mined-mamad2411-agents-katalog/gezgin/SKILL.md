---
name: gezgin
description: Explore destinations, places, activities, derived city-and-interest community views, canonical Events, concrete EventInstances, and privacy-safe member matches with AI-first Gezgin data, then coordinate explicit profile, presence, interest, follow, and participation actions. Use when a user asks what to do, whom to meet, where to go, destination research, personalized travel planning, member discovery, city community discovery, presence, or meetup coordination.
metadata:
  skill-contract-version: "3.0.2"
---

# Gezgin

Use the tools supplied by the declared Gezgin MCP dependency to complete the user's travel or community goal.

## Keep the runtime boundary

- Treat the live MCP catalog, schemas, metadata, and results as authoritative.
- This installed package implements Gezgin Skill Contract `3.0.2` and targets Gezgin Agent Contract `3.0.2`. On the first Gezgin use in a task and after a reconnect or update, inspect the live `gezgin/minimumSkillContractVersion` metadata when the client exposes it. Update only when that minimum is newer than the installed skill-contract version; do not add timer-based probes or extra tool calls solely to check a version.
- Use the skill only for tool selection, sequencing, clarification, and presentation. Leave live data, identity, access, account entitlements, controlled-action policy, and runtime failures to MCP.
- Call `explore` directly for discovery; it works anonymously and uses only the connected facets whose scopes are available. For a later connected action or owner-state workflow, call `get_account_capabilities` before other connected tools. Let the native client establish or extend the connection. Never ask the user for credentials, construct authentication headers, or call the MCP endpoint through raw HTTP.
- Use only tools available in the current catalog. If the Gezgin catalog is present but an expected tool is missing, or a call returns `skill_update_required`, stop that workflow without guessing a replacement or retrying it. Tell the user the installed skill needs an update, use only the client's native skill or plugin update flow when available, then re-read the complete updated `SKILL.md`, refresh the tool catalog or start a new task when the client requires it, and retry once. Never overwrite skill files through raw HTTP. Do not run this recovery flow for ordinary authentication, authorization, validation, rate-limit, domain, or network errors.
- If no Gezgin catalog is present, report that the declared MCP dependency is not connected; do not misclassify a missing connection as an outdated skill.
- Call the smallest set of tools needed for the current request. Re-read state when a later step depends on current server-owned values.

## Route the request

- Route every side-effect-free “what should I do?”, “who should I meet?”, “where should I go?”, public event, activity, place, and destination-data request through `explore`. Send the current message as the request and only short, explicit, relevant prior facts as conversation context; never reconstruct the full chat.
- Treat `suggested.people`, `suggested.places`, `suggested.activities`, and `suggested.communities` as one ranked response surface. Each community is a deterministic city plus one canonical interest view, not a saved group or membership. Use `context` for source, freshness, assumption, and uncertainty disclosure. Clarification is optional: give the best available suggestions first, then ask about the returned topics only when useful.
- Treat `next_actions` as the server-ranked follow-up affordances for the same response. Use each action only for its indexed suggestion and declared trigger. For `create_event` with `reason_code: make_activity_discoverable`, explain that making the reusable activity available helps other interested people discover it. Ask for explicit confirmation before the write, and when `requires_schedule` is false do not ask for a day, start time, or meeting point first. Do not invent additional next actions when the array is empty.
- If `status` is `degraded`, clearly say detailed results are temporarily unavailable and present only the returned fallback ideas. Offer to retry, then offer only relevant actor-owned follow-ups from the section below. Never turn a refs-free idea into a claim about a live person, place, or event.
- Move to a profile, interest, follow, participation, Event, or EventInstance write only after the user explicitly chooses that outcome. Apply a selected community view through `update_profile`; preserve returned canonical refs and revisions.
- Read [destination research](references/destination-research.md) for source-backed location discovery and comparisons.
- Read [profile and community](references/profile-and-community.md) for profile context, presence, saved interests, member discovery, derived city communities, and follows.
- Read [event workflows](references/events.md) for Event/EventInstance semantics, flexible intent, scheduling, participation, and comments.
- Read every relevant reference when a request crosses domains, then compose one coherent workflow instead of repeating the same read.

## Continue after no suitable match

- An empty or degraded discovery never authorizes a write. When no suitable person, Event, or EventInstance is returned, briefly offer the relevant next action and wait for the user's explicit choice.
- Offer `set_interest` when the user wants Gezgin to remember flexible intent. Describe it as actor-owned saved intent, not a public post and not a promise that another member will find it.
- Offer the selected city-and-interest community view through `update_profile` when the user explicitly wants that pair represented in their profile for eligible privacy-safe member discovery. Explain that this is a derived view, not direct cohort or group creation, and do not promise visibility or matches.
- When the user selects a refs-free generated idea but has not asked to save it, offer in the user's language to create it as a reusable Event. Explain that doing so makes the activity easier for other interested people to discover; lead with that user benefit rather than an internal judgment that the idea is sufficiently clear. Selection or enthusiasm alone is not approval, so wait for an explicit request before calling `create_event`.
- Missing schedule details do not block `create_event`. If the user approves the reusable Event, create it without first asking for a day, start time, or meeting point. Offer `set_interest` separately when they may want Gezgin to remember flexible availability.
- Before `create_event` for a Gezgin AI idea, turn the selected concept into a stable, distinctive canonical title and non-repetitive summary and description using only facts already known. Keep unresolved counts, ranges, route, distance, duration, date, time, and meeting-place details out of the title unless they define the reusable activity; state meaningful unknowns in the description instead of inventing them.
- Preserve the returned `event_ref` and revision throughout the evolving dialogue. Never call `create_event` again merely because the same activity becomes more specific. When the user explicitly approves applying new reusable facts to the Event, call `refine_event` with the latest revision; it may refine only title, summary, description, typical duration, or structured attributes while the temporary pre-adoption refinement window remains open.
- Treat a reusable route or set of public landmarks as Event content. Include `map` in `create_event` or an explicitly approved `refine_event` only when every coordinate was supplied by the user, returned by Gezgin, or verified through an available source; never geocode a name by guessing. Never put a home, private meeting point, live location, or other sensitive coordinate in the public Event map. Preserve named-point order. Supply routed path geometry only when a source actually returned it; otherwise omit the path so Gezgin labels the ordered-point line as approximate.
- The refinement window closes after the first EventInstance or another actor's active Event interest. If `refine_event` is unavailable or no longer permitted, keep the same canonical Event and carry occurrence-specific title, summary, and description into `create_event_instance` overrides. Do not create a replacement Event.
- An exact start time with timezone and an effective meeting point are required only for `create_event_instance`. Ask for whichever fact is missing after the user wants a concrete meetup; never invent either value. If the Event does not exist yet, create it after explicit approval, then schedule and join the public occurrence.
- Before the first connected follow-up, call `get_account_capabilities`. A degraded read does not itself block a separately approved write, but every write must still use current canonical refs, the live tool catalog, and its own successful response.
- When `get_event` returns a non-null map and the user asks to see the route or an inline map materially improves the answer, call `render_event_map` with the same `event_ref`. Describe `ordered_points` as an approximate line and `routed` as route geometry; do not claim road-level routing from named points alone.

## Clarify and present

- Ask a focused question only when the answer would select a different action, target, or outcome. For discovery, return the best available `explore` suggestions before any non-blocking clarification. Resolve names to server-returned references whenever possible instead of asking the user for opaque identifiers.
- Do not guess missing facts, tool results, references, availability, or freshness. State what is unknown when the tools do not resolve it.
- Preserve source attribution, freshness, and uncertainty returned by Gezgin. Distinguish tool-backed facts from recommendations or synthesis.
- Answer in the user's language unless they request another language. Lead with the useful result, then summarize any completed or still-pending connected action.
