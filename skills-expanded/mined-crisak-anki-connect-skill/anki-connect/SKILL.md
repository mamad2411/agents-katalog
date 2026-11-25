---
name: anki-connect
description: Manipulate Anki flashcards via curl using the Anki-Connect API. Create cards, manage decks, search notes, customize note types, and control Anki entirely through HTTP requests.
compatibility: opencode, claude-code, copilot-cli
license: MIT
metadata:
  author: custom
  version: 1.0.0
---

## What I do

I enable AI agents to control Anki completely through the Anki-Connect HTTP API using curl. I provide all the knowledge needed to:

- Create flashcards (single or batch)
- Manage decks (create, delete, list, configure)
- Search and find notes/cards
- Customize note types (models), templates, fields, and CSS styling
- Manage tags (add, remove, replace, clear unused)
- Control Anki GUI (browse, review, add cards dialog, edit notes)
- Handle media files (upload, retrieve, delete, list)
- Get statistics and review history
- Full card control (suspend, unsuspend, forget, relearn, answer)
- Export/import decks as .apkg files
- Manage deck configurations

## When to use me

Activate this skill when the user wants to:

- Create flashcards dynamically or in bulk
- Search if a question exists in any deck
- List available tags or note types
- Modify existing cards, notes, or note types
- Create custom card designs, templates, or CSS styling
- Manage decks and deck configurations
- Control Anki GUI programmatically
- Get statistics about reviews or collection
- Any operation involving Anki that requires the AI to execute curl commands

## Prerequisites

**IMPORTANT**: Before making any Anki-Connect request, the AI MUST:

1. Verify Anki is running and Anki-Connect is available
2. If the server is not responding, inform the user they need to open Anki

### Verification Command

```bash
curl -s localhost:8765 -X POST -d '{"action": "requestPermission", "version": 6}'
```

If the response is empty or connection is refused, tell the user:
> "Anki-Connect is not running. Please open Anki and ensure the Anki-Connect add-on is installed (Tools > Add-ons > Anki-Connect)."

## API Base

- **URL**: `http://localhost:8765`
- **Port**: 8765 (default)
- **Version**: 6 (use version 6 for all requests)
- **Method**: POST with JSON body

## Request Format

All requests use curl with POST:

```bash
curl localhost:8765 -X POST -d '{"action": "ACTION_NAME", "version": 6, "params": {...}}'
```

## Response Format

Successful response:
```json
{"result": [...], "error": null}
```

Error response:
```json
{"result": null, "error": "error description"}
```

---

## API Reference by Category

---

### Card Actions

#### getEaseFactors - Get ease factors of cards
Returns an array with the ease factor for each of the given cards (in the same order).

```bash
curl localhost:8765 -X POST -d '{"action": "getEaseFactors", "version": 6, "params": {"cards": [1483959291685, 1483959293217]}}'
```

#### setEaseFactors - Set ease factors of cards
Sets ease factor of cards by card ID; returns `true` if successful (all cards existed) or `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "setEaseFactors", "version": 6, "params": {"cards": [1483959291685, 1483959293217], "easeFactors": [4100, 3900]}}'
```

#### setSpecificValueOfCard - Set specific card values
Sets specific value of a single card. Some keys require `warning_check: true`. Can set flags, ease factor, review order in filtered deck, and database column "data".

```bash
curl localhost:8765 -X POST -d '{"action": "setSpecificValueOfCard", "version": 6, "params": {"card": 1483959291685, "keys": ["flags", "odue"], "newValues": ["1", "-100"]}}'
```

#### suspend - Suspend cards
Suspend cards by card ID; returns `true` if successful or `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "suspend", "version": 6, "params": {"cards": [1483959291685, 1483959293217]}}'
```

#### unsuspend - Unsuspend cards
Unsuspend cards by card ID; returns `true` if successful or `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "unsuspend", "version": 6, "params": {"cards": [1483959291685, 1483959293217]}}'
```

#### suspended - Check if card is suspended
Check if card is suspended by its ID. Returns `true` if suspended, `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "suspended", "version": 6, "params": {"card": 1483959293217}}'
```

#### areSuspended - Check multiple cards suspension status
Returns an array indicating whether each of the given cards is suspended. If card doesn't exist returns `null`.

```bash
curl localhost:8765 -X POST -d '{"action": "areSuspended", "version": 6, "params": {"cards": [1483959291685, 1483959293217, 1234567891234]}}'
```

#### areDue - Check if cards are due
Returns an array indicating whether each of the given cards is due. Note: cards in learning queue with large interval (>20 min) are treated as not due.

```bash
curl localhost:8765 -X POST -d '{"action": "areDue", "version": 6, "params": {"cards": [1483959291685, 1483959293217]}}'
```

#### getIntervals - Get card intervals
Returns an array of the most recent intervals for each card ID, or a 2-dimensional array of all intervals when `complete` is `true`. Negative intervals are in seconds, positive in days.

```bash
# Recent intervals only
curl localhost:8765 -X POST -d '{"action": "getIntervals", "version": 6, "params": {"cards": [1502298033753, 1502298036657]}}'
# Complete interval history
curl localhost:8765 -X POST -d '{"action": "getIntervals", "version": 6, "params": {"cards": [1502298033753, 1502298036657], "complete": true}}'
```

