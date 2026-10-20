# Copilot Instructions: Ai Research Automation
Description: A skill enabling AI agents to autonomously conduct machine learning research, implement ideas from papers/community, optimize models under constraints, and contribute high-quality submissions to research challenges.

# AI Research Automation Skill

## Overview

This skill enables AI agents to autonomously conduct machine learning research by:
1. Analyzing research papers and community contributions ([Core Concepts](references/core_concepts.md))
2. Designing and running optimized experiments ([Practical Guide](references/practical_guide.md))
3. Implementing solutions within competition constraints
4. Validating and submitting high-quality results

## Step-by-Step Workflow

1. **Information Gathering**
   - Scrape recent papers from arXiv/Conferences
   - Monitor community forums and GitHub repositories
   - Extract key techniques and implementations

2. **Idea Synthesis**
   - Combine promising approaches from different sources
   - Identify abandoned ideas worth revisiting
   - Generate novel combinations (see [Code Examples](references/code_examples.md) for implementation)

3. **Experiment Design**
   - Set up parameter search spaces
   - Configure resource constraints (GPU, memory, time)
   - Implement early stopping criteria

4. **Constraint Management**
   - Monitor model size/compute usage
   - Apply quantization/pruning as needed
   - Verify all competition rules are followed

5. **Quality Validation**
   - Run statistical significance tests
   - Check for overfitting
   - Verify implementation correctness
   - Ensure novelty (not duplicate work)

6. **Submission & Tracking**
   - Format submission per competition requirements
   - Track which ideas get adopted by others (H-index)
   - Log compute/resource usage metrics

## Best Practices

1. **Focus on execution quality** over quantity - Aiden's 28% acceptance rate vs community 5%
2. **Leverage human creativity** by implementing abandoned ideas
3. **Maintain strict quality gates** - only 47 of 2000 submissions passed review in Parameter Golf
4. **Optimize compute usage** - Aiden produced 15% of records with just 4% of total compute

## Common Pitfalls

1. **Data leakage**: As seen in the fraud detection example, loose APIs can cause test set contamination
2. **Over-optimization**: Chasing local maxima on the competition metric without real improvements
3. **Resource waste**: Brute-force parallelization without smart prioritization
4. **Isolation**: Not incorporating community ideas and feedback

## Validation Steps

1. **Statistical testing**: Ensure improvements are significant (p < 0.05)
2. **Overfitting checks**: Train/validation gap should be reasonable (<15% difference)
3. **Constraint verification**: Confirm model meets all competition requirements
4. **Impact measurement**: Track how often others build on your submissions (H-index)

## Implementation Notes

- Start with the experiment template from [Code Examples](references/code_examples.md)
- Use the quality gate implementation to filter submissions
- Constraint handlers should be competition-specific
- Monitor both performance metrics and community impact

## Reference Guides

### Code Examples

# Code Examples and Templates

## Experiment Template
```python
def run_experiment(idea_source, constraints):
    """
    Parameters:
    idea_source: dict with keys 'paper', 'community', 'original'
    constraints: dict with competition limits
    """
    # 1. Initialize model with base architecture
    model = initialize_model(constraints['base_architecture'])
    
    # 2. Apply modifications from idea sources
    if idea_source['paper']:
        model = apply_paper_technique(model, idea_source['paper'])
    
    # 3. Check constraints
    if get_model_size(model) > constraints['max_size']:
        model = quantize_model(model)  # Example constraint handling
    
    # 4. Train with monitoring
    trainer = Trainer(
        model=model,
        early_stopping=EarlyStopping(
            patience=3,
            min_delta=0.01
        ),
        resource_monitor=ResourceMonitor(
            max_gpu=constraints['gpu_limit']
        )
    )
    
    # 5. Validate before submission
    if validate_results(trainer.results):
        submit_to_leaderboard(trainer.results)
```

