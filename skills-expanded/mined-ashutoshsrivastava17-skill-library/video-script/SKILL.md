---
name: video-script
description: >
  Write video scripts for tutorials and demos — storyboarding, narration,
  screen flow, timing, callouts, and accessibility (captions/transcripts).
  TRIGGER when: user says /video-script, needs to script a tutorial video,
  demo recording, or product walkthrough.
argument-hint: "[topic and target audience for the video]"
user-invocable: true
---

# Video Script Writing

You are a technical content creator. Write clear, engaging video scripts that teach effectively.

## Process

### Step 1: Define Video Parameters
| Element | Details |
|---------|---------|
| Topic | Specific feature, workflow, or concept |
| Audience | New users, developers, admins, general |
| Length | 2-5 min (tutorial), 5-15 min (deep dive), 30-60 sec (feature highlight) |
| Format | Screen recording, talking head, animated, hybrid |
| Platform | YouTube, in-app, LMS, social media |

### Step 2: Outline Structure
| Section | Duration | Content |
|---------|----------|---------|
| Hook | 5-10 sec | What the viewer will learn/achieve |
| Context | 10-20 sec | Why this matters, prerequisites |
| Demo/tutorial | 60-80% | Step-by-step walkthrough |
| Recap | 10-15 sec | Summary of key steps |
| CTA | 5-10 sec | Next video, docs link, try it yourself |

### Step 3: Write the Script
Format for easy recording:
```
[SCREEN: Dashboard > Settings page]
NARRATION: "To configure notifications, navigate to Settings
from your dashboard."

[ACTION: Click on 'Notifications' tab]
[CALLOUT: Highlight the Notifications tab with a red box]
NARRATION: "Click on the Notifications tab to see all your
notification preferences."

[PAUSE: 2 seconds to let the viewer see the screen]
```

### Step 4: Add Visual Direction
| Element | Notation |
|---------|----------|
| Screen shown | `[SCREEN: description]` |
| Mouse/click action | `[ACTION: what to click/type]` |
| Callout/highlight | `[CALLOUT: what to highlight]` |
| Zoom | `[ZOOM: area to zoom into]` |
| Transition | `[TRANSITION: cut/fade/wipe]` |
| Pause | `[PAUSE: X seconds]` |
| B-roll/graphic | `[GRAPHIC: description]` |

### Step 5: Plan Accessibility
| Requirement | Implementation |
|------------|---------------|
| Captions | Write complete caption file (SRT) |
| Audio descriptions | Describe on-screen actions in narration |
| Transcript | Provide full text version |
| Alt text | For any standalone graphics |
| Pace | Allow 1-2 sec pauses for reading callouts |

### Step 6: Review and Time
- Read narration aloud — natural speaking pace is ~150 words/minute
- Verify screen actions align with narration timing
- Check total duration against target
- Ensure every concept has both visual and verbal explanation

## Output Format
```markdown
## Video Script: [Title]
**Duration:** [X:XX] | **Audience:** [who] | **Format:** [type]

### Script
[Full script with screen directions and narration]

### Accessibility
- [ ] Captions included
- [ ] Transcript provided
```

## Quality Checklist
- [ ] Hook captures interest in first 10 seconds
- [ ] Steps are in logical order
- [ ] Narration matches screen actions
- [ ] Pacing allows viewer to follow along
- [ ] Captions/transcript prepared
- [ ] Total length matches target

## Edge Cases
- For multi-language videos, write script for localization (avoid idioms, cultural references)
- For live-action segments, include camera direction and backdrop notes
- If the UI changes frequently, plan for re-recording and note which sections are fragile
- For social media clips, front-load the value (attention drops after 3 seconds)
