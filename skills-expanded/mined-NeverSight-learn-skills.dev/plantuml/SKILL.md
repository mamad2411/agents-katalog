---
name: plantuml
description: 'This skill should be used when the user invokes "/plantuml" to create a diagram from the current context using PlantUML and output the resulting image path.'
tools: Bash
disable-model-invocation: true
---

# Create diagrams with PlantUML

Create a diagram from the most recent interaction context using PlantUML. Generate a PNG image with a transparent background and output it as a markdown image so it renders inline.

## How to create a diagram

1. Extract or derive diagrammable data from the current context.
2. If the Emacs foreground color is not already known from a previous diagram in this session, query it:
   ```sh
   emacsclient --eval '
   (face-foreground (quote default))'
   ```
   This returns a hex color like `"#eeffff"`. Reuse it for all subsequent diagrams.
3. Write a PlantUML file to a temporary file using that color.
4. Run PlantUML on the file.
5. Output the result as a markdown image on its own line:
   ```
   ![description](/tmp/agent-diagram-XXXX.png)
   ```

```sh
plantuml -tpng /tmp/agent-diagram-XXXX.puml
```

## PlantUML template

```plantuml
@startuml
skinparam backgroundColor transparent
skinparam shadowing true
skinparam roundcorner 10
skinparam defaultFontName "Helvetica"
skinparam defaultFontColor #eeffff

' Set foreground color on all element types
skinparam titleFontColor #eeffff
skinparam sequenceLifeLineBorderColor #eeffff
skinparam sequenceArrowColor #eeffff
skinparam sequenceGroupHeaderFontColor #eeffff
skinparam sequenceGroupBorderColor #eeffff
skinparam sequenceDividerFontColor #eeffff
skinparam sequenceDividerBorderColor #eeffff
skinparam actorBorderColor #eeffff
skinparam actorFontColor #eeffff
skinparam participantFontColor #eeffff
skinparam participantBorderColor #eeffff
skinparam collectionsFontColor #eeffff
skinparam collectionsBorderColor #eeffff
skinparam noteFontColor #eeffff
skinparam noteBorderColor #eeffff
skinparam arrowFontColor #eeffff
skinparam classFontColor #eeffff
skinparam classBorderColor #eeffff
skinparam classAttributeFontColor #eeffff
skinparam packageFontColor #eeffff
skinparam packageBorderColor #eeffff
skinparam componentFontColor #eeffff
skinparam componentBorderColor #eeffff
skinparam interfaceFontColor #eeffff
skinparam interfaceBorderColor #eeffff

' ... diagram content ...
@enduml
```

## Rules

- Query the Emacs foreground color once per session and reuse it for all subsequent diagrams. Only query again if the color is not already known.
- Always use `skinparam backgroundColor transparent` for transparent background.
- Always use a timestamp in the filename (e.g., `/tmp/agent-diagram-$(date +%s).png`). Never use descriptive names.
- Set the queried foreground color on `defaultFontColor` and all relevant `skinparam` entries for borders, arrows, and text so the diagram is readable on the user's Emacs background.
- After PlantUML runs successfully, output a markdown image (`![description](path)`) on its own line.
- Choose an appropriate diagram type for the data (sequence, class, component, activity, state, etc.).
- Include a title when it adds clarity.
- If no diagrammable data exists in the recent context, inform the user.
