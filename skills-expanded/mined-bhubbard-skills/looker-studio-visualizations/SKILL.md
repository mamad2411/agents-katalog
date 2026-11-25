---
name: looker-studio-visualizations
description: "Guidelines for developing custom Looker Studio Community Visualizations using JavaScript, CSS, and the dscc library."
---

# Looker Studio Community Visualizations

Looker Studio provides the ability to build **Community Visualizations**, allowing developers to create custom charts (like D3.js graphics, custom gauges, or complex tables) using standard web technologies.

## Architecture

A Community Visualization consists of three main parts:
1.  **JavaScript/CSS:** The actual rendering code.
2.  **Manifest (`manifest.json`):** Describes the visualization, its name, and its capabilities.
3.  **Config (`config.json`):** Defines the Looker Studio property panel (the inputs for Dimensions, Metrics, and styling options).

## The `dscc` Library

To bridge the gap between Looker Studio and your custom JavaScript, you must use the Data Studio Community Component (`dscc`) library.

### Subscribing to Data

The core of a visualization is subscribing to updates. Looker Studio pushes data to your code whenever the report filters change, the user alters the style panel, or the data refreshes.

```javascript
const dscc = require('@google/dscc');

// Function that renders the visualization
function drawViz(data) {
  // data.tables.DEFAULT contains the rows of data
  // data.style contains the user's styling choices
  console.log(data);
  
  // Render your D3/Canvas/HTML here...
}

// Subscribe to data and style changes
dscc.subscribeToData(drawViz, {transform: dscc.objectTransform});
```

## Local Development
*   Use the `dscc-gen` utility to scaffold new visualization projects.
*   Host your JS and CSS in a Google Cloud Storage bucket and point your `manifest.json` `devMode` or `prodMode` URLs to that bucket for rendering within Looker Studio.
