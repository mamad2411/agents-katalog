---
name: ai-image-generator-pipeline
description: "Automate AI image generation from webhooks with DALL-E/Flux, optimization, and WordPress/CDN upload. Use when the user needs batch image creation, content automation, or visual asset pipelines."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "FLUX_API_KEY", "WORDPRESS_URL", "WORDPRESS_API_TOKEN", "AWS_S3_BUCKET", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        "bins": ["imagemagick", "ffmpeg"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎨"
    }
  }
---

## Overview

The **AI Image Generator Pipeline** is a production-ready automation skill that transforms webhook triggers into fully optimized, published images across your digital ecosystem. This skill orchestrates a complete workflow: receive webhook events → intelligently generate or enhance prompts → call DALL-E 3 or Flux AI → optimize images for web/mobile → upload to WordPress, AWS S3, or Cloudinary → notify stakeholders.

**Why this matters:** Content teams waste 40% of time on image sourcing and optimization. This skill eliminates manual steps, ensures consistency, and scales visual content production without hiring designers.

**Integrations:** WordPress (REST API), AWS S3, Cloudinary, Slack (notifications), Zapier (webhook triggers), Make.com, Google Drive (backup storage), Stripe (usage billing).

---

## Quick Start

Try these example prompts immediately to see the skill in action:

```
Generate a hero image for a blog post about sustainable fashion with 
DALL-E 3, optimize for web (1920x1080), and upload to my WordPress 
media library with alt text "sustainable fashion hero image".
```

```
Webhook trigger: When a new Shopify product is created, generate 
a product lifestyle image using Flux AI with the product description 
as the prompt, compress to 500KB, and upload to S3 with CDN URL.
```

```
Batch generate 5 variations of a minimalist coffee shop interior 
using DALL-E, apply Instagram-style filters, add watermarks, and 
create a WordPress gallery post with all variations.
```

```
Monitor incoming webhook events from my email marketing platform. 
For each campaign, generate a hero banner image from the campaign 
subject line, optimize for mobile (800x600), and auto-insert into 
the email template's image placeholder.
```

---

## Capabilities

### 1. **Intelligent Prompt Generation**
- Accepts raw webhook data and transforms it into detailed, style-consistent prompts
- Maintains prompt templates for brand consistency (e.g., "minimalist tech startup aesthetic")
- Supports dynamic variables: `{product_name}`, `{brand_color}`, `{target_audience}`
- Automatic prompt enhancement with style descriptors, lighting, composition cues

**Example:**
```
Input webhook: {"product": "Blue Wireless Earbuds", "category": "electronics"}
Generated prompt: "Premium blue wireless earbuds on white marble surface, 
studio lighting, minimalist composition, product photography, 8k, trending on behance"
```

### 2. **Multi-Model Image Generation**
- **DALL-E 3**: Superior quality, better prompt adherence, ideal for branded content
- **Flux AI**: Faster generation, excellent for batch operations, lower cost
- Model selection logic: automatic based on quality/speed requirements or user preference
- Supports size variants: 1024x1024, 1024x1792, 1792x1024 (DALL-E); flexible (Flux)
- Retry logic with exponential backoff for API failures

### 3. **Advanced Image Optimization**
- **Format conversion**: JPEG (web), PNG (transparency), WebP (modern browsers), AVIF (next-gen)
- **Compression**: Intelligent quality settings (0-100), target file sizes (50KB-5MB)
- **Resizing**: Responsive breakpoints (mobile: 375px, tablet: 768px, desktop: 1920px)
- **Watermarking**: Brand logo overlay, text watermarks, opacity control
- **Filters & effects**: Saturation boost, contrast enhancement, color grading presets
- **Metadata embedding**: SEO-friendly alt text, EXIF data, copyright notices

**Example:**
```
Optimize for WordPress: 
- Generate 3 sizes: 300x300 (thumbnail), 800x600 (medium), 1920x1080 (full)
- Convert to WebP with quality 85
- Compress to max 200KB per image
- Add brand watermark (bottom-right, 20% opacity)
- Embed alt text and SEO keywords
```

### 4. **Multi-Destination Publishing**
- **WordPress**: Direct REST API upload to media library, auto-attach to posts, set featured images
- **AWS S3**: Bucket organization by date/category, CloudFront CDN integration, access control
- **Cloudinary**: Cloud-based optimization, dynamic URL transformations, version control
- **Google Drive**: Automated backup, folder organization, sharing permissions
- **Custom webhooks**: POST optimized image URLs to your own systems

### 5. **Webhook Event Processing**
- Listens on custom webhook endpoint (auto-generated)
- Supports: Shopify (product creation), WordPress (post publish), Stripe (payment events), custom JSON
- Webhook signature verification (HMAC-SHA256) for security
- Automatic retry on failed deliveries (3 attempts, exponential backoff)
- Webhook history and audit logs

