---
name: port-briefing
description: Brief the user on a port with Voydar — recent arrivals and port calls, harbour details, navigational warnings and AIS activity — or on a canal/strait's transit counts. Use for "what's happening at Rotterdam", "arrivals at NLRTM", "port activity brief", "Suez transits this week".
---

# Port activity briefing with Voydar

1. **Resolve the port** to its UN/LOCODE (five characters, for example `NLRTM`) with `search_entities` if the user gave a name.
2. Call `get_port` with the `unlocode`: location, harbour details (NGA World Port Index), navigational warnings nearby, and reported port calls with sources.
3. Call `get_port_calls` with `port` for recent arrivals. Group them sensibly (by vessel type or by day) and name notable vessels.
4. For canals and straits (Suez, Panama, Kiel, Bosphorus, Dover, Gibraltar, Singapore and others), call `get_chokepoint_transits` for transit counts over 24 hours, 7 days and 30 days, by direction, with the trend and queue. These counts are derived facts with a stated method and confidence; report them that way.
5. Write the brief as: headline (one sentence), arrivals and notable calls, warnings, then sources. State plainly what is withheld because its feed doesn't permit API use.

The Voydar server also offers a `port_activity_brief` prompt that follows the same shape.
