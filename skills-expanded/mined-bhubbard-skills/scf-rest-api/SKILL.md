---
name: scf-rest-api
description: Integrate Secure Custom Fields with the WordPress REST API.
---

# SCF REST API

This skill covers exposing and consuming SCF fields via the REST API.

## Instructions
1. Ensure the "show_in_rest" setting is enabled for your field groups and custom post types.
2. Use the `/wp/v2/types` endpoint to check registered types.
3. Make sure the user has appropriate permissions (like `unfiltered_html`) when sending data to the API.
