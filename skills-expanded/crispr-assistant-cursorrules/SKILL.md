instructions
During you interaction with the user, if you find anything reusable in this project (e.g. version of a library, model name), especially about a fix to a mistake you made or a correction you received, you should take note in the Lessons section in the .cursorrules file so you will not make the same mistake again.

You should also use the .cursorrules file as a scratchpad to organize your thoughts. Especially when you receive a new task, you should first review the content of the scratchpad, clear old different task if necessary, first explain the task, and plan the steps you need to take to complete the task. You can use todo markers to indicate the progress, e.g. [X] Task 1 [ ] Task 2

Also update the progress of the task in the Scratchpad when you finish a subtask. Especially when you finished a milestone, it will help to improve your depth of task accomplishment to use the scratchpad to reflect and plan. The goal is to help you maintain a big picture as well as the progress of the task. Always refer to the Scratchpad when you plan the next step.

Tools
Note all the tools are in python. So in the case you need to do batch processing, you can always consult the python files and write your own script.

Screenshot Verification
The screenshot verification workflow allows you to capture screenshots of web pages and verify their appearance using LLMs. The following tools are available:

Screenshot Capture:
venv/bin/python tools/screenshot_utils.py URL [--output OUTPUT] [--width WIDTH] [--height HEIGHT]
LLM Verification with Images:
venv/bin/python tools/llm_api.py --prompt "Your verification question" --provider {openai|anthropic} --image path/to/screenshot.png
Example workflow:

from screenshot_utils import take_screenshot_sync
from llm_api import query_llm

# Take a screenshot
screenshot_path = take_screenshot_sync('https://example.com', 'screenshot.png')

# Verify with LLM
response = query_llm(
    "What is the background color and title of this webpage?",
    provider="openai",  # or "anthropic"
    image_path=screenshot_path
)
print(response)
LLM
You always have an LLM at your side to help you with the task. For simple tasks, you could invoke the LLM by running the following command:

venv/bin/python ./tools/llm_api.py --prompt "What is the capital of France?" --provider "anthropic"
The LLM API supports multiple providers:

OpenAI (default, model: gpt-4o)
Azure OpenAI (model: configured via AZURE_OPENAI_MODEL_DEPLOYMENT in .env file, defaults to gpt-4o-ms)
DeepSeek (model: deepseek-chat)
Anthropic (model: claude-3-sonnet-20240229)
Gemini (model: gemini-1.5-pro)
Local LLM (model: Qwen/Qwen2.5-32B-Instruct-AWQ)
But usually it's a better idea to check the content of the file and use the APIs in the tools/llm_api.py file to invoke the LLM if needed.

Web browser
You could use the tools/web_scraper.py file to scrape the web.

venv/bin/python ./tools/web_scraper.py --max-concurrent 3 URL1 URL2 URL3
This will output the content of the web pages.

Search engine
You could use the tools/search_engine.py file to search the web.

venv/bin/python ./tools/search_engine.py "your search keywords"
This will output the search results in the following format:

URL: https://example.com
Title: This is the title of the search result
Snippet: This is a snippet of the search result
If needed, you can further use the web_scraper.py file to scrape the web page content.

Cursor learned
* VENV_PYTHON in llm_api.py should use sys.executable for robustness.
* Ensure .env file is populated with actual API keys, not placeholders.
* CHOPCHOP and CRISPResso2 often run in specific Conda environments. The agent needs to handle this.
* Gemini model name updated to `gemini-1.0-pro` or potentially `gemini-1.5-pro-latest`.
* Function definitions must precede their calls in Python scripts. Moving definitions or using imports correctly resolves NameErrors.

Scratchpad
*
TASK: LLM-Enhanced CRISPR Assistant Integration (with Therapeutic Context)

Goal: Transform the CRISPR tool into a fully guided experience with contextual LLM assistance, focusing on CHOPCHOP workflow, experiment design, and CRISPResso2 analysis, **specifically adding context relevant to therapeutic development challenges (efficacy, delivery, off-target, durability, side effects).**