#### findCards - Find cards by query
Returns an array of card IDs for a given query. Functionally identical to `guiBrowse` but without GUI for better performance.

```bash
curl localhost:8765 -X POST -d '{"action": "findCards", "version": 6, "params": {"query": "deck:current"}}'
```

#### cardsToNotes - Convert card IDs to note IDs
Returns an unordered array of note IDs for the given card IDs. For cards with the same note, the ID is only given once.

```bash
curl localhost:8765 -X POST -d '{"action": "cardsToNotes", "version": 6, "params": {"cards": [1502098034045, 1502098034048, 1502298033753]}}'
```

#### cardsModTime - Get card modification times
Returns a list of objects containing the modification time for each card ID. About 15x faster than `cardsInfo`.

```bash
curl localhost:8765 -X POST -d '{"action": "cardsModTime", "version": 6, "params": {"cards": [1498938915662, 1502098034048]}}'
```

#### cardsInfo - Get detailed card info
Returns a list of objects containing for each card ID: card fields, front/back sides including CSS, note type, deck name, ease, interval, and more.

```bash
curl localhost:8765 -X POST -d '{"action": "cardsInfo", "version": 6, "params": {"cards": [1498938915662, 1502098034048]}}'
```

#### forgetCards - Forget cards
Makes cards new again (resets review history).

```bash
curl localhost:8765 -X POST -d '{"action": "forgetCards", "version": 6, "params": {"cards": [1498938915662, 1502098034048]}}'
```

#### relearnCards - Make cards relearning
Makes cards enter the relearning queue.

```bash
curl localhost:8765 -X POST -d '{"action": "relearnCards", "version": 6, "params": {"cards": [1498938915662, 1502098034048]}}'
```

#### answerCards - Answer cards (non-GUI)
Answer cards by card ID. Ease is between 1 (Again) and 4 (Easy). Will start the timer immediately. Returns `true` if card exists, `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "answerCards", "version": 6, "params": {"answers": [{"cardId": 1498938915662, "ease": 2}, {"cardId": 1502098034048, "ease": 4}]}}'
```

#### setDueDate - Set due date for cards
Set Due Date. Turns cards into review cards if they are new, and makes them due on a certain date.
- `0` = today
- `1!` = tomorrow + change interval to 1
- `3-7` = random choice of 3-7 days

```bash
curl localhost:8765 -X POST -d '{"action": "setDueDate", "version": 6, "params": {"cards": [1498938915662, 1502098034048], "days": "3-7"}}'
```

---

### Deck Actions

#### deckNames - List all deck names
Gets the complete list of deck names for the current user.

```bash
curl localhost:8765 -X POST -d '{"action": "deckNames", "version": 6}'
```

#### deckNamesAndIds - List decks with IDs
Gets the complete list of deck names and their respective IDs.

```bash
curl localhost:8765 -X POST -d '{"action": "deckNamesAndIds", "version": 6}'
```

#### getDecks - Get decks for cards
Accepts an array of card IDs and returns an object with each deck name as key and its value an array of the given cards which belong to it.

```bash
curl localhost:8765 -X POST -d '{"action": "getDecks", "version": 6, "params": {"cards": [1502298036657, 1502298033753, 1502032366472]}}'
```

#### createDeck - Create a new deck
Create a new empty deck. Will not overwrite a deck that exists with the same name. Use `::` for nested decks.

```bash
curl localhost:8765 -X POST -d '{"action": "createDeck", "version": 6, "params": {"deck": "Japanese::JLPT::N3"}}'
```

#### changeDeck - Move cards to another deck
Moves cards with the given IDs to a different deck, creating the deck if it doesn't exist yet.

```bash
curl localhost:8765 -X POST -d '{"action": "changeDeck", "version": 6, "params": {"cards": [1502098034045, 1502098034048, 1502298033753], "deck": "Japanese::JLPT N3"}}'
```

#### deleteDecks - Delete decks
Deletes decks with the given names. The argument `cardsToo` must be set to `true` to delete the cards too.

```bash
curl localhost:8765 -X POST -d '{"action": "deleteDecks", "version": 6, "params": {"decks": ["Japanese::JLPT N5", "Easy Spanish"], "cardsToo": true}}'
```

#### getDeckConfig - Get deck configuration
Gets the configuration group object for the given deck.

```bash
curl localhost:8765 -X POST -d '{"action": "getDeckConfig", "version": 6, "params": {"deck": "Default"}}'
```

#### saveDeckConfig - Save deck configuration
Saves the given configuration group, returning `true` on success or `false` if the ID is invalid.

```bash
curl localhost:8765 -X POST -d '{"action": "saveDeckConfig", "version": 6, "params": {"config": {"lapse": {"leechFails": 8, "delays": [10], "minInt": 1, "leechAction": 0, "mult": 0}, "dyn": false, "autoplay": true, "mod": 1502970872, "id": 1, "maxTaken": 60, "new": {"bury": true, "order": 1, "initialFactor": 2500, "perDay": 20, "delays": [1, 10], "separate": true, "ints": [1, 4, 7]}, "name": "Default", "rev": {"bury": true, "ivlFct": 1, "ease4": 1.3, "maxIvl": 36500, "perDay": 100, "minSpace": 1, "fuzz": 0.05}, "timer": 0, "replayq": true, "usn": -1}}}'
```

