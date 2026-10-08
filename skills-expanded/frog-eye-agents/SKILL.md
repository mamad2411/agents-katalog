# AGENTS.md — Frog Eye

Frogger-Klon, gespielt aus der First-Person-Perspektive eines Frosches mit biologisch motivierter Frosch-Optik.

## Stack
- **Three.js** (npm, ES Modules) — 3D Szene, Low-Poly, kein Shader-Framework außer für Vision-Pass
- **Vite** — Dev-Server (`npm run dev`) und Build (`npm run build`)
- **ESLint** — `npm run lint` — flat config (`eslint.config.js`), prefer-const, no-var

## Modulstruktur

| Pfad | Verantwortung |
|------|--------------|
| `src/main.js` | Bootstrap: Scene + Loop starten, alles verdrahten |
| `src/scene.js` | Three.js Scene, Renderer, Kamera, Lichter, Resize |
| `src/frog/frog.js` | Grid-Position, Sprung-Logik, Freeze-Zustand |
| `src/frog/frogCamera.js` | First-Person-Kamera, Sprungbogen-Animation |
| `src/vision/frogEyePass.js` | Custom FBO + GLSL Barrel-Distortion + Farbshift (kein EffectComposer — split-screen inkompatibel) |
| `src/vision/motionMask.js` | Statische Objekte ausblenden (M8) |
| `src/world/grid.js` | Spielfeld-Raster, Reihen-Typen, Koordinaten |
| `src/world/road.js` | Straßen-Geometrie + Fahrzeug-Spawning |
| `src/world/river.js` | Fluss-Geometrie + Plattform-Spawning |
| `src/world/vehicle.js` | Auto/Lkw Entity — Body + Kabine + Räder (Zylinder + Rim) + Auspuff (Lkw) |
| `src/world/platform.js` | Log (Zylinder+Kappen), Schildkröte (Panzer/Flossen/Augen), Krokodil (Segmente/Augen) — Sink-Zyklus |
| `src/world/goal.js` | 5 Ziel-Slots, Gewinn-Check |
| `src/ui/hud.js` | HTML-Overlay: Punkte, Leben, Timer |
| `src/ui/screens.js` | Start/Game-Over/Level-Up Screens |
| `src/utils/constants.js` | UPPER_SNAKE Konstanten: Dimensionen, Geschwindigkeiten |
| `src/utils/pool.js` | Object Pool für Fahrzeuge/Plattformen |
| `src/utils/collision.js` | Grid-Kollision: Frosch ↔ Fahrzeug, Feld-Typ |

## Konventionen
- **ES Modules only** — kein CommonJS, kein Default-Export-Chaos
- **Named exports** aus jedem Modul
- **Kurze Funktionen** — max. ~20 Zeilen, eine Aufgabe
- **Kein Kommentar** für Offensichtliches — nur für nicht-offensichtliche Entscheidungen
- **Low-Poly**: `MeshPhongMaterial({ flatShading: true })`, keine Texturen, Vertex-Farben
- **Grid-System**: Frosch bewegt sich in ganzen Feldern (1 Feld = 1 Three.js-Unit)
- Temporärer Code in `main.js` ist mit `// Temp:` markiert und wird in späteren Milestones ersetzt

## Frosch-Vision (Milestone 7+)
- Post-Processing via **custom FBO + ShaderMaterial** (kein EffectComposer — split-screen inkompatibel)
- Fisheye: Barrel-Distortion GLSL, linke + rechte Bildschirmhälfte getrennt
- Farbshift: Rot-Kanal → 20%, Grün/Blau → 100%
- Motion Mask: Statische Objekte → ~15% Opacity via Three.js Layers (Layer 1 = statisch, Layer 2 = bewegend)

## Aktueller Stand
- **Milestone 1 ✓**: Vite + ESLint + Three.js läuft
- **Milestone 2 ✓**: Spielfeld — Gras, Straße (Curbs + Dashes), Fluss (animiert), Seerosen-Slots
- **Milestone 3 ✓**: Frosch springt grid-basiert; Kamera dreht sich mit `facingAngle`; W=springen, A/D=drehen
- **Milestone 4 ✓**: 11 Fahrzeuge fahren, wrappen, töten den Frosch; Pool, Kollision, Leben
- **Dual-Eye Vision ✓**: Zwei Kameras (je 120° FOV, 50° nach außen geneigt) → ~214° Sichtfeld; Nasenstreifen; `renderDualEye()` mit Scissor/Viewport; `autoClear=false`
- **Milestone 5 ✓**: Plattformen (Log/Turtle/Croc), Schildkröten-Sink-Zyklus, `frog.worldX` für Drift, Ertrinken
- **Milestone 6 ✓**: Ziel-Slots, Score (+10/+50), Level-Up (Speed ×1.25), filledSlots State
- **Milestone 7 ✓**: Fisheye-Shader — Barrel-Distortion + Farbshift (custom FBO, kein EffectComposer)
- **Milestone 8 ✓**: Motion Mask — Layer 1/2, statische Objekte ~15% Opacity
- **Milestone 9 ✓**: HUD (Score/Leben/Level/Timer), Minimap, Game-End-Logic
- **Milestone 10 (laufend)**: Fahrzeuge mit Rädern + Auspuff; Plattformen detailliert (Zylinder-Log, Schildkröte mit Anatomie, Krokodil mit Segmenten); Wasser mit 3-Frequenz-Wellen + Spekularhighlight

## Wichtige Spielfeld-Zahlen (aus `constants.js`)
- Rasterbreite: 13 Felder
- Reihen gesamt: 16 (0 = Start, 15 = Ziel-Gras)
- Straße: Reihen 1–5
- Mittleres Gras: Reihe 6
- Fluss: Reihen 7–12
- Ziel: Reihen 13–15 (5 Slots)
