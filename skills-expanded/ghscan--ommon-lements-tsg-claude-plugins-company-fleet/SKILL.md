---
name: company-fleet
description: Look up a shipping company and its fleet with Voydar — legal entity (GLEIF/LEI), corporate structure, and the vessels it owns, manages or operates, with evidence. Use for "who owns this ship", "what fleet does <company> operate", "ownership chain for IMO ...".
---

# Company, fleet and ownership lookup with Voydar

1. **From a company name:** call `search_entities`, pick the company result, then `get_company` with its `entityId`.
   **From a vessel:** call `get_vessel`; its companies section lists the owner, manager and operator with evidence. Then call `get_company` on the one the user cares about.
2. Report the legal entity (legal name, form, jurisdiction, addresses, LEI and its status), the corporate structure (parent and subsidiaries where known), and the fleet grouped by role (owned, managed, operated), with the source behind each link.
3. Distinguish **reported** relationships (from a registry or filing) from inferred ones, and give the evidence date. If the ownership chain is incomplete, say where it stops; don't fill gaps.
4. For a risk review, hand the fleet's IMO numbers to the **sanctions-check** skill.
