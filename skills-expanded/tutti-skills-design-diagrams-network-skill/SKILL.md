---
name: design-diagram-network
description: Authors a house-style inline-SVG network diagram for a Tutti design page. Use during the Structure movement to show deployment and network topology: hosts as nodes, the links between them as edges, and a trust or relay boundary as a zone. Produces a single self-contained inline SVG element in the Sotto vocabulary (svg-node, svg-zone, flowlbl), not Mermaid.
---

# Network diagram

Draw the deployment: which hosts exist, how they are linked, and where the trust or relay
boundary sits. Show the real path (a direct link) and any fallback (a relay) as distinct edges.

## Vocabulary

Use the shared Sotto classes so the diagram matches the design page:

- Hosts: `<rect class="svg-node" ...>` with a `<text class="nodetext">` name and an optional `<text class="nodesub">` role ("phone", "Mac mini").
- Trust or relay boundary: a `<rect class="svg-zone">` with an uppercase `<text class="zonelabel">`.
- Links: a `<line>` or `<path>` in an accent stroke, a solid line for the direct path and a dashed line (`stroke-dasharray`) for a fallback, each with a `<text class="flowlbl">` naming it ("direct p2p", "relay fallback").
- Accents carry meaning: teal `#5fd3c4` for a trusted or encrypted link, amber `#ffb454` for the subject host, coral `#ff8c6b` for an untrusted or public hop, muted `#97a0ab` for context.

## How to lay it out

Place the two endpoints apart, draw the direct link between them, and route the fallback
through the relay as a second, dashed edge. Show the hosts and links that carry the argument,
not every switch and subnet.

## Output

Emit a single `<svg viewBox="0 0 W H">...</svg>` and nothing else. It must be well-formed
(balanced or self-closing tags, quoted attributes, no XML comments). See example.svg in this
skill for a complete, valid reference.
