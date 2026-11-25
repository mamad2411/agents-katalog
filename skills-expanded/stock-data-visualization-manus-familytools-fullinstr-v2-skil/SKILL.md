---
name: stock-data-visualization-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for stock-data-visualization using latest full-instruction v2 family injection.
allowed-tools:
  - asset_path_check
  - browser_render_screenshot
  - copy_tree
  - d3_v6_vendor
  - dom_svg_inspect
  - list_dir
  - read_file
  - read_table
  - run_python
  - run_shell
  - stock_data_prepare
  - web_app_scaffold
  - write_file
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: Stock Data Visualization

## 1. When to use this skill
Use this skill when the task requires creating a single-page web application that visualizes stock data using D3.js (v6). The task typically involves reading stock descriptions and individual stock price histories, and rendering them into interactive charts alongside a data table. The final output is expected to be an `index.html` file supported by CSS, JS, and data files in a specific directory structure.

## 2. Visible input and artifact inventory
The input data consists of stock descriptions and individual stock data located in the `/root/data/` directory. The expected output artifacts include the main HTML file at `/root/output/index.html`, the D3 library at `/root/output/js/d3.v6.min.js`, the visualization logic at `/root/output/js/visualization.js`, the styling at `/root/output/css/style.css`, and the copied data in the `/root/output/data/` directory.

## 3. Execution procedure for the current task
First, read the visible instruction and verify the existence of input data files using the appropriate tools. Next, prepare the data by copying the required files from the input directory to the output data directory. Then, scaffold the web application to create the basic directory structure and empty files for HTML, CSS, and JS. After that, set up the D3.js library by placing it at the correct path. Proceed to implement the HTML structure, CSS styling, and D3.js logic to load the data, render the bubble chart, and render the data table. Finally, verify that all asset paths in the HTML and JS files are relative and correctly point to the copied data and scripts.

## 4. Family tool routing and useful placeholder snippets
Use the data preparation tools to duplicate the dataset into the output directory. The web app scaffold tool is useful for quickly setting up the output structure. The D3 v6 vendor tool is essential for providing the exact D3 version required. Use the DOM SVG inspect tool to verify that the generated SVG elements match the requirements. The asset path check tool helps confirm that all linked assets resolve correctly. Finally, the browser render screenshot tool can be used to visually inspect the final web app layout and rendering.

## 5. Validation checks before final submission
Verify that the main HTML file exists and loads without errors. Check that the D3 library, visualization logic, and styling files exist. Ensure the data directory contains the necessary files. Confirm that all SVG circle elements correspond to stock bubbles and no decorative circles are present. Verify that the legend is implemented as a div element, not within the SVG. Ensure tooltips and cross-highlighting functionality are implemented in the JS code.

## 6. Common failure modes and repair actions
If the chart fails to render, check if the D3 library is correctly placed and linked. If data fails to load, ensure paths in the visualization logic point to the output data directory and not the original data directory. If decorative circles are found, modify the visualization logic to remove them or use different SVG elements for non-data visual components. If the legend is inside the SVG, refactor the code to render it as HTML div elements.

## 7. Finalizer capsule
If the task is nearing the maximum step limit and the full interactive visualization is not complete, ensure the minimum required artifacts are present. Create the directory structure, place the HTML, CSS, and JS files, ensure the D3 library is vendored, and copy the data to the output data directory. This ensures the output shape matches the instruction, even if the visual rendering is imperfect.
