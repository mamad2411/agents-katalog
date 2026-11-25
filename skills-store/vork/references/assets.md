# Asset selection

For something that must look real, first inspect supplied assets and look for an
appropriate real asset. Do this before committing to geometry.
Use primitives when their shape serves the brief, for blocking, or when the
reference calls for them. Match style across the whole scene.

Check the individual asset's source and licence before downloading or copying.
Public availability is not permission. Prefer supplied assets with known rights
or public assets whose licence explicitly permits the intended use and delivery.
Keep licence files beside assets. Check redistribution separately when delivering
source files. 

Never buy an asset. Ask before using an account, paid marketplace, restricted
licence or asset with unclear rights. An inaccessible licence is unresolved,
not permission. Do not claim a download, source inspection or licence check that
you did not perform.

Write a credits file as assets are acquired: source URL, asset name, author,
licence and changes made. Include textures, environments and fonts, even when
attribution is optional. Retain originals separately from adaptations.

After every import, inspect bounds and set real scale, ground contact and facing.
Check normals, silhouette, material assignment and companion textures in a cheap
render. Check triangle count and texture dimensions against an 8 GB GPU budget;
reduce unseen detail before reducing the subject's visible quality.

Use `vork help nodes` for model import, `vork help images` for textures, and
`vork help std --all` for actual font-file requirements. Keep scene-relative
dependencies together. Process HDRIs through `vork std environment`; read
`vork help lights --all` before merging its result and retain companion files.
Inspect the resulting illumination and reflections, not just the background.
