---
name: schedule-a-social-media-post
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Schedule an approved social media post to publish at the intended time and channel.

## Preconditions

- You have approved copy, creative, links, and target channel.
- You have access to the social account or scheduling platform.
- You know the publish date, time, and time zone.

## Steps

1. **Open the scheduler.** Select the correct brand account and channel. → *Expect:* the composer is tied to the intended account.
2. **Add copy and media.** Paste approved text, upload images or video, and add alt text where supported. → *Expect:* the preview matches the approved post.
3. **Check links and tags.** Verify URLs, UTM parameters, mentions, hashtags, and product tags. → *Expect:* links open correctly and tags point to the right accounts.
4. **Set publish time.** Choose the date, time, and time zone. → *Expect:* the scheduled time displays correctly.
5. **Review platform preview.** Check cropping, character limits, thumbnails, and link cards. → *Expect:* the post is readable and visually intact.
6. **Schedule the post.** ⚠️ *Irreversible:* before scheduling, confirm account, time, copy, and media because the post may publish automatically. → *Expect:* the post appears in the scheduled queue.
7. **Record the schedule.** Add the post to the campaign calendar or tracker. → *Expect:* stakeholders can see when it will publish.

## Decision points

- If the preview breaks layout → revise media dimensions or copy before scheduling.
- If approval is missing → save as draft and request approval.
- If the topic is sensitive or news-related → recheck timing shortly before publication.

## Failure modes & recovery

- **F1 Wrong account:** detect the brand or region account is incorrect → delete the scheduled draft and recreate it on the right account.
- **F2 Broken link:** detect the URL fails or lacks tracking → edit the scheduled post before publish.
- **F3 Failed schedule:** detect the post remains a draft or error state → retry or publish manually at the planned time.

## Verification

The post is in the scheduled queue for the correct account, channel, date, time zone, copy, media, and link.

## Variations

- Multi-channel campaign: adapt copy and media separately for each platform.
- Regulated industry: require legal or compliance approval before scheduling.
- Live event: schedule only evergreen posts and leave real-time updates unscheduled.

## Safety & privacy

Low risk. Do not publish private customer data, embargoed announcements, unlicensed media, or internal links.
