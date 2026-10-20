# Copilot Instructions: Multimodal Ai Interaction With Gemini 3.5 Flash
Description: Master the use of Gemini 3.5 Flash for multimodal AI tasks, including image analysis, video understanding, document processing, and structured data extraction. Learn best practices, pitfalls, and workflows to maximize efficiency and accuracy.

### Overview
Gemini 3.5 Flash is a powerful multimodal AI model that excels in tasks involving image analysis, video understanding, document processing, and structured data extraction. This skill will guide you through the core concepts and practical workflows to leverage Gemini 3.5 Flash effectively.

### Core Concepts
Before diving into the workflows, it's essential to understand the core concepts of multimodal AI interaction. Refer to [Core Concepts](references/core_concepts.md) for a detailed explanation.

### Step-by-Step Workflow
1. **Image Analysis**
   - Upload an image to the Gemini app.
   - Use the following prompt template:
     ```
     Look at everything in this image and provide a detailed analysis. Include any relevant steps or actions based on the content.
     ```
   - Validate the output by cross-checking with the actual image.

2. **Video Understanding**
   - Drag and drop a video file directly into the Gemini app.
   - Use the following prompt template:
     ```
     Give me the top five insights from this video with exact timestamps. Then find the data table shown around the 23-minute mark and recreate it as a Python chart.
     ```
   - Validate the insights by checking them against the actual video.

3. **Document Processing**
   - Upload a document to AI Studio.
   - Use the following prompt template:
     ```
     Act as a contract lawyer. Read this entire agreement and flag every hidden fee, automatic renewal clause, and penalty that a client could miss on a first read.
     ```
   - Switch the thinking level from low to high for more accurate results.

4. **Structured Data Extraction**
   - Upload multiple receipt photos to AI Studio.
   - Define your schema visually in the structured output panel.
   - Use the following prompt template:
     ```
     Extract clean structured data from all these receipts without writing a single line of API code.
     ```
   - Validate the JSON output for accuracy.

### Code/Prompt Snippets
Refer to [Code Examples](references/code_examples.md) for detailed code snippets and prompt templates.

### Best Practices
- Always validate the output by cross-checking with the actual content.
- Use high thinking levels for tasks requiring high accuracy.
- Keep your prompts specific to stay on track.

### Common Pitfalls
- Avoid using low thinking levels for critical tasks.
- Be cautious of the default thinking level change from high to medium.
- Validate long context retrieval manually.

### Validation and Testing
- Cross-check insights with actual video content.
- Validate JSON output against the original receipts.
- Manually verify long context retrieval.

For more detailed guidelines, refer to [Practical Guide](references/practical_guide.md).

## Reference Guides

### Code Examples

### Code Examples and Prompt Templates

This document provides detailed code snippets and prompt templates for using Gemini 3.5 Flash in various workflows.

#### Image Analysis
```
Look at everything in this image and provide a detailed analysis. Include any relevant steps or actions based on the content.
```

#### Video Understanding
```
Give me the top five insights from this video with exact timestamps. Then find the data table shown around the 23-minute mark and recreate it as a Python chart.
```

#### Document Processing
```
Act as a contract lawyer. Read this entire agreement and flag every hidden fee, automatic renewal clause, and penalty that a client could miss on a first read.
```

#### Structured Data Extraction
```
Extract clean structured data from all these receipts without writing a single line of API code.
```

#### Python Chart Recreation
```python
import matplotlib.pyplot as plt

# Example data
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 40]

# Plotting the chart
plt.plot(x, y)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Sample Chart')
plt.show()
```

These examples and templates will help you get started with Gemini 3.5 Flash in your workflows.

### Core Concepts

### Core Concepts of Multimodal AI Interaction

Multimodal AI interaction involves the use of AI models that can process and understand multiple types of data inputs, such as images, videos, and text. Gemini 3.5 Flash is a prime example of such a model, offering capabilities that span across various data types.

#### Key Features
1. **Image Analysis**: Gemini 3.5 Flash can analyze images to provide detailed insights and actionable steps. For example, it can identify objects in a fridge and suggest recipes based on the available ingredients.
2. **Video Understanding**: The model can process long videos to extract key insights and recreate data tables as Python charts.
3. **Document Processing**: It can read and analyze long documents, flagging important clauses and penalties in legal contracts.
4. **Structured Data Extraction**: Gemini 3.5 Flash can extract structured data from receipts and other documents, outputting clean JSON without the need for additional API code.

#### Practical Applications
- **Recipe Generation**: Upload a photo of your fridge contents and get a detailed recipe.
- **Video Summarization**: Drop a long video into the Gemini app and receive timestamped insights.
- **Legal Document Review**: Upload a contract and get a detailed analysis of hidden fees and penalties.
- **Expense Tracking**: Extract structured data from multiple receipts for easy expense tracking.

Understanding these core concepts is essential for leveraging the full potential of Gemini 3.5 Flash in various workflows.

### Practical Guide

### Practical Guide to Using Gemini 3.5 Flash

This guide provides detailed steps and best practices for using Gemini 3.5 Flash in various workflows.

#### Image Analysis
1. **Upload Image**: Use the Gemini app to upload an image.
2. **Prompt**: Use a specific prompt to get detailed analysis.
3. **Validate**: Cross-check the output with the actual image.

#### Video Understanding
1. **Drag and Drop**: Drop a video file directly into the Gemini app.
2. **Prompt**: Use a prompt to extract insights and recreate data tables.
3. **Validate**: Check the insights against the actual video.

#### Document Processing
1. **Upload Document**: Upload a document to AI Studio.
2. **Prompt**: Use a prompt to flag important clauses and penalties.
3. **Switch Thinking Level**: Change the thinking level from low to high for more accurate results.

#### Structured Data Extraction
1. **Upload Receipts**: Upload multiple receipt photos to AI Studio.
2. **Define Schema**: Set up fields visually in the structured output panel.
3. **Prompt**: Use a prompt to extract structured data.
4. **Validate**: Check the JSON output for accuracy.

#### Best Practices
- **Validation**: Always validate the output by cross-checking with the actual content.
- **Thinking Levels**: Use high thinking levels for tasks requiring high accuracy.
- **Specific Prompts**: Keep your prompts specific to stay on track.

#### Common Pitfalls
- **Low Thinking Levels**: Avoid using low thinking levels for critical tasks.
- **Default Thinking Level**: Be cautious of the default thinking level change from high to medium.
- **Long Context Retrieval**: Validate long context retrieval manually.

Following this guide will help you maximize the efficiency and accuracy of your workflows with Gemini 3.5 Flash.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[NEW Gemini Features Explained — How to Use Google’s Latest AI Upgrade](https://www.youtube.com/watch?v=kn9Gh5HWqQs)** by AI Master