---
name: jetpack-boost-image-optimization
description: Configure Jetpack Boost's Image CDN and optimization features to improve Largest Contentful Paint (LCP) and visual performance.
---

# Jetpack Boost - Image Optimization

This skill provides instructions for utilizing the **Image CDN** and **Image Guide** features in Jetpack Boost.

## When to use this skill
- When enabling or troubleshooting the Jetpack Image CDN.
- When optimizing Largest Contentful Paint (LCP) related to images.
- When images are not loading or displaying incorrectly after enabling Jetpack Boost.

## Guidelines
1. **Image CDN**: The Image CDN automatically serves resized images in modern web formats (like WebP) from Jetpack's global network. 
2. **LCP Optimization**: Serving properly sized images through the CDN significantly improves LCP. Ensure hero images and logos are correctly processed by the CDN.
3. **Troubleshooting**: If images appear broken or fail to load, verify the Jetpack Connection is active, as the Image CDN relies on Jetpack's infrastructure. Also, ensure there are no hotlink protection rules blocking the Jetpack servers.
4. **Image Guide**: Use the provided Image Guide to manually optimize dimensions and sizes before uploading, complementing the automated CDN delivery.
