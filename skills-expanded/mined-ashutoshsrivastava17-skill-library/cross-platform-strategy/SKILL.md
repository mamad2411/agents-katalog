---
name: cross-platform-strategy
description: >
  Evaluate and choose a mobile development strategy — Flutter vs. native (Kotlin/Swift)
  vs. Kotlin Multiplatform (KMP) vs. React Native vs. .NET MAUI. Decision framework
  covering team skills, platform API access, performance, long-term maintenance, and cost.
  TRIGGER when: user says /cross-platform-strategy, asks whether to use Flutter or native,
  needs to choose a mobile framework, or wants to evaluate cross-platform vs. native tradeoffs.
argument-hint: "[app requirements or decision context]"
user-invocable: true
---

# Cross-Platform Strategy

You are a senior engineering leader. Help the user make an informed, evidence-based decision about mobile development approach — cross-platform vs. native — with structured analysis and clear tradeoffs.

## Process

### Step 1: Understand the Context

| Question | Why It Matters |
|----------|---------------|
| What platforms are required? (iOS, Android, Web, Desktop) | Narrows the options |
| What is the team's current expertise? | Learning curve and velocity impact |
| What platform APIs are needed? (Camera, Bluetooth, ARKit, HealthKit, NFC) | Native API depth |
| What are the performance requirements? (60fps animations, real-time, GPU-intensive) | Framework capability limits |
| What is the expected app lifespan? (1 year MVP vs. 10+ year product) | Long-term maintenance cost |
| What is the hiring plan? | Talent availability for chosen technology |
| What is the budget? (single team vs. platform teams) | Team structure impact |
| Is there an existing codebase? | Migration vs. greenfield |

### Step 2: Framework Comparison

| Criteria | Flutter | Native (Kotlin/Swift) | KMP (Kotlin Multiplatform) | React Native | .NET MAUI |
|----------|---------|----------------------|---------------------------|-------------|-----------|
| **Language** | Dart | Kotlin + Swift | Kotlin (shared) + Swift/Kotlin (UI) | JavaScript/TypeScript | C# |
| **UI Rendering** | Own engine (Skia/Impeller) | Platform native | Platform native | Platform native (bridge) | Platform native |
| **Code Sharing** | ~90-95% (UI + logic) | 0% (separate codebases) | ~50-70% (logic only) | ~85-90% (UI + logic) | ~90% (UI + logic) |
| **Platform API Access** | Via plugins + platform channels | Full, immediate | Full (native UI layer) | Via native modules (bridge) | Via handlers |
| **Performance** | Near-native (AOT compiled) | Best possible | Native | Good (improved with new arch) | Good |
| **Hot Reload** | Stateful hot reload (fast) | Limited (Compose preview) | No | Fast Refresh | Hot Reload |
| **App Size** | +5-10MB (engine) | Baseline | +2-3MB (runtime) | +7-10MB (JS engine) | +5-8MB (runtime) |
| **Maturity** | Since 2018, Google-backed | 15+ years each | Since 2020, JetBrains-backed | Since 2015, Meta-backed | Since 2022, Microsoft-backed |
| **Community** | Large, fast-growing | Largest | Growing rapidly | Large | Moderate |
| **Hiring** | Growing pool, Dart is niche | Largest pool | Kotlin devs (large pool) | JS devs (largest pool) | .NET devs (moderate) |

### Step 3: Evaluate Each Option

#### Flutter

**Best for:**
- Teams shipping to iOS + Android with one codebase
- UI-heavy apps with custom designs (not strictly platform-native look)
- Startups and small teams maximizing velocity
- Apps that also need Web or Desktop targets

**Strengths:**
- Single codebase for UI and logic (~95% code sharing)
- Fastest development velocity for cross-platform
- Excellent widget library and ecosystem
- Consistent look across platforms (pixel-perfect)
- Strong tooling (DevTools, hot reload)
- Growing enterprise adoption (Google, BMW, Toyota, eBay)

**Weaknesses:**
- Custom rendering engine means UI doesn't look 100% native by default (Material/Cupertino widgets approximate it)
- Platform-specific features require plugins or platform channels
- Dart is less widely known than Kotlin/Swift/JS
- Larger app size (~5-10MB for engine)
- Some platform APIs have plugin gaps or lag behind native SDKs
- Not ideal for apps deeply integrated with platform UI (widgets, system extensions)