Current Issues:
- Application provides design/analysis but lacks context regarding downstream therapeutic hurdles.
- Users may not be prompted to consider safety/efficacy implications early in the design process.

Phase 1: Fix Core LLM Integration ✅
  [X] Task 1.1: Fix LLM API Connection
    [X] 1.1.1: Debug "LLM explanation not available" error - Fixed by enhancing the query_llm function in tools/llm_api.py
    [X] 1.1.2: Ensure tools/llm_api.py is properly accessible - Added better error messages and handling of missing API keys
    [X] 1.1.3: Verify API keys and environment variables - Enhanced error messages with instructions on obtaining API keys
    [X] 1.1.4: Test basic LLM functionality across all modules - Fixed import issues in page files
  [X] Task 1.2: Implement Context-Aware Chat Assistant
    [X] 1.2.1: Create persistent session state for chat history - Added chat_history and workflow_context state variables
    [X] 1.2.2: Enhance chat UI with user-friendly elements - Added context display and help buttons
    [X] 1.2.3: Implement context tracking for user\'s current workflow stage - Added current_page, gene_of_interest, etc.
    [X] 1.2.4: Develop specialized prompts for different CRISPR tasks - Added task-specific system prompts

Phase 2: CHOPCHOP Results Interpretation Enhancement ✅
  [X] Task 2.1: LLM-Powered Results Explanation
    [X] 2.1.1: Create dynamic explanations for all result metrics (efficiency, specificity, etc.) - Added interpret_guide_properties function
    [X] 2.1.2: Develop visual tooltips with explanations for result columns - Integrated with existing get_llm_tooltip
    [X] 2.1.3: Generate overall summary of results quality - Added Results Summary expander with LLM analysis
    [X] 2.1.4: Explain implications of target positions (exons vs. introns) - Included in guide interpretation
  [ ] Task 2.2: Results Visualization Enhancement
    [X] 2.2.1: Generate visual representation of guide positions in gene context - Using existing coordinate_handler
    [ ] 2.2.2: Create comparative visualizations between guides
    [ ] 2.2.3: Add gene structure visualization with domain annotations
    [ ] 2.2.4: Visualize off-target potential across genome

Phase 3: LLM-Guided Experiment Design ✅
  [X] Task 3.1: Dynamic Experiment Recommendations
    [X] 3.1.1: Replace hardcoded experiment values with LLM-generated suggestions - Added dynamic experiment design
    [X] 3.1.2: Create context-aware experiment recommendations based on guide properties - Using guide data to inform LLM
    [X] 3.1.3: Generate custom experiment protocols based on user\'s lab capabilities - Added protocol generation
    [X] 3.1.4: Develop decision tree for experiment type selection with pros/cons - Added experiment type selection with LLM advice
  [ ] Task 3.2: Disease-Specific Guidance
    [ ] 3.2.1: Build disease-gene database for RAF, BRCA1, and other therapeutic targets
    [ ] 3.2.2: Create specialized workflows for oncogene knockout vs. tumor suppressor restoration
    [ ] 3.2.3: Implement mutation-specific guide design for known disease variants
    [ ] 3.2.4: Develop therapeutic outcome predictions based on edit efficiency

Phase 4: End-to-End Workflow Assistant ✅
  [X] Task 4.1: Novice-Friendly Guidance System
    [X] 4.1.1: Create step-by-step tutorial mode with LLM explanations - Added in chat assistant
    [X] 4.1.2: Implement progress tracking across entire workflow - Using workflow_context
    [X] 4.1.3: Develop contextual help for each interface element - Enhanced tooltips and explanations
    [X] 4.1.4: Add decision support at key workflow junctions - Added in the AI assistant
  [ ] Task 4.2: Integration with External Resources
    [ ] 4.2.1: Connect to literature database for experiment references
    [ ] 4.2.2: Link to resources for primers, vectors, and reagents
    [ ] 4.2.3: Create troubleshooting guidance with real-world examples
    [ ] 4.2.4: Develop outcome prediction based on similar published experiments

