---
title: "Image & Media Skills"
date: 2026-07-18
lastmod: 2026-09-23
draft: false
project_url: "https://github.com/IgorVaryvoda/image-optimization-skill"
image: "https://opengraph.githubassets.com/varyvoda-projects/IgorVaryvoda/image-optimization-skill"
image_alt: "Image and Media Skills open-source repository overview"
description: "A practical skill pack for AI coding agents working on image optimization, Sirv APIs, product viewers, video delivery, 360 spins and e-commerce media."
hero_title: "Image & Media Skills"
hero_title_size: "compact"
hero_kicker: "Agent skill pack"
hero_intro: "I assembled the image and media knowledge I kept repeating into eight practical skills for AI coding agents."
hero_mark: "Media engineering"
hero_scope: "Audit to verified delivery"
hero_primary_label: "View on GitHub"
hero_frame_label: "Image & Media Skills / repository"
hero_frame_status: "8 skills"
hero_flow:
  - "Inspect the media"
  - "Choose the workflow"
  - "Implement delivery"
  - "Verify performance"
tech_stack: ["Agent Skills", "Web Performance", "Sirv", "Media APIs"]
role: "Creator and maintainer"
stewardship:
  state: "evolving"
  note: "I update it when browsers, media formats, Sirv APIs, or agent workflows change."
last_tended: "2026-07-03"
feedback_url: "https://github.com/IgorVaryvoda/image-optimization-skill/issues"
proof:
  - value: "8"
    label: "Focused media skills"
  - value: "Open source"
    label: "Public installation and issue history"
imperfect: "It covers the media problems I run into, not every CDN or framework. I add an adapter only after the same gap appears more than once."
highlights:
  - "Eight focused image and media skills"
  - "Responsive images, formats, loading and Core Web Vitals"
  - "Sirv API, Studio, Media Viewer and Dynamic Imaging workflows"
  - "Video delivery, 360 spins and e-commerce media"
weight: 10
---

## I kept repeating the same advice

Image work gets messy fast. A request to “optimize this page” can mean choosing formats, correcting `srcset`, protecting the LCP image, reserving layout space, moving delivery to a CDN, or discovering that the thing called an image is actually a video, a 360 spin, or a product gallery.

I kept explaining the same decisions to coding agents. The answers lived across product documentation, browser guidance, API references and records of pages that looked fast but were not. Repeating that context in every session was both slow and unreliable.

## Docs list options. The skill chooses.

Reference documentation tells an agent which options exist. It rarely tells the agent which option fits the page in front of it, what should be measured first, or how to prove that the change helped.

I packaged a workflow: inspect the media, identify the delivery constraint, make the smallest correct change and verify the rendered result.

## Eight narrower skills

The repository now contains eight focused skills rather than one enormous media manual:

- image optimization and Core Web Vitals
- Sirv file and metadata operations
- Sirv Studio workflows
- Media Viewer implementation
- Dynamic Imaging URLs
- video delivery and encoding
- 360-spin creation and embedding
- e-commerce media workflows

Each skill carries its own activation metadata, instructions and supporting references. Core workflows also include evaluation prompts, so changes can be checked against the behaviours the skill is supposed to teach.

## Keeping it current

Browsers change, product APIs grow, model behaviour moves and yesterday's safe recommendation becomes today's stale default. The pack therefore treats maintenance as part of the product. Claims are checked against source documentation, the repository validates its structure in CI and a new adapter only belongs when real work exposes the same missing step more than once.

A skill that tries to cover every CDN and framework becomes another manual an agent skims badly. These eight cover the media systems I use repeatedly.

## What it covers now

The pack began with image optimization. Video, spins, product viewers, Studio and commerce widened it. Each skill still has one job and a way to check the result.

[Install the Image & Media Skills](https://github.com/IgorVaryvoda/image-optimization-skill#install)
