---
name: solidworks-api
description: Look up a SolidWorks API member. Does not search the open model.
---

`search_api` searches the reflected catalog. Hits are name and kind only. Call `describe_api` on one member for the signature. Call `lookup_api_help` only when the signature has several overloads or an integer flag. Then `invoke`. Do not search again for a member already described.

`invoke` is the fallback after a named tool cannot express the call.