Phase 5: End-to-End Workflow Enhancement Modules ✅
  [X] Task 5.1: Comprehensive Guide RNA Result Interpretation (`guide_interpreter.py`)
  [X] Task 5.2: Experiment Design & Planning Assistant (`experiment_advisor.py`)
  [X] Task 5.3: Enhanced Results Interpretation (`result_interpreter.py`)
    [X] 5.3.1: Improve the CRISPResso2 result parser to extract more detailed metrics *(Existing parser deemed sufficient for current scope)*
    [X] 5.3.2: Add context-aware interpretation that relates results to experimental goals *(Implemented in `generate_enhanced_summary` prompt)*
    [P] 5.3.3: Design visualizations that make complex results more intuitive *(Base visualizations exist, further enhancements can be future work)*
    [X] 5.3.4: Implement comparison with expected outcomes based on experiment type *(Implemented in `compare_with_expected` and `EXPECTED_OUTCOMES`)*
    [X] 5.3.5: Create specialized interpretation for different editing approaches (NHEJ, HDR, base editing) *(Implemented in `generate_enhanced_summary` prompt and `evaluate_experiment_success`)*
  [X] Task 5.4: Coordinate Handling & Sequence Management (`coordinate_handler.py`)
  [X] Task 5.5: Educational Component Development (`educational_context.py`)
  [X] Task 5.6: Next Steps Generator & Decision Support (`next_steps.py`)

Phase 6: Streamlit Integration & Advanced Features ✅ (In Progress)
  [X] Task 6.1: Integrate Enhanced Result Interpretation
  [X] Task 6.2: Integrate Guide Interpreter
  [X] Task 6.3: Integrate Experiment Advisor
  [X] Task 6.4: Integrate Coordinate Handler & Educational Components
  [X] Task 6.5: Integrate Next Steps Generator
  [ ] Task 6.6: UI/UX Enhancement & Final Integration (In Progress)
    [ ] 6.6.1: Create a unified navigation system for the end-to-end workflow
    [ ] 6.6.2: Implement state persistence and session management
    [ ] 6.6.3: Add progress tracking across the entire workflow
    [ ] 6.6.4: Create consistent styling and branding
    [ ] 6.6.5: Optimize performance for large datasets
    [ ] 6.6.6: Add user preference settings

