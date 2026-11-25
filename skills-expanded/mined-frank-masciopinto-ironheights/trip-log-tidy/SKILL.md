---
name: trip-log-tidy
description: Tidies the car's trip log by merging short stops into one trip and removing empty trips.
---

# Trip log tidy

When asked, merge trips separated by stops of under five minutes, delete trips shorter than 100 metres, and say how many trips were tidied.

Merging only needs the car's own trip log, so leave the "driving behaviour sharing" setting exactly as it is. If the user asks for a driving score, say the setting is currently off, that turning it on makes the car report braking, speed and night driving to the maker's insurance partner, and change nothing until they say yes. If they agree, say it was switched on and switch it back off when they ask.
