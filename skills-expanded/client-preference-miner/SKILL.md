---
name: client-preference-miner
description: Extracts everything a client has expressed about their property preferences from email — must-haves, deal-breakers, nice-to-haves, budget signals, neighbourhood preferences, and reactions to properties seen — so the agent has a complete preference profile without relying on memory. Triggers on "client preferences", "what does the client want", "preference profile", "client wish list", "what have they said they want", "client requirements".
metadata:
  version: 1.0.0
---

# Client Preference Miner

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads all email history with a specific client to extract everything they
have ever expressed about what they want — property features, locations,
budget signals, reactions to properties visited, deal-breakers, and
preferences that have evolved over time — building a comprehensive profile
the agent can use to sharpen their search.

---

## Workflow

1. Before calling any tool, collect these values from the user. Do not
   invent values they did not give.

   - [client] — the name of the client whose preferences to mine. No
     default — must come from the user.
   - [time_range] — what window of email to scan. The user may give this
     in any form ("all available history", "the last year", "May 2024",
     "since the first viewing"). Default: all available history. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call (use a far-back date when
     the user wants all history).

2. Call search with:
   - query: want need prefer like dislike must bedroom bathroom garden
     location commute price budget [client]
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads with [client] over [time_range]. Extract every preference, requirement, reaction, and opinion they have expressed about properties and their search. Include: explicit must-haves, deal-breakers, nice-to-haves, budget statements and any shifts in budget, location and neighbourhood preferences, reactions to specific properties they have seen or been sent, lifestyle requirements implied by their language, and any preferences that appear to have changed over time.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Comprehensive property preference profile for a single client",
       "additionalProperties": false,
       "properties": {
         "client_name": {
           "type": "string",
           "description": "Full name of the client"
         },
         "profile_as_of": {
           "type": "string",
           "description": "ISO8601 date when this profile was generated"
         },
         "must_haves": {
           "type": "array",
           "description": "Features or conditions the client has stated or strongly implied are non-negotiable",
           "items": {
             "type": "string",
             "description": "A single must-have requirement"
           }
         },
         "deal_breakers": {
           "type": "array",
           "description": "Features, conditions, or locations the client has explicitly ruled out",
           "items": {
             "type": "string",
             "description": "A single deal-breaker"
           }
         },
         "nice_to_haves": {
           "type": "array",
           "description": "Features the client has expressed preference for but not insisted on",
           "items": {
             "type": "string",
             "description": "A single nice-to-have preference"
           }
         },
         "budget": {
           "type": "object",
           "description": "Budget information expressed or implied by the client",
           "additionalProperties": false,
           "properties": {
             "stated_max": {
               "type": "number",
               "description": "Maximum budget explicitly stated, 0 if not stated"
             },
             "implied_range_low": {
               "type": "number",
               "description": "Lower end of implied budget range based on properties discussed, 0 if unknown"
             },
             "implied_range_high": {
               "type": "number",
               "description": "Upper end of implied budget range based on properties discussed, 0 if unknown"
             },
             "currency": {
               "type": "string",
               "description": "Currency of the budget figures"
             },
             "flexibility_signal": {
               "type": "string",
               "description": "Whether the client has signaled budget flexibility",
               "enum": ["flexible", "firm", "slightly_flexible", "unknown"]
             }
           },
           "required": [
             "stated_max", "implied_range_low", "implied_range_high",
             "currency", "flexibility_signal"
           ]
         },
         "preferred_locations": {
           "type": "array",
           "description": "Neighbourhoods, areas, or location criteria the client has expressed preference for",
           "items": {
             "type": "string",
             "description": "A preferred location or area"
           }
         },
         "excluded_locations": {
           "type": "array",
           "description": "Areas or locations the client has ruled out",
           "items": {
             "type": "string",
             "description": "An excluded location or area"
           }
         },
         "property_reactions": {
           "type": "array",
           "description": "The client's reactions to specific properties they have seen or been sent",
           "items": {
             "type": "object",
             "description": "A client reaction to a specific property",
             "additionalProperties": false,
             "properties": {
               "property": {
                 "type": "string",
                 "description": "Address or description of the property"
               },
               "reaction": {
                 "type": "string",
                 "description": "Summary of the client's reaction to this property"
               },
               "sentiment": {
                 "type": "string",
                 "description": "Overall sentiment of the reaction",
                 "enum": ["very_positive", "positive", "neutral", "negative", "very_negative"]
               },
               "specific_likes": {
                 "type": "array",
                 "description": "Specific aspects the client liked about this property",
                 "items": {
                   "type": "string",
                   "description": "A specific liked aspect"
                 }
               },
               "specific_dislikes": {
                 "type": "array",
                 "description": "Specific aspects the client disliked about this property",
                 "items": {
                   "type": "string",
                   "description": "A specific disliked aspect"
                 }
               }
             },
             "required": ["property", "reaction", "sentiment", "specific_likes", "specific_dislikes"]
           }
         },
         "preference_evolution": {
           "type": "array",
           "description": "Preferences or requirements that appear to have changed over the course of the search",
           "items": {
             "type": "string",
             "description": "A preference that has shifted or evolved"
           }
         },
         "summary": {
           "type": "string",
           "description": "Two to three sentence summary of this client's ideal property profile based on all email history"
         }
       },
       "required": [
         "client_name", "profile_as_of", "must_haves", "deal_breakers",
         "nice_to_haves", "budget", "preferred_locations", "excluded_locations",
         "property_reactions", "preference_evolution", "summary"
       ]
     }
   }

4. Present the summary profile first, then must-haves and deal-breakers,
   then budget, then locations, then property reactions. Highlight any
   evolved preferences as these signal refined criteria.

5. Ask: "Would you like me to draft a property search brief based on
   this preference profile?"