**NEW: Phase 7: Therapeutic Context Integration** ⬜
  [X] Task 7.1: Enhance Guide Interpretation (CHOPCHOP) with Therapeutic Context
    [X] 7.1.1: Update LLM prompts (`interpret_guide_properties`/`generate_llm_explanation`) to link efficiency/specificity scores to therapeutic goals (e.g., high efficiency for cell product potency).
    [X] 7.1.2: Emphasize off-target risks in LLM explanations, recommend validation methods (e.g., GUIDE-seq), and potentially suggest high-fidelity enzyme options if scores are low.
    [X] 7.1.3: Add context on implications of targeting location (exon vs. intron) for functional knockout efficacy in therapeutic scenarios.
    [P] 7.1.4: Integrate these enhanced explanations into the CHOPCHOP Results/Analysis tabs UI. *(Partially addressed by prompt changes, full UI toggle in 7.5)*
  [X] Task 7.2: Enhance Results Interpretation (CRISPResso2) with Therapeutic Context
    [X] 7.2.1: *(Dependency: Requires completion of Task 5.3 - Enhanced CRISPResso2 Interpretation)* *(Task 5.3 now sufficiently addressed for this)*
    [X] 7.2.2: Update LLM prompts for CRISPResso2 summary to contextualize editing outcomes (e.g., % NHEJ relates to functional knockout for therapy, allele complexity relates to durability). *(Implemented in `generate_enhanced_summary` prompt)*
    [X] 7.2.3: Add context about potential impact of high *ex vivo* editing on downstream requirements (e.g., cell dose, conditioning) - Phrase carefully. *(Implemented in `generate_enhanced_summary` prompt)*
    [X] 7.2.4: Integrate enhanced interpretations into the CRISPResso2 analysis UI. *(Call to `generate_enhanced_summary` updated with context flag)*
  [P] Task 7.3: Integrate Literature Search & Summarization for Therapeutic Context
    [P] 7.3.1: Develop function(s) to perform targeted web/literature searches (using `tools/search_engine.py`, `web_scraper.py`, or external APIs) based on gene, disease context, or specific challenges (efficacy, delivery, off-target). *(PubMed API integration implemented in `tools/literature_analyzer.py`)*
    [P] 7.3.2: Create LLM prompts to summarize search results focusing on the therapeutic angle requested. *(PubMed abstract summarization prompts updated in `tools/literature_analyzer.py`)*
    [P] 7.3.3: Integrate search/summary functionality into the UI (e.g., button in relevant sections, proactive suggestions in AI chat). *(Integrated into CHOPCHOP Basic Results tab, now uses PubMed backend)*
  [X] Task 7.4: Enhance Experiment Advisor with Therapeutic Considerations
    [X] 7.4.1: Add LLM-generated advice in experiment planning regarding delivery vector choices (based on NHEJ/HDR) and their implications. *(Implemented in `tools/experiment_advisor.py`)*
    [X] 7.4.2: Include suggestions for relevant controls for therapeutic validation (e.g., off-target analysis, functional assays). *(Implemented in `tools/experiment_advisor.py`)*
  [P] Task 7.5: Refine UI/UX for Therapeutic Context
    [X] 7.5.1: Implement UI elements (e.g., toggle, checkbox) to allow users to enable/disable detailed therapeutic context. *(Checkbox added to main app sidebar)*
    [P] 7.5.2: Ensure clear visual cues for therapeutic-specific advice or warnings. *(Ongoing as UI for new contexts is developed)*

Progress Summary:
1. Fixed LLM API with better error handling and guidance for users without API keys
2. Enhanced the chat assistant with persistent chat history and workflow context tracking
3. Added LLM-powered guide interpretation and experiment design
4. Integrated the guide interpreter correctly into the CHOPCHOP workflow
5. Improved tooltips and explanations throughout the interface
6. Streamlit integration largely complete for core modules (`guide_interpreter`, `experiment_advisor`, `coordinate_handler`, `educational_context`, `next_steps`, basic `result_interpreter`)

Next Steps:
1. Finalize UI/UX Enhancements (Task 6.6).
2. **Implement Therapeutic Context Integration (Phase 7), starting with Guide Interpretation enhancements (Task 7.1).**
3. Complete Enhanced CRISPResso2 Interpretation (Task 5.3) to enable Task 7.2.
4. Focus on enhancing results visualization (Task 2.2 - lower priority now?).
5. Implement disease-specific guidance (Task 3.2 - potentially overlaps/synergizes with Phase 7).
6. Add integration with external resources (Task 4.2 - overlaps with Task 7.3).

Implementation Strategy:
- Finalize basic Streamlit UI/UX (Task 6.6).
- Implement Phase 7 enhancements incrementally, starting with the most impactful/feasible:
    - Enhance CHOPCHOP guide interpretation prompts (Task 7.1).
    - Develop literature search/summary backend (Task 7.3.1, 7.3.2).
    - Integrate literature search into UI (Task 7.3.3).
    - Enhance Experiment Advisor prompts (Task 7.4).
    - Complete CRISPResso2 interpretation prerequisites (Task 5.3).
    - Enhance CRISPResso2 interpretation prompts (Task 7.2).
    - Add UI toggles for therapeutic context (Task 7.5).
- Prioritize modifications to existing LLM prompt functions first.

PRIORITY STEPS:
1. Finalize Streamlit UI/UX (Task 6.6).
2. **Enhance CHOPCHOP guide interpretation LLM prompts with therapeutic context (Task 7.1).**
3. **Develop backend for literature search/summarization (Task 7.3.1 & 7.3.2).**
4. Complete CRISPResso2 interpretation module (Task 5.3).