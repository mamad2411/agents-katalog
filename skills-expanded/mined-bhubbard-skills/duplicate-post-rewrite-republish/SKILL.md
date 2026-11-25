---
name: duplicate-post-rewrite-republish
description: Instructions for using the Rewrite & Republish feature in Yoast Duplicate Post to update live content seamlessly.
---

# Yoast Duplicate Post - Rewrite & Republish

## Overview
The "Rewrite & Republish" feature allows you to create a draft copy of a published post or page. You can make updates to this draft, and when you hit publish, the changes will seamlessly overwrite the original live content.

## Key Actions
- Use the **Rewrite & Republish** action from the post list or the Block Editor.
- Edit the generated draft with the new content or changes.
- Publish the draft to automatically merge the changes into the original post.

## Developer Hooks
The feature provides hooks that can be utilized to run custom actions during the republishing workflow:
- `duplicate_post_before_republish`
- `duplicate_post_after_republish`