### 6. **Batch Operations & Scheduling**
- Process multiple images in parallel (configurable concurrency: 1-10)
- Schedule generation at off-peak hours to save API costs
- Cron-based triggers: "Generate product images every morning at 2 AM"
- Dry-run mode to preview outputs before publishing

---

## Configuration

### Required Environment Variables

```bash
# Image Generation APIs
OPENAI_API_KEY=sk-...              # DALL-E 3 access
FLUX_API_KEY=flux-...              # Flux AI access (optional)

# WordPress Integration
WORDPRESS_URL=https://mysite.com   # Your WordPress domain
WORDPRESS_API_TOKEN=abc123xyz      # Application password (WordPress 5.6+)
WORDPRESS_USER=automation          # API user account

# AWS S3 Integration
AWS_S3_BUCKET=my-images-bucket     # S3 bucket name
AWS_ACCESS_KEY_ID=AKIA...          # IAM access key
AWS_SECRET_ACCESS_KEY=...          # IAM secret key
AWS_REGION=us-east-1               # S3 region

# Cloudinary (Optional)
CLOUDINARY_CLOUD_NAME=mycloud      # Cloudinary account
CLOUDINARY_API_KEY=...             # Cloudinary API key
CLOUDINARY_API_SECRET=...          # Cloudinary API secret

# Slack Notifications (Optional)
SLACK_WEBHOOK_URL=https://hooks... # Slack incoming webhook
SLACK_CHANNEL=#content-alerts      # Notification channel

# Security
WEBHOOK_SECRET=your-secret-key     # HMAC signing key for webhooks
```

### Configuration Options

```yaml
# config.yaml example
image_generation:
  model: "dalle3"                   # "dalle3" or "flux"
  quality: "high"                   # "standard", "high"
  size: "1024x1024"                 # DALL-E sizes
  style: "vivid"                    # "vivid" or "natural"

optimization:
  formats: ["webp", "jpg"]          # Output formats
  quality: 85                       # JPEG/WebP quality (0-100)
  max_file_size_kb: 200             # Max compressed size
  add_watermark: true               # Embed brand watermark
  watermark_path: "./assets/logo.png"
  watermark_opacity: 0.2

publishing:
  primary_destination: "s3"         # "wordpress", "s3", "cloudinary"
  secondary_destinations: ["wordpress"]
  s3_folder_structure: "images/{date}/{category}"
  wordpress_post_status: "draft"    # Auto-publish or save as draft
  generate_srcset: true             # Create responsive image sets

webhook:
  port: 3000
  path: "/webhook/images"
  timeout_ms: 30000
  max_retries: 3

notifications:
  slack_enabled: true
  notify_on: ["success", "failure"]
  include_image_preview: true
```

### Setup Instructions

1. **Install dependencies:**
   ```bash
   npm install openai @aws-sdk/client-s3 cloudinary axios
   # or: pip install openai boto3 cloudinary requests
   ```

2. **Set environment variables:**
   ```bash
   export OPENAI_API_KEY="sk-..."
   export WORDPRESS_URL="https://mysite.com"
   # ... (see above for all vars)
   ```

3. **Generate webhook endpoint:**
   ```bash
   # The skill auto-generates a unique webhook URL:
   # https://openclaw.ai/webhooks/ai-image-gen-{skill_id}
   # Copy this and add it to your Shopify/WordPress/Stripe webhook settings
   ```

4. **Test the connection:**
   ```bash
   curl -X POST https://openclaw.ai/webhooks/ai-image-gen-{skill_id} \
     -H "Content-Type: application/json" \
     -d '{"product": "Test Product", "description": "A blue widget"}'
   ```

---

## Example Outputs

### Scenario 1: E-Commerce Product Image Generation

**Input (Shopify webhook):**
```json
{
  "event": "product.created",
  "product": {
    "id": 12345,
    "title": "Wireless Noise-Canceling Headphones",
    "description": "Premium audio with 30-hour battery",
    "vendor": "AudioTech Pro"
  }
}
```

**Generated Prompt:**
```
"Premium wireless noise-canceling headphones in matte black and silver, 
studio product photography, white background, professional lighting, 
high-end audio equipment aesthetic, 8k quality, trending on product hunt"
```

**Output:**
```
WordPress Media Library:
├── audiotech-pro-headphones-1024x1024.webp (150 KB)
├── audiotech-pro-headphones-800x600.webp (98 KB)
├── audiotech-pro-headphones-300x300.webp (32 KB)
└── Meta: alt="Premium wireless noise-canceling headphones by AudioTech Pro"

AWS S3:
└── s3://my-images/images/2024-01-15/electronics/
    ├── audiotech-pro-headphones-full.webp
    └── audiotech-pro-headphones-thumb.webp

Slack Notification:
✅ Image generated successfully
Product: Wireless Noise-Canceling Headphones
Model: DALL-E 3
Size: 1024x1024
File size: 150 KB
WordPress: https://mysite.com/wp-content/uploads/2024/01/audiotech-pro.webp
CDN URL: https://d123.cloudfront.net/images/2024-01-15/audiotech-pro.webp
```

