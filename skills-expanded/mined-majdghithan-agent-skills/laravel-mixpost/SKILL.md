---
name: laravel-mixpost
description: Self-host and operate Mixpost (the open/self-hosted social-media scheduler by Inovector) inside a Laravel app - install, edition choice (Lite vs Pro/Team vs Enterprise), Horizon/Redis/queue setup, connecting providers (LinkedIn, Meta/Facebook/Instagram, TikTok, YouTube), scheduling posts, uploading media, and the real-world gotchas (LinkedIn API-version sunsetting, laptop-sleep missed schedules, asset/manifest issues). Use when installing Mixpost, connecting a social provider, scheduling/publishing posts programmatically, or debugging why a Mixpost post failed to publish.
---

# Mixpost (self-hosted social scheduler on Laravel)

Mixpost by Inovector is a self-hostable social-media management/scheduling app that installs *into* a Laravel application. It publishes to LinkedIn, Facebook Pages, Instagram, TikTok, YouTube, X, and more, on a schedule, from your own server - no third-party SaaS fees.

## Editions - pick the right one (this decision saves pain)

- **Mixpost Lite** - free/open-source, single workspace, core scheduling. Good for one account.
- **Mixpost Pro / Team** (`inovector/mixpost-pro-team`) - paid license; multiple workspaces, more providers, media library, AI features, engagement inbox, a built-in MCP server (v6+). **The right choice for a solo operator or small team.**
- **Mixpost Enterprise** (`inovector/mixpost-enterprise`) - adds a full **SaaS layer** (customers, subscriptions, payments, `mixpost_e_*` tables). **Do NOT use this for a single-user/internal tool** - the SaaS layer adds an email-verification wall, a second asset bundle, and payment-webhook CSRF handling that cause avoidable early bugs. An Enterprise *license key* also authorizes Pro, so you can install Pro with the same credentials.

## Requirements

| Dependency | Requirement |
|---|---|
| PHP | 8.3+ (**8.4+** if on Laravel 13 / Symfony 8) |
| Laravel | 11 / 12 / 13 (per Mixpost major) |
| Redis | 6.2+ |
| Queues | `laravel/horizon` ^5 (Mixpost provides supervisor config) |
| FFmpeg | required (video processing) |
| DB | MySQL or PostgreSQL |

## Install (Pro/Team)

```bash
# auth.json holds the packages.inovector.com license credentials - GITIGNORE IT (contains the key)
composer require inovector/mixpost-pro-team "^6.0"
php artisan mixpost:install         # migrations, config, first workspace
php artisan mixpost:publish-assets  # publishes to public/vendor/mixpost
```
Then follow the install steps for **job batching config**, **CSRF exclusions** for provider webhooks, `QUEUE_CONNECTION=redis`, Horizon supervisors (`'defaults' => \Inovector\Mixpost\Horizon::supervisors()`), and creating the admin user. Serve the app over **HTTPS** - LinkedIn/Meta OAuth redirect URLs require it.

**Redis prefix isolation:** if other Laravel projects share the same Redis, set a distinct `REDIS_PREFIX` so their queues don't collide with Mixpost's `publish-post` queue.

## Running it reliably

- Mixpost needs the **Laravel scheduler running every minute** (cron, or a supervised `schedule:work`) plus **Horizon** processing the queues. Run both as supervised/launchd services with restart-on-crash.
- **Laptop-sleep caveat:** Mixpost does **not** back-fill scheduler ticks missed while the machine slept. If you self-host on a laptop, keep it awake during posting windows (`caffeinate` on macOS) and schedule posts inside awake hours - a post scheduled while asleep simply won't fire.

## Connecting providers (each is its own developer app)

- **LinkedIn** - a LinkedIn developer app with the "Share on LinkedIn" product (personal-profile posting is self-serve). Company Pages need the Community Management API.
- **Meta (Facebook Page + Instagram)** - a Meta app with "Facebook Login for Business" and scopes `pages_manage_posts`, `instagram_content_publish`, etc. Dev mode is fine for your own accounts; IG must be a Business/Creator account linked to the Page.
- **TikTok** - a TikTok developer app with the Content Posting API. **Unaudited apps can only create drafts / SELF_ONLY** - drafts land in the TikTok app inbox to publish manually. Submit the Direct Post audit early (2-4 weeks).
- **YouTube** - Google Cloud project + YouTube Data API v3. **Unaudited uploads are locked private** - flip to public in Studio, or submit the compliance audit.

## Publishing / scheduling programmatically

Posts are workspace-scoped. Each post has one or more **versions** whose `content` is JSON, roughly:
```json
[{ "body": "<the text>", "media": ["<media_id>"], "url": null }]
```
Set the post's `scheduled_at` in **UTC** and its status to scheduled. Prefer the **built-in Mixpost MCP server** (v6+, `create-post-tool` / `list-accounts-tool`) or Mixpost's own APIs over hand-writing rows.

**Upload media** with the uploader, not by hand:
```php
use Inovector\Mixpost\Facades\WorkspaceManager;
use Inovector\Mixpost\Support\MediaUploader;

WorkspaceManager::loadById($workspaceId);
$mediaId = MediaUploader::fromLocalPath($absolutePath)->uploadAndInsert()->id;
// then reference $mediaId in the post version's "media" array
```
(The MCP `upload-media-by-url-tool` has a `getUrlGenerator()` bug in some builds - use `MediaUploader::fromLocalPath()`.)

## Real-world gotchas (the ones that cost hours)

### LinkedIn "NONEXISTENT_VERSION" (HTTP 426) on publish
Mixpost hardcodes the LinkedIn REST API version header (format `YYYYMM`, e.g. `202507`). **LinkedIn sunsets each version ~12 months after release**, so an older Mixpost build eventually sends a version LinkedIn no longer accepts, and publishing fails with 426 / `NONEXISTENT_VERSION`. Fix: override the LinkedIn provider to send a version **within the last ~12 months**, and **bump it every few months**. Note the publish path may resolve the provider via a hardcoded `connectLinkedinProvider()` method rather than the `providers()` map - override both.

### LinkedIn service form "saves nothing"
In some builds the LinkedIn service settings form silently saves nothing because a hidden `app_id` field validates `null` against a `string` rule without `nullable`. Override the service/manager to make it nullable.

### "The manifest.json file could not be found" at /mixpost
Usually after `composer update`. Re-run `php artisan mixpost:publish-assets --force=1`.

### Post scheduled but never published
Check, in order: (1) is the **scheduler** actually running every minute? (2) is **Horizon** up and draining the queue? (3) did the machine **sleep** through the scheduled time (no back-fill)? (4) is the provider **token** still valid / the app still in the right mode (TikTok drafts, YouTube private)?

## Sources
[Mixpost docs](https://docs.mixpost.app) · [Inovector Mixpost](https://mixpost.app) · [LinkedIn API versioning](https://learn.microsoft.com/en-us/linkedin/marketing/versioning) · [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started)