#### setDeckConfigId - Set deck configuration
Changes the configuration group for the given decks to the one with the given ID.

```bash
curl localhost:8765 -X POST -d '{"action": "setDeckConfigId", "version": 6, "params": {"decks": ["Default"], "configId": 1}}'
```

#### cloneDeckConfigId - Clone deck configuration
Creates a new configuration group with the given name, cloning from the group with the given ID, or from the default group if unspecified.

```bash
curl localhost:8765 -X POST -d '{"action": "cloneDeckConfigId", "version": 6, "params": {"name": "Copy of Default", "cloneFrom": 1}}'
```

#### removeDeckConfigId - Remove deck configuration
Removes the configuration group with the given ID. Cannot remove default (ID=1).

```bash
curl localhost:8765 -X POST -d '{"action": "removeDeckConfigId", "version": 6, "params": {"configId": 1502972374573}}'
```

#### getDeckStats - Get deck statistics
Gets statistics such as total cards, new cards, learning cards, and review cards for the given decks.

```bash
curl localhost:8765 -X POST -d '{"action": "getDeckStats", "version": 6, "params": {"decks": ["Japanese::JLPT N5", "Easy Spanish"]}}'
```

---

### Graphical Actions

#### guiBrowse - Open Card Browser with query
Invokes the Card Browser dialog and searches for a given query. Returns array of card IDs found. Supports `reorderCards` parameter for sorting.

```bash
curl localhost:8765 -X POST -d '{"action": "guiBrowse", "version": 6, "params": {"query": "deck:current"}}'
# With sorting
curl localhost:8765 -X POST -d '{"action": "guiBrowse", "version": 6, "params": {"query": "deck:current", "reorderCards": {"order": "descending", "columnId": "noteCrt"}}}'
```

#### guiSelectCard - Select card in Card Browser
Finds the open Card Browser dialog and selects a card given a card identifier. Returns `true` if browser is open, `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "guiSelectCard", "version": 6, "params": {"card": 1494723142483}}'
```

#### guiSelectedNotes - Get selected notes in Card Browser
Finds the open Card Browser dialog and returns an array of identifiers of the notes that are selected.

```bash
curl localhost:8765 -X POST -d '{"action": "guiSelectedNotes", "version": 6}'
```

#### guiAddCards - Open Add Cards dialog
Invokes the Add Cards dialog, presets the note using the given deck, model, fields, and tags. Returns the ID of the note which would be added.

```bash
curl localhost:8765 -X POST -d '{"action": "guiAddCards", "version": 6, "params": {"note": {"deckName": "Default", "modelName": "Cloze", "fields": {"Text": "The capital of Romania is {{c1::Bucharest}}", "Extra": "Romania is a country in Europe"}, "tags": ["countries"]}}}'
```

#### guiEditNote - Open Edit dialog for a note
Opens the Edit dialog with a note corresponding to given note ID.

```bash
curl localhost:8765 -X POST -d '{"action": "guiEditNote", "version": 6, "params": {"note": 1649198355435}}'
```

#### guiAddNoteSetData - Set data in Add Note dialog
Sets fields, tags, deck, and note type in the Add Note dialog. Only works if dialog is open. Optionally appends to fields/tags.

```bash
# Replace
curl localhost:8765 -X POST -d '{"action": "guiAddNoteSetData", "version": 6, "params": {"note": {"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Hello", "Back": "World"}, "tags": ["new", "api"]}}}'
# Append
curl localhost:8765 -X POST -d '{"action": "guiAddNoteSetData", "version": 6, "params": {"note": {"fields": {"Front": " more text"}, "tags": ["extra"]}, "append": true}}'
```

#### guiCurrentCard - Get current review card info
Returns information about the current card or `null` if not in review mode.

```bash
curl localhost:8765 -X POST -d '{"action": "guiCurrentCard", "version": 6}'
```

#### guiStartCardTimer - Start/reset card timer
Starts or resets the timer for the current card. Useful for deferring start time when displayed via API for more accurate timing.

```bash
curl localhost:8765 -X POST -d '{"action": "guiStartCardTimer", "version": 6}'
```

#### guiShowQuestion - Show question
Shows question text for the current card; returns `true` if in review mode or `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "guiShowQuestion", "version": 6}'
```

#### guiShowAnswer - Show answer
Shows answer text for the current card; returns `true` if in review mode or `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "guiShowAnswer", "version": 6}'
```

#### guiAnswerCard - Answer current card (GUI mode)
Answers the current card in GUI review mode. Note: the answer must be displayed first. Ease: 1=Again, 2=Hard, 3=Good, 4=Easy.

```bash
curl localhost:8765 -X POST -d '{"action": "guiAnswerCard", "version": 6, "params": {"ease": 3}}'
```

#### guiUndo - Undo last action
Undo the last action/card; returns `true` if succeeded or `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "guiUndo", "version": 6}'
```

#### guiDeckOverview - Open Deck Overview dialog
Opens the Deck Overview dialog for the deck with the given name.

```bash
curl localhost:8765 -X POST -d '{"action": "guiDeckOverview", "version": 6, "params": {"name": "Default"}}'
```

#### guiDeckBrowser - Open Deck Browser dialog
Opens the Deck Browser dialog.

