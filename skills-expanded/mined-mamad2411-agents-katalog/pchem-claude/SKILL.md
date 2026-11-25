# PChem - Chemistry and FYS Educational Tools

## Project Overview

A Streamlit-based web application providing interactive chemistry education tools for physical chemistry courses. The application includes 25+ tools spanning thermodynamics, kinetics, quantum chemistry, electrochemistry, AI/ML demonstrations, and data analysis utilities.

## Architecture

### Current Structure (Legacy)
```
pchem/
├── apps/                    # Streamlit application modules
│   ├── pchemapp.py         # Main entry point (dispatcher)
│   ├── util.py             # Shared utilities
│   ├── base.py             # Chemistry utilities (electron configs, etc.)
│   └── [app modules].py    # Individual app modules with run() functions
├── pchem/                   # Python package
│   ├── __init__.py
│   └── calorimetry.py      # Calorimetry calculations
├── tests/                   # pytest tests
├── requirements.txt         # Dependencies
└── setup.py                # Package setup
```

### App Categories

**Educational/Visualization Tools:**
- Thermodynamics: 1st Law, 2nd Law Calorimeter, Mystery Gas
- Kinetics: CHE 120 Kinetics (Arrhenius), Ocean Optics Kinetics
- Quantum: Variational Gaussian, Linear Variational, Zeff, Electron Visualization
- General: Periodic Table, Compressibility Factor, Equilibrium

**Data Analysis Tools:**
- UV-Vis, Raman, and CSV data combination
- Excel/Solartron data plotting
- Electrochemistry peak picking
- Impedance analysis
- Fuel cell analysis

**AI/ML Demonstrations:**
- GPT-4o-mini Image Classifier/Regression
- GPT-3 vs ChatGPT comparison
- Neural Network Game
- MIR Puzzle

## Development

### Running Locally
```bash
streamlit run apps/pchemapp.py
```

### Running Tests
```bash
pytest tests/
```

### Dependencies
Key dependencies (see requirements.txt):
- streamlit - Web framework
- numpy, scipy, pandas - Numerical computing
- matplotlib, plotly - Visualization
- sympy - Symbolic mathematics
- openai - AI integrations
- CoolProp - Thermodynamic properties

## App Module Contract

Each app module must implement a `run()` function:
```python
# apps/myapp.py
import streamlit as st

def run():
    st.header("My App Title")
    # App implementation here
```

## Deployment

### Heroku
Uses `Procfile` and `setup.sh` for configuration.

### Production (Nginx + Multiple Instances)
- 8 parallel Streamlit processes (ports 8500-8507)
- Nginx load balancer
- WebSocket support for Streamlit

## Code Style

- Follow PEP 8
- Use type hints where practical
- Keep app modules self-contained
- Share common utilities via util.py and base.py

## Testing

Tests are in `tests/` directory. Run with:
```bash
pytest tests/ -v
```

CI/CD via GitHub Actions runs tests on every push.

## BioTek ABTS page (`/biotek-abts`)

`pchemapps/biotek_to_excel.py` (Gen5 parser) and `pchemapps/biotek_to_excel_v2.py`
(combiner) are **mirrors of the canonical copies in
`~/Dropbox/dwyer-research/2605/`**; the only edit is the package import in v2.
Fix bugs there first, then re-copy. `pchemapps/biotek_abts.py` is the Streamlit
front end (upload .txt files, editable plate map, Excel download, plotly
charts). Tests: `tests/test_biotek_to_excel*.py`. Headless check: monkeypatch
`st.file_uploader` in a wrapper script and drive it with
`streamlit.testing.v1.AppTest` (page_link fails outside `st.navigation`).

## Modernization

This project is undergoing modernization to use Streamlit's multi-page architecture. See `MODERNIZATION_PLAN.md` for the full plan.

### Key Changes
- **Separate URLs**: Each app will have its own URL (e.g., `/kinetics`, `/impedance`)
- **Sidebar Navigation**: Apps organized into categories in the sidebar
- **Modern APIs**: Upgrade from `@st.cache` to `@st.cache_data`/`@st.cache_resource`
- **Updated Dependencies**: Streamlit 1.53+, OpenAI 1.0+, etc.

### New App Module Pattern (Post-Modernization)
```python
# pages/kinetics/arrhenius.py
import streamlit as st

st.header("CHE 120 Kinetics")
# Implementation as top-level code (no run() wrapper)
```

## Common Pitfalls

1. **OpenAI API**: The v1.0+ API is completely different from v0.x
   ```python
   # OLD
   import openai
   openai.ChatCompletion.create(...)

   # NEW
   from openai import OpenAI
   client = OpenAI()
   client.chat.completions.create(...)
   ```

2. **Streamlit Caching**: Use `@st.cache_data` for data, `@st.cache_resource` for connections/models

3. **Session State**: Use `st.session_state` instead of internal APIs
