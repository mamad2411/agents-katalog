---
name: ace-context-engineering
description: Use for self-improving language models through evolving contexts. Enables LLMs to treat contexts as evolving playbooks that accumulate, refine, and organize strategies through generation, reflection, and curation. Triggers: context engineering, playbook evolution, self-improvement, agentic context, delta updates, grow-and-refine.
---

# ACE (Agentic Context Engineering)

A framework that enables large language models to self-improve by treating contexts as evolving playbooks that accumulate, refine, and organize strategies through a modular process of generation, reflection, and curation.

## When to Use

- **Context Collapse Prevention**: When iterative rewriting erodes details over time
- **Brevity Bias Solutions**: When contexts become too brief and lose nuance  
- **Self-Supervised Learning**: When adapting without labeled supervision
- **Continuous Improvement**: When needing to accumulate domain-specific knowledge
- **Efficient Adaptation**: When reducing latency and costs of model fine-tuning

## Core Architecture

### Three-Role System

1. **Generator** - Produces reasoning trajectories for new queries
   - Surfaces effective strategies and recurring pitfalls
   - Creates comprehensive problem-solving approaches
   - Identifies patterns in successful vs failed attempts

2. **Reflector** - Separates evaluation from curation
   - Extracts insights from execution outcomes
   - Tracks helpful/harmful counters for strategies
   - Provides structured feedback on approach effectiveness

3. **Curator** - Converts lessons into structured delta updates
   - Performs deterministic merging with de-duplication
   - Maintains helpful/harmful counters
   - Implements pruning and consolidation logic

## Key Features

### 🔄 Incremental Delta Updates
Instead of rewriting full prompts, ACE performs localized edits:
- Preserve prior knowledge while accumulating new insights
- Maintain detailed, domain-specific information
- Prevent context erosion through targeted modifications

### 📈 Grow-and-Refine Mechanism
Balances expansion with redundancy management:
- Steady context expansion through new insights
- Semantic similarity-based merging
- Automated pruning of redundant strategies

### 🎓 Self-Supervised Adaptation
Leverages natural execution feedback:
- No labeled supervision required
- Learns from task success/failure patterns
- Adapts to domain-specific challenges

## Quick Start Implementation

### Initialize ACE System

```python
# Basic ACE setup
ace_config = {
    'generator_model': 'gpt-4',
    'reflector_model': 'claude-3-haiku', 
    'curator_model': 'claude-3-sonnet',
    'max_tokens': 4096,
    'playbook_token_budget': 80000
}

# Initialize system
ace_system = ACEContextEngineering(ace_config)
```

### Process New Query

```python
# Generate response with current playbook
response = ace_system.process_query(
    query= user_input,
    current_playbook=existing_context
)

# Reflect on outcome and update playbook
if execution_feedback:
    updated_playbook = ace_system.reflect_and_update(
        query= user_input,
        response= response,
        feedback= execution_feedback,
        playbook= existing_playbook
    )
```

## Playbook Structure

Evolving contexts follow this structured format:

```
## STRATEGIES & INSIGHTS
[str-00001] helpful=5 harmful=0 :: Always verify data types before processing
[str-00002] helpful=3 harmful=1 :: Consider edge cases in financial data
[str-00003] helpful=8 harmful=0 :: Use type hints for better code clarity

## PATTERNS & TEMPLATES
[pat-00004] helpful=6 harmful=0 :: For API calls: validate -> request -> handle -> log
[pat-00005] helpful=4 harmful=2 :: Database queries: parameterize -> batch -> index

## COMMON MISTAKES TO AVOID
[mis-00006] helpful=7 harmful=0 :: Don't forget timezone conversions in date handling
[mis-00007] helpful=5 harmful=1 :: Avoid hardcoded environment-specific values

## DOMAIN KNOWLEDGE
[dom-00008] helpful=9 harmful=0 :: Financial calculations require decimal precision
[dom-00009] helpful=6 harmful=0 :: Medical data needs HIPAA compliance checks
```

### Bullet Management

Each insight includes:
- **ID**: `[section_slug-00000]` for tracking and versioning
- **Counters**: `helpful=X harmful=Y` updated through reflection
- **Content**: `:: actual strategy, pattern, or knowledge`

## Performance Benefits

### Efficiency Improvements
- **82.3% lower latency** compared to traditional fine-tuning approaches
- **75.1% fewer rollouts** needed for adaptation
- **91.5% cost reduction** in online learning scenarios

### Accuracy Gains
- **+10.6% improvement** on agent tasks (AppWorld benchmarks)
- **+8.6% improvement** on domain-specific tasks (FiNER, XBRL)
- **Matches GPT-4.1 performance** using smaller open-source models

