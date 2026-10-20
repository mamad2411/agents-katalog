---
description: 
globs: 
alwaysApply: true
---
# Memory Integration with Previous Thoughts and Concepts

**Description:** These rules guide how the AI should leverage previous thoughts and conceptual discussions, especially when there are no file modifications but there is valuable conceptual thinking being developed.

## When to Apply These Rules

Apply these rules particularly when:

- The current conversation is addressing conceptual topics without immediate code changes
- The user is exploring design options, architectural patterns, or problem-solving approaches
- Previous messages in the same session contain relevant context for the current question
- You need to connect code changes with previous discussions about related concepts
- Building on ideas that have high confidence scores from previous interactions

## How to Integrate Previous Thoughts

1. **Within Session Continuity:**
   - At the beginning of your response, check if this conversation continues a previous thought thread
   - If relevant, refer back to key insights from earlier in the conversation using language like "As we discussed earlier..."
   - Ensure that your response builds coherently on the previously established concepts
   - Consider confidence scores from previous interactions when deciding which threads to continue

2. **Sequential Thinking Tools:**
   - For complex reasoning tasks spanning multiple messages, use the `mcp_chroma_dev_chroma_sequential_thinking` tool to record the thought process
   - Structure thoughts with clear numbering: "Thought 1 of N", "Thought 2 of N", etc.
   - Include a logical progression that explicitly connects to previous thoughts in the sequence
   - Reference code contexts from related discussions when building on file-modifying interactions

3. **When Providing Conceptual Guidance:**
   - Use the `mcp_chroma_dev_chroma_find_similar_thoughts` tool to search for relevant previous thoughts
   - Reference similar past considerations with "This relates to our previous discussion about X..."
   - Cross-reference related concepts that emerged in earlier parts of the conversation
   - When referring to code, cite related snippets that were captured in previous interactions

4. **Knowledge Integration Strategy:**
   - Synthesize knowledge across related conversations by using the `session_id` parameter to retrieve thoughts within the same session
   - Build a coherent mental model by explicitly connecting new concepts to previously established ones
   - When appropriate, use the phrase "Building on our previous discussion..." to signal continuity
   - Leverage bi-directional linking between code and discussions to connect concepts with implementations

5. **Documentation of Conceptual Evolution:**
   - For important conceptual breakthroughs, mark them with "Key insight:" to make them easier to identify later
   - When recording sequential thoughts, ensure the `next_thought_needed` parameter is set appropriately to indicate if further development is expected
   - Use consistent terminology across responses to maintain conceptual integrity
   - For high-confidence insights that lead to code changes, note the relationship to potentially create derived learnings

6. **Code Context Connection:**
   - When discussing code that has been modified in previous interactions, reference the relevant context
   - Use tool sequence patterns to understand the evolution of solutions across conversations
   - Connect conceptual discussions to concrete implementations where applicable
   - Leverage bidirectional links between chat history and code chunks when available

## Implementation Details

When using the sequential thinking tools:

```python
# Example of sequential thinking tool use
mcp_chroma_dev_chroma_sequential_thinking(
    thought="[Content of the current thought]",
    thought_number=current_number,
    total_thoughts=expected_total,
    session_id="[current_session_id]",
    branch_id="[optional_branch_id]",
    branch_from_thought=0,  # Set to parent thought number if branching
    next_thought_needed=True  # Whether more thoughts are expected
)
```

When finding similar thoughts:

```python
# Example of finding similar thoughts
mcp_chroma_dev_chroma_find_similar_thoughts(
    query="[Current topic or question]",
    session_id="[current_session_id]",  # Optional: limit to current session
    n_results=5,
    threshold=0.7,
    include_branches=True
)
```

When accessing context-rich chat history:

```python
# Example of finding related code contexts
mcp_chroma_dev_chroma_query_documents(
    collection_name="chat_history_v1",
    query_texts=["[Related concept or implementation detail]"],
    n_results=3
)
```