```bash
curl localhost:8765 -X POST -d '{"action": "guiDeckBrowser", "version": 6}'
```

#### guiDeckReview - Start deck review
Starts review for the deck with the given name.

```bash
curl localhost:8765 -X POST -d '{"action": "guiDeckReview", "version": 6, "params": {"name": "Default"}}'
```

#### guiImportFile - Import file
Invokes the Import dialog with an optional file path. Supports all file types Anki supports. Only Anki 2.1.52+.

```bash
curl localhost:8765 -X POST -d '{"action": "guiImportFile", "version": 6, "params": {"path": "/path/to/cards.txt"}}'
```

#### guiExitAnki - Close Anki gracefully
Schedules a request to gracefully close Anki. This operation is asynchronous.

```bash
curl localhost:8765 -X POST -d '{"action": "guiExitAnki", "version": 6}'
```

#### guiCheckDatabase - Check database
Requests a database check, but returns immediately. Always returns `true`.

```bash
curl localhost:8765 -X POST -d '{"action": "guiCheckDatabase", "version": 6}'
```

#### guiPlayAudio - Play audio for current card
Plays any Audio for the current side of the current card; returns `true` if succeeded or `false` otherwise.

```bash
curl localhost:8765 -X POST -d '{"action": "guiPlayAudio", "version": 6}'
```

---

### Media Actions

#### storeMediaFile - Upload media file
Stores a file in the media folder. Can use `data` (base64), `path` (absolute path), or `url`. Prefix filename with `_` to prevent auto-deletion. `deleteExisting` can prevent overwriting.

```bash
# From base64
curl localhost:8765 -X POST -d '{"action": "storeMediaFile", "version": 6, "params": {"filename": "_hello.txt", "data": "SGVsbG8sIHdvcmxkIQ=="}}'
# From URL
curl localhost:8765 -X POST -d '{"action": "storeMediaFile", "version": 6, "params": {"filename": "image.png", "url": "https://example.com/image.png"}}'
# From absolute path
curl localhost:8765 -X POST -d '{"action": "storeMediaFile", "version": 6, "params": {"filename": "_config.txt", "path": "/path/to/file"}}'
```

#### retrieveMediaFile - Retrieve media file
Retrieves the base64-encoded contents of a specified file. Returns `false` if file doesn't exist.

```bash
curl localhost:8765 -X POST -d '{"action": "retrieveMediaFile", "version": 6, "params": {"filename": "_hello.txt"}}'
```

#### getMediaFilesNames - List media files
Gets the names of media files matching the pattern. Returns all names by default.

```bash
curl localhost:8765 -X POST -d '{"action": "getMediaFilesNames", "version": 6, "params": {"pattern": "_hell*.txt"}}'
```

#### getMediaDirPath - Get media folder path
Gets the full path to the `collection.media` folder of the currently opened profile.

```bash
curl localhost:8765 -X POST -d '{"action": "getMediaDirPath", "version": 6}'
```

#### deleteMediaFile - Delete media file
Deletes the specified file inside the media folder.

```bash
curl localhost:8765 -X POST -d '{"action": "deleteMediaFile", "version": 6, "params": {"filename": "image.png"}}'
```

---

### Miscellaneous Actions

#### requestPermission - Request API permission
Requests permission to use the API. This is the only method that accepts requests from any origin. Should be the first call made.

```bash
curl localhost:8765 -X POST -d '{"action": "requestPermission", "version": 6}'
```

#### version - Get API version
Gets the version of the API exposed by this plugin. Currently versions 1 through 6 are defined.

```bash
curl localhost:8765 -X POST -d '{"action": "version", "version": 6}'
```

#### apiReflect - Get available API actions
Gets information about the AnkiConnect APIs available. Use `scopes: ["actions"]` and optionally filter with `actions` array.

```bash
# List all available actions
curl localhost:8765 -X POST -d '{"action": "apiReflect", "version": 6, "params": {"scopes": ["actions"], "actions": null}}'
# Check specific actions
curl localhost:8765 -X POST -d '{"action": "apiReflect", "version": 6, "params": {"scopes": ["actions"], "actions": ["deckNames", "addNote"]}}'
```

#### sync - Sync with AnkiWeb
Synchronizes the local Anki collections with AnkiWeb.

```bash
curl localhost:8765 -X POST -d '{"action": "sync", "version": 6}'
```

#### getProfiles - List all profiles
Retrieve the list of profiles.

```bash
curl localhost:8765 -X POST -d '{"action": "getProfiles", "version": 6}'
```

#### getActiveProfile - Get active profile
Retrieve the active profile name.

```bash
curl localhost:8765 -X POST -d '{"action": "getActiveProfile", "version": 6}'
```

#### loadProfile - Switch profile
Selects the profile specified in request.

```bash
curl localhost:8765 -X POST -d '{"action": "loadProfile", "version": 6, "params": {"name": "user1"}}'
```

#### multi - Execute multiple actions
Performs multiple actions in one request, returning an array with the response of each action.

```bash
curl localhost:8765 -X POST -d '{"action": "multi", "version": 6, "params": {"actions": [{"action": "deckNames"}, {"action": "modelNames"}, {"action": "getTags"}]}}'
```

#### exportPackage - Export deck to .apkg
Exports a given deck in `.apkg` format. Use `includeSched` to include scheduling data.

