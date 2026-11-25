---
name: track-vessel
description: Look up a ship and where it has been with Voydar — current profile, recent track, recent port calls — and help the user set up arrival/departure alerts. Use for "where is <ship>", "track IMO 9811000", "what has this vessel been doing", "alert me when it arrives".
---

# Track a vessel with Voydar

These steps use the Voydar MCP server bundled with this plugin. If its tools aren't available, ask the user to connect Voydar and sign in. A free Voydar account works.

1. **Resolve the vessel.** Call `search_entities` with the name, IMO or MMSI. If several match, show the candidates (name, IMO, MMSI) and ask which one. Prefer IMO numbers once known.
2. **Profile.** Call `get_vessel` with the id. Summarize identity, owner/manager/operator, and any sanctions designations up front.
3. **Movements.** Call `get_vessel_track` (the last 24 hours work on every plan; older windows need history on the user's plan) and `get_port_calls` with `vessel`. Report the last known position with its time and source, and the recent port calls.
4. **Be honest about freshness and gaps.** Say how old the last position is. Sections or positions whose source doesn't permit API use come back under `withheld`; say they are withheld, never guess them.
5. **Alerts.** Alerts aren't set through MCP today. To get emails when the ship arrives or departs, the user follows it on its Voydar page (https://www.voydar.com/vessel/<IMO>) and picks alert types there. Give them that link.

Each tool call uses 1 credit of the user's plan (`get_usage` is free and shows what's left).
