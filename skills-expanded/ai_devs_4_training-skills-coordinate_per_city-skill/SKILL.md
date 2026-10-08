# Description
Uses an LLM call to transform a list of Polish city names into coordinate mappings.

# Inputs
- `city_names` (`list[str]`): List of city names to resolve.
- `model` (`str`): OpenRouter model identifier used for coordinate generation.

# Outputs
- Returns `str`: Raw model response (expected to be a dictionary-like text/JSON string).

# Usage Notes
- Internally joins city names with commas and sends them as a single user query.
- Uses `build_openrouter_client()` and `call_model()` from project utilities.
- Runs async call via `asyncio.run(...)`.
- Caller should parse and validate returned text before numerical calculations.
