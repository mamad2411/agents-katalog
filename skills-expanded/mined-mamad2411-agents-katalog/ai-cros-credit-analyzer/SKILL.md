# AI-CROS Credit Analyzer Skill

## Trigger
When user wants to build, create, or scaffold the AI-CROS Credit Analyzer project - a credit report parsing, analysis, and dispute letter generation system.

## Action

The project is located at: `~/Projects/ai-cros-credit-analyzer`

To run:

```bash
cd ~/Projects/ai-cros-credit-analyzer

# Node.js
npm install
cp .env.example .env  # Add your OPENAI_API_KEY
npm start

# OR Python
python -m venv venv
source venv/bin/activate
pip install -r python/requirements.txt
cp .env.example .env  # Add your OPENAI_API_KEY
uvicorn python.app:app --reload
```

## Project Structure

Create the complete project:

```
ai-cros-credit-analyzer/
├── prompts/
│   ├── parser.prompt.txt      # Credit report parsing prompt
│   ├── analyzer.prompt.txt    # Analysis prompt
│   └── letter.prompt.txt      # Dispute letter generation prompt
├── schemas/
│   ├── parser.schema.json     # Parser JSON schema
│   ├── analyzer.schema.json   # Analyzer JSON schema
│   └── letter.schema.json     # Letter JSON schema
├── fixtures/
│   ├── sample-raw-input.json
│   ├── sample-parser-output.json
│   ├── sample-analyzer-output.json
│   └── sample-letter-output.json
├── frontend/
│   └── index.html             # Upload/analysis UI
├── src/
│   ├── app.js                 # Express server
│   ├── routes/
│   │   ├── parse-report.js
│   │   ├── analyze-report.js
│   │   └── generate-letters.js
│   ├── services/
│   │   └── openai.js
│   ├── utils/
│   │   ├── loadPrompt.js
│   │   ├── loadSchema.js
│   │   └── validateJson.js
│   └── middleware/
│       └── errorHandler.js
├── python/
│   ├── app.py                 # FastAPI server
│   ├── services/
│   │   └── openai_client.py
│   └── requirements.txt
├── postman/
│   └── ai-cros.postman_collection.json
├── qa/
│   ├── checklist.md
│   └── test-cases.md
├── .env.example
├── package.json
├── requirements.txt
└── README.md
```

## Implementation Notes

- Use OpenAI API with JSON Schema for structured outputs
- Three-step pipeline: Parse → Analyze → Generate Letters
- Human review required before sending any disputes
- Always include compliance disclaimers
- Server-side only (never expose API keys)

## Quick Start

```bash
# Node.js
npm install
npm start

# Python
python -m venv venv
source venv/bin/activate
pip install -r python/requirements.txt
uvicorn python.app:app --reload
```

## Features

1. **Parser** - Extracts and normalizes credit report data
2. **Analyzer** - Identifies potential issues and dispute opportunities
3. **Letter Generator** - Creates compliance-safe dispute frameworks
4. **Frontend** - Browser-based UI for upload and analysis

## Compliance

- No guaranteed outcomes
- FCRA/CROA/TSR-aware
- Human review workflow
- Always include compliance notices