```bash
curl localhost:8765 -X POST -d '{"action": "exportPackage", "version": 6, "params": {"deck": "Default", "path": "/data/Deck.apkg", "includeSched": true}}'
```

#### importPackage - Import .apkg file
Imports a file in `.apkg` format into the collection. Note: path is relative to Anki's collection.media folder.

```bash
curl localhost:8765 -X POST -d '{"action": "importPackage", "version": 6, "params": {"path": "/data/Deck.apkg"}}'
```

#### reloadCollection - Reload collection
Tells Anki to reload all data from the database.

```bash
curl localhost:8765 -X POST -d '{"action": "reloadCollection", "version": 6}'
```

---

### Model Actions (Note Types)

#### modelNames - List all note types
Gets the complete list of model names for the current user.

```bash
curl localhost:8765 -X POST -d '{"action": "modelNames", "version": 6}'
```

#### modelNamesAndIds - List note types with IDs
Gets the complete list of model names and their corresponding IDs.

```bash
curl localhost:8765 -X POST -d '{"action": "modelNamesAndIds", "version": 6}'
```

#### findModelsById - Find models by ID
Gets a list of models for the provided model IDs.

```bash
curl localhost:8765 -X POST -d '{"action": "findModelsById", "version": 6, "params": {"modelIds": [1704387367119, 1704387398570]}}'
```

#### findModelsByName - Find models by name
Gets a list of models for the provided model names.

```bash
curl localhost:8765 -X POST -d '{"action": "findModelsByName", "version": 6, "params": {"modelNames": ["Basic", "Basic (and reversed card)"]}}'
```

#### modelFieldNames - Get field names of a note type
Gets the complete list of field names for the provided model name.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldNames", "version": 6, "params": {"modelName": "Basic"}}'
```

#### modelFieldDescriptions - Get field descriptions
Gets the complete list of field descriptions (text seen in GUI editor when field is empty) for the provided model name.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldDescriptions", "version": 6, "params": {"modelName": "Basic"}}'
```

#### modelFieldFonts - Get field fonts
Gets the complete list of fonts along with their font sizes for the provided model name.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldFonts", "version": 6, "params": {"modelName": "Basic"}}'
```

#### modelFieldsOnTemplates - Get fields on templates
Returns an object indicating the fields on the question and answer side of each card template for the given model name.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldsOnTemplates", "version": 6, "params": {"modelName": "Basic (and reversed card)"}}'
```

#### createModel - Create a new note type
Creates a new model with the given name, fields, and card templates. Use `isCloze: true` for Cloze type. Optionally specify `css` and `Name` for templates.

```bash
curl localhost:8765 -X POST -d '{"action": "createModel", "version": 6, "params": {"modelName": "CustomModel", "inOrderFields": ["Field1", "Field2", "Field3"], "css": ".card { font-family: Arial; font-size: 20px; }", "isCloze": false, "cardTemplates": [{"Name": "Card 1", "Front": "{{Field1}}", "Back": "{{Field2}}"}]}}'
```

#### modelTemplates - Get templates of a note type
Returns an object indicating the template content for each card connected to the provided model by name.

```bash
curl localhost:8765 -X POST -d '{"action": "modelTemplates", "version": 6, "params": {"modelName": "Basic (and reversed card)"}}'
```

#### modelStyling - Get CSS styling of a note type
Gets the CSS styling for the provided model by name.

```bash
curl localhost:8765 -X POST -d '{"action": "modelStyling", "version": 6, "params": {"modelName": "Basic (and reversed card)"}}'
```

#### updateModelTemplates - Modify card templates
Modify the templates of an existing model by name. Only specified cards and sides will be modified.

```bash
curl localhost:8765 -X POST -d '{"action": "updateModelTemplates", "version": 6, "params": {"model": {"name": "Custom", "templates": {"Card 1": {"Front": "{{Question}}?", "Back": "{{Answer}}!"}}}}'
```

#### updateModelStyling - Modify CSS
Modify the CSS styling of an existing model by name.

```bash
curl localhost:8765 -X POST -d '{"action": "updateModelStyling", "version": 6, "params": {"model": {"name": "Custom", "css": "p { color: blue; }"}}}'
```

#### findAndReplaceInModels - Find and replace in templates/CSS
Find and replace string in existing model by model name. Set front/back/css to true/false to control where to replace.

```bash
curl localhost:8765 -X POST -d '{"action": "findAndReplaceInModels", "version": 6, "params": {"model": {"modelName": "Basic", "findText": "text_to_replace", "replaceText": "replace_with_text", "front": true, "back": true, "css": true}}}'
```

#### modelTemplateRename - Rename a template
Renames a template in an existing model.

```bash
curl localhost:8765 -X POST -d '{"action": "modelTemplateRename", "version": 6, "params": {"modelName": "Basic", "oldTemplateName": "Card 1", "newTemplateName": "Card 1 renamed"}}'
```

#### modelTemplateReposition - Reposition a template
Repositions a template in an existing model. Index starts at 0.

```bash
curl localhost:8765 -X POST -d '{"action": "modelTemplateReposition", "version": 6, "params": {"modelName": "Basic", "templateName": "Card 1", "index": 1}}'
```

#### modelTemplateAdd - Add a template
Adds a template to an existing model by name. Use `updateModelTemplates` to update existing templates.