**When NOT to use Flutter:**
- App heavily relies on platform-specific APIs with no mature Flutter plugin (ARKit, CarPlay, Widgets)
- Strict "must look exactly like a native app" requirement
- Team has deep native expertise and no cross-platform need
- App is for a single platform only

#### Native (Kotlin + Swift)

**Best for:**
- Apps requiring maximum platform integration
- Performance-critical apps (gaming, AR, real-time audio/video)
- Large companies with dedicated platform teams
- Apps using cutting-edge platform APIs on day one

**Strengths:**
- Best performance, smallest app size
- Immediate access to all platform APIs (day-one support)
- Largest developer community and hiring pool
- Deepest IDE support (Android Studio, Xcode)
- No abstraction layer — full control
- Best for platform-specific UX (widgets, extensions, watchOS, Wear OS)

**Weaknesses:**
- Two separate codebases to maintain (Kotlin + Swift)
- Double the development effort for equivalent features
- Requires hiring/training for both platforms
- Business logic is duplicated (unless using KMP for shared logic)
- Harder to keep feature parity across platforms

**When NOT to go native:**
- Small team that can't sustain two codebases
- App is UI-heavy with no deep platform integration
- Budget doesn't support two platform teams
- Speed to market is critical

#### Kotlin Multiplatform (KMP)

**Best for:**
- Teams with strong Kotlin/Android expertise wanting iOS too
- Apps where business logic is complex but UI should be platform-native
- Gradual adoption in existing native apps (share logic incrementally)
- Companies that want native UI quality with shared business logic

**Strengths:**
- Share business logic (networking, data, domain) while keeping native UI
- Each platform gets truly native UI (Compose + SwiftUI)
- Incremental adoption — add to existing native apps module by module
- Kotlin is widely known, excellent language
- JetBrains-backed with Google endorsement
- Libraries like Ktor, SQLDelight, kotlinx.serialization work cross-platform

**Weaknesses:**
- Only shares logic, not UI (~50-70% sharing, not 90%+)
- Still need UI developers for both platforms
- iOS tooling is less mature than Android tooling
- Compose Multiplatform (for shared UI) is newer and less battle-tested
- Smaller ecosystem than Flutter or React Native
- Swift interop has friction points

**When NOT to use KMP:**
- Team wants maximum code sharing including UI
- No existing Kotlin expertise on the team
- Simple app where shared logic doesn't justify the complexity

#### React Native

**Best for:**
- Teams with strong JavaScript/TypeScript expertise
- Apps with web counterparts (shared knowledge, potentially shared code)
- Companies in the JS/TS ecosystem (Node.js backend)
- Brownfield integration into existing native apps

**Strengths:**
- Large ecosystem (npm), massive community
- Leverages existing JS/TS developer pool (largest in the world)
- Uses platform native components (looks native)
- New Architecture (Fabric + TurboModules) significantly improves performance
- Mature, used by Meta, Microsoft, Shopify, Discord
- Expo simplifies development workflow dramatically

**Weaknesses:**
- JavaScript bridge (legacy arch) adds latency for complex interactions
- Complex native modules require Kotlin/Swift knowledge anyway
- Performance ceiling lower than Flutter/native for animation-heavy apps
- Upgrade path between versions can be painful
- Debugging across JS/native boundary is harder

**When NOT to use React Native:**
- Team has no JS/TS experience
- App is GPU-intensive or animation-heavy
- Need to access very new platform APIs quickly (native module lag)

#### .NET MAUI

**Best for:**
- Teams with strong C#/.NET expertise
- Enterprise apps in the Microsoft ecosystem
- Apps targeting iOS + Android + Windows + macOS

**Strengths:**
- C# is a mature, type-safe language
- Single project targets mobile + desktop
- Good for enterprise apps with .NET backend
- Microsoft-backed with Visual Studio integration

**Weaknesses:**
- Smallest mobile community of all options
- Fewer third-party libraries
- Performance and stability issues still being addressed
- Limited adoption outside Microsoft ecosystem
- Harder to hire mobile developers with .NET MAUI experience

### Step 4: Decision Framework

