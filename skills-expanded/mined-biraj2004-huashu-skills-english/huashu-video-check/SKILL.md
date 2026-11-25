---
name: huashu-video-check
description: Check video titles, thumbnails, and opening hooks based on MrBeast's strategies. Use when the user mentions "video title", "thumbnail", "click-through rate", "CTR", or "watch time".
---

# Video Thumbnail, Title & Hook Review

A professional review capability for video titles, thumbnails, and content engagement — based on the MrBeast methodology — to improve click-through rate and watch time.

## When to Use This Skill

This skill is automatically loaded when:

- The user says "check the title and thumbnail" or "check content engagement"
- After a video script draft is completed
- The user mentions "low click-through rate" or "short watch time"
- Need to optimise video titles or thumbnails

## Core Objectives

- **Improve click-through rate**: Titles and thumbnails attract users to click
- **Improve watch time**: Strong content engagement keeps viewers watching to the end
- **Build reusable formulas**: Standardised thumbnail, title, and engagement strategies

## Review Dimensions

### 1️⃣ Title Review (Strong Contrast Strategy)

### 2️⃣ Thumbnail Review (Results-First Strategy)

### 3️⃣ Content Engagement Review (Opening confirmation → Mid-section surprise → Closing payoff)

---

## 1️⃣ Title Review: Strong Contrast Strategy

### Core Principle

**Focus on the strongest single contrast — don't list everything**

### 5 Strong Contrast Formulas

#### Formula 1: Quantity Contrast

**Format**: `Small quantity vs Large quantity`

**Examples**:

- ✅ "1 Prompt Wrote 1,000 Lines of Code"
- ✅ "3 People vs a Team of 300 — Who Wins?"
- ✅ "1 Tool That Replaces 10 Tools"

**Best for**: Tutorial content, efficiency content, tool reviews

---

#### Formula 2: Price Contrast

**Format**: `Low price vs High price` or `Free vs Paid`

**Examples**:

- ✅ "£15 vs £150 AI — How Big Is the Gap?"
- ✅ "What Can Free AI Do? I Tested 10 Tools"
- ✅ "Same Features — Is Claude Worth 10x More Than GPT?"

**Best for**: Reviews, comparisons

---

#### Formula 3: Results Contrast

**Format**: `Low results vs High results` or `Before vs After`

**Examples**:

- ✅ "300K Followers vs 0 — I Only Did One Thing Right"
- ✅ "From 0 to 1,000 Views — I Used 3 Techniques"
- ✅ "Same Video, Different Title — Views Increased 10x"

**Best for**: Experience sharing, growth stories

---

#### Formula 4: Strength Contrast

**Format**: `Beginner / Underdog vs Expert / Powerhouse`

**Examples**:

- ✅ "Beginner vs Cursor: Who Writes This Feature Faster?"
- ✅ "I Pitted AI Against a Programmer — The Results Were Shocking"
- ✅ "Complete Novice Attempts to Build an App with AI"

**Best for**: Challenge content, experiment content

---

#### Formula 5: Time Contrast

**Format**: `Short time vs Long time` or `Fast vs Slow`

**Examples**:

- ✅ "3 Minutes vs 3 Hours: Is AI Coding Actually Faster?"
- ✅ "I Finished in 1 Day What Took Others a Week"
- ✅ "From Learning to Proficiency — Cursor Takes Just 10 Minutes"

**Best for**: Tutorial content, efficiency content

---

### Title Type Selection Guide

| Content Type | Recommended Title Type | Example |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-video-check
description: Check video titles, thumbnails, and opening hooks based on MrBeast's strategies. Use when the user mentions "video title", "thumbnail", "click-through rate", "CTR", or "watch time".
---

# Video Thumbnail, Title & Hook Review

A professional review capability for video titles, thumbnails, and content engagement — based on the MrBeast methodology — to improve click-through rate and watch time.

## When to Use This Skill

This skill is automatically loaded when:

- The user says "check the title and thumbnail" or "check content engagement"
- After a video script draft is completed
- The user mentions "low click-through rate" or "short watch time"
- Need to optimise video titles or thumbnails

## Core Objectives

- **Improve click-through rate**: Titles and thumbnails attract users to click
- **Improve watch time**: Strong content engagement keeps viewers watching to the end
- **Build reusable formulas**: Standardised thumbnail, title, and engagement strategies

## Review Dimensions

### 1️⃣ Title Review (Strong Contrast Strategy)

### 2️⃣ Thumbnail Review (Results-First Strategy)

### 3️⃣ Content Engagement Review (Opening confirmation → Mid-section surprise → Closing payoff)

---

## 1️⃣ Title Review: Strong Contrast Strategy

### Core Principle

**Focus on the strongest single contrast — don't list everything**

### 5 Strong Contrast Formulas

#### Formula 1: Quantity Contrast

**Format**: `Small quantity vs Large quantity`

**Examples**:

- ✅ "1 Prompt Wrote 1,000 Lines of Code"
- ✅ "3 People vs a Team of 300 — Who Wins?"
- ✅ "1 Tool That Replaces 10 Tools"

**Best for**: Tutorial content, efficiency content, tool reviews

---

#### Formula 2: Price Contrast

**Format**: `Low price vs High price` or `Free vs Paid`

**Examples**:

- ✅ "£15 vs £150 AI — How Big Is the Gap?"
- ✅ "What Can Free AI Do? I Tested 10 Tools"
- ✅ "Same Features — Is Claude Worth 10x More Than GPT?"

**Best for**: Reviews, comparisons

---

#### Formula 3: Results Contrast

**Format**: `Low results vs High results` or `Before vs After`

**Examples**:

- ✅ "300K Followers vs 0 — I Only Did One Thing Right"
- ✅ "From 0 to 1,000 Views — I Used 3 Techniques"
- ✅ "Same Video, Different Title — Views Increased 10x"

**Best for**: Experience sharing, growth stories

---

#### Formula 4: Strength Contrast

**Format**: `Beginner / Underdog vs Expert / Powerhouse`

**Examples**:

- ✅ "Beginner vs Cursor: Who Writes This Feature Faster?"
- ✅ "I Pitted AI Against a Programmer — The Results Were Shocking"
- ✅ "Complete Novice Attempts to Build an App with AI"

**Best for**: Challenge content, experiment content

---

#### Formula 5: Time Contrast

**Format**: `Short time vs Long time` or `Fast vs Slow`

**Examples**:

- ✅ "3 Minutes vs 3 Hours: Is AI Coding Actually Faster?"
- ✅ "I Finished in 1 Day What Took Others a Week"
- ✅ "From Learning to Proficiency — Cursor Takes Just 10 Minutes"

**Best for**: Tutorial content, efficiency content

---

### Title Type Selection Guide

| Content Type | Recommended Title Type | Example |
|-------------|----------------------|---------|
| Tutorial | Results contrast, time contrast | "One Cursor Feature That Doubled My Efficiency" |
| Review | Price/performance contrast | "Free AI vs Paid AI — How Big Is the Gap?" |
| Challenge | Strength/quantity contrast | "Beginner Challenges Themselves to Build an App with AI" |
| Experience sharing | Results contrast | "Same Video, Different Title — Views Increased 10x" |

---

### Title Types to Avoid

❌ **Listicle-style**: "5 Common Features of Cursor"

- Problem: No conflict, no suspense
- Fix: Focus on the 1 strongest feature → "One Cursor Feature That Doubled My Efficiency"

❌ **Bland**: "Cursor Tutorial"

- Problem: No attraction, no specific value
- Fix: Add results contrast → "Get Started with Cursor in 3 Minutes — 5x Faster Workflow"

❌ **Abstract**: "The Future Trends of AI Coding"

- Problem: Too abstract, hard to picture
- Fix: Make it specific → "3 Months of AI-Assisted Coding — Here's What I Found"

---

### Title Checklist

When reviewing a title, confirm:

- [ ] Does the title have a clear contrast or conflict? (quantity, price, results, strength, or time)
- [ ] Is the title focused on 1 core point? (not listing multiple things)
- [ ] Can the title make the viewer picture a scene or scenario?
- [ ] Does the title create suspense? (makes you want to know the outcome)
- [ ] Is the title the right length? (15–25 words; no more than 30)
- [ ] Is the title honest? (can be delivered on in the video)

---

## 2️⃣ Thumbnail Review: Results Display Strategy

### Core Principle

**Choose the thumbnail strategy based on subscriber count and content type**

### Face Thumbnails (Use with Caution)

**✅ Suitable for**:

- Subscriber count > 100K (face has brand value)
- Content types: Challenge content, Vlog, high-emotion content
- Extreme and consistent expression (surprise / excitement / shock)
- An established, fixed thumbnail style

**❌ Not suitable for**:

- Subscriber count < 100K (face has no brand value; results are more direct)
- Technical tutorial content (results matter more than emotion)
- Different expression every video (can't build visual consistency)

---

### Results-Display Thumbnails (Recommended — Test First)

**✅ Suitable for**:

- Tutorial content: Before/After comparisons
- Review content: Product close-up + key data
- Technical content: Code/interface screenshots + result display
- Subscriber count < 100K (results are more direct than a face)

---

### Thumbnail Design Elements

#### 1. Strong Contrast

- **Colour contrast**: Warm vs cool tones (blue + orange)
- **Size contrast**: Core element enlarged; secondary elements reduced
- **Number contrast**: Large number vs small number (300K vs 0)

#### 2. Visual Focus

- **1–2 core elements**: Don't crowd the thumbnail
- **Clear visual anchor**: What does the viewer see first?

#### 3. Minimal Text

- **0–5 words**: Visual should carry the message; minimise text
- **Consistent font**: Fixed font to build brand recognition

#### 4. Consistent Style

- **Fixed colour scheme**: e.g., blue + orange
- **Fixed layout**: e.g., result on the left, number on the right
- **Fixed font**: Consistent thumbnail style every video

---

### Thumbnail Type Recommendations

| Content Type | Recommended Thumbnail | Example |
|-------------|----------------------|---------|
| Tutorial | Before/After comparison | Original code on left, optimised on right |
| Review | Product close-up + data | Product UI + performance numbers |
| Challenge | Extreme scene + emotion | Optional face (if it tests well) |
| Experience sharing | Data comparison | View count growth chart |

---

### Thumbnail Designs to Avoid

❌ **Text-only thumbnails**: Too much information; no visual impact
❌ **Too many elements**: Visually chaotic; no clear focus
❌ **Different style every video**: Can't build viewer recognition

---

### A/B Testing Recommendation

- Prepare 2 thumbnails for the same video
- A: Face thumbnail (if you want to test this)
- B: Results-display thumbnail
- Track click-through rate data; keep the better-performing one

---

### Thumbnail Checklist

When reviewing a thumbnail, confirm:

- [ ] Does the thumbnail type suit the content and subscriber count? (results display first)
- [ ] Does the thumbnail have strong contrast? (colour, size, numbers)
- [ ] Does the thumbnail have a clear visual focus? (1–2 core elements)
- [ ] Is the text on the thumbnail minimal? (0–5 words)
- [ ] Is the thumbnail style consistent? (colour scheme, layout, font)
- [ ] Does the thumbnail complement the title? (dual attraction: visual + text)

---

## 3️⃣ Content Engagement Review: Suspense Delay Strategy

### Core Principle

**Build suspense in the opening, exceed expectations in the middle, deliver on the promise at the close**

### Standard Engagement Structure

```text
Title / Thumbnail: Core suspense (strongest contrast or conflict)
    ↓
Opening (first 30 seconds – 1 minute):
- Confirm the title promise exists (build trust)
- Create suspense: "Can it actually be done?"
- Preview what's coming: "But before that, first..."
    ↓
Middle section (main content):
- Core teaching / demonstration
- Add an "unexpected surprise" (exceeds expectations)
- Keep reminding of the suspense: "Almost there, nearly time..."
    ↓
Closing (final 1–3 minutes):
- Deliver on the title promise (show the core content)
- Summarise key points
- Call to Action (subscribe / like / comment)
```

---

### Duration Control Guide

| Total Video Length | Opening Confirmation | Middle Content | Closing Payoff |
|-------------------|---------------------|----------------|----------------|
| 3–5 minutes | 30 seconds | 2–3 minutes | 1 minute |
| 5–10 minutes | 1 minute | 6–7 minutes | 2 minutes |
| 10–15 minutes | 1–2 minutes | 8–10 minutes | 3 minutes |

---

### Engagement Review Example

#### Example: Tutorial Video

**Title**: One Cursor Feature That Doubled My Efficiency

**✅ Correct engagement**:

**Opening (30 seconds)**:

```text
"There's a Cursor feature that saves me 3 hours on every project.
What feature? I'll demo it shortly.
But first, let me quickly run through the basics of Cursor,
so you can understand why this feature is so powerful."
```

← Confirms the promise exists, builds suspense

**Middle section (5–8 minutes)**:

```text
- Basic feature walkthrough
- Installation and setup
- Common issues
(Viewer: "Oh, there's this too — learnt something.")
```

← Unexpected surprise, exceeds expectations

**Closing (2 minutes)**:

```text
"Right, now for that core feature.
Here it is (demo)... See how powerful that is?
I've used it for 3 months — saves 3 hours on every project..."
```

← Delivers on the promise, closes the loop

---

**❌ Incorrect engagement**:

**Opening completely ignores the title**:

```text
"Today we're learning to use Cursor. Cursor is an AI coding tool..."
```

Problem: Viewer doesn't know when "the efficiency-doubling feature" will appear → they drop off mid-video

**Opening reveals everything upfront**:

```text
"Cursor has a feature called XX that doubles your efficiency. Here's how to use it..."
```

Problem: No suspense for the rest → shorter watch time

**Title says A, video is all about B**:

```text
Title: "One Cursor Feature That Doubled My Efficiency"
Video: Covers all basic Cursor features; the "efficiency-doubling feature" is never addressed
```

Problem: Feels deceptive → subscriber loss

**Suspense drags on too long**:

```text
10-minute video; the "efficiency-doubling feature" isn't mentioned until 8 minutes in
```

Problem: Viewer loses patience → drops off mid-video

---

### Common Errors (Must Avoid)

| Error | Consequence | Correct Approach |
|-------|-------------|-----------------|
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Tutorial | Results contrast, time contrast | "One Cursor Feature That Doubled My Efficiency" |
| Review | Price/performance contrast | "Free AI vs Paid AI — How Big Is the Gap?" |
| Challenge | Strength/quantity contrast | "Beginner Challenges Themselves to Build an App with AI" |
| Experience sharing | Results contrast | "Same Video, Different Title — Views Increased 10x" |

---

### Title Types to Avoid

❌ **Listicle-style**: "5 Common Features of Cursor"

- Problem: No conflict, no suspense
- Fix: Focus on the 1 strongest feature → "One Cursor Feature That Doubled My Efficiency"

❌ **Bland**: "Cursor Tutorial"

- Problem: No attraction, no specific value
- Fix: Add results contrast → "Get Started with Cursor in 3 Minutes — 5x Faster Workflow"

❌ **Abstract**: "The Future Trends of AI Coding"

- Problem: Too abstract, hard to picture
- Fix: Make it specific → "3 Months of AI-Assisted Coding — Here's What I Found"

---

### Title Checklist

When reviewing a title, confirm:

- [ ] Does the title have a clear contrast or conflict? (quantity, price, results, strength, or time)
- [ ] Is the title focused on 1 core point? (not listing multiple things)
- [ ] Can the title make the viewer picture a scene or scenario?
- [ ] Does the title create suspense? (makes you want to know the outcome)
- [ ] Is the title the right length? (15–25 words; no more than 30)
- [ ] Is the title honest? (can be delivered on in the video)

---

## 2️⃣ Thumbnail Review: Results Display Strategy

### Core Principle

**Choose the thumbnail strategy based on subscriber count and content type**

### Face Thumbnails (Use with Caution)

**✅ Suitable for**:

- Subscriber count > 100K (face has brand value)
- Content types: Challenge content, Vlog, high-emotion content
- Extreme and consistent expression (surprise / excitement / shock)
- An established, fixed thumbnail style

**❌ Not suitable for**:

- Subscriber count < 100K (face has no brand value; results are more direct)
- Technical tutorial content (results matter more than emotion)
- Different expression every video (can't build visual consistency)

---

### Results-Display Thumbnails (Recommended — Test First)

**✅ Suitable for**:

- Tutorial content: Before/After comparisons
- Review content: Product close-up + key data
- Technical content: Code/interface screenshots + result display
- Subscriber count < 100K (results are more direct than a face)

---

### Thumbnail Design Elements

#### 1. Strong Contrast

- **Colour contrast**: Warm vs cool tones (blue + orange)
- **Size contrast**: Core element enlarged; secondary elements reduced
- **Number contrast**: Large number vs small number (300K vs 0)

#### 2. Visual Focus

- **1–2 core elements**: Don't crowd the thumbnail
- **Clear visual anchor**: What does the viewer see first?

#### 3. Minimal Text

- **0–5 words**: Visual should carry the message; minimise text
- **Consistent font**: Fixed font to build brand recognition

#### 4. Consistent Style

- **Fixed colour scheme**: e.g., blue + orange
- **Fixed layout**: e.g., result on the left, number on the right
- **Fixed font**: Consistent thumbnail style every video

---

### Thumbnail Type Recommendations

| Content Type | Recommended Thumbnail | Example |
|-------------|----------------------|---------|
| Tutorial | Before/After comparison | Original code on left, optimised on right |
| Review | Product close-up + data | Product UI + performance numbers |
| Challenge | Extreme scene + emotion | Optional face (if it tests well) |
| Experience sharing | Data comparison | View count growth chart |

---

### Thumbnail Designs to Avoid

❌ **Text-only thumbnails**: Too much information; no visual impact
❌ **Too many elements**: Visually chaotic; no clear focus
❌ **Different style every video**: Can't build viewer recognition

---

### A/B Testing Recommendation

- Prepare 2 thumbnails for the same video
- A: Face thumbnail (if you want to test this)
- B: Results-display thumbnail
- Track click-through rate data; keep the better-performing one

---

### Thumbnail Checklist

When reviewing a thumbnail, confirm:

- [ ] Does the thumbnail type suit the content and subscriber count? (results display first)
- [ ] Does the thumbnail have strong contrast? (colour, size, numbers)
- [ ] Does the thumbnail have a clear visual focus? (1–2 core elements)
- [ ] Is the text on the thumbnail minimal? (0–5 words)
- [ ] Is the thumbnail style consistent? (colour scheme, layout, font)
- [ ] Does the thumbnail complement the title? (dual attraction: visual + text)

---

## 3️⃣ Content Engagement Review: Suspense Delay Strategy

### Core Principle

**Build suspense in the opening, exceed expectations in the middle, deliver on the promise at the close**

### Standard Engagement Structure

```text
Title / Thumbnail: Core suspense (strongest contrast or conflict)
    ↓
Opening (first 30 seconds – 1 minute):
- Confirm the title promise exists (build trust)
- Create suspense: "Can it actually be done?"
- Preview what's coming: "But before that, first..."
    ↓
Middle section (main content):
- Core teaching / demonstration
- Add an "unexpected surprise" (exceeds expectations)
- Keep reminding of the suspense: "Almost there, nearly time..."
    ↓
Closing (final 1–3 minutes):
- Deliver on the title promise (show the core content)
- Summarise key points
- Call to Action (subscribe / like / comment)
```

---

### Duration Control Guide

| Total Video Length | Opening Confirmation | Middle Content | Closing Payoff |
|-------------------|---------------------|----------------|----------------|
| 3–5 minutes | 30 seconds | 2–3 minutes | 1 minute |
| 5–10 minutes | 1 minute | 6–7 minutes | 2 minutes |
| 10–15 minutes | 1–2 minutes | 8–10 minutes | 3 minutes |

---

### Engagement Review Example

#### Example: Tutorial Video

**Title**: One Cursor Feature That Doubled My Efficiency

**✅ Correct engagement**:

**Opening (30 seconds)**:

```text
"There's a Cursor feature that saves me 3 hours on every project.
What feature? I'll demo it shortly.
But first, let me quickly run through the basics of Cursor,
so you can understand why this feature is so powerful."
```

← Confirms the promise exists, builds suspense

**Middle section (5–8 minutes)**:

```text
- Basic feature walkthrough
- Installation and setup
- Common issues
(Viewer: "Oh, there's this too — learnt something.")
```

← Unexpected surprise, exceeds expectations

**Closing (2 minutes)**:

```text
"Right, now for that core feature.
Here it is (demo)... See how powerful that is?
I've used it for 3 months — saves 3 hours on every project..."
```

← Delivers on the promise, closes the loop

---

**❌ Incorrect engagement**:

**Opening completely ignores the title**:

```text
"Today we're learning to use Cursor. Cursor is an AI coding tool..."
```

Problem: Viewer doesn't know when "the efficiency-doubling feature" will appear → they drop off mid-video

**Opening reveals everything upfront**:

```text
"Cursor has a feature called XX that doubles your efficiency. Here's how to use it..."
```

Problem: No suspense for the rest → shorter watch time

**Title says A, video is all about B**:

```text
Title: "One Cursor Feature That Doubled My Efficiency"
Video: Covers all basic Cursor features; the "efficiency-doubling feature" is never addressed
```

Problem: Feels deceptive → subscriber loss

**Suspense drags on too long**:

```text
10-minute video; the "efficiency-doubling feature" isn't mentioned until 8 minutes in
```

Problem: Viewer loses patience → drops off mid-video

---

### Common Errors (Must Avoid)

| Error | Consequence | Correct Approach |
|-------|-------------|-----------------|
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Tutorial | Results contrast, time contrast | "One Cursor Feature That Doubled My Efficiency" |
| Review | Price/performance contrast | "Free AI vs Paid AI — How Big Is the Gap?" |
| Challenge | Strength/quantity contrast | "Beginner Challenges Themselves to Build an App with AI" |
| Experience sharing | Results contrast | "Same Video, Different Title — Views Increased 10x" |

---

### Title Types to Avoid

❌ **Listicle-style**: "5 Common Features of Cursor"

- Problem: No conflict, no suspense
- Fix: Focus on the 1 strongest feature → "One Cursor Feature That Doubled My Efficiency"

❌ **Bland**: "Cursor Tutorial"

- Problem: No attraction, no specific value
- Fix: Add results contrast → "Get Started with Cursor in 3 Minutes — 5x Faster Workflow"

❌ **Abstract**: "The Future Trends of AI Coding"

- Problem: Too abstract, hard to picture
- Fix: Make it specific → "3 Months of AI-Assisted Coding — Here's What I Found"

---

### Title Checklist

When reviewing a title, confirm:

- [ ] Does the title have a clear contrast or conflict? (quantity, price, results, strength, or time)
- [ ] Is the title focused on 1 core point? (not listing multiple things)
- [ ] Can the title make the viewer picture a scene or scenario?
- [ ] Does the title create suspense? (makes you want to know the outcome)
- [ ] Is the title the right length? (15–25 words; no more than 30)
- [ ] Is the title honest? (can be delivered on in the video)

---

## 2️⃣ Thumbnail Review: Results Display Strategy

### Core Principle

**Choose the thumbnail strategy based on subscriber count and content type**

### Face Thumbnails (Use with Caution)

**✅ Suitable for**:

- Subscriber count > 100K (face has brand value)
- Content types: Challenge content, Vlog, high-emotion content
- Extreme and consistent expression (surprise / excitement / shock)
- An established, fixed thumbnail style

**❌ Not suitable for**:

- Subscriber count < 100K (face has no brand value; results are more direct)
- Technical tutorial content (results matter more than emotion)
- Different expression every video (can't build visual consistency)

---

### Results-Display Thumbnails (Recommended — Test First)

**✅ Suitable for**:

- Tutorial content: Before/After comparisons
- Review content: Product close-up + key data
- Technical content: Code/interface screenshots + result display
- Subscriber count < 100K (results are more direct than a face)

---

### Thumbnail Design Elements

#### 1. Strong Contrast

- **Colour contrast**: Warm vs cool tones (blue + orange)
- **Size contrast**: Core element enlarged; secondary elements reduced
- **Number contrast**: Large number vs small number (300K vs 0)

#### 2. Visual Focus

- **1–2 core elements**: Don't crowd the thumbnail
- **Clear visual anchor**: What does the viewer see first?

#### 3. Minimal Text

- **0–5 words**: Visual should carry the message; minimise text
- **Consistent font**: Fixed font to build brand recognition

#### 4. Consistent Style

- **Fixed colour scheme**: e.g., blue + orange
- **Fixed layout**: e.g., result on the left, number on the right
- **Fixed font**: Consistent thumbnail style every video

---

### Thumbnail Type Recommendations

| Content Type | Recommended Thumbnail | Example |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-video-check
description: Check video titles, thumbnails, and opening hooks based on MrBeast's strategies. Use when the user mentions "video title", "thumbnail", "click-through rate", "CTR", or "watch time".
---

# Video Thumbnail, Title & Hook Review

A professional review capability for video titles, thumbnails, and content engagement — based on the MrBeast methodology — to improve click-through rate and watch time.

## When to Use This Skill

This skill is automatically loaded when:

- The user says "check the title and thumbnail" or "check content engagement"
- After a video script draft is completed
- The user mentions "low click-through rate" or "short watch time"
- Need to optimise video titles or thumbnails

## Core Objectives

- **Improve click-through rate**: Titles and thumbnails attract users to click
- **Improve watch time**: Strong content engagement keeps viewers watching to the end
- **Build reusable formulas**: Standardised thumbnail, title, and engagement strategies

## Review Dimensions

### 1️⃣ Title Review (Strong Contrast Strategy)

### 2️⃣ Thumbnail Review (Results-First Strategy)

### 3️⃣ Content Engagement Review (Opening confirmation → Mid-section surprise → Closing payoff)

---

## 1️⃣ Title Review: Strong Contrast Strategy

### Core Principle

**Focus on the strongest single contrast — don't list everything**

### 5 Strong Contrast Formulas

#### Formula 1: Quantity Contrast

**Format**: `Small quantity vs Large quantity`

**Examples**:

- ✅ "1 Prompt Wrote 1,000 Lines of Code"
- ✅ "3 People vs a Team of 300 — Who Wins?"
- ✅ "1 Tool That Replaces 10 Tools"

**Best for**: Tutorial content, efficiency content, tool reviews

---

#### Formula 2: Price Contrast

**Format**: `Low price vs High price` or `Free vs Paid`

**Examples**:

- ✅ "£15 vs £150 AI — How Big Is the Gap?"
- ✅ "What Can Free AI Do? I Tested 10 Tools"
- ✅ "Same Features — Is Claude Worth 10x More Than GPT?"

**Best for**: Reviews, comparisons

---

#### Formula 3: Results Contrast

**Format**: `Low results vs High results` or `Before vs After`

**Examples**:

- ✅ "300K Followers vs 0 — I Only Did One Thing Right"
- ✅ "From 0 to 1,000 Views — I Used 3 Techniques"
- ✅ "Same Video, Different Title — Views Increased 10x"

**Best for**: Experience sharing, growth stories

---

#### Formula 4: Strength Contrast

**Format**: `Beginner / Underdog vs Expert / Powerhouse`

**Examples**:

- ✅ "Beginner vs Cursor: Who Writes This Feature Faster?"
- ✅ "I Pitted AI Against a Programmer — The Results Were Shocking"
- ✅ "Complete Novice Attempts to Build an App with AI"

**Best for**: Challenge content, experiment content

---

#### Formula 5: Time Contrast

**Format**: `Short time vs Long time` or `Fast vs Slow`

**Examples**:

- ✅ "3 Minutes vs 3 Hours: Is AI Coding Actually Faster?"
- ✅ "I Finished in 1 Day What Took Others a Week"
- ✅ "From Learning to Proficiency — Cursor Takes Just 10 Minutes"

**Best for**: Tutorial content, efficiency content

---

### Title Type Selection Guide

| Content Type | Recommended Title Type | Example |
|-------------|----------------------|---------|
| Tutorial | Results contrast, time contrast | "One Cursor Feature That Doubled My Efficiency" |
| Review | Price/performance contrast | "Free AI vs Paid AI — How Big Is the Gap?" |
| Challenge | Strength/quantity contrast | "Beginner Challenges Themselves to Build an App with AI" |
| Experience sharing | Results contrast | "Same Video, Different Title — Views Increased 10x" |

---

### Title Types to Avoid

❌ **Listicle-style**: "5 Common Features of Cursor"

- Problem: No conflict, no suspense
- Fix: Focus on the 1 strongest feature → "One Cursor Feature That Doubled My Efficiency"

❌ **Bland**: "Cursor Tutorial"

- Problem: No attraction, no specific value
- Fix: Add results contrast → "Get Started with Cursor in 3 Minutes — 5x Faster Workflow"

❌ **Abstract**: "The Future Trends of AI Coding"

- Problem: Too abstract, hard to picture
- Fix: Make it specific → "3 Months of AI-Assisted Coding — Here's What I Found"

---

### Title Checklist

When reviewing a title, confirm:

- [ ] Does the title have a clear contrast or conflict? (quantity, price, results, strength, or time)
- [ ] Is the title focused on 1 core point? (not listing multiple things)
- [ ] Can the title make the viewer picture a scene or scenario?
- [ ] Does the title create suspense? (makes you want to know the outcome)
- [ ] Is the title the right length? (15–25 words; no more than 30)
- [ ] Is the title honest? (can be delivered on in the video)

---

## 2️⃣ Thumbnail Review: Results Display Strategy

### Core Principle

**Choose the thumbnail strategy based on subscriber count and content type**

### Face Thumbnails (Use with Caution)

**✅ Suitable for**:

- Subscriber count > 100K (face has brand value)
- Content types: Challenge content, Vlog, high-emotion content
- Extreme and consistent expression (surprise / excitement / shock)
- An established, fixed thumbnail style

**❌ Not suitable for**:

- Subscriber count < 100K (face has no brand value; results are more direct)
- Technical tutorial content (results matter more than emotion)
- Different expression every video (can't build visual consistency)

---

### Results-Display Thumbnails (Recommended — Test First)

**✅ Suitable for**:

- Tutorial content: Before/After comparisons
- Review content: Product close-up + key data
- Technical content: Code/interface screenshots + result display
- Subscriber count < 100K (results are more direct than a face)

---

### Thumbnail Design Elements

#### 1. Strong Contrast

- **Colour contrast**: Warm vs cool tones (blue + orange)
- **Size contrast**: Core element enlarged; secondary elements reduced
- **Number contrast**: Large number vs small number (300K vs 0)

#### 2. Visual Focus

- **1–2 core elements**: Don't crowd the thumbnail
- **Clear visual anchor**: What does the viewer see first?

#### 3. Minimal Text

- **0–5 words**: Visual should carry the message; minimise text
- **Consistent font**: Fixed font to build brand recognition

#### 4. Consistent Style

- **Fixed colour scheme**: e.g., blue + orange
- **Fixed layout**: e.g., result on the left, number on the right
- **Fixed font**: Consistent thumbnail style every video

---

### Thumbnail Type Recommendations

| Content Type | Recommended Thumbnail | Example |
|-------------|----------------------|---------|
| Tutorial | Before/After comparison | Original code on left, optimised on right |
| Review | Product close-up + data | Product UI + performance numbers |
| Challenge | Extreme scene + emotion | Optional face (if it tests well) |
| Experience sharing | Data comparison | View count growth chart |

---

### Thumbnail Designs to Avoid

❌ **Text-only thumbnails**: Too much information; no visual impact
❌ **Too many elements**: Visually chaotic; no clear focus
❌ **Different style every video**: Can't build viewer recognition

---

### A/B Testing Recommendation

- Prepare 2 thumbnails for the same video
- A: Face thumbnail (if you want to test this)
- B: Results-display thumbnail
- Track click-through rate data; keep the better-performing one

---

### Thumbnail Checklist

When reviewing a thumbnail, confirm:

- [ ] Does the thumbnail type suit the content and subscriber count? (results display first)
- [ ] Does the thumbnail have strong contrast? (colour, size, numbers)
- [ ] Does the thumbnail have a clear visual focus? (1–2 core elements)
- [ ] Is the text on the thumbnail minimal? (0–5 words)
- [ ] Is the thumbnail style consistent? (colour scheme, layout, font)
- [ ] Does the thumbnail complement the title? (dual attraction: visual + text)

---

## 3️⃣ Content Engagement Review: Suspense Delay Strategy

### Core Principle

**Build suspense in the opening, exceed expectations in the middle, deliver on the promise at the close**

### Standard Engagement Structure

```text
Title / Thumbnail: Core suspense (strongest contrast or conflict)
    ↓
Opening (first 30 seconds – 1 minute):
- Confirm the title promise exists (build trust)
- Create suspense: "Can it actually be done?"
- Preview what's coming: "But before that, first..."
    ↓
Middle section (main content):
- Core teaching / demonstration
- Add an "unexpected surprise" (exceeds expectations)
- Keep reminding of the suspense: "Almost there, nearly time..."
    ↓
Closing (final 1–3 minutes):
- Deliver on the title promise (show the core content)
- Summarise key points
- Call to Action (subscribe / like / comment)
```

---

### Duration Control Guide

| Total Video Length | Opening Confirmation | Middle Content | Closing Payoff |
|-------------------|---------------------|----------------|----------------|
| 3–5 minutes | 30 seconds | 2–3 minutes | 1 minute |
| 5–10 minutes | 1 minute | 6–7 minutes | 2 minutes |
| 10–15 minutes | 1–2 minutes | 8–10 minutes | 3 minutes |

---

### Engagement Review Example

#### Example: Tutorial Video

**Title**: One Cursor Feature That Doubled My Efficiency

**✅ Correct engagement**:

**Opening (30 seconds)**:

```text
"There's a Cursor feature that saves me 3 hours on every project.
What feature? I'll demo it shortly.
But first, let me quickly run through the basics of Cursor,
so you can understand why this feature is so powerful."
```

← Confirms the promise exists, builds suspense

**Middle section (5–8 minutes)**:

```text
- Basic feature walkthrough
- Installation and setup
- Common issues
(Viewer: "Oh, there's this too — learnt something.")
```

← Unexpected surprise, exceeds expectations

**Closing (2 minutes)**:

```text
"Right, now for that core feature.
Here it is (demo)... See how powerful that is?
I've used it for 3 months — saves 3 hours on every project..."
```

← Delivers on the promise, closes the loop

---

**❌ Incorrect engagement**:

**Opening completely ignores the title**:

```text
"Today we're learning to use Cursor. Cursor is an AI coding tool..."
```

Problem: Viewer doesn't know when "the efficiency-doubling feature" will appear → they drop off mid-video

**Opening reveals everything upfront**:

```text
"Cursor has a feature called XX that doubles your efficiency. Here's how to use it..."
```

Problem: No suspense for the rest → shorter watch time

**Title says A, video is all about B**:

```text
Title: "One Cursor Feature That Doubled My Efficiency"
Video: Covers all basic Cursor features; the "efficiency-doubling feature" is never addressed
```

Problem: Feels deceptive → subscriber loss

**Suspense drags on too long**:

```text
10-minute video; the "efficiency-doubling feature" isn't mentioned until 8 minutes in
```

Problem: Viewer loses patience → drops off mid-video

---

### Common Errors (Must Avoid)

| Error | Consequence | Correct Approach |
|-------|-------------|-----------------|
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Tutorial | Before/After comparison | Original code on left, optimised on right |
| Review | Product close-up + data | Product UI + performance numbers |
| Challenge | Extreme scene + emotion | Optional face (if it tests well) |
| Experience sharing | Data comparison | View count growth chart |

---

### Thumbnail Designs to Avoid

❌ **Text-only thumbnails**: Too much information; no visual impact
❌ **Too many elements**: Visually chaotic; no clear focus
❌ **Different style every video**: Can't build viewer recognition

---

### A/B Testing Recommendation

- Prepare 2 thumbnails for the same video
- A: Face thumbnail (if you want to test this)
- B: Results-display thumbnail
- Track click-through rate data; keep the better-performing one

---

### Thumbnail Checklist

When reviewing a thumbnail, confirm:

- [ ] Does the thumbnail type suit the content and subscriber count? (results display first)
- [ ] Does the thumbnail have strong contrast? (colour, size, numbers)
- [ ] Does the thumbnail have a clear visual focus? (1–2 core elements)
- [ ] Is the text on the thumbnail minimal? (0–5 words)
- [ ] Is the thumbnail style consistent? (colour scheme, layout, font)
- [ ] Does the thumbnail complement the title? (dual attraction: visual + text)

---

## 3️⃣ Content Engagement Review: Suspense Delay Strategy

### Core Principle

**Build suspense in the opening, exceed expectations in the middle, deliver on the promise at the close**

### Standard Engagement Structure

```text
Title / Thumbnail: Core suspense (strongest contrast or conflict)
    ↓
Opening (first 30 seconds – 1 minute):
- Confirm the title promise exists (build trust)
- Create suspense: "Can it actually be done?"
- Preview what's coming: "But before that, first..."
    ↓
Middle section (main content):
- Core teaching / demonstration
- Add an "unexpected surprise" (exceeds expectations)
- Keep reminding of the suspense: "Almost there, nearly time..."
    ↓
Closing (final 1–3 minutes):
- Deliver on the title promise (show the core content)
- Summarise key points
- Call to Action (subscribe / like / comment)
```

---

### Duration Control Guide

| Total Video Length | Opening Confirmation | Middle Content | Closing Payoff |
|-------------------|---------------------|----------------|----------------|
| 3–5 minutes | 30 seconds | 2–3 minutes | 1 minute |
| 5–10 minutes | 1 minute | 6–7 minutes | 2 minutes |
| 10–15 minutes | 1–2 minutes | 8–10 minutes | 3 minutes |

---

### Engagement Review Example

#### Example: Tutorial Video

**Title**: One Cursor Feature That Doubled My Efficiency

**✅ Correct engagement**:

**Opening (30 seconds)**:

```text
"There's a Cursor feature that saves me 3 hours on every project.
What feature? I'll demo it shortly.
But first, let me quickly run through the basics of Cursor,
so you can understand why this feature is so powerful."
```

← Confirms the promise exists, builds suspense

**Middle section (5–8 minutes)**:

```text
- Basic feature walkthrough
- Installation and setup
- Common issues
(Viewer: "Oh, there's this too — learnt something.")
```

← Unexpected surprise, exceeds expectations

**Closing (2 minutes)**:

```text
"Right, now for that core feature.
Here it is (demo)... See how powerful that is?
I've used it for 3 months — saves 3 hours on every project..."
```

← Delivers on the promise, closes the loop

---

**❌ Incorrect engagement**:

**Opening completely ignores the title**:

```text
"Today we're learning to use Cursor. Cursor is an AI coding tool..."
```

Problem: Viewer doesn't know when "the efficiency-doubling feature" will appear → they drop off mid-video

**Opening reveals everything upfront**:

```text
"Cursor has a feature called XX that doubles your efficiency. Here's how to use it..."
```

Problem: No suspense for the rest → shorter watch time

**Title says A, video is all about B**:

```text
Title: "One Cursor Feature That Doubled My Efficiency"
Video: Covers all basic Cursor features; the "efficiency-doubling feature" is never addressed
```

Problem: Feels deceptive → subscriber loss

**Suspense drags on too long**:

```text
10-minute video; the "efficiency-doubling feature" isn't mentioned until 8 minutes in
```

Problem: Viewer loses patience → drops off mid-video

---

### Common Errors (Must Avoid)

| Error | Consequence | Correct Approach |
|-------|-------------|-----------------|
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Tutorial | Before/After comparison | Original code on left, optimised on right |
| Review | Product close-up + data | Product UI + performance numbers |
| Challenge | Extreme scene + emotion | Optional face (if it tests well) |
| Experience sharing | Data comparison | View count growth chart |

---

### Thumbnail Designs to Avoid

❌ **Text-only thumbnails**: Too much information; no visual impact
❌ **Too many elements**: Visually chaotic; no clear focus
❌ **Different style every video**: Can't build viewer recognition

---

### A/B Testing Recommendation

- Prepare 2 thumbnails for the same video
- A: Face thumbnail (if you want to test this)
- B: Results-display thumbnail
- Track click-through rate data; keep the better-performing one

---

### Thumbnail Checklist

When reviewing a thumbnail, confirm:

- [ ] Does the thumbnail type suit the content and subscriber count? (results display first)
- [ ] Does the thumbnail have strong contrast? (colour, size, numbers)
- [ ] Does the thumbnail have a clear visual focus? (1–2 core elements)
- [ ] Is the text on the thumbnail minimal? (0–5 words)
- [ ] Is the thumbnail style consistent? (colour scheme, layout, font)
- [ ] Does the thumbnail complement the title? (dual attraction: visual + text)

---

## 3️⃣ Content Engagement Review: Suspense Delay Strategy

### Core Principle

**Build suspense in the opening, exceed expectations in the middle, deliver on the promise at the close**

### Standard Engagement Structure

```text
Title / Thumbnail: Core suspense (strongest contrast or conflict)
    ↓
Opening (first 30 seconds – 1 minute):
- Confirm the title promise exists (build trust)
- Create suspense: "Can it actually be done?"
- Preview what's coming: "But before that, first..."
    ↓
Middle section (main content):
- Core teaching / demonstration
- Add an "unexpected surprise" (exceeds expectations)
- Keep reminding of the suspense: "Almost there, nearly time..."
    ↓
Closing (final 1–3 minutes):
- Deliver on the title promise (show the core content)
- Summarise key points
- Call to Action (subscribe / like / comment)
```

---

### Duration Control Guide

| Total Video Length | Opening Confirmation | Middle Content | Closing Payoff |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-video-check
description: Check video titles, thumbnails, and opening hooks based on MrBeast's strategies. Use when the user mentions "video title", "thumbnail", "click-through rate", "CTR", or "watch time".
---

# Video Thumbnail, Title & Hook Review

A professional review capability for video titles, thumbnails, and content engagement — based on the MrBeast methodology — to improve click-through rate and watch time.

## When to Use This Skill

This skill is automatically loaded when:

- The user says "check the title and thumbnail" or "check content engagement"
- After a video script draft is completed
- The user mentions "low click-through rate" or "short watch time"
- Need to optimise video titles or thumbnails

## Core Objectives

- **Improve click-through rate**: Titles and thumbnails attract users to click
- **Improve watch time**: Strong content engagement keeps viewers watching to the end
- **Build reusable formulas**: Standardised thumbnail, title, and engagement strategies

## Review Dimensions

### 1️⃣ Title Review (Strong Contrast Strategy)

### 2️⃣ Thumbnail Review (Results-First Strategy)

### 3️⃣ Content Engagement Review (Opening confirmation → Mid-section surprise → Closing payoff)

---

## 1️⃣ Title Review: Strong Contrast Strategy

### Core Principle

**Focus on the strongest single contrast — don't list everything**

### 5 Strong Contrast Formulas

#### Formula 1: Quantity Contrast

**Format**: `Small quantity vs Large quantity`

**Examples**:

- ✅ "1 Prompt Wrote 1,000 Lines of Code"
- ✅ "3 People vs a Team of 300 — Who Wins?"
- ✅ "1 Tool That Replaces 10 Tools"

**Best for**: Tutorial content, efficiency content, tool reviews

---

#### Formula 2: Price Contrast

**Format**: `Low price vs High price` or `Free vs Paid`

**Examples**:

- ✅ "£15 vs £150 AI — How Big Is the Gap?"
- ✅ "What Can Free AI Do? I Tested 10 Tools"
- ✅ "Same Features — Is Claude Worth 10x More Than GPT?"

**Best for**: Reviews, comparisons

---

#### Formula 3: Results Contrast

**Format**: `Low results vs High results` or `Before vs After`

**Examples**:

- ✅ "300K Followers vs 0 — I Only Did One Thing Right"
- ✅ "From 0 to 1,000 Views — I Used 3 Techniques"
- ✅ "Same Video, Different Title — Views Increased 10x"

**Best for**: Experience sharing, growth stories

---

#### Formula 4: Strength Contrast

**Format**: `Beginner / Underdog vs Expert / Powerhouse`

**Examples**:

- ✅ "Beginner vs Cursor: Who Writes This Feature Faster?"
- ✅ "I Pitted AI Against a Programmer — The Results Were Shocking"
- ✅ "Complete Novice Attempts to Build an App with AI"

**Best for**: Challenge content, experiment content

---

#### Formula 5: Time Contrast

**Format**: `Short time vs Long time` or `Fast vs Slow`

**Examples**:

- ✅ "3 Minutes vs 3 Hours: Is AI Coding Actually Faster?"
- ✅ "I Finished in 1 Day What Took Others a Week"
- ✅ "From Learning to Proficiency — Cursor Takes Just 10 Minutes"

**Best for**: Tutorial content, efficiency content

---

### Title Type Selection Guide

| Content Type | Recommended Title Type | Example |
|-------------|----------------------|---------|
| Tutorial | Results contrast, time contrast | "One Cursor Feature That Doubled My Efficiency" |
| Review | Price/performance contrast | "Free AI vs Paid AI — How Big Is the Gap?" |
| Challenge | Strength/quantity contrast | "Beginner Challenges Themselves to Build an App with AI" |
| Experience sharing | Results contrast | "Same Video, Different Title — Views Increased 10x" |

---

### Title Types to Avoid

❌ **Listicle-style**: "5 Common Features of Cursor"

- Problem: No conflict, no suspense
- Fix: Focus on the 1 strongest feature → "One Cursor Feature That Doubled My Efficiency"

❌ **Bland**: "Cursor Tutorial"

- Problem: No attraction, no specific value
- Fix: Add results contrast → "Get Started with Cursor in 3 Minutes — 5x Faster Workflow"

❌ **Abstract**: "The Future Trends of AI Coding"

- Problem: Too abstract, hard to picture
- Fix: Make it specific → "3 Months of AI-Assisted Coding — Here's What I Found"

---

### Title Checklist

When reviewing a title, confirm:

- [ ] Does the title have a clear contrast or conflict? (quantity, price, results, strength, or time)
- [ ] Is the title focused on 1 core point? (not listing multiple things)
- [ ] Can the title make the viewer picture a scene or scenario?
- [ ] Does the title create suspense? (makes you want to know the outcome)
- [ ] Is the title the right length? (15–25 words; no more than 30)
- [ ] Is the title honest? (can be delivered on in the video)

---

## 2️⃣ Thumbnail Review: Results Display Strategy

### Core Principle

**Choose the thumbnail strategy based on subscriber count and content type**

### Face Thumbnails (Use with Caution)

**✅ Suitable for**:

- Subscriber count > 100K (face has brand value)
- Content types: Challenge content, Vlog, high-emotion content
- Extreme and consistent expression (surprise / excitement / shock)
- An established, fixed thumbnail style

**❌ Not suitable for**:

- Subscriber count < 100K (face has no brand value; results are more direct)
- Technical tutorial content (results matter more than emotion)
- Different expression every video (can't build visual consistency)

---

### Results-Display Thumbnails (Recommended — Test First)

**✅ Suitable for**:

- Tutorial content: Before/After comparisons
- Review content: Product close-up + key data
- Technical content: Code/interface screenshots + result display
- Subscriber count < 100K (results are more direct than a face)

---

### Thumbnail Design Elements

#### 1. Strong Contrast

- **Colour contrast**: Warm vs cool tones (blue + orange)
- **Size contrast**: Core element enlarged; secondary elements reduced
- **Number contrast**: Large number vs small number (300K vs 0)

#### 2. Visual Focus

- **1–2 core elements**: Don't crowd the thumbnail
- **Clear visual anchor**: What does the viewer see first?

#### 3. Minimal Text

- **0–5 words**: Visual should carry the message; minimise text
- **Consistent font**: Fixed font to build brand recognition

#### 4. Consistent Style

- **Fixed colour scheme**: e.g., blue + orange
- **Fixed layout**: e.g., result on the left, number on the right
- **Fixed font**: Consistent thumbnail style every video

---

### Thumbnail Type Recommendations

| Content Type | Recommended Thumbnail | Example |
|-------------|----------------------|---------|
| Tutorial | Before/After comparison | Original code on left, optimised on right |
| Review | Product close-up + data | Product UI + performance numbers |
| Challenge | Extreme scene + emotion | Optional face (if it tests well) |
| Experience sharing | Data comparison | View count growth chart |

---

### Thumbnail Designs to Avoid

❌ **Text-only thumbnails**: Too much information; no visual impact
❌ **Too many elements**: Visually chaotic; no clear focus
❌ **Different style every video**: Can't build viewer recognition

---

### A/B Testing Recommendation

- Prepare 2 thumbnails for the same video
- A: Face thumbnail (if you want to test this)
- B: Results-display thumbnail
- Track click-through rate data; keep the better-performing one

---

### Thumbnail Checklist

When reviewing a thumbnail, confirm:

- [ ] Does the thumbnail type suit the content and subscriber count? (results display first)
- [ ] Does the thumbnail have strong contrast? (colour, size, numbers)
- [ ] Does the thumbnail have a clear visual focus? (1–2 core elements)
- [ ] Is the text on the thumbnail minimal? (0–5 words)
- [ ] Is the thumbnail style consistent? (colour scheme, layout, font)
- [ ] Does the thumbnail complement the title? (dual attraction: visual + text)

---

## 3️⃣ Content Engagement Review: Suspense Delay Strategy

### Core Principle

**Build suspense in the opening, exceed expectations in the middle, deliver on the promise at the close**

### Standard Engagement Structure

```text
Title / Thumbnail: Core suspense (strongest contrast or conflict)
    ↓
Opening (first 30 seconds – 1 minute):
- Confirm the title promise exists (build trust)
- Create suspense: "Can it actually be done?"
- Preview what's coming: "But before that, first..."
    ↓
Middle section (main content):
- Core teaching / demonstration
- Add an "unexpected surprise" (exceeds expectations)
- Keep reminding of the suspense: "Almost there, nearly time..."
    ↓
Closing (final 1–3 minutes):
- Deliver on the title promise (show the core content)
- Summarise key points
- Call to Action (subscribe / like / comment)
```

---

### Duration Control Guide

| Total Video Length | Opening Confirmation | Middle Content | Closing Payoff |
|-------------------|---------------------|----------------|----------------|
| 3–5 minutes | 30 seconds | 2–3 minutes | 1 minute |
| 5–10 minutes | 1 minute | 6–7 minutes | 2 minutes |
| 10–15 minutes | 1–2 minutes | 8–10 minutes | 3 minutes |

---

### Engagement Review Example

#### Example: Tutorial Video

**Title**: One Cursor Feature That Doubled My Efficiency

**✅ Correct engagement**:

**Opening (30 seconds)**:

```text
"There's a Cursor feature that saves me 3 hours on every project.
What feature? I'll demo it shortly.
But first, let me quickly run through the basics of Cursor,
so you can understand why this feature is so powerful."
```

← Confirms the promise exists, builds suspense

**Middle section (5–8 minutes)**:

```text
- Basic feature walkthrough
- Installation and setup
- Common issues
(Viewer: "Oh, there's this too — learnt something.")
```

← Unexpected surprise, exceeds expectations

**Closing (2 minutes)**:

```text
"Right, now for that core feature.
Here it is (demo)... See how powerful that is?
I've used it for 3 months — saves 3 hours on every project..."
```

← Delivers on the promise, closes the loop

---

**❌ Incorrect engagement**:

**Opening completely ignores the title**:

```text
"Today we're learning to use Cursor. Cursor is an AI coding tool..."
```

Problem: Viewer doesn't know when "the efficiency-doubling feature" will appear → they drop off mid-video

**Opening reveals everything upfront**:

```text
"Cursor has a feature called XX that doubles your efficiency. Here's how to use it..."
```

Problem: No suspense for the rest → shorter watch time

**Title says A, video is all about B**:

```text
Title: "One Cursor Feature That Doubled My Efficiency"
Video: Covers all basic Cursor features; the "efficiency-doubling feature" is never addressed
```

Problem: Feels deceptive → subscriber loss

**Suspense drags on too long**:

```text
10-minute video; the "efficiency-doubling feature" isn't mentioned until 8 minutes in
```

Problem: Viewer loses patience → drops off mid-video

---

### Common Errors (Must Avoid)

| Error | Consequence | Correct Approach |
|-------|-------------|-----------------|
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| 3–5 minutes | 30 seconds | 2–3 minutes | 1 minute |
| 5–10 minutes | 1 minute | 6–7 minutes | 2 minutes |
| 10–15 minutes | 1–2 minutes | 8–10 minutes | 3 minutes |

---

### Engagement Review Example

#### Example: Tutorial Video

**Title**: One Cursor Feature That Doubled My Efficiency

**✅ Correct engagement**:

**Opening (30 seconds)**:

```text
"There's a Cursor feature that saves me 3 hours on every project.
What feature? I'll demo it shortly.
But first, let me quickly run through the basics of Cursor,
so you can understand why this feature is so powerful."
```

← Confirms the promise exists, builds suspense

**Middle section (5–8 minutes)**:

```text
- Basic feature walkthrough
- Installation and setup
- Common issues
(Viewer: "Oh, there's this too — learnt something.")
```

← Unexpected surprise, exceeds expectations

**Closing (2 minutes)**:

```text
"Right, now for that core feature.
Here it is (demo)... See how powerful that is?
I've used it for 3 months — saves 3 hours on every project..."
```

← Delivers on the promise, closes the loop

---

**❌ Incorrect engagement**:

**Opening completely ignores the title**:

```text
"Today we're learning to use Cursor. Cursor is an AI coding tool..."
```

Problem: Viewer doesn't know when "the efficiency-doubling feature" will appear → they drop off mid-video

**Opening reveals everything upfront**:

```text
"Cursor has a feature called XX that doubles your efficiency. Here's how to use it..."
```

Problem: No suspense for the rest → shorter watch time

**Title says A, video is all about B**:

```text
Title: "One Cursor Feature That Doubled My Efficiency"
Video: Covers all basic Cursor features; the "efficiency-doubling feature" is never addressed
```

Problem: Feels deceptive → subscriber loss

**Suspense drags on too long**:

```text
10-minute video; the "efficiency-doubling feature" isn't mentioned until 8 minutes in
```

Problem: Viewer loses patience → drops off mid-video

---

### Common Errors (Must Avoid)

| Error | Consequence | Correct Approach |
|-------|-------------|-----------------|
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| 3–5 minutes | 30 seconds | 2–3 minutes | 1 minute |
| 5–10 minutes | 1 minute | 6–7 minutes | 2 minutes |
| 10–15 minutes | 1–2 minutes | 8–10 minutes | 3 minutes |

---

### Engagement Review Example

#### Example: Tutorial Video

**Title**: One Cursor Feature That Doubled My Efficiency

**✅ Correct engagement**:

**Opening (30 seconds)**:

```text
"There's a Cursor feature that saves me 3 hours on every project.
What feature? I'll demo it shortly.
But first, let me quickly run through the basics of Cursor,
so you can understand why this feature is so powerful."
```

← Confirms the promise exists, builds suspense

**Middle section (5–8 minutes)**:

```text
- Basic feature walkthrough
- Installation and setup
- Common issues
(Viewer: "Oh, there's this too — learnt something.")
```

← Unexpected surprise, exceeds expectations

**Closing (2 minutes)**:

```text
"Right, now for that core feature.
Here it is (demo)... See how powerful that is?
I've used it for 3 months — saves 3 hours on every project..."
```

← Delivers on the promise, closes the loop

---

**❌ Incorrect engagement**:

**Opening completely ignores the title**:

```text
"Today we're learning to use Cursor. Cursor is an AI coding tool..."
```

Problem: Viewer doesn't know when "the efficiency-doubling feature" will appear → they drop off mid-video

**Opening reveals everything upfront**:

```text
"Cursor has a feature called XX that doubles your efficiency. Here's how to use it..."
```

Problem: No suspense for the rest → shorter watch time

**Title says A, video is all about B**:

```text
Title: "One Cursor Feature That Doubled My Efficiency"
Video: Covers all basic Cursor features; the "efficiency-doubling feature" is never addressed
```

Problem: Feels deceptive → subscriber loss

**Suspense drags on too long**:

```text
10-minute video; the "efficiency-doubling feature" isn't mentioned until 8 minutes in
```

Problem: Viewer loses patience → drops off mid-video

---

### Common Errors (Must Avoid)

| Error | Consequence | Correct Approach |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-video-check
description: Check video titles, thumbnails, and opening hooks based on MrBeast's strategies. Use when the user mentions "video title", "thumbnail", "click-through rate", "CTR", or "watch time".
---

# Video Thumbnail, Title & Hook Review

A professional review capability for video titles, thumbnails, and content engagement — based on the MrBeast methodology — to improve click-through rate and watch time.

## When to Use This Skill

This skill is automatically loaded when:

- The user says "check the title and thumbnail" or "check content engagement"
- After a video script draft is completed
- The user mentions "low click-through rate" or "short watch time"
- Need to optimise video titles or thumbnails

## Core Objectives

- **Improve click-through rate**: Titles and thumbnails attract users to click
- **Improve watch time**: Strong content engagement keeps viewers watching to the end
- **Build reusable formulas**: Standardised thumbnail, title, and engagement strategies

## Review Dimensions

### 1️⃣ Title Review (Strong Contrast Strategy)

### 2️⃣ Thumbnail Review (Results-First Strategy)

### 3️⃣ Content Engagement Review (Opening confirmation → Mid-section surprise → Closing payoff)

---

## 1️⃣ Title Review: Strong Contrast Strategy

### Core Principle

**Focus on the strongest single contrast — don't list everything**

### 5 Strong Contrast Formulas

#### Formula 1: Quantity Contrast

**Format**: `Small quantity vs Large quantity`

**Examples**:

- ✅ "1 Prompt Wrote 1,000 Lines of Code"
- ✅ "3 People vs a Team of 300 — Who Wins?"
- ✅ "1 Tool That Replaces 10 Tools"

**Best for**: Tutorial content, efficiency content, tool reviews

---

#### Formula 2: Price Contrast

**Format**: `Low price vs High price` or `Free vs Paid`

**Examples**:

- ✅ "£15 vs £150 AI — How Big Is the Gap?"
- ✅ "What Can Free AI Do? I Tested 10 Tools"
- ✅ "Same Features — Is Claude Worth 10x More Than GPT?"

**Best for**: Reviews, comparisons

---

#### Formula 3: Results Contrast

**Format**: `Low results vs High results` or `Before vs After`

**Examples**:

- ✅ "300K Followers vs 0 — I Only Did One Thing Right"
- ✅ "From 0 to 1,000 Views — I Used 3 Techniques"
- ✅ "Same Video, Different Title — Views Increased 10x"

**Best for**: Experience sharing, growth stories

---

#### Formula 4: Strength Contrast

**Format**: `Beginner / Underdog vs Expert / Powerhouse`

**Examples**:

- ✅ "Beginner vs Cursor: Who Writes This Feature Faster?"
- ✅ "I Pitted AI Against a Programmer — The Results Were Shocking"
- ✅ "Complete Novice Attempts to Build an App with AI"

**Best for**: Challenge content, experiment content

---

#### Formula 5: Time Contrast

**Format**: `Short time vs Long time` or `Fast vs Slow`

**Examples**:

- ✅ "3 Minutes vs 3 Hours: Is AI Coding Actually Faster?"
- ✅ "I Finished in 1 Day What Took Others a Week"
- ✅ "From Learning to Proficiency — Cursor Takes Just 10 Minutes"

**Best for**: Tutorial content, efficiency content

---

### Title Type Selection Guide

| Content Type | Recommended Title Type | Example |
|-------------|----------------------|---------|
| Tutorial | Results contrast, time contrast | "One Cursor Feature That Doubled My Efficiency" |
| Review | Price/performance contrast | "Free AI vs Paid AI — How Big Is the Gap?" |
| Challenge | Strength/quantity contrast | "Beginner Challenges Themselves to Build an App with AI" |
| Experience sharing | Results contrast | "Same Video, Different Title — Views Increased 10x" |

---

### Title Types to Avoid

❌ **Listicle-style**: "5 Common Features of Cursor"

- Problem: No conflict, no suspense
- Fix: Focus on the 1 strongest feature → "One Cursor Feature That Doubled My Efficiency"

❌ **Bland**: "Cursor Tutorial"

- Problem: No attraction, no specific value
- Fix: Add results contrast → "Get Started with Cursor in 3 Minutes — 5x Faster Workflow"

❌ **Abstract**: "The Future Trends of AI Coding"

- Problem: Too abstract, hard to picture
- Fix: Make it specific → "3 Months of AI-Assisted Coding — Here's What I Found"

---

### Title Checklist

When reviewing a title, confirm:

- [ ] Does the title have a clear contrast or conflict? (quantity, price, results, strength, or time)
- [ ] Is the title focused on 1 core point? (not listing multiple things)
- [ ] Can the title make the viewer picture a scene or scenario?
- [ ] Does the title create suspense? (makes you want to know the outcome)
- [ ] Is the title the right length? (15–25 words; no more than 30)
- [ ] Is the title honest? (can be delivered on in the video)

---

## 2️⃣ Thumbnail Review: Results Display Strategy

### Core Principle

**Choose the thumbnail strategy based on subscriber count and content type**

### Face Thumbnails (Use with Caution)

**✅ Suitable for**:

- Subscriber count > 100K (face has brand value)
- Content types: Challenge content, Vlog, high-emotion content
- Extreme and consistent expression (surprise / excitement / shock)
- An established, fixed thumbnail style

**❌ Not suitable for**:

- Subscriber count < 100K (face has no brand value; results are more direct)
- Technical tutorial content (results matter more than emotion)
- Different expression every video (can't build visual consistency)

---

### Results-Display Thumbnails (Recommended — Test First)

**✅ Suitable for**:

- Tutorial content: Before/After comparisons
- Review content: Product close-up + key data
- Technical content: Code/interface screenshots + result display
- Subscriber count < 100K (results are more direct than a face)

---

### Thumbnail Design Elements

#### 1. Strong Contrast

- **Colour contrast**: Warm vs cool tones (blue + orange)
- **Size contrast**: Core element enlarged; secondary elements reduced
- **Number contrast**: Large number vs small number (300K vs 0)

#### 2. Visual Focus

- **1–2 core elements**: Don't crowd the thumbnail
- **Clear visual anchor**: What does the viewer see first?

#### 3. Minimal Text

- **0–5 words**: Visual should carry the message; minimise text
- **Consistent font**: Fixed font to build brand recognition

#### 4. Consistent Style

- **Fixed colour scheme**: e.g., blue + orange
- **Fixed layout**: e.g., result on the left, number on the right
- **Fixed font**: Consistent thumbnail style every video

---

### Thumbnail Type Recommendations

| Content Type | Recommended Thumbnail | Example |
|-------------|----------------------|---------|
| Tutorial | Before/After comparison | Original code on left, optimised on right |
| Review | Product close-up + data | Product UI + performance numbers |
| Challenge | Extreme scene + emotion | Optional face (if it tests well) |
| Experience sharing | Data comparison | View count growth chart |

---

### Thumbnail Designs to Avoid

❌ **Text-only thumbnails**: Too much information; no visual impact
❌ **Too many elements**: Visually chaotic; no clear focus
❌ **Different style every video**: Can't build viewer recognition

---

### A/B Testing Recommendation

- Prepare 2 thumbnails for the same video
- A: Face thumbnail (if you want to test this)
- B: Results-display thumbnail
- Track click-through rate data; keep the better-performing one

---

### Thumbnail Checklist

When reviewing a thumbnail, confirm:

- [ ] Does the thumbnail type suit the content and subscriber count? (results display first)
- [ ] Does the thumbnail have strong contrast? (colour, size, numbers)
- [ ] Does the thumbnail have a clear visual focus? (1–2 core elements)
- [ ] Is the text on the thumbnail minimal? (0–5 words)
- [ ] Is the thumbnail style consistent? (colour scheme, layout, font)
- [ ] Does the thumbnail complement the title? (dual attraction: visual + text)

---

## 3️⃣ Content Engagement Review: Suspense Delay Strategy

### Core Principle

**Build suspense in the opening, exceed expectations in the middle, deliver on the promise at the close**

### Standard Engagement Structure

```text
Title / Thumbnail: Core suspense (strongest contrast or conflict)
    ↓
Opening (first 30 seconds – 1 minute):
- Confirm the title promise exists (build trust)
- Create suspense: "Can it actually be done?"
- Preview what's coming: "But before that, first..."
    ↓
Middle section (main content):
- Core teaching / demonstration
- Add an "unexpected surprise" (exceeds expectations)
- Keep reminding of the suspense: "Almost there, nearly time..."
    ↓
Closing (final 1–3 minutes):
- Deliver on the title promise (show the core content)
- Summarise key points
- Call to Action (subscribe / like / comment)
```

---

### Duration Control Guide

| Total Video Length | Opening Confirmation | Middle Content | Closing Payoff |
|-------------------|---------------------|----------------|----------------|
| 3–5 minutes | 30 seconds | 2–3 minutes | 1 minute |
| 5–10 minutes | 1 minute | 6–7 minutes | 2 minutes |
| 10–15 minutes | 1–2 minutes | 8–10 minutes | 3 minutes |

---

### Engagement Review Example

#### Example: Tutorial Video

**Title**: One Cursor Feature That Doubled My Efficiency

**✅ Correct engagement**:

**Opening (30 seconds)**:

```text
"There's a Cursor feature that saves me 3 hours on every project.
What feature? I'll demo it shortly.
But first, let me quickly run through the basics of Cursor,
so you can understand why this feature is so powerful."
```

← Confirms the promise exists, builds suspense

**Middle section (5–8 minutes)**:

```text
- Basic feature walkthrough
- Installation and setup
- Common issues
(Viewer: "Oh, there's this too — learnt something.")
```

← Unexpected surprise, exceeds expectations

**Closing (2 minutes)**:

```text
"Right, now for that core feature.
Here it is (demo)... See how powerful that is?
I've used it for 3 months — saves 3 hours on every project..."
```

← Delivers on the promise, closes the loop

---

**❌ Incorrect engagement**:

**Opening completely ignores the title**:

```text
"Today we're learning to use Cursor. Cursor is an AI coding tool..."
```

Problem: Viewer doesn't know when "the efficiency-doubling feature" will appear → they drop off mid-video

**Opening reveals everything upfront**:

```text
"Cursor has a feature called XX that doubles your efficiency. Here's how to use it..."
```

Problem: No suspense for the rest → shorter watch time

**Title says A, video is all about B**:

```text
Title: "One Cursor Feature That Doubled My Efficiency"
Video: Covers all basic Cursor features; the "efficiency-doubling feature" is never addressed
```

Problem: Feels deceptive → subscriber loss

**Suspense drags on too long**:

```text
10-minute video; the "efficiency-doubling feature" isn't mentioned until 8 minutes in
```

Problem: Viewer loses patience → drops off mid-video

---

### Common Errors (Must Avoid)

| Error | Consequence | Correct Approach |
|-------|-------------|-----------------|
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Opening completely ignores title | Viewer doesn't know when the key content arrives → drops off | Confirm the promise within first 30 seconds – 1 minute |
| Opening reveals everything | No suspense for the rest → short watch time | Delay the suspense reveal until the closing |
| Title says A, video is all B | Feels deceptive → subscriber loss | Title must always be delivered on |
| Suspense drags too long | Viewer loses patience → drops off | Allocate time appropriately based on video length |

---

### Content Engagement Checklist

When reviewing content engagement, confirm:

- [ ] Within the first 30 seconds – 1 minute, is the core content from the title referenced?
- [ ] Is clear suspense established? (makes the viewer want to watch to the end)
- [ ] Does the middle section have an "unexpected surprise"? (content beyond the title promise)
- [ ] Does the closing deliver on the title promise?
- [ ] Is the suspense delay an appropriate length? (not too long for viewers)
- [ ] Is the suspense reinforced periodically? ("Almost there, nearly time...")
- [ ] Is there a Call to Action at the close? (subscribe / like / comment)

---

## Complete Review Process

### Step 1: Title Review

1. Identify the title type (5 contrast formulas)
2. Check for focus on 1 core point
3. Check for suspense
4. Check title length (15–25 words)

### Step 2: Thumbnail Review

1. Select strategy based on subscriber count and content type
2. Check for strong contrast (colour, size, numbers)
3. Check visual focus (1–2 core elements)
4. Check text minimalism (0–5 words)
5. Check style consistency

### Step 3: Content Engagement Review

1. Check that opening confirms the title promise (30 seconds – 1 minute)
2. Check for unexpected mid-section surprise
3. Check that closing delivers on the promise
4. Check that suspense delay is appropriately timed
5. Check for Call to Action

### Step 4: Overall Assessment

- [ ] Are the title, thumbnail, and content consistent?
- [ ] Does it attract users to click?
- [ ] Does it keep users watching to the end?
- [ ] Is there a clear value proposition?

---

## Reference Resources

- `/video-creation/_knowledge_base/MrBeast-thumbnail-title-and-engagement-strategy-Oct2025.md` — Detailed MrBeast case analysis
- `/media-experience/content-strategy/thumbnail-title-and-engagement-MrBeast-case.md` — Practical experience summary

---

## Success Examples

- **An AI Coding Tutorial Video**: Used "3 Minutes vs 3 Hours" contrast title — click-through rate improved by 40%
- **A Product Review Video**: Used results-display thumbnail — watch time improved by 25%

---

**Last Updated**: 2025-11-07
**Applicable Projects**: Video creation
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