## Integration Patterns

### For Development Workflows

```python
# Code review with ACE context
code_review_prompt = f"""
Review this code using the evolved playbook:

{current_playbook}

Code to review:
{code_snippet}

Focus on patterns from the playbook that apply to this code.
"""
```

### For Domain Adaptation

```python
# Specialize playbook for specific domain
domain_playbook = ace_system.specialize_playbook(
    base_playbook=general_playbook,
    domain_examples=domain_specific_data,
    specialization_iterations=5
)
```

### For Continuous Learning

```python
# Real-time playbook updates
class LearningLoop:
    def __init__(self):
        self.ace = ACEContextEngineering()
        self.playbook = initial_playbook
        
    def process_and_learn(self, query, execution_result):
        # Generate using current knowledge
        response = self.ace.generate(query, self.playbook)
        
        # Execute and reflect
        if execution_result.success:
            self.playbook = self.ace.update_playbook(
                query, response, execution_result, self.playbook
            )
        
        return response
```

## Advanced Features

### Bullet Analysis Engine
```python
# Semantic similarity for deduplication
similarity_threshold = 0.9
duplicates = ace_system.find_similar_bullets(
    new_bullets, 
    existing_playbook, 
    similarity_threshold
)

# Merge overlapping insights
merged = ace_system.merge_bullets(duplicates)
```

### Multi-Model Coordination
```python
# Specialized models for different roles
models = {
    'generator': 'gpt-4',           # Creative reasoning
    'reflector': 'claude-3-sonnet',  # Analytical reflection  
    'curator': 'claude-3-haiku'      # Efficient organization
}

ace_system = ACEContextEngineering(models=models)
```

### Performance Monitoring
```python
# Track playbook effectiveness
metrics = ace_system.analyze_playbook_performance(
    playbook=current_playbook,
    test_queries=benchmark_set,
    metrics=['accuracy', 'latency', 'token_efficiency']
)
```

## Usage Patterns

### 1. Offline Adaptation
- Prepare training dataset with examples
- Run multi-epoch training with periodic evaluation
- Save best-performing playbook version

### 2. Online Adaptation  
- Start with existing playbook
- Update incrementally with each new query
- Monitor performance drift and retrain if needed

### 3. Evaluation Mode
- Compare playbook performance against baseline
- Test on held-out benchmark set
- Analyze improvement patterns and gaps

## Integration with Existing Skills

This ACE skill enhances and works with:
- **spawn-team** - Evolve development playbooks for full-stack projects
- **continuous-learning-v2** - Provide structured approach to instinct evolution
- **writing-skills** - Improve skill creation through context accumulation
- **agent-ui** - Enhance agent interactions with evolved contexts

## Configuration Options

```python
config = {
    # Model selection
    'generator_model': 'gpt-4',
    'reflector_model': 'claude-3-sonnet', 
    'curator_model': 'claude-3-haiku',
    
    # Learning parameters
    'max_num_rounds': 3,              # Reflection iterations
    'curator_frequency': 1,             # Update frequency
    'playbook_token_budget': 80000,      # Context size limit
    
    # Quality control
    'helpful_threshold': 0.7,           # Minimum helpful ratio
    'similarity_threshold': 0.9,          # Deduplication threshold
    'min_examples_for_insight': 3,        # Evidence requirement
}
```

## Monitoring and Maintenance

### Performance Tracking
- Monitor helpful/harmful ratios over time
- Track playbook size growth and pruning effectiveness
- Measure accuracy improvements on benchmark sets

### Quality Assurance
- Regular evaluation on test suites
- Manual review of high-impact insights
- A/B testing against previous playbook versions

### Evolution Management
- Archive old playbook versions
- Track lineage of insight evolution
- Export/import playbook for sharing

## Advanced Applications

### Multi-Domain Playbooks
```python
# Specialized sub-playbooks
domains = {
    'finance': finance_playbook,
    'healthcare': healthcare_playbook,
    'legal': legal_playbook
}

# Domain-aware generation
response = ace_system.generate_with_context(
    query=query,
    domain=detect_domain(query),
    specialized_playbooks=domains
)
```

### Collaborative Learning
```python
# Merge playbooks from multiple sources
community_playbook = ace_system.merge_playbooks([
    user_playbook,
    team_playbook, 
    community_best_practices
])

# Weight insights by source reliability
weighted_playbook = ace_system.weight_insights(
    playbook=community_playbook,
    source_weights={'personal': 0.6, 'team': 0.3, 'community': 0.1}
)
```

---

*ACE transforms static contexts into living knowledge bases that evolve and improve through experience, preventing context collapse while enabling continuous, self-supervised learning.*