```
Do you need both iOS and Android?
  ├── No (single platform) → Go Native
  └── Yes
      ├── Do you have an existing native codebase?
      │   ├── Yes → KMP (share logic incrementally) or stay native
      │   └── No (greenfield)
      │       ├── Is maximum platform API integration critical? (AR, HealthKit, CarPlay)
      │       │   ├── Yes → Native (or KMP for shared logic)
      │       │   └── No
      │       │       ├── What is the team's primary language?
      │       │       │   ├── Dart / no preference → Flutter
      │       │       │   ├── Kotlin / JVM → KMP + Compose Multiplatform (or Flutter)
      │       │       │   ├── JavaScript / TypeScript → React Native
      │       │       │   ├── C# / .NET → .NET MAUI
      │       │       │   └── Swift + Kotlin → Native (or KMP)
      │       │       └── Is UI custom/branded (not platform-native)?
      │       │           ├── Yes → Flutter (best for custom UI)
      │       │           └── No (must look 100% native) → KMP or React Native
```

### Step 5: Cost & Team Structure Analysis

| Approach | Team Size (for equivalent output) | Maintenance Burden | Hiring Difficulty |
|----------|----------------------------------|-------------------|-------------------|
| **Flutter** | 1x (one team) | Low (single codebase) | Medium (Dart is niche but learnable) |
| **Native** | 2x (two platform teams) | High (two codebases) | Low (large talent pool) |
| **KMP** | 1.5x (shared + platform UI) | Medium | Low-Medium (Kotlin developers) |
| **React Native** | 1x (one team) | Medium (bridge maintenance) | Low (JS developers everywhere) |
| **MAUI** | 1x (one team) | Medium | High (niche mobile skill) |

### Step 6: Migration Considerations

| From | To | Strategy |
|------|-----|---------|
| **Native → Flutter** | Rewrite or strangler (add Flutter modules via add-to-app) |
| **Native → KMP** | Incremental — extract shared logic module by module |
| **React Native → Flutter** | Rewrite (architecturally different) |
| **React Native → Native** | Incremental with brownfield native modules |
| **Flutter → Native** | Rare — usually means Flutter wasn't the right choice |

**add-to-app strategy (incremental Flutter adoption):**
- Keep existing native app
- Embed Flutter screens for new features
- Gradually migrate screens to Flutter
- Eventually replace native shell entirely (or keep hybrid)

## Output Format

```markdown
## Recommendation
- **Approach:** [Flutter / Native / KMP / React Native]
- **Rationale:** [2-3 sentences on why]
- **Risk:** [Main risk of this choice]

## Evaluation Matrix
| Criteria | Weight | Flutter | Native | KMP | React Native |
|----------|--------|---------|--------|-----|-------------|
| Team skills | ... | /5 | /5 | /5 | /5 |
| Platform API needs | ... | /5 | /5 | /5 | /5 |
| Performance requirements | ... | /5 | /5 | /5 | /5 |
| Development velocity | ... | /5 | /5 | /5 | /5 |
| Long-term maintenance | ... | /5 | /5 | /5 | /5 |
| Hiring & talent | ... | /5 | /5 | /5 | /5 |
| **Weighted Total** | | **/30** | **/30** | **/30** | **/30** |

## Team Structure
[Recommended team composition for chosen approach]

## Migration Plan (if applicable)
[How to transition from current approach]

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| ... | ... |
```

## Quality Checklist

- [ ] Decision is based on actual requirements, not hype or preference
- [ ] Team skills and hiring realities are factored in
- [ ] Platform API needs are inventoried (not just assumed)
- [ ] Performance requirements are quantified (not just "must be fast")
- [ ] Long-term maintenance cost is considered (not just initial development)
- [ ] A proof-of-concept validates the riskiest assumption before committing
- [ ] Stakeholders understand the tradeoffs of the chosen approach

## Edge Cases

- If the app is primarily a WebView wrapper, consider a PWA instead of any native framework
- If targeting foldables, Wear OS, watchOS, or tvOS, evaluate framework support for those form factors (Flutter has limited watch/TV support)
- If the app needs to ship SDKs to other developers, native is usually required (Flutter SDKs add the engine to consumers' apps)
- For apps in regulated industries needing FIPS-compliant crypto, verify the framework's crypto libraries are certified
- If the team is 1-2 developers, Flutter or React Native maximizes output; native with a team that small means constant context-switching
- Kotlin Multiplatform + Compose Multiplatform is converging toward Flutter-like code sharing but with native rendering — evaluate as it matures
- Consider that switching frameworks mid-project is extremely expensive — invest in a proof-of-concept before committing
