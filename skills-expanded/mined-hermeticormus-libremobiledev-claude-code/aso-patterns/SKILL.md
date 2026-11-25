---
name: aso-patterns
description: "App Store Optimization playbook: iOS keyword field rules, a title and subtitle framework, Google Play description structure, store A/B testing, review prompts, a seasonal calendar, and screenshot sizes. Use when writing store metadata or planning listing experiments."
---

# ASO Patterns

## iOS Keyword Field Optimization

### Rules
- 100 characters total, comma-separated, no spaces after commas
- Never repeat words already in title or subtitle
- Plurals count as separate index terms — include both if space allows
- No competitor brand names (Apple rejects listings for this)
- Special characters and spaces do not index — avoid them

### Example: Fitness App Keyword Field
```
workout,gym,exercise,training,calories,cardio,strength,yoga,HIIT,steps,weight,diet,health,coach
```
Character count: 93 — leaves room to swap underperformers after ranking data accumulates.

### Title + Subtitle Framework
```
Title:   [Primary keyword] - [Differentiator]    (30 chars)
         "Habit Tracker - Daily Planner"

Subtitle: [Secondary keyword] + [Benefit]         (30 chars)
          "Build Routines, Reach Your Goals"
```

---

## Google Play Description Optimization

### Keyword Density Strategy
- Long description is fully indexed — work primary keyword in naturally 3-5x in 4000 chars
- Front-load: first 3 lines visible before "Read more" fold — treat as ad copy
- Structured formatting: use line breaks, bullet points, ALL CAPS section headers (no HTML)
- Keyword placement: title > short description > first paragraph > rest of description

### Opening 3-Line Formula
```
[Primary keyword] that [does unique thing]. [Target user] use [App Name] to [outcome 1],
[outcome 2], and [outcome 3]. [Social proof or differentiator].

Example:
Meditation app that fits into any schedule. Busy professionals use Calm Hour to reduce
stress, improve sleep, and build daily mindfulness habits in just 10 minutes a day.
Over 2 million people have transformed their mornings with Calm Hour.
```

---

## A/B Testing Process

### iOS Product Page Optimization
- Up to 3 treatment variants against default product page
- Can test: app icon, screenshots, preview video, promotional text
- Apple auto-splits traffic; collects until statistical significance
- Minimum 1 week run time; 2-4 weeks recommended for low-traffic apps

### Google Play Experiments
- Create via Play Console > Store Listing > Create experiment
- Supports: icon, feature graphic, screenshots, short/long description
- Traffic split: 10-50% to variant; remaining to original
- Collect 500+ conversions per variant for valid results

### What to Test First (Priority Order)
1. First screenshot (highest single conversion lever)
2. App icon (affects click-through from search results)
3. Title (small changes only — track ranking impact carefully)
4. Short description (Android only — shown in search)

---

## Review Request Implementation

### iOS (SKStoreReviewController)
```swift
import StoreKit

func requestReviewIfAppropriate() {
    // Only request after positive moment
    guard userCompletedPositiveAction else { return }
    guard appLaunchCount > 5 else { return } // avoid asking too early

    if let scene = UIApplication.shared.connectedScenes
        .first(where: { $0.activationState == .foregroundActive }) as? UIWindowScene {
        SKStoreReviewController.requestReview(in: scene)
    }
}
```

Note: Apple controls whether the dialog actually shows. You cannot force it. Max 3 times per 365 days.

### Android (In-App Review API)
```kotlin
import com.google.android.play.core.review.ReviewManagerFactory

class ReviewHelper(private val activity: Activity) {
    fun requestReview(onComplete: () -> Unit) {
        val manager = ReviewManagerFactory.create(activity)
        val request = manager.requestReviewFlow()

        request.addOnCompleteListener { task ->
            if (task.isSuccessful) {
                val reviewInfo = task.result
                val flow = manager.launchReviewFlow(activity, reviewInfo)
                flow.addOnCompleteListener { onComplete() }
            } else {
                onComplete() // continue user flow even if review fails
            }
        }
    }
}
```

---

## Seasonal ASO Calendar

| Period | Keyword Strategy |
|--------|-----------------|
| Jan 1-15 | new year resolutions, goals, habits, fresh start |
| Feb | valentine, love, gifts, couples |
| Aug-Sep | back to school, study, organize, productivity |
| Nov | black friday, deals, gifts, holiday |
| Dec | christmas, new year, review, wrap up |

Update keyword field and promotional text (iOS) before each season. Promotional text can be updated without resubmitting the app.

---

## Screenshot Size Reference

### iOS
| Device | Resolution | Required? |
|--------|------------|-----------|
| 6.9" iPhone | 1320x2868 | Yes (new) |
| 6.5" iPhone | 1242x2688 | Yes |
| 5.5" iPhone | 1242x2208 | Yes |
| 12.9" iPad | 2048x2732 | Yes (if iPad supported) |

### Android
| Device | Resolution | Required? |
|--------|------------|-----------|
| Phone | 1080x1920 min | Yes |
| 7" tablet | 1024x600 min | Recommended |
| 10" tablet | 1280x800 min | Recommended |
| Feature graphic | 1024x500 | Yes |

---

## Conversion Rate Anti-Patterns

- Screenshots showing UI without context or user benefit
- Title that is brand name only with no keywords ("MyApp" not "MyApp - Task Manager")
- Description starting with "Welcome to MyApp" instead of value proposition
- Not responding to negative reviews (algorithms factor in developer responsiveness)
- Requesting review on first app launch before user has experienced value
