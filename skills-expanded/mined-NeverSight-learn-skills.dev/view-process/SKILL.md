---
name: view-process
description: Launch a visual viewer for BPMN, DMN, or Form files in the browser.
argument-hint: "[.bpmn, .dmn, or .form file]"
---

Launch the Camunda file viewer to visually inspect a BPMN process, DMN decision table, or Camunda Form.

$ARGUMENTS

Auto-detects file type from extension (.bpmn, .dmn, .form) and loads the right viewer (bpmn-js, dmn-js, or form-js).

Start it with: node tools/camunda-viewer/serve.js <file>
