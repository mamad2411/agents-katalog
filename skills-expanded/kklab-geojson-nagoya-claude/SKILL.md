# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an interactive map application displaying the 16 wards of Nagoya City, Japan. It uses Leaflet.js to render GeoJSON boundary data for each ward, with interactive features like hover effects and click-to-zoom.

## Common Development Commands

### Running the Application
```bash
# Using Python's built-in server
python -m http.server 8000

# Using Node.js serve
npx serve

# Access at http://localhost:8000
```

### Building GeoJSON Data
If you need to regenerate the ward data:
```bash
# Download individual ward GeoJSON files (codes 23101-23116)
for code in 23101 23102 23103 23104 23105 23106 23107 23108 23109 23110 23111 23112 23113 23114 23115 23116; do
  curl -L -o "${code}.json" "https://raw.githubusercontent.com/niiyz/JapanCityGeoJson/master/geojson/23/${code}.json"
done

# Merge into single file
node merge_geojson.js
```

## Architecture

### Data Flow
1. `nagoya_wards.geojson` contains merged GeoJSON data for all 16 wards
2. `app.js` fetches this data and renders it using Leaflet
3. Ward properties include both `ward` (区名) and `code` (行政コード)

### Key Components

**app.js**
- `wardColors`: Maps ward names to specific colors for visual distinction
- `style()`: Applies colors based on ward name from properties
- `highlightFeature()` / `resetHighlight()`: Handles interactive hover effects
- `updateInfo()`: Updates the info panel with ward details
- `onEachFeature()`: Binds events and popups to each ward polygon

### GeoJSON Structure
The data uses properties from Japan's N03 dataset:
- `N03_004`: Ward name (original property)
- `ward`: Added property with ward name
- `code`: Administrative code (23101-23116)

## Ward Codes Reference
- 23101: 千種区 (Chikusa-ku)
- 23102: 東区 (Higashi-ku)
- 23103: 北区 (Kita-ku)
- 23104: 西区 (Nishi-ku)
- 23105: 中村区 (Nakamura-ku)
- 23106: 中区 (Naka-ku)
- 23107: 昭和区 (Showa-ku)
- 23108: 瑞穂区 (Mizuho-ku)
- 23109: 熱田区 (Atsuta-ku)
- 23110: 中川区 (Nakagawa-ku)
- 23111: 港区 (Minato-ku)
- 23112: 南区 (Minami-ku)
- 23113: 守山区 (Moriyama-ku)
- 23114: 緑区 (Midori-ku)
- 23115: 名東区 (Meito-ku)
- 23116: 天白区 (Tempaku-ku)