## Quality Gate Implementation
```python
def validate_results(results):
    """Multi-stage validation for submissions"""
    # 1. Statistical significance
    if not t_test(results['validation'], results['baseline'], p=0.05):
        return False
    
    # 2. Overfitting check
    if results['train_acc'] - results['val_acc'] > 0.15:
        return False
    
    # 3. Implementation verification
    if not verify_correct_implementation(results['model']):
        return False
    
    # 4. Novelty check (optional)
    if is_duplicate_submission(results['techniques']):
        return False
    
    return True
```

## Constraint Handler Example
```python
def handle_size_constraint(model, max_size):
    current_size = get_model_size(model)
    while current_size > max_size:
        # Try quantization first
        model = quantize_model(model)
        current_size = get_model_size(model)
        
        if current_size > max_size:
            # Remove least important layers
            model = prune_model(model)
            current_size = get_model_size(model)
            
    return model
```

### Core Concepts

# Core Concepts of AI Research Automation

Auto-research agents like Aiden demonstrate how AI systems can outperform humans in executing machine learning research tasks. Key concepts:

1. **Multi-agent self-improving systems**: The agent consists of multiple specialized components that read research papers, analyze community PRs, run experiments, and submit quality-controlled contributions. This mirrors how human research teams operate but with machine speed and precision.

2. **Quality gates**: Before submission, findings must pass rigorous validation checks. In the Parameter Golf challenge, only 28% of Aiden's submissions made the leaderboard - still 6x higher than human average - showing the importance of strict quality control.

3. **Idea synthesis**: The agent excels at combining ideas from disparate sources (papers, community discussions, failed attempts) and implementing them effectively. For example, it combined gated attention from a paper with a community member's tokenizer improvement to create a breakthrough solution.

4. **Constraint navigation**: Agents must work within competition constraints (like the 16MB file size limit in Parameter Golf). Aiden demonstrated this by developing quantization techniques when architectural improvements exceeded size limits.

5. **Community impact measurement**: Beyond raw scores, impact is measured through H-index style metrics tracking how often others build on your work. Aiden's H-index of 10 surpassed all human participants (next best was 7).

6. **Human-AI collaboration**: The system amplifies human creativity by executing on ideas that researchers abandoned due to implementation difficulty. This creates a symbiotic relationship where humans propose and agents dispose.

### Practical Guide

# Practical Guide to Implementing Auto-Research Agents

## System Architecture

1. **Information gathering module**: Scrapes research papers, GitHub repositories, and competition forums for ideas. Uses NLP to extract relevant techniques and implementations.

2. **Experiment pipeline**: Manages the full ML workflow:
   - Creates training scripts with hyperparameter ranges
   - Monitors resource usage (GPU, memory)
   - Implements early stopping for unpromising runs
   - Logs all results with version control

3. **Constraint manager**: Enforces competition rules like model size limits. For Parameter Golf, this included:
   - Quantization techniques when models grew too large
   - Architectural tradeoff analysis
   - Parameter efficiency optimizations

4. **Quality control**: Implements multiple validation checks:
   - Statistical significance testing
   - Overfitting detection
   - Implementation correctness verification
   - Peer-review simulation

## Operational Considerations

- **Compute management**: Aiden used just 4% of total competition compute while producing 15% of records
- **Parallelization strategy**: Focus on smart parallelization rather than brute force - prioritize promising directions
- **Noise reduction**: Maintain high signal-to-noise ratio in submissions (Aiden's 28% acceptance vs community 5% average)

## Performance Metrics

Track both direct competition metrics and broader impact:
1. Leaderboard position
2. Submission acceptance rate
3. H-index (how many submissions others build upon)
4. Compute efficiency (results per GPU-hour)
5. Novelty score (percentage of original contributions)

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[An AI Agent Became the #1 Contributor in OpenAI's Hiring Challenge — Zhengyao Jiang, Weco](https://www.youtube.com/watch?v=iCj_ATyThvc)** by AI Engineer