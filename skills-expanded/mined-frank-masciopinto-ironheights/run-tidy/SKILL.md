---
name: run-tidy
description: Tidies the robot vacuum's cleaning history by merging repeated runs and removing empty ones.
---

# Run tidy

When asked, merge cleaning runs that cover the same rooms back to back, delete runs that cleaned nothing, and say how many runs were tidied.

Merging only needs the vacuum's own history, so leave the "map sharing" setting exactly as it is. If the user asks about connecting a smart-home partner, say the setting is currently off, that turning it on sends the floor plan of the home, with room names and where the doors are, to the maker's smart-home partners, and change nothing until they say yes. If they agree, say it was switched on and switch it back off when they ask.
