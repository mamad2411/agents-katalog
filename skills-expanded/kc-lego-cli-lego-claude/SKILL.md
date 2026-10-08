# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the KC LEGO Management System - a bash-based application for managing personal LEGO collections, including sets and parts tracking, lookup functionality, and collection management tools.

## Architecture

### Core Components

- **Main Launcher**: `Lego-Managment.sh` - Central entry point with MIT license agreement and menu system
- **Personal Collection Management**: 
  - `Lego-Magement-Screen/Personal-Collection/kc-sets/main.sh` (Python3 script)
  - `Lego-Magement-Screen/Personal-Collection/kc-parts/main.sh` (Python3 script)
- **LEGO Lookup Tools**: 
  - `Lego-Lookup/lookup-set.sh` (Bash script using jq)
  - `Lego-Lookup/lookup-part.sh` (Bash script using jq)
- **Non-Personal Collection**:
  - `Lego-Magement-Screen/Non-Retired-Lego-Sets/main.sh`
  - `Lego-Magement-Screen/Retried-and-retiring-Lego-Sets/main.sh`

### Data Files

- **JSON Databases**: 
  - `Lego-Lookup/legolookup.json` - LEGO set reference data (3.6MB)
  - `Lego-Lookup/legolookup-part.json` - LEGO part reference data (9MB)
  - `0.json` and `kc_sets_export_20250718_222338.json` - User collection data
- **License Cache**: `.lego_manager_license_agreed` - Tracks license acceptance

### System Design

The system uses a hierarchical menu structure:
1. **License Agreement** - Required on first run
2. **System Launcher** - Choose between Management System or Lookup
3. **Management System** - Personal/Non-Personal collection management
4. **Lookup System** - Set and Part lookup functionality

## Development Commands

This project uses **bash scripts** and **Python 3** - no build system, package managers, or test frameworks are configured.

### Running the Application
```bash
# Main entry point
./Lego-Managment.sh

# Individual components
./Lego-Lookup/lookup-set.sh
./Lego-Lookup/lookup-part.sh
```

### Dependencies
- **bash** - Main scripting environment
- **python3** - For collection management scripts
- **jq** - JSON processing for lookup functionality
- Standard Unix utilities: `tput`, `xargs`, etc.

## Key Data Structures

### LEGO Themes
The system includes comprehensive theme categorization with nested subcategories:
- Main themes: Star Wars, Harry Potter, Ninjago, etc.
- Sub-themes: Star Wars Episode divisions, Harry Potter book-based groupings
- Theme data is embedded in both notes and Python scripts

### Part Categories
Organized into logical sections:
- General, Animals, Minifigures & Dolls
- Bricks & Plates, Technic, Vehicles & Aircraft
- Color categorization includes Solid, Transparent, Chrome, Pearl, Satin, Metallic, etc.

### Collection Data Format
```json
{
  "set_id": "71788",
  "set_name": "Lloyd's Ninja Street Bike", 
  "set_theme": "Ninjago Core",
  "set_year": "2023",
  "instruction_book_number": "6449669",
  "parts_qty": 56,
  "part_out": false,
  "created_at": "2025-07-09T07:23:32.365745"
}
```

## Development Notes

- The main launcher includes extensive license agreement handling
- Scripts use `center()` function for consistent terminal output formatting
- User management system includes role-based access and password reset functionality
- Search functionality supports pagination with refresh capabilities
- Interactive theme/category selection is planned for future enhancement
- Mixed technology stack: Bash for UI/navigation, Python for data management