```bash
curl localhost:8765 -X POST -d '{"action": "modelTemplateAdd", "version": 6, "params": {"modelName": "Basic", "template": {"Name": "Card 3", "Front": "Front html {{Field1}}", "Back": "Back html {{Field2}}"}}}'
```

#### modelTemplateRemove - Remove a template
Removes a template from an existing model.

```bash
curl localhost:8765 -X POST -d '{"action": "modelTemplateRemove", "version": 6, "params": {"modelName": "Basic", "templateName": "Card 1"}}'
```

#### modelFieldRename - Rename a field
Rename the field name of a given model.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldRename", "version": 6, "params": {"modelName": "Basic", "oldFieldName": "Front", "newFieldName": "FrontRenamed"}}'
```

#### modelFieldReposition - Reposition a field
Reposition the field within the field list of a given model. Index starts at 0.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldReposition", "version": 6, "params": {"modelName": "Basic", "fieldName": "Back", "index": 0}}'
```

#### modelFieldAdd - Add a new field
Creates a new field within a given model. Optionally specify `index` to position it.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldAdd", "version": 6, "params": {"modelName": "Basic", "fieldName": "NewField", "index": 0}}'
```

#### modelFieldRemove - Remove a field
Deletes a field within a given model.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldRemove", "version": 6, "params": {"modelName": "Basic", "fieldName": "Front"}}'
```

#### modelFieldSetFont - Set field font
Sets the font for a field within a given model.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldSetFont", "version": 6, "params": {"modelName": "Basic", "fieldName": "Front", "font": "Courier"}}'
```

#### modelFieldSetFontSize - Set field font size
Sets the font size for a field within a given model.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldSetFontSize", "version": 6, "params": {"modelName": "Basic", "fieldName": "Front", "fontSize": 10}}'
```

#### modelFieldSetDescription - Set field description
Sets the description (text seen in GUI editor when field is empty) for a field. Returns `false` on Anki 2.1.49 and below.

```bash
curl localhost:8765 -X POST -d '{"action": "modelFieldSetDescription", "version": 6, "params": {"modelName": "Basic", "fieldName": "Front", "description": "example field description"}}'
```

---

### Note Actions

#### addNote - Create a single flashcard
Creates a note using the given deck and model, with the provided fields and tags. Returns the note ID on success, `null` on failure. Supports audio, video, and picture embedding.

Options:
- `allowDuplicate`: Set `true` to allow duplicate cards
- `duplicateScope`: "deck" to check duplicates in target deck only, otherwise checks entire collection
- `duplicateScopeOptions.deckName`: Deck to check for duplicates
- `duplicateScopeOptions.checkChildren`: Check child decks too (default false)
- `duplicateScopeOptions.checkAllModels`: Check across all note types (default false)

```bash
curl localhost:8765 -X POST -d '{"action": "addNote", "version": 6, "params": {"note": {"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Question", "Back": "Answer"}, "tags": ["tag1"], "options": {"allowDuplicate": false, "duplicateScope": "deck", "duplicateScopeOptions": {"deckName": "Default", "checkChildren": false, "checkAllModels": false}}}}}'
```

With media:
```bash
curl localhost:8765 -X POST -d '{"action": "addNote", "version": 6, "params": {"note": {"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Audio example", "Back": "Answer"}, "audio": [{"url": "https://example.com/audio.mp3", "filename": "audio.mp3", "fields": ["Front"]}]}}}'
```

#### addNotes - Create multiple flashcards at once
Creates multiple notes using the given deck and model. Returns an array of note IDs. Errors are gathered and returned.

```bash
curl localhost:8765 -X POST -d '{"action": "addNotes", "version": 6, "params": {"notes": [{"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Q1", "Back": "A1"}, "tags": ["batch"]}, {"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Q2", "Back": "A2"}, "tags": ["batch"]}]}}'
```

#### canAddNotes - Check if notes can be added
Accepts an array of note definitions and returns an array of booleans indicating whether each can be created.

```bash
curl localhost:8765 -X POST -d '{"action": "canAddNotes", "version": 6, "params": {"notes": [{"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Q", "Back": "A"}, "tags": ["test"]}]}}'
```

#### canAddNotesWithErrorDetail - Check with error details
Returns array of objects with `canAdd` boolean and `error` explanation for each note.

```bash
curl localhost:8765 -X POST -d '{"action": "canAddNotesWithErrorDetail", "version": 6, "params": {"notes": [{"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Q1", "Back": "A1"}}, {"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Q2", "Back": "A2"}}]}}'
```

#### updateNoteFields - Modify note fields
Modify the fields of an existing note. Can also include audio/video/picture files. Warning: Cannot update a note while viewing it in the browser.

```bash
curl localhost:8765 -X POST -d '{"action": "updateNoteFields", "version": 6, "params": {"note": {"id": 1514547547030, "fields": {"Front": "New question", "Back": "New answer"}}}}'
```

#### updateNote - Update fields and/or tags
Modify the fields and/or tags of an existing note. Combines `updateNoteFields` and `updateNoteTags`. Fields are updated first.

```bash
curl localhost:8765 -X POST -d '{"action": "updateNote", "version": 6, "params": {"note": {"id": 1514547547030, "fields": {"Front": "New question", "Back": "New answer"}, "tags": ["new", "tags"]}}}'
```

