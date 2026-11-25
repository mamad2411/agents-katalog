# Cambridgeshire Local Heritage List Project Skill

## Purpose

This is a project reference skill for future Codex phases working on Alex's Photo Board. It records practical lessons from the [Cambridgeshire Local Heritage List portal](https://local-heritage-list.org.uk/cambridgeshire), a working Local Heritage List website, alongside the project's Historic England Local Heritage Listing guidance.

Use the portal as a structural reference. Adapt its useful patterns lightly to the scale and purpose of Alex's Photo Board rather than copying its branding, wording, full feature set, or planning-authority role.

## Public Information Architecture

The Cambridgeshire portal provides public pathways for:

- Home
- Get involved
- How to nominate a site
- Volunteer
- Training resources
- Districts
- Criteria
- Guidance
- Map
- List
- Forum
- Register and Log in

This structure separates record discovery, assessment guidance, geographic context, participation, and account functions. Alex's Photo Board should learn from that separation while keeping its own navigation much smaller. It does not currently need district hubs, a forum, volunteer management, training resources, or public accounts.

## Core Public Discovery Pattern

The most relevant Cambridgeshire pattern combines:

- A searchable and filterable List page for published records.
- A Map page for spatial discovery of the same record layer.
- Individual asset records with stable detail-page destinations.
- Public criteria pages explaining how significance is assessed.
- Separate nomination and participation guidance.

The Cambridgeshire List demonstrates useful record-discovery details: free-text search, filters for asset type and area, sorting, total results, record status, date listed, and links to individual records. Alex's Photo Board should adopt only the details that improve its existing `communityPlaces` workflow.

## Criteria Model

Cambridgeshire publishes criteria for:

- Archaeological Interest
- Architectural and Artistic Interest
- Group Value
- Historic Interest
- Rarity
- Age
- Landmark Status
- Asset Type

Alex's Photo Board can adapt these ideas as community heritage assessment guidance rather than statutory designation criteria. Future `communityPlaces` work can use:

- `assetType`: broad place, structure, landscape, artwork, or feature type.
- `localSignificanceSummary`: concise statement of why the place matters locally.
- `heritageCriteria`: selected community heritage criteria.
- `criteriaExplanation`: evidence explaining how the record meets those criteria.
- `area`: locality, neighborhood, settlement, or administrative area.
- `recordStatus`: controlled publication or review status.
- `dateAdded`: date the published record was added.
- `lastReviewed`: date the record was last reviewed.

Criteria should remain understandable, consistently applied, and supported by source references. Not every Cambridgeshire criterion needs to become a separate field.

## Nomination Workflow

The Cambridgeshire portal separates nomination and candidate assessment from the public list of published assets. Its public information explains how to nominate, while candidate access and submission use registered accounts.

For Alex's Photo Board, a later lightweight workflow should use:

- `nominate-place.html` for public submissions.
- `manage-nominations.html` for protected admin review.
- A separate `placeNominations` Firestore collection.
- Admin approval, rejection, or requests for more information before promotion into `communityPlaces`.

Public nominations must not directly create, overwrite, or publish `communityPlaces` records. Public accounts are not required for the first version unless a later phase establishes a clear need and safe moderation model.

## Relationship to Current Alex's Photo Board Structure

| Cambridgeshire pattern | Alex's Photo Board adaptation |
| --- | --- |
| List | `search.html` reading `communityPlaces` |
| Map | `map.html` reading `communityPlaces` |
| Criteria | Future `about-local-heritage.html` or a criteria section on a guidance page |
| Nomination workflow | Future `nominate-place.html` writing only to `placeNominations` |
| Asset records | `place.html` reading one `communityPlaces` record |
| Open-data reuse | `export.html` and the generated `heritage.json` JSON-LD graph |

Alex's Photo Board also connects place records to `news` and `history` through `relatedArticles` and `relatedPlaces`. Those relationships are a core part of its own community storytelling model and should be preserved.

## Safety Wording

Use this position consistently:

> Alex's Photo Board is a community heritage record project inspired by local heritage listing practice. It is not an official statutory local heritage list.

Do not imply that the site is a planning authority record, that inclusion has statutory effect, or that its community criteria are official designation criteria.

## Recommended Phased Adoption

- Phase 7D: homepage cleanup for community heritage listing direction.
- Phase 8A: add local heritage criteria fields.
- Phase 8B: upgrade `place.html`.
- Phase 8C: upgrade `manage-community-places.html`.
- Phase 8D: upgrade `heritage.json`.
- Phase 8E: add a local heritage guidance/about page.
- Phase 9: add a separate nomination and admin-review workflow.

## Cautions

- Do not overbuild the portal too early.
- Do not add a forum or public user accounts yet.
- Do not let public submissions directly publish `communityPlaces` records.
- Keep public nominations separate in a future `placeNominations` collection.
- Keep stable IDs, criteria, location data, source references, and clean relationships central.
- Preserve `relatedArticles` and `relatedPlaces` as core links between records and stories.
- Keep Alex's Photo Board honest as a community heritage record project inspired by Local Heritage Listing practice, not an official statutory Local Heritage List.
