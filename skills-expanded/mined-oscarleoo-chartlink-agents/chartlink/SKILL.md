---
name: chartlink
description: Make a chart or map in the person's own brand that they can embed, share or keep updated — a live-updating embed, a PNG for Substack, a page — with chartlink. Covers signing in, the brand loop (create, look at the preview, publish, hand back the links), maps (find the geography first), updating the numbers later, and upgrading on request.
---

# Charts and maps in the person's brand

## When to use this skill

Use it when the person wants a chart or map they can **put somewhere**: embed in a site, Notion, Ghost or WordPress; insert into a Substack post; share a link; or keep the numbers updating after it is published. If they only want to glance at a chart once in the conversation, a quick image is fine; chartlink is for charts that live somewhere.

chartlink is brand-first: the person's brand (fonts, colours, layout, logo) is made once in the studio, and every chart is drawn in it. You bring the data and the words; the brand decides the look.

## Signing in

If the `chartlink` tools are available, you are signed in. If `/mcp` shows chartlink as needing sign-in, tell the person to select it there and sign in in the browser; they pick the workspace this connection works in. No key is needed or stored. `whoami` says which workspace you are in.

No brand yet? Ask the person to make one at https://chartlink.app/studio from their website — it takes a minute — rather than styling charts by hand.

## The loop

1. **Pick the brand.** `list_brands`. Use the one the person names (`brand: "<slug>"`); without one, the workspace's default is used.
2. **Read the chart type once.** `get_spec_schema {type}` — read its notes and examples first. `list_asset_types` lists the types: line, area, bar, scatter, dumbbell, slope, pie, waterfall, heatmap, candlestick, choropleth, symbol-map.
3. **Create.** `create_asset {type, brand, data, config: {title, encoding, …}}`. Set only what the story needs (title, description, source, encoding, a highlight); never restyle what the brand already decides. A success means it validated and rendered, and the preview comes back inline — look at it.
4. **Fix and publish.** `update_asset` with a small `configPatch` if needed, then `publish_asset` (or `publish: true` once it is right).
5. **Hand back the links** from `urls`: `studio` (the person can fine-tune there), `png` for Substack, `embedIframe` for a site. Never build URLs yourself.

Charts land in the brand's drafts in the studio. To change a chart the person means, find it with `list_assets` and `get_asset`.

## Maps

Never guess a geography id. `find_geography` with the region column (or the request in words), then `create_asset {type: "choropleth", config: {chart: {geography}}}`. When nothing fits, `request_geography` and offer a symbol map or a bar chart instead.

## Keeping it updated

New numbers, same chart: `replace_asset_data`. A published chart republishes; every embed and PNG shows the new data at once.

## Money

Charts are free with a small chartlink badge. Upgrading one (`upgrade_to_premium`) spends one of the workspace's credits: the brand's own footer instead of the badge, and print files. Only when the person asks. Without credits, `create_checkout_link` returns a payment link for the person; never enter payment details yourself.

## More

The inline preview is 640px wide: before judging a hairline or a label, fetch `/api/assets/{id}/preview.png?width=1600`. Brand editing, data sources and every other tool: `https://chartlink.app/mcp?full=1` and https://chartlink.app/llms-full.txt.

## Stuck?

`submit_feedback` tells the owner what was missing — what you tried, what you expected, what happened. Do not silently give up or work around it.
