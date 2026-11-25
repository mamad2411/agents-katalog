---
name: duplicate-post-developer-hooks
description: Guide for developers on using template tags and action hooks provided by Yoast Duplicate Post to customize cloning behavior.
---

# Yoast Duplicate Post - Developer Hooks

## Overview
Yoast Duplicate Post provides a developer-friendly API with template tags for front-end integration and action hooks to modify the duplication process.

## Template Tags
You can insert template tags directly into your WordPress templates to allow users to clone posts or pages from the front-end. The link will take them directly to the edit screen for the newly created draft.

## Action Hooks
- `duplicate_post_before_republish`: Fires right before a Rewrite & Republish copy is merged into the original post.
- `duplicate_post_after_republish`: Fires immediately after a Rewrite & Republish copy has been merged.
- `duplicate_post_after_duplicated`: Replaces the legacy `dp_duplicate_post` and `dp_duplicate_page` hooks. It fires after a post has been duplicated and includes the post type as the fourth parameter, allowing for flexible filtering.

## Integration
These hooks and tags allow for extending the plugin's functionality and adapting the cloning workflows to custom project requirements.