#### updateNoteModel - Update note type
Update the model, fields, and tags of an existing note. Allows changing the note's model entirely.

```bash
curl localhost:8765 -X POST -d '{"action": "updateNoteModel", "version": 6, "params": {"note": {"id": 1514547547030, "modelName": "NewModel", "fields": {"NewField1": "content1", "NewField2": "content2"}, "tags": ["new", "tags"]}}}'
```

#### updateNoteTags - Set note tags
Set a note's tags by note ID. Old tags will be removed.

```bash
curl localhost:8765 -X POST -d '{"action": "updateNoteTags", "version": 6, "params": {"note": 1483959289817, "tags": ["european-languages"]}}'
```

#### getNoteTags - Get note's tags
Get a note's tags by note ID.

```bash
curl localhost:8765 -X POST -d '{"action": "getNoteTags", "version": 6, "params": {"note": 1483959289817}}'
```

#### addTags - Add tags to notes
Adds tags to notes by note ID.

```bash
curl localhost:8765 -X POST -d '{"action": "addTags", "version": 6, "params": {"notes": [1483959289817, 1483959291695], "tags": "european-languages"}}'
```

#### removeTags - Remove tags from notes
Remove tags from notes by note ID.

```bash
curl localhost:8765 -X POST -d '{"action": "removeTags", "version": 6, "params": {"notes": [1483959289817, 1483959291695], "tags": "european-languages"}}'
```

#### replaceTags - Replace tags in specific notes
Replace tags in notes by note ID.

```bash
curl localhost:8765 -X POST -d '{"action": "replaceTags", "version": 6, "params": {"notes": [1483959289817, 1483959291695], "tag_to_replace": "european-languages", "replace_with_tag": "french-languages"}}'
```

#### getTags - List all tags
Gets the complete list of tags for the current user.

```bash
curl localhost:8765 -X POST -d '{"action": "getTags", "version": 6}'
```

#### replaceTagsInAllNotes - Replace tags globally
Replace tags in all the notes for the current user.

```bash
curl localhost:8765 -X POST -d '{"action": "replaceTagsInAllNotes", "version": 6, "params": {"tag_to_replace": "old", "replace_with_tag": "new"}}'
```

#### clearUnusedTags - Clear unused tags
Clears all the unused tags in the notes for the current user.

```bash
curl localhost:8765 -X POST -d '{"action": "clearUnusedTags", "version": 6}'
```

#### findNotes - Find notes by query
Returns an array of note IDs for a given query. Query syntax: https://docs.ankiweb.net/searching.html

```bash
curl localhost:8765 -X POST -d '{"action": "findNotes", "version": 6, "params": {"query": "deck:Default tag:important"}}'
```

#### notesInfo - Get detailed note info
Returns a list of objects containing for each note ID: fields, tags, note type, modification time, cards, and profile.

```bash
# By note IDs
curl localhost:8765 -X POST -d '{"action": "notesInfo", "version": 6, "params": {"notes": [1502298033753]}}'
# By query
curl localhost:8765 -X POST -d '{"action": "notesInfo", "version": 6, "params": {"query": "deck:current"}}'
```

#### notesModTime - Get note modification times
Returns a list of objects containing for each note ID the modification time.

```bash
curl localhost:8765 -X POST -d '{"action": "notesModTime", "version": 6, "params": {"notes": [1502298033753]}}'
```

#### deleteNotes - Delete notes
Deletes notes with the given IDs. If a note has several cards, all associated cards will be deleted.

```bash
curl localhost:8765 -X POST -d '{"action": "deleteNotes", "version": 6, "params": {"notes": [1502298033753]}}'
```

#### removeEmptyNotes - Remove empty notes
Removes all the empty notes for the current user.

```bash
curl localhost:8765 -X POST -d '{"action": "removeEmptyNotes", "version": 6}'
```

---

### Statistic Actions

#### getNumCardsReviewedToday - Get cards reviewed today
Gets the count of cards reviewed in the current day (with day start time as configured by user).

```bash
curl localhost:8765 -X POST -d '{"action": "getNumCardsReviewedToday", "version": 6}'
```

#### getNumCardsReviewedByDay - Get cards reviewed by day
Gets the number of cards reviewed as a list of pairs (dateString, number).

```bash
curl localhost:8765 -X POST -d '{"action": "getNumCardsReviewedByDay", "version": 6}'
```

#### getCollectionStatsHTML - Get collection statistics
Gets the collection statistics report as HTML.

```bash
curl localhost:8765 -X POST -d '{"action": "getCollectionStatsHTML", "version": 6, "params": {"wholeCollection": true}}'
```

#### cardReviews - Get card review history
Requests all card reviews for a specified deck after a certain time. Returns list of 9-tuples (reviewTime, cardID, usn, buttonPressed, newInterval, previousInterval, newFactor, reviewDuration, reviewType).

```bash
curl localhost:8765 -X POST -d '{"action": "cardReviews", "version": 6, "params": {"deck": "default", "startID": 1594194095740}}'
```

#### getReviewsOfCards - Get reviews of specific cards
Requests all card reviews for each card ID. Returns dictionary mapping card ID to list of review dictionaries.

