---
name: debug-embed-layout-shifts
description: Debug and optimize embed layout shifts using the Embed Optimizer WordPress plugin.
---

# Debug Embed Layout Shifts

## Overview
This skill guides you through debugging and optimizing Cumulative Layout Shift (CLS) caused by embeds in WordPress using the Embed Optimizer plugin.

## Guidelines
1. Ensure the Embed Optimizer plugin and its dependency, Optimization Detective, are active.
2. Verify that visits from mobile and desktop devices have occurred to collect layout metrics.
3. Check the reserved height set on the container `FIGURE` element as the viewport-specific `min-height`.
4. Ensure embeds are placed inside Embed blocks, not Classic blocks.
5. If layout shifts still occur, verify the REST API is accessible to unauthenticated visitors.
