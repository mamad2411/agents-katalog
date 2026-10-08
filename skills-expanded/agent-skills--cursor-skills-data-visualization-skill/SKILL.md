# Data Visualization

## Library Selection
| Use Case | Library |
|----------|---------|
| Quick static plots | matplotlib |
| Statistical plots | seaborn |
| Interactive plots | plotly |
| Scientific plots | matplotlib + custom |
| Dashboards | plotly dash / streamlit |
| 3D plots | matplotlib / plotly |

## matplotlib Quick Start
```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Sine Wave')
ax.legend()
plt.tight_layout()
plt.savefig('plot.png', dpi=150)
```

## seaborn for Statistical Plots
```python
import seaborn as sns
import pandas as pd

df = pd.read_csv('data.csv')
sns.boxplot(data=df, x='group', y='value')
plt.savefig('boxplot.png')
```

## plotly for Interactive
```python
import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(x=[1,2,3], y=[4,5,6], mode='markers'))
fig.write_html('interactive.html')
```

## Best Practices
- Choose the right chart type for the data
- Label axes and include units
- Use color intentionally (not just for decoration)
- Avoid chart junk: 3D effects, excessive gridlines
- Ensure accessibility: color-blind friendly palettes
- Save at 150+ DPI for print quality
