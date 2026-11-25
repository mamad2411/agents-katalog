---
name: seo-llm
description: Use when optimizing content for LLM-powered search engines (ChatGPT, Perplexity, Gemini, Claude, Bing AI, Qwen), implementing RAG optimization, prompt engineering for search visibility, semantic SEO, and ensuring content ranks highly in AI-driven search results. Includes techniques for ChatGPT SEO, Perplexity Authority, Gemini Rich Results, and Claude Source Attribution.
license: MIT
---

# SEO LLM Skill — Search Engine Optimization for AI-Driven Search

## Overview

This skill provides comprehensive guidance for optimizing content for **LLM-powered search engines** including ChatGPT, Perplexity, Gemini, Claude, Bing AI, and Qwen. It includes RAG optimization, prompt engineering for search visibility, semantic SEO, and ensuring content ranks highly in AI-driven search results. Based on prompt engineering best practices and RAG optimization techniques.

## When to Use

**Use this skill when:**

- Optimizing content for ChatGPT search results
- Optimizing content for Perplexity AI search
- Optimizing content for Gemini search
- Optimizing content for Claude search
- Optimizing content for Bing AI search
- Optimizing content for Qwen search
- Implementing RAG optimization techniques
- Designing semantic SEO strategies for AI search
- Creating content that ranks in AI-powered search results
- Implementing prompt engineering for search visibility
- Optimizing for ChatGPT SEO (OpenAI's search)
- Optimizing for Perplexity Authority (authoritative sources)
- Optimizing for Gemini Rich Results (structured data)
- Optimizing for Claude Source Attribution (source credibility)
- Implementing semantic keyword targeting
- Optimizing for conversational search queries
- Creating content that AI search engines prioritize
- Implementing entity-based SEO for AI search
- Optimizing for voice search and natural language queries
- Creating content with clear answer structures for AI search
- Implementing schema markup for AI search visibility
- Optimizing for multi-turn conversation search
- Creating content that ranks in AI-powered knowledge graphs

**Do NOT use this skill when:**

- Optimizing for traditional search engines (Google, Bing, Yahoo) - use traditional SEO skills
- Designing database schema (use database-design skill)
- Creating UI components (use frontend-design skill)
- Implementing basic keyword targeting without AI context (use traditional SEO skill)
- Managing non-search-related content strategy (use content-strategy skill)
- Building LLM applications without search optimization needs (use llm-integrations skill)
- Creating technical documentation without search visibility requirements (use documentation-best-practices skill)

**Why avoid:** LLM SEO requires different techniques than traditional SEO. Focus on AI search optimization patterns.

## Core Concepts

### AI Search Engine Landscape

| Search Engine  | Key Optimization Factor           | Best For                   |
| -------------- | --------------------------------- | -------------------------- |
| **ChatGPT**    | Authority, recency, relevance     | Conversational search, Q&A |
| **Perplexity** | Authority, citations, depth       | Research, detailed answers |
| **Gemini**     | Rich results, structured data     | Visual search, multimodal  |
| **Claude**     | Source attribution, credibility   | Trust-based search         |
| **Bing AI**    | Microsoft ecosystem integration   | Enterprise search          |
| **Qwen**       | Alibaba ecosystem, Chinese market | Chinese language search    |

### RAG Optimization

```python
# RAG Pipeline with Re-ranking
from langchain_core.documents import Document
from reranking import RAGPipeline, rerank_documents

# Basic RAG
chunks = [
    "The capital of France is Paris, a beautiful city.",
    "Paris is the capital and most populous city of France.",
    "Have you visited Paris? It's the capital city known for the Eiffel Tower."
]

def basic_rag(query: str, docs: list) -> list:
    """Basic RAG retrieval."""
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.similarity_search(query, k=3)

# Advanced RAG with reranking
def advanced_rag(query: str, docs: list) -> list:
    """Advanced RAG with LLM-based reranking."""
    reranked = rerank_documents(query=query, docs=docs, top_n=3)
    return reranked

# Query
query = "What is the capital of France?"
results = advanced_rag(query, chunks)
```

### Prompt Engineering for Search

```python
# Optimized prompt for AI search
def create_search_optimized_prompt(topic: str, intent: str = "informational") -> str:
    """Create a prompt optimized for AI search results."""

    prompts = {
        "informational": f"""
        You are an expert on {topic}. Provide a comprehensive, well-structured answer.

        Requirements:
        1. Start with a clear, direct answer
        2. Provide detailed explanations with examples
        3. Include relevant statistics and data
        4. Cite authoritative sources
        5. Use bullet points for key information
        6. End with a concise summary

        Topic: {topic}
        """,

        "comparative": f"""
        Compare and contrast {topic} with relevant alternatives.

        Requirements:
        1. Create a comparison table
        2. List pros and cons for each option
        3. Provide use case recommendations
        4. Include pricing and availability
        5. Cite sources for all claims

        Topic: {topic}
        """,

        "how_to": f"""
        Provide a step-by-step guide for {topic}.

        Requirements:
        1. Number each step clearly
        2. Include prerequisites
        3. Provide code examples where relevant
        4. Include common pitfalls and how to avoid them
        5. End with expected outcomes

        Topic: {topic}
        """
    }

    return prompts.get(intent, prompts["informational"])
```

## Search Engine Optimization Patterns

### ChatGPT SEO

```python
# ChatGPT SEO Optimization
def optimize_for_chatgpt(content: str) -> dict:
    """Optimize content for ChatGPT search."""

    return {
        "authority_signals": [
            "Cite authoritative sources",
            "Include author credentials",
            "Show recent updates",
            "Link to trusted domains"
        ],
        "structure_signals": [
            "Clear question-answer format",
            "Conversational tone",
            "Direct answers in first paragraph",
            "Use of bullet points for scannability"
        ],
        "engagement_signals": [
            "Answer length: 300-800 words",
            "Include examples and use cases",
            "Address common follow-up questions",
            "Provide actionable takeaways"
        ],
        "optimization_tips": [
            "Use natural language queries",
            "Focus on user intent",
            "Create comprehensive answers",
            "Include relevant keywords naturally"
        ]
    }

# Example usage
chatgpt_optimization = optimize_for_chatgpt("How to use React hooks")
```

### Perplexity Authority

```python
# Perplexity Authority Optimization
def optimize_for_perplexity(content: str) -> dict:
    """Optimize content for Perplexity search."""

    return {
        "authority_signals": [
            "Cite multiple authoritative sources",
            "Include direct quotes from experts",
            "Show source credibility metrics",
            "Link to primary sources"
        ],
        "depth_signals": [
            "Comprehensive coverage (1000+ words)",
            "Include historical context",
            "Provide multiple perspectives",
            "Address edge cases"
        ],
        "citation_signals": [
            "Use inline citations",
            "Include source URLs",
            "Show citation count",
            "Link to original research"
        ],
        "optimization_tips": [
            "Create in-depth guides",
            "Include expert quotes",
            "Cite primary sources",
            "Show comprehensive coverage"
        ]
    }

# Example usage
perplexity_optimization = optimize_for_perplexity("Machine learning algorithms")
```

### Gemini Rich Results

```python
# Gemini Rich Results Optimization
def optimize_for_gemini(content: str) -> dict:
    """Optimize content for Gemini search."""

    return {
        "rich_signals": [
            "Include structured data (JSON-LD)",
            "Add image captions",
            "Use video schema",
            "Implement FAQ schema"
        ],
        "multimodal_signals": [
            "Include high-quality images",
            "Add alt text descriptions",
            "Use video content",
            "Implement 3D models where relevant"
        ],
        "visual_signals": [
            "Use clear headings",
            "Include infographics",
            "Add comparison tables",
            "Implement collapsible sections"
        ],
        "optimization_tips": [
            "Add JSON-LD structured data",
            "Include high-quality images",
            "Use semantic HTML",
            "Implement schema markup"
        ]
    }

# Example usage with JSON-LD
def create_json_ld_for_gemini():
    """Create JSON-LD schema for Gemini."""
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to Optimize for Gemini",
        "description": "Step-by-step guide to optimize content for Gemini search",
        "step": [
            {
                "@type": "HowToStep",
                "name": "Add Structured Data",
                "description": "Implement JSON-LD schema markup"
            },
            {
                "@type": "HowToStep",
                "name": "Optimize Images",
                "description": "Add high-quality images with alt text"
            },
            {
                "@type": "HowToStep",
                "name": "Use Semantic HTML",
                "description": "Implement proper heading hierarchy"
            }
        ]
    }
```

### Claude Source Attribution

```python
# Claude Source Attribution Optimization
def optimize_for_claude(content: str) -> dict:
    """Optimize content for Claude search."""

    return {
        "credibility_signals": [
            "Cite peer-reviewed sources",
            "Show author credentials",
            "Include publication dates",
            "Link to original research"
        ],
        "attribution_signals": [
            "Direct quotes with attribution",
            "Paraphrase with citation",
            "Show source credibility",
            "Link to original content"
        ],
        "trust_signals": [
            "No promotional language",
            "Present balanced views",
            "Cite multiple sources",
            "Acknowledge limitations"
        ],
        "optimization_tips": [
            "Cite authoritative sources",
            "Show source credibility",
            "Present balanced views",
            "Include citations"
        ]
    }

# Example usage
claude_optimization = optimize_for_claude("Climate change impacts")
```

## Semantic SEO for AI Search

### Entity-Based Optimization

```python
# Entity-Based SEO
def optimize_for_entities(topic: str) -> dict:
    """Optimize content for AI search entity recognition."""

    return {
        "primary_entity": topic,
        "related_entities": [
            f"types of {topic}",
            f"benefits of {topic}",
            f"challenges of {topic}",
            f"best practices for {topic}",
            f"tools for {topic}"
        ],
        "entity_relationships": [
            f"{topic} vs alternatives",
            f"{topic} for beginners",
            f"{topic} for experts",
            f"future of {topic}"
        ],
        "optimization_tips": [
            "Use entity names naturally",
            "Create entity-focused content",
            "Link to related entities",
            "Use semantic variations"
        ]
    }

# Example usage
entity_optimization = optimize_for_entities("machine learning")
```

### Conversational Search Optimization

````python
# Conversational Search Optimization
def optimize_for_conversational_search(query_type: str) -> str:
    """Optimize content for conversational AI search."""

    conversational_patterns = {
        "question": f"""
        Q: How do I get started with this?

        A: Getting started with this is straightforward. Follow these steps:

        1. **Understand the basics** - Learn the fundamental concepts
        2. **Set up your environment** - Install required tools
        3. **Create your first project** - Build something simple
        4. **Expand your knowledge** - Learn advanced concepts

        For more information, see the comprehensive guide.
        """,

        "comparison": f"""
        Q: What's the difference between option A and option B?

        A: Here's a comparison of option A and option B:

        | Aspect | Option A | Option B |
        |--------|----------|----------|
        | Ease of use | High | Medium |
        | Performance | High | High |
        | Learning curve | Steep | Gentle |

        Choose Option A if you prioritize performance. Choose Option B if you prefer ease of use.
        """,

        "tutorial": f"""
        Q: Can you show me how to do this?

        A: Sure! Here's a step-by-step tutorial:

        **Step 1:** Prepare your environment
        ```python
        # Install required packages
        pip install package-name
        ```

        **Step 2:** Implement the solution
        ```python
        # Your code here
        result = process_data()
        ```

        **Step 3:** Verify the results
        Check that the output matches expected values.
        """
    }

    return conversational_patterns.get(query_type, conversational_patterns["question"])
````

## Best Practices

### 1. Create Answer-Focused Content

```python
# ✅ GOOD: Answer-focused content
def create_answer_focused_content(question: str) -> str:
    """Create content optimized for AI search answers."""

    return f"""
    **Question: {question}**

    **Direct Answer:** [Provide a clear, concise answer in the first paragraph]

    **Detailed Explanation:** [Expand on the answer with detailed information]

    **Examples:** [Include relevant examples]

    **Key Takeaways:** [Summarize the main points]
    """

# ❌ BAD: Information-dump content
def create_information_dump():
    """BAD: No clear answer structure."""
    return "This is a lot of information about the topic..."
```

### 2. Optimize for Semantic Search

```python
# ✅ GOOD: Semantic search optimization
def optimize_for_semantic_search(topic: str) -> dict:
    """Optimize content for semantic search engines."""

    return {
        "semantic_keywords": [
            f"what is {topic}",
            f"how to use {topic}",
            f"{topic} examples",
            f"{topic} best practices",
            f"{topic} for beginners"
        ],
        "entity_optimization": [
            f"types of {topic}",
            f"benefits of {topic}",
            f"challenges with {topic}"
        ],
        "conversational_phrases": [
            f"I want to learn about {topic}",
            f"Can you explain {topic}",
            f"Show me how to use {topic}"
        ]
    }
```

### 3. Implement Schema Markup

```python
# ✅ GOOD: Schema markup for AI search
def create_schema_markup(topic: str) -> dict:
    """Create schema markup for AI search visibility."""

    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"Complete Guide to {topic}",
        "description": f"A comprehensive guide to {topic} for AI search optimization",
        "author": {
            "@type": "Person",
            "name": "Expert Author"
        },
        "datePublished": "2024-01-01",
        "keywords": f"{topic}, AI search, SEO"
    }
```

### 4. Optimize for Voice Search

```python
# ✅ GOOD: Voice search optimization
def optimize_for_voice_search(topic: str) -> dict:
    """Optimize content for voice-activated AI search."""

    return {
        "natural_language_phrases": [
            f"what is {topic}",
            f"how does {topic} work",
            f"tell me about {topic}",
            f"explain {topic} to me"
        ],
        "question_format": [
            f"What is {topic}?",
            f"How does {topic} work?",
            f"Can you explain {topic}?"
        ],
        "answer_length": "150-300 words (optimal for voice responses)"
    }
```

## Common Anti-Patterns

### ❌ Bad: Keyword Stuffing

```python
# ❌ BAD: Keyword stuffing
def bad_keyword_stuffing():
    """BAD: Over-optimization with keywords."""
    return """
    machine learning machine learning algorithms machine learning techniques
    machine learning methods machine learning tools machine learning frameworks
    """
```

**Problems:**

- AI search penalizes over-optimization
- Poor user experience
- May trigger spam detection

### ✅ Good: Natural Language

```python
# ✅ GOOD: Natural language optimization
def good_natural_language(topic: str):
    """GOOD: Natural language content."""
    return f"""
    {topic} is a powerful technology that enables...

    ## What is {topic}?
    {topic} stands for...

    ## How to Use {topic}
    Here's how you can get started with {topic}...
    """
```

### ❌ Bad: No Answer Structure

```python
# ❌ BAD: No answer structure
def bad_answer_structure():
    """BAD: No clear answer format."""
    return "This content has information but no clear answer..."
```

### ✅ Good: Clear Answer Format

```python
# ✅ GOOD: Clear answer format
def good_answer_format(question: str) -> str:
    """GOOD: Clear answer format."""
    return f"""
    **Question: {question}**

    **Answer:** [Direct answer here]

    **Explanation:** [Detailed explanation]

    **Examples:** [Relevant examples]
    """
```

## Real-World Impact

**Before this skill:**

- Content not optimized for AI search
- Low visibility in AI search results
- Poor performance in ChatGPT, Perplexity, Gemini, Claude searches
- Missing RAG optimization

**After this skill:**

- Content optimized for all AI search engines
- High visibility in AI search results
- Optimized for ChatGPT SEO, Perplexity Authority, Gemini Rich Results, Claude Source Attribution
- Proper RAG implementation for search visibility

## Cross-References

- **`llm-integrations`** - For LLM provider configuration
- **`langchain`** - For LangChain RAG implementation
- **`langgraph`** - For stateful RAG workflows
- **`qwen-agent`** - For Qwen-specific search optimization

## References

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [RAG Techniques](https://github.com/nirdiamant/rag_techniques)
- [ChatGPT SEO Best Practices](https://www.promptingguide.ai/readings)
- [Structured Data Markup](https://schema.org/)
- [Semantic SEO Guide](https://dair-ai.github.io/prompt-engineering-guide/)
