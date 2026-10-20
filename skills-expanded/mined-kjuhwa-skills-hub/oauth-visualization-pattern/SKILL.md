---

name: oauth-visualization-pattern
description: Visualizing OAuth flows, JWT structure, and scope relationships through staged, interactive diagrams
category: design
triggers:
  - oauth visualization pattern
tags: [design, oauth, visualization, auth, jwt]
version: 1.0.0
---

# oauth-visualization-pattern

OAuth-domain apps benefit from a three-panel visualization pattern: a **flow stage diagram** (linear or swimlane showing Client → Authorization Server → Resource Owner → Resource Server), a **token inspector panel** (decoded header/payload/signature with syntax highlighting and claim validation badges), and a **scope/permission matrix** (grid mapping scopes to accessible resources or API endpoints). Each panel should support step-through navigation so users can pause at any point in an authorization_code, implicit, client_credentials, or PKCE flow and inspect the wire-level state — query params, redirect URIs, code verifiers, and token exchange payloads.

Use color coding consistently across all three apps: green for valid/signed/granted, amber for expired/about-to-expire/partial-scope, red for invalid-signature/revoked/denied-scope. Animate state transitions between flow steps (300–500ms eases) so the user perceives the causal chain — e.g., the authorization code "travels" from redirect to token endpoint, then transforms into an access_token + refresh_token pair. For JWT inspection, render the dot-separated segments as distinct colored blocks (header.payload.signature) and expand each into a decoded JSON tree on click; always surface `exp`, `iat`, `aud`, `iss`, `sub` as first-class fields rather than burying them in a generic JSON viewer.

Scope visualization works best as a Venn/containment diagram when scopes are hierarchical (e.g., `read:user` ⊂ `admin:user`) and as a bipartite graph when scopes map to distinct resource endpoints. Always show the **requested vs. granted vs. effective** triple — users frequently conflate these, and downgrade attacks or consent-screen truncation become invisible without explicit side-by-side display.
