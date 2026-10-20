---
name: rpg-maker
description: "Build RPG Maker MZ or MV JavaScript plugins, edit game data, and troubleshoot events or Pixi.js rendering."
category: game-engines
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["rpg-maker", "rpgmaker-mz", "javascript-plugins", "pixijs", "gamedev", "event-scripting", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# RPG Maker MZ/MV Game Development AI Skill Guide (Claude)

## Overview & Engine Architecture
RPG Maker MZ (and MV) is a 2D tile-based JRPG game creation engine powered by a modern JavaScript and **Pixi.js WebGL** rendering pipeline packaged inside the **NW.js (Chromium)** desktop runtime. The engine uses a pure JSON data model (**`data/*.json`**), an **Event Interpreter state machine**, and an object-oriented core architecture (**`rmmz_core.js`**, **`rmmz_managers.js`**, **`rmmz_objects.js`**, **`rmmz_scenes.js`**, **`rmmz_windows.js`**). Claude operates as a Principal JRPG Systems Architect and JavaScript Plugin Developer, specializing in **MZ/MV plugin architecture**, **Pixi.js rendering optimization**, **custom combat/quest system scripting**, and **save-game serialization (`DataManager`)**.

### RPG Maker MZ/MV Core Runtime & Plugin Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 RPG Maker MZ Runtime Engine                 │
│                                                             │
│  Presentation & WebGL Rendering Tier                        │
│  ├── NW.js Desktop Wrapper / Browser HTML5 Canvas           │
│  ├── Pixi.js v5 WebGL Render Pipeline (Sprites, Tilemaps)   │
│  └── Scene Flow Controller (`SceneManager`, `Scene_Base`)   │
│                                                             │
│  Game Data & Object Layer                                   │
│  ├── Game Singletons (`$gameParty`, `$gameActors`, `$gameMap`)│
│  ├── Event Command Interpreter (`Game_Interpreter`)         │
│  └── JSON Database Cache (`data/System.json`, `data/Map*.json`)│
│                                                             │
│  Extensibility & Plugin Engine                              │
│  ├── Plugin Manager (`PluginManager.registerCommand`)       │
│  └── Prototype Method Monkey-Patching Engine                │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **RPG Maker MZ/MV Plugin Development**: Author clean, compliant JavaScript plugins with strict JSDoc/Plugin Header annotations (`/*:`, `@target MZ`, `@command`, `@param`), monkey-patching methods safely using aliased original references.
2. **Save Data Serialization**: Hook `DataManager.makeSaveContents` and `DataManager.extractSaveContents` to persist custom gameplay data across player saves without breaking save compatibility.
3. **Event Interpreter & Logic Triage**: Diagnose infinite loops, frozen parallel process events, unhandled conditional branches, and missing `Break Loop` commands.
4. **Asset & Path Sanitization**: Fix broken web/mobile deployments caused by non-ASCII characters, spaces in filenames, and missing `.ogg` / `.m4a` audio format fallbacks.

---

## Production JavaScript Plugin: Dynamic Quest Log System (RPG Maker MZ)

Save this script as `js/plugins/CustomQuestSystem.js` and register inside `js/plugins.js`:

```javascript
// ==============================================================================
// RPG Maker MZ Plugin: Dynamic Quest Log & Tracker
// Adds custom quest tracking with save persistence and Plugin Commands.
// ==============================================================================
/*:
 * @target MZ
 * @plugindesc v1.0.0 Adds an extensible Quest Tracking System with save data persistence.
 * @author AI Systems Engineering
 *
 * @command addQuest
 * @text Add Quest
 * @desc Adds a new quest to the player's active quest log.
 *
 * @arg questId
 * @text Quest ID
 * @type string
 * @desc Unique identifier for the quest.
 *
 * @arg questTitle
 * @text Quest Title
 * @type string
 * @desc Human-readable title of the quest.
 */

(() => {
  'use strict';

  const pluginName = 'CustomQuestSystem';

  // 1. Data Model Extension
  class QuestManager {
    constructor() {
      this._quests = {};
    }

    addQuest(id, title) {
      if (!this._quests[id]) {
        this._quests[id] = { id: id, title: title, completed: false };
        console.log(`[QuestSystem] Added Quest: ${title} (${id})`);
      }
    }

    completeQuest(id) {
      if (this._quests[id]) {
        this._quests[id].completed = true;
        console.log(`[QuestSystem] Completed Quest: ${id}`);
      }
    }

    getQuests() {
      return Object.values(this._quests);
    }
  }

  // 2. Global Instance and Save Data Serialization Hook
  const _DataManager_makeSaveContents = DataManager.makeSaveContents;
  DataManager.makeSaveContents = function() {
    const contents = _DataManager_makeSaveContents.call(this);
    contents.customQuestData = $gameSystem._questManager ? $gameSystem._questManager._quests : {};
    return contents;
  };

  const _DataManager_extractSaveContents = DataManager.extractSaveContents;
  DataManager.extractSaveContents = function(contents) {
    _DataManager_extractSaveContents.call(this, contents);
    if (!$gameSystem._questManager) {
      $gameSystem._questManager = new QuestManager();
    }
    if (contents.customQuestData) {
      $gameSystem._questManager._quests = contents.customQuestData;
    }
  };

  const _Game_System_initialize = Game_System.prototype.initialize;
  Game_System.prototype.initialize = function() {
    _Game_System_initialize.call(this);
    this._questManager = new QuestManager();
  };

  // 3. Register RPG Maker MZ Plugin Commands
  PluginManager.registerCommand(pluginName, 'addQuest', args => {
    if ($gameSystem._questManager) {
      $gameSystem._questManager.addQuest(args.questId, args.questTitle);
    }
  });
})();
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Game Freezes Indefinitely on Map Entry** | Parallel Process or Autorun event running without an exit condition, locking the `Game_Interpreter`. | 1. Press `F9` in Test Play to open the Variable/Switch debug menu.<br>2. Look for Autorun events missing a Self Switch `A=ON` to transition to an empty page.<br>3. Check loops for missing `Break Loop` commands. |
| **Browser Web Build Fails: `Failed to load resource (404/CORS)`** | Audio/image asset filenames contain spaces or uppercase letters that fail on case-sensitive web servers (Linux/Nginx). | 1. Rename all asset files in `audio/` and `img/` to strict lowercase with hyphens (e.g. `bgm-battle.ogg`).<br>2. Update references in `data/System.json`. |
| **TypeError: Cannot read property of undefined on Battle Start** | Plugin load order collision where a lower plugin overwrites `Scene_Battle.prototype.create` without calling the alias. | 1. In Plugin Manager, place core library plugins (e.g. VisuStella / Yanfly) at the top of the load order.<br>2. Ensure custom plugins preserve the prototype alias: `_alias.call(this)`. |
| **NW.js Memory Leak / Crashing After 30 Minutes of Play** | Pixi.js texture cache retaining uncached map assets during frequent transitions. | Periodically trigger `ImageManager.clear()` on chapter transitions or major world map loads. |

---

## Command Line Syntax & Debugging

```bash
# 1. Launch RPG Maker Project in Dedicated Test Play Debug Mode
"C:\Program Files\RPG Maker MZ\nwjs-win\nw.exe" "C:\GameProjects\MyRPG" --test --debug

# 2. Open Embedded Chromium Developer Tools Console in Game Window
# Press F8 or F12 during game execution
```

### Essential File Locations
- **Database Files**: `<ProjectRoot>/data/*.json`
- **Plugin Manifest**: `<ProjectRoot>/js/plugins.js`
- **Engine Core Code**: `<ProjectRoot>/js/rmmz_core.js`

---

## Agent Operational Directive
> **MANDATORY**: When monkey-patching engine methods in JavaScript plugins, always alias and invoke the original method (`const _alias = Class.prototype.func; Class.prototype.func = function() { _alias.call(this); ... }`) to ensure multi-plugin interoperability.
