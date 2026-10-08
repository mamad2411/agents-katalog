# GLM Dashboard Explainer

An interactive pedagogical tool for teaching Generalised Linear Models (GLMs).

## Project Vision

Build a guided, step-by-step interactive dashboard that helps learners understand:
1. How different data types require different model families
2. The role of link functions in connecting linear predictors to response constraints
3. How maximum likelihood estimation "tunes" model parameters
4. The distinction between systematic (β) and random (α) components

## Core Pedagogical Framework

The GLM is presented as a data flow:

```
[X₁] ─h₁()→ ┐
[X₂] ─h₂()→ ├─→ [η = Xβ] ─g⁻¹()→ [μ] ─f(·;μ,α)→ [Y]
[X₃] ─h₃()→ ┘                              ↓
                                      [y] (observed)
```

Where:
- **h()** = Predictor transformers (log, sqrt, polynomial)
- **η = Xβ** = Linear predictor
- **g⁻¹()** = Inverse link function (logit⁻¹, exp, identity)
- **μ** = Expected value of Y
- **f()** = Distribution family (Binomial, Poisson, Gaussian, etc.)
- **Y** = Random variable (what the model says could happen)
- **y** = Observed data (what actually happened)

## Key Distinctions to Maintain

1. **Y vs y**: Y is the modelled random variable; y is observed data
2. **β vs α**: β tunes the systematic component (via Xβ → μ); α tunes dispersion in f()
3. **Link vs Distribution**: These are separate choices, though often paired conventionally

## Page Structure (Guided Flow)

1. **Scenario Selection** - Choose a data problem type (binary, count, continuous, etc.)
2. **Data Exploration** - Paginated table view of the dataset
3. **Model Family Selection** - Choose distribution and link function
4. **Predictor Transformations** - Apply h() transforms to X variables
5. **Model Fitting** - Manual slider exploration then algorithmic optimization
6. **Advanced: Loss Function Comparison** - Compare MLE to other loss functions

## Tech Stack

**Primary**: Standalone HTML files with vanilla JavaScript

- **Structure**: Static HTML pages served from `docs/` directory
- **Code examples**: R and Python for follow-along exercises (tabbed display)
- **Interactive visualisations**: Canvas API, D3.js, Plotly.js - all vanilla JS (no build step)
- **Math rendering**: KaTeX (CDN-based)
- **Hosting**: GitHub Pages (static site from `docs/` folder) at **https://stats-board.jonminton.net/** (custom domain via `docs/CNAME`; DNS CNAME record lives in Netlify DNS for jonminton.net; old jonminton.github.io/glm-dashboard-explainer/ URLs 301-redirect with paths preserved)
- **No build step**: All HTML files are self-contained with inline CSS/JS

*Note: The project originally planned to use Quarto but moved to standalone HTML for simplicity and faster iteration. Quarto files have been removed.*

## Tutorial Series (Current Focus)

A series of guided tutorials, each demonstrating a complete GLM workflow for different data types.
See `.claude/specs/tutorial-series.md` for detailed implementation plan.

### Current Status

| # | Tutorial | GLM Family | Status |
|---|----------|------------|--------|
| 1 | Heart Rate Prediction | Gaussian + Identity | **COMPLETE** |
| 2 | Heart Disease Classification | Binomial + Logit | **COMPLETE** |
| 3 | Bike Rental Counts | Poisson + Log | **COMPLETE** |
| 4 | Overdispersed Counts | Negative Binomial + Log | **COMPLETE** |
| 5 | Blood Pressure Prediction | Gamma + Log | **COMPLETE** |
| 6 | Exam Performance Rates | Beta + Logit | **COMPLETE** |
| 7 | Pain Level Assessment | Ordinal + Cumulative Logit | **COMPLETE** |
| 8 | Doctor Visit Counts | Zero-Inflated Poisson | **COMPLETE** |

### Tutorial Files
```
docs/
├── index.html                      # Tutorial/datasets index page
└── tutorials/
    ├── 01-gaussian/                # Tutorial 1: Heart Rate (Gaussian)
    │   ├── systematic.html         # Select response & predictors
    │   ├── link.html               # Link function selection
    │   ├── distribution.html       # Distribution selection
    │   ├── fitting.html            # Fitting method explanation
    │   ├── code.html               # R/Python implementation
    │   └── advanced.html           # Log-likelihood derivation (KaTeX)
    ├── 02-logistic/                # Tutorial 2: Heart Disease (Binomial)
    ├── 03-poisson/                 # Tutorial 3: Bike Rentals (Poisson)
    ├── 04-negbin/                  # Tutorial 4: Overdispersed Counts
    ├── 05-gamma/                   # Tutorial 5: Blood Pressure (Gamma)
    ├── 06-beta/                    # Tutorial 6: Exam Proportions (Beta)
    ├── 07-ordinal/                 # Tutorial 7: Pain Levels (Ordinal)
    └── 08-zeroinfl/                # Tutorial 8: Doctor Visits (ZIP)
```

### Design Pattern
Each tutorial follows a 6-page flow:
1. **Systematic** → Select response & predictors
2. **Link** → Choose link function (with wrong-choice feedback)
3. **Distribution** → Choose distribution family
4. **Fitting** → Understand MLE/IRLS
5. **Code** → R and Python implementation
6. **Advanced** → Log-likelihood derivation, custom MLE

