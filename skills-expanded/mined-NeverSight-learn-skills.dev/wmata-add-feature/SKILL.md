---
name: wmata-add-feature
description: Add a new dashboard feature (chart, panel, metric, or whole tab) to app/dashboard.py while preserving the existing patterns for caching, color coding, and demo-mode fallback. Use when the user wants to extend the Streamlit UI.
---

# Add a Dashboard Feature

This skill helps add UI features to `app/dashboard.py` consistently with the existing three-tab structure.

## Before Coding

1. **Read `app/dashboard.py`** in full. It's long but well-structured. Note:
   - Sidebar logic (station selector, auto-refresh)
   - The 5-metric row at the top
   - How each tab is delimited (`with tab_rail:` etc.)
   - The demo-mode `DEMO_*` constants used when no API key is set
   - Color coding: rail uses `LINE_COLORS`, bus arrivals use green badges

2. **Decide where the feature goes:**
   - A station-specific panel → Rail tab
   - A bus-specific panel → Bus tab
   - A system-wide metric or aggregated view → System tab
   - Cross-cutting (e.g., a search box) → sidebar
   - A whole new dimension (e.g., historical) → new tab — add to `st.tabs([...])`

3. **Identify which API call(s) you need.** Prefer `wmata/client.py` functions; if a needed endpoint isn't wrapped, run the `wmata-add-endpoint` skill first.

## Implementation

1. **Cache API calls** — wrap network functions with `@st.cache_data(ttl=N)` where N is seconds. Live data: 30–60s. Reference data (stations, routes): 3600s.

2. **Handle demo mode** — branch on `if api_key:` and provide a small `DEMO_*` constant for the demo path. The app must continue to render without a key.

3. **Defensive against empty data** — every list comprehension should tolerate empty input. Use `if items:` guards before charts.

4. **Follow the visual idiom:**
   - Section headers: `st.subheader("...")` or `st.markdown("### ...")`
   - Tables: build a pandas DataFrame, then `st.markdown(df.to_html(...), unsafe_allow_html=True)` for color-coded rows; or `st.dataframe(df)` for plain tables
   - Charts: Plotly horizontal bars are the existing idiom (`px.bar(..., orientation='h')`)
   - Metrics: `st.metric("Label", value, delta=delta)` in a `st.columns(N)` row
   - Long lists: wrap in `st.expander("Show all ...")`

5. **Respect the rail-vs-bus type asymmetry** — rail `Min` is a STRING (use `format_min()`); bus `Minutes` is an INT.

6. **Test in the browser** — run `streamlit run app/dashboard.py`, click through the new feature, verify:
   - Renders with API key
   - Renders in demo mode (rename `.env` temporarily, or use a wrong key)
   - No regression on other tabs
   - No console errors / Python tracebacks visible in the terminal

## Document the Test Result

Add a row to `tests/test_results.md` under a new "Iteration N" section. Use the same table format as existing iterations: test ID, level (L3 for UI), what, pass condition, result, notes.

## Anti-Patterns to Avoid

- **Don't add an API key input field.** The key must come from `.env` only — adding a UI input is a security regression.
- **Don't fetch in a loop without caching.** Every uncached call counts against the 50K/day limit.
- **Don't break demo mode.** A reviewer or student should be able to clone, run, and see *something* without registering for a key.
- **Don't import heavy ML libraries** (sklearn, torch, transformers) unless the feature explicitly needs them — keep the deploy small.
