---
name: chart_guide
display_name: Chart Guide
icon: "📈"
description: Guidance for data visualisation and chart creation.
tools:
  - chart
tags: []
---
DATA VISUALISATION:
- When you analyse tabular data (CSV, Excel, JSON) and the results would be
  clearer as a chart, use the create_chart tool to render an interactive
  Plotly chart inline.  Supported types: bar, horizontal_bar, line, scatter,
  pie, donut, histogram, box, area, heatmap.
- Common triggers: user asks to 'plot', 'chart', 'graph', 'visualise', or
  when comparing categories, showing trends over time, or displaying
  distributions.  You may also proactively suggest a chart when it adds value.
- data_source accepts: inline CSV/TSV data, a file path, or an attachment
  filename.  For small tables you can paste the data directly.
  The tool auto-unpivots wide-format data when needed.
- To save the chart as a PNG image (for sending via Telegram or email),
  set save_to_file='filename.png'.  The returned message includes the
  absolute file path you can pass to send_telegram_photo or email attachments.
- Chart + send: create_chart with save_to_file='chart.png', then
  send_telegram_photo or attach it to email.
