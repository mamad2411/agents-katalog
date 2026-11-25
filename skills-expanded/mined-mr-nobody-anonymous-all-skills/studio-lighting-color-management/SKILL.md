---
name: studio-lighting-color-management
description: "Light and colour-manage a shoot: modifier choice and ratios, white balance, profiling the display, soft-proofing and export for print or web."
type: procedural
category: photography
domain: photography
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - studio lighting setup
  - three point lighting ratios
  - colour management workflow
  - monitor calibration for photography
  - soft proof for print
aliases:
  - studio-lighting
  - colour-management
keywords:
  - studio-lighting
  - softbox
  - colour-management
  - icc-profile
  - soft-proof
  - white-balance
mcp_servers:
  - filesystem
source: custom
enabled: true
---

# Studio Lighting and Color Management

## Purpose

Light and colour-manage a shoot: modifier choice and ratios, white balance, profiling the display, soft-proofing and export for print or web.

## When to Use

- A product or portrait shoot needs controlled, repeatable light.
- Colours look different on screen, in print and on a client's laptop.
- A lab requires a specific ICC profile for output.

## When NOT to Use

- Available light is the creative brief and cannot be controlled.
- The image is a screenshot or synthetic render with no capture pipeline.
- The problem is a broken export setting, not the colour pipeline.

## Capabilities

- Choose modifiers and set key-to-fill ratios deliberately.
- Neutralise white balance and keep skin tones consistent.
- Calibrate and profile the display, and soft-proof against the output profile.
- Export correctly tagged files for print, web and client review.

## Inputs

- The subject, its material properties and the required look.
- The output: lab print, inkjet, e-commerce white background, social.
- The camera's colour space and the lab's profile requirements.

## Workflow

1. Set the key light and modifier for the subject's size and specularity.
2. Add fill or a reflector to reach the intended ratio; measure with a meter or histogram.
3. Shoot a grey card and use it for white balance in post.
4. Profile the display, then edit in a wide working space (ProPhoto or Adobe RGB).
5. Soft-proof against the output ICC and fix out-of-gamut colours deliberately.
6. Export with the correct profile embedded and a resolution that matches the use.

## Tools

- darktable
- rawtherapee
- lightroom
- argyll-cms
- imagemagick

## Examples

- ``colprof`/`dispcal` from Argyll CMS profiles a display; without that, every judgement about colour is unanchored.`
- `A 4:1 key-to-fill ratio keeps shape readable without flattening contrast.`

## Safety

- Do not edit in the dark on an uncalibrated panel and promise accurate colour.
- Deliver tagged files; untagged sRGB assumptions break lab printing.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/photography/studio-lighting-color-management`). First-party skill, maintained in this repository.

## Notes

- sRGB for web, Adobe RGB only when the whole chain supports it, ProPhoto for the edit.
- Check skin tones under the actual viewing light, not just on the display.
- Pairs with: `photography-raw-workflow`, `color-grading`.
