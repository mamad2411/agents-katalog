---
name: prompt-engineering
description: Design effective prompts for LLMs. Outputs prompt templates, few-shot examples, chain-of-thought reasoning, and structured output formats.
argument-hint: [task type, model, quality requirements]
allowed-tools: Read, Write, Bash
---

# Prompt Engineering

Design effective prompts for large language models. Not trial-and-error — systematic techniques with few-shot examples, chain-of-thought, and structured outputs.

## Process

1. **Define task.** Classification, extraction, generation, reasoning, code.
2. **Choose technique.** Zero-shot, few-shot, chain-of-thought, ReAct.
3. **Write system prompt.** Role, constraints, output format.
4. **Add examples.** Input-output pairs for few-shot learning.
5. **Structure output.** JSON, XML, markdown for parsing.
6. **Test edge cases.** Ambiguous inputs, missing data, adversarial.
7. **Measure quality.** Accuracy, consistency, latency, cost.

## Output Format

### Prompt Template: [Task Name]

**Model:** GPT-4  
**Technique:** Few-shot with chain-of-thought  
**Accuracy:** 92% (100 test cases)  
**Avg Tokens:** 350 input, 150 output

---

## Zero-Shot Prompting

```
# Basic instruction
Classify this email as spam or not spam:
"Congratulations! You've won $1M. Click here to claim."

# Better: Add context and format
You are an email filter. Classify emails as "spam" or "not_spam".

Email: "Congratulations! You've won $1M. Click here to claim."
Classification:
```

---

## Few-Shot Prompting

```
Classify customer sentiment (positive, negative, neutral).

Example 1:
Review: "This product is amazing! Best purchase ever."
Sentiment: positive

Example 2:
Review: "Terrible quality. Broke after one day."
Sentiment: negative

Example 3:
Review: "It works as expected."
Sentiment: neutral

Now classify:
Review: "Great value for money, highly recommend!"
Sentiment:
```

**Best practices:**
- 3-5 examples optimal
- Cover edge cases
- Diverse examples

---

## Chain-of-Thought (CoT)

```
# Without CoT (often wrong)
Q: A store has 23 apples. They sell 15 and receive 30 more. How many now?
A: 38

# With CoT (more accurate)
Q: A store has 23 apples. They sell 15 and receive 30 more. How many now?
A: Let's think step-by-step:
1. Start: 23 apples
2. After selling: 23 - 15 = 8 apples
3. After receiving: 8 + 30 = 38 apples
Answer: 38 apples
```

### Self-Consistency CoT
```
Generate 5 different reasoning paths, pick most common answer.
Improves accuracy on complex reasoning tasks.
```

---

## Structured Output

### JSON Format
```
Extract information from this text as JSON:

Text: "John Smith, age 32, lives in New York. Email: john@example.com"

Output format:
{
  "name": string,
  "age": number,
  "city": string,
  "email": string
}

Response:
{
  "name": "John Smith",
  "age": 32,
  "city": "New York",
  "email": "john@example.com"
}
```

### XML Format
```
Extract entities and wrap in XML:

Text: "Apple Inc. announced iPhone 15 on September 12, 2023."

<entities>
  <organization>Apple Inc.</organization>
  <product>iPhone 15</product>
  <date>September 12, 2023</date>
</entities>
```

---

## ReAct (Reasoning + Acting)

```
You have access to tools: [search, calculate, lookup_database].
Use this format:

Thought: [reasoning about what to do]
Action: [tool to use]
Action Input: [input to tool]
Observation: [result from tool]
... (repeat Thought/Action/Observation as needed)
Answer: [final answer to user]

Question: What is the population of the capital of France?

Thought: I need to find the capital of France first.
Action: search
Action Input: "capital of France"
Observation: The capital of France is Paris.

Thought: Now I need the population of Paris.
Action: search
Action Input: "population of Paris"
Observation: Paris has approximately 2.2 million people.

Answer: The population of Paris, the capital of France, is approximately 2.2 million.
```

---

## Role Assignment

```
# Generic (weak)
Write a marketing email.

# Specific role (better)
You are an expert email marketer with 10 years experience in B2B SaaS.
Write a cold outreach email to a CTO about our AI-powered analytics platform.
Use a consultative tone, focus on ROI, keep under 150 words.
```

---

## Constraints & Guardrails

