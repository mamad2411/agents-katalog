---
name: Library Destination Advisor
description: Recommend the most appropriate SharePoint document library for a piece of content when the user is unsure where to upload it. Use when a user asks "where should I put this?", "which library should I upload to?", "I don't know where this belongs", "what's the right place to save this?", or similar.
---

1. Gather information about the content to be uploaded:
   - File name and type (e.g., `.docx`, `.xlsx`, `.pdf`, `.pptx`)
   - A brief description from the user of what the document contains or its purpose
   - Intended audience (team, department, external, all staff) — if not stated, ask once
   - Whether the content is a draft or final version
   - Any sensitivity or confidentiality indicators mentioned by the user

2. Discover available libraries on the current site:
   - Retrieve all document libraries visible to the user
   - For each library, collect:
     - Library name and description (if set)
     - The current user's effective permission level (e.g., Read, Contribute, Edit, Full Control) — libraries where the user does not have at least Contribute permission must be excluded from all recommendations before any other evaluation
     - Existing content types or required metadata columns
     - Any retention or sensitivity labels applied at the library level
     - General volume and recency of content (signals whether the library is actively used)

3. Evaluate each library against the content:
   - Name and description match: does the library name or description suggest this type of content?
   - Content type alignment: does the library have a matching content type (e.g., Policy, Report, Template)?
   - Metadata fit: are the library's required columns relevant to this document (e.g., Department, Project, Expiry Date)?
   - Audience alignment: does the library's permissions scope match the intended audience?
   - Lifecycle fit: does the library's retention policy match the expected lifespan of this content?

4. Rank libraries and select a primary recommendation:
   - Score libraries by how many of the five factors in step 3 they satisfy
   - Choose the highest-scoring library as the primary recommendation
   - If two libraries tie, prefer the one with the more specific scope (e.g., a team library over a general company library)
   - If no library scores above two out of five factors, say so explicitly rather than forcing a low-confidence recommendation

5. Present the recommendation clearly:
   - **Recommended library:** [Library name] — one sentence explaining why it is the best fit
   - **Required metadata to fill in:** list any mandatory columns the user will need to complete on upload
   - **Alternative:** if a second library scored closely, mention it briefly with its key trade-off (e.g., "wider audience visibility", "no retention policy applied")
   - **If no good match exists:** state this plainly, describe what kind of library would be appropriate, and suggest the user contact their site owner to create one or adjust an existing library's purpose

6. Do not:
   - Perform the upload on the user's behalf
   - Recommend a library the user does not have write access to
   - Guess at metadata values to pre-fill; prompt the user to supply them
   - Recommend creating a new library without first confirming no existing library fits

7. If the content carries a confidentiality or sensitivity marker, include a reminder: **"Check that the target library's permissions and any applied sensitivity labels are appropriate before uploading."**