### Scenario 2: Blog Content Image Generation

**Input (WordPress post publish event):**
```json
{
  "event": "post.published",
  "post": {
    "id": 42,
    "title": "10 Sustainable Fashion Trends for 2024",
    "excerpt": "Eco-friendly clothing is no longer niche. Here are the trends defining sustainable fashion.",
    "category": "Fashion"
  }
}
```

**Generated Output:**
```
Image 1 (Hero banner - 1920x1080):
- Prompt: "Sustainable fashion 2024 trends, eco-friendly clothing, 
  organic materials, minimalist aesthetic, diverse models, natural lighting, 
  editorial photography, trending on vogue"
- Format: WebP, 85% quality, 180 KB
- Alt text: "Sustainable fashion trends 2024 - eco-friendly clothing collection"
- Destination: WordPress featured image + S3 backup

Image 2 (Social media square - 1080x1080):
- Same prompt, cropped for Instagram
- Format: WebP, 90% quality, 120 KB
- Watermark: "SustainableFashionBlog.com" (bottom-right, 15% opacity)

Batch Output:
├── featured-image-hero-1920x1080.webp
├── featured-image-hero-1080x1080.webp (Instagram)
├── featured-image-hero-800x600.webp (mobile)
└── featured-image-hero-300x300.webp (thumbnail)
```

---

## Tips & Best Practices

### 1. **Prompt Engineering for Consistency**
- Create brand style guides as prompt templates:
  ```
  Template: "{product_name} in {brand_color}, {style} aesthetic, 
  {lighting}, {composition}, {quality_level}, trending on {platform}"
  ```
- Use consistent descriptors: "studio lighting" vs "natural light", "minimalist" vs "maximalist"
- Test prompts manually first; refine before automating

### 2. **Cost Optimization**
- DALL-E 3: $0.04-0.10 per image (1024x1024). Best for hero/featured images.
- Flux: $0.01-0.03 per image. Best for batch operations and thumbnails.
- **Strategy:** Use Flux for thumbnails/social, DALL-E 3 for hero images
- Set up cost alerts: notify when monthly spend exceeds $100
- Use dry-run mode to preview before publishing (saves API calls)

### 3. **Image Optimization Best Practices**
- **WebP format:** 25-35% smaller than JPEG, supported by 95% of browsers
- **Responsive images:** Generate 3 sizes minimum (mobile/tablet/desktop)
- **File size targets:** Thumbnails <50KB, medium <150KB, full <300KB
- **Watermarking:** Use 15-25% opacity to avoid obscuring content
- **SEO:** Always include descriptive alt text (80-120 characters)

### 4. **Webhook Reliability**
- Implement idempotency: use product ID + timestamp as unique key to prevent duplicates
- Monitor webhook logs: check failed deliveries in the skill dashboard
- Set up Slack alerts for generation failures
- Test webhook signatures in development before production

### 5. **WordPress Integration Tips**
- Use "draft" status initially; review before auto-publishing
- Set featured images automatically: `_thumbnail_id` meta field
- Organize media by folder: `/2024/01/products/` structure
- Leverage WordPress image sizes: register custom sizes in theme
- Use SEO plugins (Yoast) to auto-fill meta descriptions from alt text

### 6. **Batch Processing Efficiency**
- Process in parallel (concurrency: 5-10) to reduce total time
- Schedule batch jobs at 2-4 AM to use cheaper off-peak API rates
- Monitor API rate limits: DALL-E (3 req/min free tier, 50 req/min paid)
- Use caching: store generated prompts to avoid re-generating

### 7. **Brand Consistency Across Channels**
- Create separate prompt templates for each platform:
  - Instagram: square (1080x1080), vibrant colors, trendy aesthetic
  - LinkedIn: professional (1200x627), corporate look, minimal text
  - Website: responsive (1920x1080), aligned with brand guidelines
- Use consistent color palettes: reference brand hex codes in prompts
- A/B test: generate 2 variations, track engagement to refine prompts

---

## Safety & Guardrails

### What This Skill Will NOT Do

1. **Copyright & IP Protection:**
   - Will NOT generate images that mimic copyrighted artwork or trademarked designs
   - Will NOT bypass DALL-E's content policy (no celebrity likenesses without permission)
   - Will NOT create images of real people without explicit consent
   - Recommendation: Review generated images for IP issues before publishing

2. **Harmful Content:**
   - Will NOT generate violent, explicit, or hateful content
   - Will NOT create deepfakes or misleading images
   - Will NOT generate images that violate OpenAI/Flux terms of service
   - Built-in content filters block prohibited prompts

3. **Unauthorized Publishing