```
You are a medical Q&A assistant. Follow these rules:
1. Never provide diagnoses - recommend seeing a doctor
2. Cite medical sources for factual claims
3. If asked about drug dosages, refer to FDA guidelines
4. For emergencies, tell user to call 911
5. Refuse to provide advice on self-harm

Question: [user input]
Answer:
```

---

## Prompt Chaining

```
# Step 1: Extract entities
Extract company names, dates, and dollar amounts from this article.

[Article text]

# Step 2: Summarize (uses output from Step 1)
Based on these entities: [entities from Step 1]
Write a 2-sentence summary focusing on financial impact.

# Step 3: Classify sentiment
Rate the sentiment toward each company (positive/negative/neutral):
[Summary from Step 2]
```

---

## Function Calling

```python
# OpenAI function calling
import openai

functions = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    functions=functions,
    function_call="auto"
)

# Response includes function call:
{
  "function_call": {
    "name": "get_weather",
    "arguments": '{"location": "Paris", "unit": "celsius"}'
  }
}
```

---

## Evaluation Metrics

### Accuracy
```python
correct = 0
total = len(test_cases)

for case in test_cases:
    prediction = model.generate(case['input'])
    if prediction == case['expected']:
        correct += 1

accuracy = correct / total
```

### Consistency
```python
# Run same prompt 5 times, measure agreement
responses = [model.generate(prompt) for _ in range(5)]
consistency = len(set(responses)) / len(responses)
# 1.0 = identical, 0.2 = all different
```

### Cost per Request
```python
cost_per_1k_input_tokens = 0.03  # GPT-4
cost_per_1k_output_tokens = 0.06

cost = (input_tokens / 1000 * cost_per_1k_input) + \
       (output_tokens / 1000 * cost_per_1k_output)
```

---

## Prompt Templates (Python)

```python
from string import Template

prompt_template = Template("""
Classify this support ticket into one of: $categories

Ticket: $ticket_text

Category:
""")

prompt = prompt_template.substitute(
    categories="billing, technical, shipping, other",
    ticket_text="My credit card was charged twice."
)
```

### LangChain PromptTemplate
```python
from langchain import PromptTemplate

template = PromptTemplate(
    input_variables=["product", "sentiment"],
    template="Write a {sentiment} review for {product}"
)

prompt = template.format(product="iPhone", sentiment="positive")
```

---

## Testing & Iteration

```
1. Start simple (zero-shot)
2. Add examples if accuracy < 80%
3. Add chain-of-thought if reasoning task
4. Test edge cases
5. Measure cost vs quality trade-off
```

### A/B Test Prompts
```python
prompts = {
    'A': "Classify sentiment: {text}",
    'B': "You are a sentiment analyst. Classify: {text}",
    'C': "Rate sentiment (positive/negative/neutral): {text}"
}

for name, template in prompts.items():
    accuracy = evaluate_on_test_set(template, test_data)
    cost = estimate_cost(template, test_data)
    print(f"{name}: {accuracy:.2%} accuracy, ${cost:.4f} per request")
```

---

## Common Pitfalls

### ❌ Vague Instructions
```
Write something good about this product.
```

### ✅ Specific Instructions
```
Write a 100-word product description for this laptop.
Highlight: performance, battery life, portability.
Target audience: business professionals.
Tone: professional but approachable.
```

---

### ❌ No Output Format
```
Extract key points from this article.
```

### ✅ Structured Output
```
Extract key points as JSON:
{
  "main_topic": "...",
  "key_points": ["point1", "point2", "point3"],
  "conclusion": "..."
}
```

---

### ❌ Assuming Context
```
What do you think?
```

### ✅ Provide Context
```
You are reviewing a PR that adds caching to our API.
Code: [code snippet]
Review for: performance, security, maintainability.
```

## Rules

- Be specific, not vague — "professional tone" not "good writing."
- Use examples for complex tasks — few-shot beats zero-shot for accuracy.
- Chain-of-thought for reasoning — "think step-by-step" improves logic.
- Structure output for parsing — JSON/XML beats free text.
- Test with edge cases — ambiguous, missing data, adversarial.
- Measure cost vs quality — GPT-4 expensive, GPT-3.5 cheap, find balance.
- Role assignment improves quality — "expert email marketer" > generic.
- Add constraints for safety — prevent harmful, biased, or wrong outputs.
- Iterate based on failures — review wrong answers, update prompt.
- Version control prompts — track changes, A/B test, roll back if worse.
