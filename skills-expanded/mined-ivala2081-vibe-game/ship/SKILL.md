---
name: ship
description: "Take the Unity build from scene to playable WebGL build, then to an itch.io page draft. Runs final checklist (build settings, scene list, splash, icon, controls overlay), produces the build, generates the itch.io page (title, description, tags, screenshots, devlog post), and gives a step-by-step publish guide. Trigger when the user is ready to release — even a prototype, even a jam build."
disable-model-invocation: false
---

# ship

> **Ship the prototype.**
> Indie projects die in polish hell. This skill drags them across the finish line.

## When to invoke

- User says: "I want to release this" / "publish" / "submit to the jam" / "ship it"
- The game has passed `/feel-check` with overall score >6/10
- Jam deadline approaching

## Hard rules

1. **WebGL is the default target.** Lowest friction for itch.io distribution. Standalone optional.
2. **Block ship if the brief's verb doesn't work** within 10 seconds of pressing play.
3. **Block ship if no controls overlay** exists. Players need to know which keys to press.
4. **Don't block on polish** — only on hard breaks.
5. **Generate the itch.io page draft** — title, tags, description, screenshots list. The user can publish from there.

## Pre-flight checklist

Walk through, block on any RED:

| Check | Severity | How to verify |
|---|---|---|
| Build settings has the prototype scene as #0 | 🔴 RED | Read `EditorBuildSettings.asset` |
| WebGL platform module installed | 🔴 RED | Read `ProjectSettings/ProjectVersion.txt`, check `m_EditorVersionWithRevision` |
| Player Settings → Company / Product name set | 🟡 YELLOW | Read `ProjectSettings.asset` |
| Default icon set (any custom icon) | 🟡 YELLOW | Read PlayerSettings |
| Splash screen disabled or customized (Personal license shows Unity splash; doc it) | 🟢 OK | Read PlayerSettings |
| Controls overlay exists in scene | 🔴 RED | Grep for `ControlsOverlay` or visible Canvas |
| No exceptions in console on Play (best effort, can't auto-check) | 🟡 YELLOW | Ask user |
| Verb works in first 10s | 🔴 RED | Re-read `/feel-check` Fun-O-Meter or ask user |
| WebGL compression set to Gzip or Brotli (not disabled) | 🟡 YELLOW | Read PlayerSettings WebGL |

For each RED, **don't proceed** — fix it.

## Build procedure

### Step 1 — Verify pre-flight
Run all checks above. Report status. Block if RED.

### Step 2 — Build via Unity batch mode

Generate a build script: `Assets/Editor/VibeBuildScript.cs`:

```csharp
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;
using System.IO;

public class VibeBuildScript
{
    [MenuItem("vibe-game/Build WebGL")]
    public static void BuildWebGL()
    {
        var scenes = EditorBuildSettings.scenes;
        var path = "Builds/WebGL";
        Directory.CreateDirectory(path);

        var report = BuildPipeline.BuildPlayer(scenes, path,
            BuildTarget.WebGL, BuildOptions.None);

        if (report.summary.result == BuildResult.Succeeded)
            Debug.Log($"Build OK: {report.summary.totalSize} bytes");
        else
            Debug.LogError($"Build failed: {report.summary.result}");
    }
}
```

Tell the user to run it via Unity menu **vibe-game → Build WebGL**, or via CLI:
```
Unity -batchmode -quit -projectPath "<path>" -executeMethod VibeBuildScript.BuildWebGL -logFile -
```

### Step 3 — Package
Once built, instructions for zip:
```
cd Builds/WebGL && zip -r ../webgl-build.zip .
```

### Step 4 — itch.io page draft

Generate `Builds/itch-page.md` from the brief:

```markdown
# {{Brief.HOOK}}

> {{Brief.MOOD as tagline}}

## Controls
{{controls from scene}}

## About
{{Expanded hook, 2-3 sentences using mood, verb, references}}

## Credits
{{From CREDITS.md}}

## Tags
{{auto-derived from verb + mood + genre}}

## Screenshots (placeholders)
1. Hero shot — player doing the verb
2. Wide gameplay — multiple elements
3. Close-up — the juice landing
```

### Step 5 — Devlog post (bonus)

Generate `Builds/devlog-launch.md` — a launch post for Twitter/X / Mastodon / itch devlog:

```markdown
# 🎮 {{Title}} is out!

{{Hook}}

Made with vibe-game over {{timeline}}. {{One sentence about the journey.}}

▶ Play: https://YOURUSER.itch.io/{{slug}}

#indiedev #madewithunity #{{genre-tag}}
```

### Step 6 — Publish guide
End with the manual steps:

> ✓ Build at `Builds/WebGL/`, zipped at `Builds/webgl-build.zip`.
> ✓ Page draft at `Builds/itch-page.md`.
> ✓ Launch post at `Builds/devlog-launch.md`.
>
> Now do this:
> 1. Go to itch.io/dashboard → Create new project
> 2. Kind of project: HTML
> 3. Upload `webgl-build.zip`, check "This file will be played in the browser"
> 4. Set viewport: 960×540 (or your actual)
> 5. Copy `itch-page.md` content into description
> 6. Add tags from the draft
> 7. Take 3 screenshots in-game (PrintScreen during Play in Unity Editor)
> 8. Set visibility → Public
> 9. Click View page → copy URL
> 10. Tweet `devlog-launch.md` content with the URL

## Anti-patterns

- ❌ Ship without controls overlay
- ❌ Ship without the verb working in 10s
- ❌ Block ship on minor polish (the goal is shipping, not perfection)
- ❌ Skip the devlog post — marketing matters (Tyroller M10)
- ❌ Forget the CREDITS.md attributions
- ❌ Ship with debug logs / cheat keys still active

## Cross-references

- Reads: [[vibe-brief]] (for page content), [[feel-check]] (for score check), `CREDITS.md`
- Final gate. Run [[feel-check]] before this. Run [[cut]] if scope is still bloated.
