## Creating new labels

If you need to translate text using labels, use the MCP tool named:
get_or_create_label

Pass a JSON payload containing a batch of labels to create or reuse.

Request format:

[
  {
    "Language": "en-us",
    "Text": "Sample text",
    "LabelPrefix": "OptionalPrefix",
    "ForceNewLabel": false,
    "Translations": [
      {
        "Language": "it",
        "Text": "Testo semplice"
      }
    ]
  }
]

Rules and conventions:
- English (en-us) is always the primary language
- Translate always is DE, IT and ES
- If the primary text is not provided in English, it must be translate
- ForceNewLabel forces the creation of a new label even if it already exists
- LabelPrefix is optional and may be resolved dynamically by the MCP
- The tool returns the label code in the format: @LabelFile:LabelCode

Batch limits:

- Maximum 10 labels per request
