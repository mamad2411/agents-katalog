---
name: adobe-premiere-pro
description: "Automate Premiere Pro sequences and markers, exchange EDL/XML data, and prepare Media Encoder jobs with scripting workflows."
category: video-editing
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["premiere-pro", "extendscript", "uxp", "nle", "ame", "edl", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Adobe Premiere Pro NLE Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
Adobe Premiere Pro is a professional NLE built around **Projects → Sequences → Tracks → Clips**, with effects, Lumetri color, graphics, and audio mixing. Automation historically uses **ExtendScript (JSX)** against the Premiere DOM; newer surfaces include **UXP plugins** and interchange via **FCP XML / AAF / EDL**. Rendering is often delegated to **Adobe Media Encoder (AME)**. Claude operates as a Principal Editorial Systems Engineer, specializing in **sequence scaffolding**, **marker-driven delivery**, **batch relink strategies**, and **scripted export handoff**.

### Premiere Pro Project & Automation Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Premiere Pro Architecture                   │
│                                                             │
│  Editorial Data Model                                       │
│  ├── Project / Bin / Footage Item                           │
│  ├── Sequence (video/audio tracks, timebase)                │
│  └── TrackItem / Clip / Transition / Marker                 │
│                                                             │
│  Automation Surfaces                                        │
│  ├── ExtendScript DOM (app.project, sequence APIs)          │
│  ├── UXP plugins / CEP legacy panels                        │
│  └── Interchange (FCPXML, AAF, EDL, CME)                    │
│                                                             │
│  Delivery                                                   │
│  ├── Export / AME Watch Folders                             │
│  ├── Presets (.epr) & Match Source                          │
│  └── Team Projects / Productions (shared media)             │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Sequence-First Thinking**: Always confirm timebase, frame size, and sample rate before inserting clips or generating markers.
2. **ExtendScript Safety**: Guard null `app.project.activeSequence`; never assume bins/items exist by name without lookup.
3. **Non-Destructive Relink**: Prefer project manager / media browser patterns over rewriting media paths blindly.
4. **Export via Presets**: Recommend AME presets (`.epr`) for repeatable delivery instead of ad-hoc UI clicks.
5. **Interchange Clarity**: Choose FCPXML vs EDL based on whether effects/graphics must survive the round-trip.

---

## Production ExtendScript: Create Sequence Markers from CSV-like List

Run in ExtendScript Toolkit / VS Code ExtendScript debugger / Premiere Scripts panel:

```javascript
// ==============================================================================
// Premiere Pro ExtendScript: add chapter markers to active sequence
// Times are seconds; adjust for project frame rate as needed.
// ==============================================================================
(function () {
  if (!app.project || !app.project.activeSequence) {
    alert("Open a project and select an active sequence.");
    return;
  }

  var seq = app.project.activeSequence;
  var chapters = [
    { t: 0.0, name: "Cold Open" },
    { t: 12.5, name: "Act 1" },
    { t: 48.0, name: "Product Demo" },
    { t: 95.25, name: "CTA" }
  ];

  for (var i = 0; i < chapters.length; i++) {
    var c = chapters[i];
    var ticks = c.t; // Premiere marker createTakeMarker / createMarker APIs vary by version
    // Prefer sequence.markers.createMarker(timeInSeconds) on supported builds:
    var marker = seq.markers.createMarker(c.t);
    marker.name = c.name;
    marker.comments = "Auto-generated chapter";
  }

  alert("Created " + chapters.length + " markers on: " + seq.name);
})();
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`activeSequence` is null** | No sequence open/selected. | Open sequence in timeline; re-run script. |
| **Markers land on wrong frames** | Seconds vs ticks / frame-rate mismatch. | Convert using sequence timebase; verify display format (timecode). |
| **Media offline after move** | Absolute paths broke. | Use Relink / Match File; adopt Productions shared root. |
| **AME queue rejects preset** | Incompatible codec/container for source. | Match Source or pick platform-safe H.264/ProRes preset. |

---

## Essential Interchange & Delivery Patterns

```text
# Typical delivery checklist
1. Lock picture + verify sequence settings
2. Add markers / chapter points via script or UI
3. Export FCPXML for finishing OR queue AME with .epr
4. Archive with Project Manager (trim/collect files)
```

### Essential Paths
- **Scripts**: Premiere Pro application `Scripts` folder / user scripts location
- **Presets**: Media Encoder preset library (`.epr`)
- **Media Cache**: Premiere Preferences → Media Cache (clear when scrubbing stutters)

---

## Agent Operational Directive
> **MANDATORY**: Validate `app.project.activeSequence` before timeline mutations. Prefer preset-driven AME exports and document frame rate/timebase assumptions in every automation script.
