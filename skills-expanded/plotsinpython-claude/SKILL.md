# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose
This is a Python plotting tutorial repository containing comprehensive documentation about data visualization in Python using Matplotlib and Seaborn. The main content is in Japanese and serves as an educational resource.

## Project Structure
- `README.md` - Main tutorial document with complete Python plotting examples
- Tutorial covers 8 major plot types with multiple variations each
- All code examples are embedded in the markdown documentation

## Python Dependencies
The tutorial requires these libraries:
```bash
pip install matplotlib seaborn pandas numpy
```

For 3D plotting examples:
```python
from mpl_toolkits.mplot3d import Axes3D
```

## Common Development Tasks

### Adding New Plot Examples
When adding new visualization examples to the tutorial:
1. Include complete, runnable code snippets
2. Add Japanese explanations for consistency
3. Follow the existing format: データの準備 → グラフの作成
4. Include appropriate figure sizes using `plt.figure(figsize=(width, height))`

### Testing Code Examples
Since this is a documentation repository without executable Python files, test examples by:
1. Copying code blocks from README.md
2. Running in a Python environment or Jupyter notebook
3. Verifying all imports and dependencies work correctly

## Code Style Guidelines
- Use Japanese comments and labels in plots for consistency
- Set random seeds (`np.random.seed(42)`) for reproducible examples
- Include grid lines with `plt.grid(True, alpha=0.3)` for readability
- Always add axis labels, titles, and legends where appropriate

## Repository Maintenance
- Keep all examples self-contained and runnable independently
- Maintain the tutorial's educational progression from basic to advanced topics
- Ensure code examples work with current library versions