```bash
curl localhost:8765 -X POST -d '{"action": "getReviewsOfCards", "version": 6, "params": {"cards": ["1653613948202"]}}'
```

#### getLatestReviewID - Get latest review time
Returns the unix time of the latest review for the given deck. Returns 0 if no review has ever been made.

```bash
curl localhost:8765 -X POST -d '{"action": "getLatestReviewID", "version": 6, "params": {"deck": "default"}}'
```

#### insertReviews - Insert review records
Inserts the given reviews into the database. Required format: list of 9-tuples (reviewTime, cardID, usn, buttonPressed, newInterval, previousInterval, newFactor, reviewDuration, reviewType).

```bash
curl localhost:8765 -X POST -d '{"action": "insertReviews", "version": 6, "params": {"reviews": [[1594194095746, 1485369733217, -1, 3, 4, -60, 2500, 6157, 0], [1594201393292, 1485369902086, -1, 1, -60, -60, 0, 4846, 0]]}}'
```

---

## Common Search Queries

Anki uses a powerful search syntax. Examples:

- `deck:MyDeck` - Cards in MyDeck
- `deck:MyDeck::SubDeck` - Cards in subdeck
- `tag:important` - Cards with tag
- `is:new` - New cards
- `is:due` - Due cards
- `is:suspended` - Suspended cards
- `"word"` - Cards containing "word"
- `"word" AND "other"` - Cards with both
- `added:1` - Added today
- `rated:1:3` - Rated "Good" today
- `prop:ivl>30` - Cards with interval > 30 days
- `deck:MyDeck tag:important is:due` - Combined search

## Usage Examples

### Create a deck
```bash
curl localhost:8765 -X POST -d '{"action": "createDeck", "version": 6, "params": {"deck": "Spanish::Verbs"}}'
```

### Check if a question exists
```bash
curl localhost:8765 -X POST -d '{"action": "findNotes", "version": 6, "params": {"query": "\"What is photosynthesis\""}}'
```

### List all tags
```bash
curl localhost:8765 -X POST -d '{"action": "getTags", "version": 6}'
```

### Create multiple cards from a list
```bash
curl localhost:8765 -X POST -d '{"action": "addNotes", "version": 6, "params": {"notes": [{"deckName": "Study", "modelName": "Basic", "fields": {"Front": "Hello", "Back": "Hola"}, "tags": ["spanish"]}, {"deckName": "Study", "modelName": "Basic", "fields": {"Front": "Goodbye", "Back": "Adiós"}, "tags": ["spanish"]}, {"deckName": "Study", "modelName": "Basic", "fields": {"Front": "Please", "Back": "Por favor"}, "tags": ["spanish"]}]}}'
```

### Update a card
```bash
curl localhost:8765 -X POST -d '{"action": "updateNoteFields", "version": 6, "params": {"note": {"id": NOTE_ID, "fields": {"Front": "new question", "Back": "new answer"}}}}'
```

### Create a custom Cloze note type
```bash
curl localhost:8765 -X POST -d '{"action": "createModel", "version": 6, "params": {"modelName": "ClozeText", "inOrderFields": ["Text", "Extra"], "isCloze": true, "cardTemplates": [{"Name": "Cloze", "Front": "{{cloze:Text}}", "Back": "{{cloze:Text}}\n\n{{Extra}}"}]}}'
```

### Suspend cards
```bash
curl localhost:8765 -X POST -d '{"action": "suspend", "version": 6, "params": {"cards": [1498938915662]}}'
```

### Export a deck
```bash
curl localhost:8765 -X POST -d '{"action": "exportPackage", "version": 6, "params": {"deck": "MyDeck", "path": "/tmp/MyDeck.apkg", "includeSched": true}}'
```

### Get deck statistics
```bash
curl localhost:8765 -X POST -d '{"action": "getDeckStats", "version": 6, "params": {"decks": ["MyDeck"]}}'
```

## Important Notes

1. **Always use curl**: Never write Python, JavaScript, or any other code. All operations must be done via curl commands.

2. **Anki must be running**: The user must have Anki open with the Anki-Connect add-on installed.

3. **Nested decks**: Use `::` separator (e.g., "Japanese::JLPT::N3")

4. **Duplicate prevention**: By default, duplicates are not allowed. Use `allowDuplicate: true` in options to allow duplicates.

5. **Cloze syntax**: For cloze cards, use `{{c1::text}}`, `{{c2::text}}` in the Text field.

6. **Card templates**: The `qfmt` (question format) and `afmt` (answer format) use `{{FieldName}}` syntax.

7. **Media filenames starting with `_`**: These files are not automatically deleted by Anki (useful for config files).

8. **Authentication**: If API key is required, add `"key": "your-api-key"` to the request body.

9. **GUI operations**: Some actions like `guiBrowse`, `guiEditNote` require Anki's GUI to be active and may not work in headless environments.

10. **Updating notes**: You must not be viewing the note that you are updating in Anki's browser, otherwise the fields will not update.

## Troubleshooting

- **Connection refused**: Anki is not running or Anki-Connect is not installed
- **Permission denied**: Check if API key is required in Anki-Connect config
- **Model not found**: Verify the model name exactly matches (case-sensitive)
- **Deck not found**: The deck must exist before adding cards to it
- **Note update failed**: The note may be open in Anki's browser - close it first