### Key Technical Decisions
- **KaTeX** for LaTeX math rendering (CDN-based)
- **Standalone HTML** files (no build step required)
- **Tabbed R/Python** code panels
- **Validated outputs** against actual R/Python sessions
- **ES6 modules** for shared JavaScript code (`docs/js/optimization/`)

## Development Principles

- **One concept per page** - Don't mix link functions and loss functions
- **Concrete before abstract** - See data before equations
- **Active before passive** - Manipulate before optimize
- **Build intuition before automation** - Manual sliders before algorithms
- **Progressive disclosure** - Beginner/Intermediate/Advanced modes

## Key Resources

- [JonStats Course Materials](https://jonminton.github.io/JonStats/)
- Prior discussion: `support/claude-concept-chat.md`

## User Feedback System

The tutorials are in alpha testing. Users can report bugs and request features via GitHub Issues.

### Querying Feedback (for Claude sessions)

```bash
# List all bug reports
gh issue list --label bug

# List all feature requests
gh issue list --label enhancement

# View a specific issue
gh issue view <issue-number>

# List open issues with details
gh issue list --label bug --state open --json number,title,body
```

### Feedback Infrastructure

- **Issue templates**: `.github/ISSUE_TEMPLATE/` (bug_report.md, feature_request.md)
- **Feedback widget**: `docs/js/feedback.js` - floating "?" button on all pages
- **Auto-context**: Widget pre-fills issues with current tutorial/page location

### Adding Feedback to New Pages

Run the build script to add the feedback widget to any new HTML files:
```bash
python3 scripts/build/add-feedback-widget.py
```

## File Structure

```
glm-dashboard-explainer/
├── CLAUDE.md                 # This file - project overview
├── .github/
│   └── ISSUE_TEMPLATE/       # GitHub issue templates
│       ├── bug_report.md
│       ├── feature_request.md
│       └── config.yml
├── .claude/
│   ├── settings.json         # Claude Code settings
│   ├── handover/             # Session handover documents
│   ├── architecture.md       # Architectural decisions (ADRs)
│   └── commands/             # Custom slash commands
├── docs/                     # Main site (GitHub Pages source)
│   ├── index.html            # Tutorial index page
│   ├── data/                 # JSON datasets (terrain, heart data, etc.)
│   ├── js/
│   │   ├── feedback.js       # Feedback widget
│   │   ├── inference/        # Shared ES6 modules for inference section
│   │   │   └── inference-math.js  # OLS/logistic fits, Hessian→vcov, grid posteriors, Metropolis, gammaQ/normalSf/chiSqSf, olsFitK, aic/bic (validated vs Python/R)
│   │   ├── hacker-stats/     # Shared ES6 modules for resampling section
│   │   │   └── resampling.js # Seeded bootstrap/permutation/quantiles — mulberry32 ported bit-faithfully to scripts/py/validate_hacker_stats.py
│   │   └── optimization/     # Shared ES6 modules
│   │       ├── algorithms.js # Optimization algorithms (gradient, Newton, MCMC)
│   │       ├── terrain.js    # Elevation lookup, Hessian, ellipse functions
│   │       └── synthetic-terrain.js  # Gaussian bump terrain generators
│   ├── css/                  # Shared CSS
│   ├── tutorials/            # GLM tutorial pages (8 complete)
│   │   ├── 01-gaussian/      # 6 HTML files per tutorial
│   │   ├── 02-logistic/
│   │   ├── 03-poisson/
│   │   ├── 04-negbin/
│   │   └── 05-gamma/
│   ├── optimization/         # Optimisation visualisation pages
│   │   ├── index.html        # 1D mean-only
│   │   ├── 2d.html           # 2D line fitting
│   │   ├── 3d.html           # 3D multiple regression
│   │   ├── 4d.html           # 4D+ beyond visualisation
│   │   ├── multi-optima.html # Speed/Accuracy/Representativeness comparison
│   │   └── mcmc.html         # Bayesian MCMC exploration
│   ├── inference/            # Statistical inference section (follows optimisation; forks after curvature)
│   │   ├── index.html        # Why uncertainty: peak shape → error bar (1D); route cards
│   │   ├── curvature.html    # Hessian → vcov → SEs; barefoot probes; ellipse; fork buttons
│   │   ├── wald.html         # (purple branch) z = β̂/SE; rejection picture; CI = unrejected nulls
│   │   ├── lr-test.html      # (purple branch) two peaks compared; Λ on χ²₁; profile CIs
│   │   ├── model-comparison.html # (purple branch) AIC/BIC ladder; junk-predictor demo
│   │   └── bayes.html        # (teal branch) quadratic-approx failures; credible intervals
│   └── hacker-stats/         # Resampling section (amber; seeded runs reproduce validation exactly)
│       ├── index.html        # Why resample: median hook; calibrate-on-the-mean loop; taxonomy router
│       ├── bootstrap.html    # Slope handshake vs Wald; median/quantile CIs; separation demo
│       ├── permutation.html  # Two-coins card shuffle (JonStats data); shuffle-Y regression null
│       ├── comparison.html   # Three routes: Wald | bootstrap | credible on three scenarios
│       ├── when-to-use.html  # Decision guide; bias/exchangeability limits
│       └── poststratification.html # Xbox study; skew-and-repair demo; MrP outro
├── scripts/
│   ├── build/                # Site processing scripts (Python)
│   ├── R/                    # R validation scripts
│   └── py/                   # Python validation/algorithm scripts
│       └── optimization/     # Python implementations (mirror JS)
└── support/                  # Background documentation
```
