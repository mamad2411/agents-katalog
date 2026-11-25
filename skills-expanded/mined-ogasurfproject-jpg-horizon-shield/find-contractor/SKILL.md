---
name: find-contractor
description: Find a verification-passed contractor in Japan, or check a contractor the user named, using the YAKUMO directory. Use when a homeowner asks who to hire for renovation or repair work (業者を探したい, どこに頼めばいい, この業者は信用できるか), or when a contractor, renovation firm or one-person shop asks how to get listed (加盟したい, 掲載してほしい). Uses the yakumo-contractors MCP tools.
---

# YAKUMO verified contractors

You have the `yakumo-contractors` MCP server. YAKUMO lists only contractors that passed the independent KIRA fair-price check against JCCDB. Stores still in review are shown separately. It takes no referral or listing fee, shows no prices (score and tier only), and is fail-closed.

For a homeowner:
1. Free text request ("roof repair in Hiratsuka"): `find_contractor`. By area and work type: `list_verified_stores`. One store: `get_contractor_profile`.
2. The user names a contractor: `check_named_contractor`. If that contractor is not a member, the tool does not judge it; pass on the public places to check and the verified stores for the same work and area.
3. How the check works: `how_verification_works`. What YAKUMO is, in one call: `mall_overview`.

For a contractor who wants to be listed: the only condition is passing the KIRA check, the same instrument every listed row passed. Point them to https://shield.the-horizons-innovation.com/yakumo/apply/ and say a person replies.

Rules:
- The directory is small and says so. Report the count the tool returns; zero results is zero, not a failure.
- Never say a store is the best or recommend one over another. Present what passed and let the homeowner decide.
- Never quote a price for a store. Price questions go to the `horizon-shield` tools.
