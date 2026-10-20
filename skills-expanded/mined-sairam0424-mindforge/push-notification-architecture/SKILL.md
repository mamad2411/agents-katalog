---
name: push-notification-architecture
version: 1.0.0
min_mindforge_version: 10.4.0
status: stable
triggers: push notification system design, notification channel design, notification delivery optimization, notification engagement, notification permission strategy, rich notification design, notification scheduling, notification preference center, silent push notification, push notification deduplication, notification analytics, push notification personalization
---

# Skill — Push Notification Architecture & Engagement

## When this skill activates
This skill activates when designing push notification systems, including channel architecture, permission strategies, delivery optimization, rich content, user preferences, or analytics-driven engagement strategies.

## Mandatory actions when this skill is active

### Before writing any code
1. Design notification channel taxonomy (Android) and categories (iOS) with proper priority levels and user control
2. Plan permission request timing — delay until user sees value, use pre-permission dialogs to improve opt-in rates
3. Establish notification personalization strategy based on user preferences, behavior, and segmentation
4. Define notification content guidelines to maximize engagement while avoiding spam perception

### During implementation
- Implement proper notification permission request flow with clear value proposition before asking
- Create notification channels/categories with appropriate importance levels, sounds, and visual characteristics
- Use rich notifications with images, action buttons, and custom layouts where applicable
- Implement silent push notifications for background data sync without interrupting users
- Build notification preference center allowing users to opt-in/out of specific notification types
- Implement notification deduplication to avoid overwhelming users with similar messages
- Track notification analytics: delivery rate, open rate, conversion rate, dismissal patterns

### After implementation
- Test notification behavior across different OS versions and device manufacturers (Samsung, Xiaomi have custom behavior)
- Verify notification permission request appears at optimal time with good opt-in rate
- Validate notification content renders correctly with proper images, actions, and formatting
- Test notification deep linking to ensure users land on correct screen with proper context
- Monitor notification performance metrics and A/B test different content, timing, and personalization strategies

## Self-check before task completion
- [ ] Notification permission request is delayed until user sees clear value, with pre-permission education
- [ ] Notification channels/categories are well-organized with user-friendly names and descriptions
- [ ] Rich notifications include relevant images, action buttons, and proper formatting
- [ ] Notification preference center allows granular control over notification types and frequency
- [ ] Silent push notifications are used appropriately for background sync without user interruption
- [ ] Analytics track delivery, engagement, and conversion to enable data-driven optimization
- [ ] Notification content follows best practices: clear value, actionable, personalized, non-spammy
