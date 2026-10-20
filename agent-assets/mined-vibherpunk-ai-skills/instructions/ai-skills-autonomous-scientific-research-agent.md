# Copilot Instructions: Autonomous Scientific Research Agent
Description: A skill for AI agents to autonomously conduct scientific research tasks, including hypothesis generation, experimentation, and iterative improvement using hierarchical problem decomposition and adversarial/collaborative loops.

## Overview
This skill enables you to autonomously conduct scientific research tasks by decomposing complex problems into hierarchical components, generating hypotheses, and iteratively improving through adversarial/collaborative loops. The core concepts are explained in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Problem Decomposition**: Break down the scientific problem into hierarchical components using structured prompts. See [Practical Guide](references/practical_guide.md) for detailed instructions.
2. **Hypothesis Generation**: Generate potential improvements for each component using adversarial/collaborative approaches. Use the prompt templates in [Code Examples](references/code_examples.md).
3. **Implementation**: Implement the generated hypotheses and run experiments.
4. **Evaluation**: Assess the results using predefined metrics and validate the improvements.
5. **Iteration**: Repeat the process, refining hypotheses based on evaluation results.

## Code/Prompt Templates
```python
# Prompt for hierarchical decomposition
prompt = "Decompose the problem of [specific scientific task] into its hierarchical components, including data, architecture, training, and metrics."

# Prompt for hypothesis generation
prompt = "Given the hierarchical components of [specific scientific task], generate potential improvements for each component."
```

## Best Practices
- **Structured Decomposition**: Always decompose problems into clear, hierarchical components to guide hypothesis generation.
- **Adversarial Collaboration**: Use multiple models to generate and critique hypotheses for better results.
- **Iterative Refinement**: Continuously refine hypotheses based on experimental results.

## Common Pitfalls
- **Saturation**: Avoid getting stuck in local optima by encouraging radical changes in hypotheses.
- **Incomplete Decomposition**: Ensure all relevant components are included in the hierarchical decomposition.

## Validation Steps
1. **Metric Evaluation**: Use predefined metrics to evaluate the success of implemented hypotheses.
2. **Peer Review**: Have another model review the results to ensure validity.
3. **Iterative Testing**: Continuously test and refine hypotheses to achieve optimal results.

For more detailed examples and pitfalls, refer to [Common Pitfalls](references/common_pitfalls.md).

## Reference Guides

### Code Examples

# Code Examples

## Prompt for Hierarchical Decomposition
```python
# Prompt to decompose a scientific problem into hierarchical components
prompt = "Decompose the problem of generating PET scans from CT scans into its hierarchical components, including data, architecture, training, and metrics."
```

## Prompt for Hypothesis Generation
```python
# Prompt to generate potential improvements for each component
prompt = "Given the hierarchical components of generating PET scans from CT scans, generate potential improvements for each component."
```

## Example of Adversarial Collaboration
```python
# Generate a hypothesis
hypothesis_prompt = "What changes can be made to the model architecture to improve PET scan generation?"
hypothesis = generate_hypothesis(hypothesis_prompt)

# Critique the hypothesis
critique_prompt = f"Critique the following hypothesis: {hypothesis}"
critique = critique_hypothesis(critique_prompt)
```

## Example of Iterative Refinement
```python
# Evaluate the implemented hypothesis
evaluation_prompt = "Evaluate the impact of changing the model architecture to 3D convolutions on PET scan generation."
evaluation = evaluate_hypothesis(evaluation_prompt)

# Refine the hypothesis based on evaluation results
refinement_prompt = f"Based on the evaluation results: {evaluation}, refine the hypothesis."
refined_hypothesis = refine_hypothesis(refinement_prompt)
```

These code examples provide practical templates for decomposing scientific problems, generating and critiquing hypotheses, and iteratively refining them based on evaluation results.

### Common Pitfalls

# Common Pitfalls

## Saturation in Hypothesis Generation
One common pitfall is getting stuck in local optima, where the model generates incremental improvements but fails to make radical changes. For example, in the CT to PET scan task, the model might continuously tweak hyperparameters without considering a shift from 2D to 3D convolutions.

