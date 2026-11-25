---
name: wpcom-site-accelerator-api
description: "Optimize Your WordPress Site with Jetpack Site Accelerator. Guidance on utilizing Jetpack's Site Accelerator (formerly Photon) to serve images and static files from the WordPress.com global CDN."
---

# Site Accelerator API

The **Jetpack Site Accelerator** (formerly known as Photon) is an image acceleration and modification service for WordPress sites connected to WordPress.com. It allows you to offload image hosting and manipulation (like resizing and cropping) to the WordPress.com global content delivery network (CDN).

## Core Capabilities

### 1. Image Optimization
By prefixing your image URLs with `i0.wp.com`, `i1.wp.com`, or `i2.wp.com`, WordPress.com will automatically fetch, cache, and serve the image from its global CDN.

**Example URL structure:**
`https://i0.wp.com/YOUR_DOMAIN.com/wp-content/uploads/image.jpg`

### 2. On-the-fly Image Manipulation
You can manipulate images by appending query arguments to the URL.

* **Resize (`w`, `h` or `resize`)**: `?w=300&h=300` or `?resize=300,300`
* **Crop (`crop`)**: `?crop=x,y,w,h` (values are percentages from 0-100 or pixel values)
* **Quality (`quality`)**: `?quality=80` (values from 1-100, useful for WebP/JPEG compression)
* **Strip Exif (`strip`)**: `?strip=all` or `?strip=info` to remove metadata and reduce file size.

### 3. Static File CDN
Beyond images, Site Accelerator can also serve static assets (CSS and JavaScript files) shipped with WordPress Core, Jetpack, and WooCommerce. 

To enable this feature programmatically (if Jetpack is installed):
```php
add_filter( 'jetpack_photon_static_file_is_eligible', '__return_true' );
```

## Implementation Guidelines

* **Domain Requirement**: Your site must be publicly accessible and connected to WordPress.com via Jetpack for the Site Accelerator to fetch your original images.
* **Cache Purging**: Images cached on the `i0.wp.com` grid are cached indefinitely. To update an image, you must change its file name on your origin server (e.g., upload `image-v2.jpg`).
* **HTTPS**: Site Accelerator automatically upgrades image delivery to HTTPS, ensuring secure connections.

## Development Considerations
* **WebP Support**: Site Accelerator will automatically serve WebP images to supported browsers without any additional query parameters.
* **Limitations**: It does not accelerate files hosted outside the `wp-content` directory (like `wp-includes/` unless explicitly supported via the static file CDN). It also has an upload limit per file (typically around 50MB).
