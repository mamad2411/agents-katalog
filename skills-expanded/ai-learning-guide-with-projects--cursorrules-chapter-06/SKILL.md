# Chapter 6: Mastering the Anthropic Claude API - Cursor Rules

## Chapter Context

This chapter introduces Anthropic Claude API as an alternative to OpenAI. Students learn Claude's API structure, system prompts, document analysis, tool use, and vision. Key focus: understanding differences and when to use Claude.

## Key Concepts

### 1. API Structure Differences
- Client: `anthropic.Anthropic()`
- Method: `client.messages.create()`
- `max_tokens` is **required** (unlike OpenAI)
- Response: `message.content[0].text` (list structure)
- Model names: `claude-3-5-sonnet-20240620`

### 2. System Prompts
- Dedicated `system` parameter (not in messages)
- More reliable adherence than OpenAI
- Better for detailed instructions
- Key Claude strength

### 3. Large Context Windows
- Claude 3.5 Sonnet: 200K tokens
- Excellent for document analysis
- Long conversation support
- Ideal for complex tasks

### 4. Tool Use
- Similar to OpenAI function calling
- Tool descriptions
- Tool execution
- Result feedback

### 5. Vision Capabilities
- Image analysis
- Base64 encoding
- Multimodal prompts
- Visual diagnostics

## Important Code Patterns

### Basic Claude Call
```python
import anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=512,  # REQUIRED
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
```

### System Parameter
```python
message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    system="You are an expert IoT engineer...",  # Dedicated parameter
    messages=[{"role": "user", "content": "..."}]
)
```

### Long Document Analysis
```python
class DocumentAnalyzer:
    def __init__(self, document: str):
        self.system = f"Answer based on this document:\n{document}"
        self.history = []
    
    def ask(self, question: str):
        self.history.append({"role": "user", "content": question})
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=self.system,
            messages=self.history
        )
        answer = message.content[0].text
        self.history.append({"role": "assistant", "content": answer})
        return answer
```

## Common Mistakes to Avoid

1. **Forgetting max_tokens**: Always required in Claude
2. **Wrong response extraction**: Use `content[0].text`, not `content`
3. **System in messages**: Use `system` parameter, not message role
4. **Not leveraging context**: Use large windows for documents
5. **Ignoring tool use**: Similar to OpenAI but different syntax

## Integration Points

- **Chapter 5**: Compare with OpenAI patterns
- **Chapter 7**: Complete API provider knowledge
- **Chapter 8**: API design patterns apply

## Related Chapters

- **Chapter 5**: OpenAI API (compare patterns)
- **Chapter 7**: Gemini API (complete provider knowledge)
- **Chapter 8**: API design patterns