## Incomplete Problem Decomposition
Another pitfall is incomplete decomposition, where not all relevant components are included in the hierarchical breakdown. For instance, neglecting data preprocessing in the CT to PET scan task can limit the model's ability to generate accurate PET scans.

## Lack of Adversarial Collaboration
Failing to use adversarial/collaborative approaches can result in less rigorous hypothesis generation and critique. Without multiple models generating and critiquing hypotheses, the process may lack diversity and thorough evaluation.

## Insufficient Iterative Refinement
Insufficient iterative refinement can halt progress prematurely. For example, stopping after the first round of hypothesis implementation and evaluation may miss further improvements that could be achieved through continuous refinement.

## Overlooking Validation Steps
Skipping validation steps, such as metric evaluation and peer review, can lead to invalid or suboptimal results. For instance, implementing a hypothesis without thorough evaluation may result in no real improvement or even degradation in performance.

By being aware of these common pitfalls, you can take proactive steps to avoid them, ensuring a more effective and efficient scientific research process.

### Core Concepts

# Core Concepts

## Hierarchical Problem Decomposition
Hierarchical problem decomposition involves breaking down complex scientific tasks into manageable components. This structured approach allows for systematic exploration and hypothesis generation. For example, in the task of generating PET scans from CT scans, the problem can be decomposed into data collection, model architecture, training procedures, and evaluation metrics.

## Hypothesis Generation
Hypothesis generation is the process of creating potential improvements or solutions for each component of the decomposed problem. This can be achieved through adversarial and collaborative approaches, where multiple models generate and critique hypotheses. For instance, in the CT to PET scan task, hypotheses might include changing the model architecture from 2D to 3D convolutions or improving data preprocessing techniques.

## Iterative Improvement
Iterative improvement involves continuously refining hypotheses based on experimental results. This loop of hypothesis generation, implementation, evaluation, and refinement drives the scientific process forward. For example, after implementing a 3D convolution hypothesis, the model's performance is evaluated, and further refinements are made based on the results.

## Adversarial/Collaborative Loops
Adversarial and collaborative loops involve using multiple models to generate and critique hypotheses. This approach ensures a diversity of ideas and rigorous evaluation. For example, one model might generate a hypothesis to change the loss function, while another model critiques the feasibility and potential impact of this change.

By understanding these core concepts, you can effectively conduct autonomous scientific research tasks, driving innovation and discovery in complex problem domains.

### Practical Guide

# Practical Guide

## Step-by-Step Problem Decomposition
1. **Identify the Main Problem**: Clearly define the scientific task you are addressing. For example, "Generate PET scans from CT scans using machine learning."
2. **Break Down into Components**: Decompose the main problem into hierarchical components such as data, architecture, training, and metrics.
3. **Document Each Component**: Create detailed documentation for each component, including its role and current state.

## Hypothesis Generation Process
1. **Review Components**: Examine each component of the decomposed problem to identify potential areas for improvement.
2. **Generate Hypotheses**: Use structured prompts to generate potential improvements for each component. For example, "What changes can be made to the model architecture to improve PET scan generation?"
3. **Critique Hypotheses**: Have another model critique the generated hypotheses to ensure feasibility and potential impact.

## Implementation and Evaluation
1. **Implement Hypotheses**: Apply the generated hypotheses to the scientific task.
2. **Run Experiments**: Conduct experiments to test the implemented hypotheses.
3. **Evaluate Results**: Use predefined metrics to assess the success of the hypotheses.

## Iterative Refinement
1. **Refine Hypotheses**: Based on the evaluation results, refine the hypotheses for further improvement.
2. **Repeat the Process**: Continuously iterate through the hypothesis generation, implementation, evaluation, and refinement loop.

By following this practical guide, you can systematically approach complex scientific tasks, driving continuous improvement and innovation.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Autonomous Agents for Scientific Tasks - Sina Shahandeh, Radicait](https://www.youtube.com/watch?v=XLEYtv3cMlw)** by AI Engineer