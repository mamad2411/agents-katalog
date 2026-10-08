---
name: "map-editor"
description: "Provides knowledge and functionality for Sango Infinity map editor, including BaseMap editing, brush tools, auto-save, and undo/redo features. Invoke when working with map editor features or troubleshooting related issues."
---

# Map Editor Skill

## Overview

This skill provides comprehensive knowledge and functionality for the Sango Infinity map editor, including BaseMap editing, brush tools, auto-save, and undo/redo features.

## Core Features

### 1. BaseMap Editing
- **BaseMap Brush**: Paint on the base map with customizable colors and brush sizes
- **BaseMap Eraser**: Erase content from the base map
- **Color Picker**: Select colors for painting
- **Alt Key Color Sampling**: Sample colors from the scene by holding Alt
- **Blend Modes**: Support for normal and multiply blend modes
- **Pressure Sensitivity**: Support for tablet pressure sensitivity via Unity's Touch API

### 2. Brush System
- **Terrain Brush**: Edit terrain height, texture, and water level
- **Grid Brush**: Edit grid properties like terrain type, area, interior, defense, and thief
- **Model Brush**: Place and edit 3D models
- **Brush Size Adjustment**: Adjustable brush size (15-150)
- **Brush Opacity**: Adjustable brush opacity (0-1)
- **Drag Continuous Editing**: Support for continuous painting while dragging

### 3. Auto-Save System
- **Quick Save**: Ctrl+S to quickly save the map
- **Auto-Save**: Automatic saving every 5 minutes (configurable)
- **Auto-Save Limit**: Maximum 20 auto-save files, older files are automatically deleted
- **Auto-Save Naming**: Files named with `_auto_save_` suffix and timestamp
- **BaseMap Synchronization**: Automatically saves base map textures when saving the map

### 4. Undo/Redo System
- **Undo**: Ctrl+Z to undo actions
- **Redo**: Ctrl+Y to redo actions
- **Command Types**: Support for terrain, grid, model, and BaseMap edit commands
- **Command Destruction**: Automatic cleanup of command resources when commands are discarded
- **Model Transform Support**: Undo/redo for model move, rotate, and scale operations

### 5. UI Features
- **Toolbar Organization**: Well-organized toolbar with clear sections
- **Season Control**: Switch between spring, summer, autumn, and winter seasons
- **View Control**: Toggle between fixed and free camera views
- **Camera Reset**: Quick camera reset functionality
- **Save Notifications**: Visual notifications for save operations
- **Shortcut Hints**: Display of keyboard shortcuts in the toolbar

## Technical Implementation

### File Structure
- `MapEditor.cs`: Main map editor class
- `Brush/TerrainBrush.cs`: Terrain editing brush
- `Brush/GridBrush.cs`: Grid editing brush
- `Brush/ModelBrush.cs`: Model editing brush
- `UndoRedo/`: Undo/redo system
  - `IUndoableCommand.cs`: Command interface
  - `ModelEditCommand.cs`: Model editing commands
  - `TerrainEditCommand.cs`: Terrain editing commands
  - `GridEditCommand.cs`: Grid editing commands
  - `BaseMapEditCommand.cs`: BaseMap editing commands
  - `UndoRedoManager.cs`: Undo/redo manager
- `Shader/brush.shader`: Brush shader with blend modes and pressure support

### Key Methods
- **AutoSave()**: Automatic save functionality with file management
- **QuickSave()**: Quick save functionality
- **SaveBaseMap()**: Save base map textures to specified location
- **RespondToMessage()**: Handle Gizmo transform messages for undo/redo
- **ApplyTexture()**: Apply texture changes to base map
- **Destroy()**: Clean up command resources

### Configuration
- **Auto-Save Interval**: 1-60 minutes (default: 5)
- **Auto-Save Limit**: 1-20 files (default: 20)
- **Brush Size**: 15-150
- **Brush Opacity**: 0-1

## Usage Examples

### BaseMap Editing
1. Select "BaseMap Brush" in terrain edit mode
2. Adjust brush size and opacity
3. Select color using color picker or Alt key sampling
4. Paint on the scene to edit the base map
5. Use Ctrl+Z to undo mistakes

### Model Editing
1. Select "模型放置" mode
2. Place models on the map
3. Select models and use W (move), E (rotate), R (scale) to transform
4. Use Ctrl+Z to undo transformations

### Auto-Save Configuration
1. Open "设置说明" tab
2. Adjust auto-save interval and limit
3. Enable/disable auto-save as needed

## Troubleshooting

### Common Issues
- **Auto-save not working**: Check if auto-save is enabled in settings
- **Undo/redo not working**: Ensure the action is supported by the undo system
- **BaseMap not saving**: Verify the save path and permissions
- **Brush not working**: Check brush settings and ensure the correct edit mode is selected

### Error Messages
- **"Color is an ambiguous reference"**: Ensure UnityEngine.Color is used instead of System.Drawing.Color
- **"MessageListenerDatabase does not contain a definition"**: Check RTEditor API usage
- **"Object does not contain a definition for Destroy"**: Use UnityEngine.Object.Destroy

## Best Practices
- **Regular Saving**: Use Ctrl+S frequently to save your work
- **Auto-Save Configuration**: Adjust auto-save interval based on project size
- **Brush Settings**: Experiment with different brush sizes and opacities for best results
- **Undo/Redo**: Use undo/redo to experiment with different changes
- **File Management**: Keep auto-save limit reasonable to avoid disk space issues

This skill provides a comprehensive guide to the Sango Infinity map editor, covering all major features and functionality to help users create and edit maps efficiently.