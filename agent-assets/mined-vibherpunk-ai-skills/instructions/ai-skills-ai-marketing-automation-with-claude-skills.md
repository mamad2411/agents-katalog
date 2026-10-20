# Copilot Instructions: Ai Marketing Automation With Claude Skills
Description: Automate marketing tasks using Claude Skills for copywriting, design, video repurposing, and research. This skill provides a comprehensive workflow to streamline marketing operations.

## Overview
This skill leverages Claude Skills to automate various marketing tasks, including copywriting, design, video repurposing, and research. By following the detailed workflow, you can streamline your marketing operations and improve efficiency.

## Core Concepts
- **Claude Skills**: Reusable instruction sets for Claude to perform specific tasks.
- **Voice Skill**: Drafts copy in your tone of voice, adapting to different communication channels.
- **Newsletter Skill**: Helps create newsletters based on your unique insights and beliefs.
- **Design Skills**: Automates the creation of presentations and social media carousels.
- **Video Repurposing Skill**: Cuts long-form videos into short clips for social media platforms.
- **Research Skills**: Provides market intelligence and customer insights.

For more details, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Set Up Claude Skills**: Download and install the necessary skills from the provided link.
2. **Customize Voice Skill**: Use the Voice Profile Builder Skill to create a voice guide tailored to your tone.
3. **Create Newsletters**: Utilize the Newsletter Skill to generate newsletters based on your unique insights.
4. **Automate Designs**: Use the Instant UI Skill and Carousel Builder Skill to create presentations and social media carousels.
5. **Repurpose Videos**: Employ the Video Repurposing Skill to cut long-form videos into short clips.
6. **Conduct Research**: Run the Market Intelligence Report and Customer Intelligence Report Skills to gather insights.

For a detailed guide, refer to [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates
```markdown
### Voice Profile Builder Skill
Prompt: "Who are you building this for, for yourself or someone else?"

### Newsletter Skill
Prompt: "Repurpose this video, I use the skill and give it my YouTube link."

### Video Repurposing Skill
Prompt: "Use the video repurposing skill to make a 2 to 3 minute clip of this YouTube video."

For more examples, see [Code Examples](references/code_examples.md).
```

## Best Practices and Common Pitfalls
- **Best Practices**:
  - Use ample data to train your Voice Skill for better tone adaptation.
  - Incorporate human-in-the-loop processes to guide AI-generated content.
  - Keep design skills specific to one use case for better results.
- **Common Pitfalls**:
  - Avoid generic AI-generated content by providing unique insights.
  - Ensure connectors like Apify and Firecrawl are properly set up for research tasks.

For more insights, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing
- **Voice Skill**: Test by drafting emails and social media posts to ensure they sound like you.
- **Newsletter Skill**: Verify the newsletter content aligns with your beliefs and lessons.
- **Design Skills**: Check the generated presentations and carousels for visual consistency.
- **Video Repurposing Skill**: Review the short clips for coherence and alignment with the original video.
- **Research Skills**: Ensure the market intelligence and customer insights reports are accurate and relevant.

## References
```json
[
  {
    "filename": "core_concepts.md",
    "content": "## Core Concepts\nClaude Skills are reusable instruction sets that enable Claude to perform specific tasks efficiently. These skills can be customized to automate various marketing operations, including copywriting, design, video repurposing, and research. The Voice Skill is particularly valuable as it drafts copy in your tone of voice, adapting to different communication channels like email, LinkedIn, and social media. The Newsletter Skill helps create newsletters based on your unique insights and beliefs, ensuring the content is not generic. Design Skills automate the creation of presentations and social media carousels, making it easier to produce visually appealing content quickly. The Video Repurposing Skill cuts long-form videos into short clips suitable for social media platforms, adding captions and transitions automatically. Research Skills provide market intelligence and customer insights, helping you stay updated with industry trends and understand customer pain points and wins."
  },
  {
    "filename": "practical_guide.md",
    "content": "## Practical Guide\nTo effectively use Claude Skills for marketing automation, follow these steps:\n1. **Set Up Claude Skills**: Download and install the necessary skills from the provided link. Ensure you have the required connectors like Apify and Firecrawl for research tasks.\n2. **Customize Voice Skill**: Use the Voice Profile Builder Skill to create a voice guide tailored to your tone. Provide ample data, including email replies, social media content, and audio transcriptions, to train the skill effectively.\n3. **Create Newsletters**: Utilize the Newsletter Skill to generate newsletters based on your unique insights. Use a values and beliefs document to inspire content and follow a human-in-the-loop process to guide the creation.\n4. **Automate Designs**: Use the Instant UI Skill and Carousel Builder Skill to create presentations and social media carousels. Keep design skills specific to one use case for better results and ensure you have example images in the reference file for consistent style.\n5. **Repurpose Videos**: Employ the Video Repurposing Skill to cut long-form videos into short clips. Use the code tab to run the skill and install necessary packages like FFmpeg, Whisper, and Remotion.\n6. **Conduct Research**: Run the Market Intelligence Report and Customer Intelligence Report Skills to gather insights. Schedule these tasks to run automatically and customize the sources you want to track."
  },
  {
    "filename": "code_examples.md",
    "content": "## Code Examples\n### Voice Profile Builder Skill\nPrompt: \"Who are you building this for, for yourself or someone else?\"\n\n### Newsletter Skill\nPrompt: \"Repurpose this video, I use the skill and give it my YouTube link.\"\n\n### Video Repurposing Skill\nPrompt: \"Use the video repurposing skill to make a 2 to 3 minute clip of this YouTube video.\"\n\n### Market Intelligence Report\nPrompt: \"Run the market intelligence report always at the day's start.\"\n\n### Customer Intelligence Report\nPrompt: \"Run the customer intelligence report on a weekly basis.\"\n\n### Topic Research Skill\nPrompt: \"I want to start setting up and working more with local LLM models, and potentially want to do a video around it. Do some research on the easiest way to use these models in a good harness, and also look which of their models I could actually run locally on my MacBook realistically.\"\n\n### Marketing Analytics Skill\nPrompt: \"Run the marketing analytics skill every day.\"\n\nThese prompts are designed to help you quickly get started with Claude Skills for marketing automation. Customize them as needed to fit your specific use cases."
  },
  {
    "filename": "common_pitfalls.md",
    "content": "## Common Pitfalls\nWhen using Claude Skills for marketing automation, be aware of the following common pitfalls:\n1. **Generic AI-Generated Content**: Avoid letting AI generate content entirely on its own. Always incorporate your unique insights and beliefs to ensure the content is not generic.\n2. **Insufficient Data for Voice Skill**: The Voice Skill requires ample data to mimic your tone effectively. Ensure you provide enough examples, including email replies, social media content, and audio transcriptions.\n3. **Broad Design Skills**: Keep design skills specific to one use case. Trying to make a skill too broad can result in inconsistent and low-quality outputs.\n4. **Improper Connector Setup**: Ensure connectors like Apify and Firecrawl are properly set up for research tasks. Without these, you may not be able to scrape necessary data from social media and other websites.\n5. **Lack of Human-in-the-Loop Processes**: Always incorporate human-in-the-loop processes to guide AI-generated content. This ensures the content aligns with your goals and preferences.\n6. **Inconsistent Validation**: Regularly test and validate the outputs of each skill to ensure they meet your standards. This includes checking the tone of voice in copy, the visual consistency of designs, and the coherence of repurposed videos."
  }
]
```

## Reference Guides

### Code Examples

## Code Examples
### Voice Profile Builder Skill
Prompt: "Who are you building this for, for yourself or someone else?"

### Newsletter Skill
Prompt: "Repurpose this video, I use the skill and give it my YouTube link."

### Video Repurposing Skill
Prompt: "Use the video repurposing skill to make a 2 to 3 minute clip of this YouTube video."

### Market Intelligence Report
Prompt: "Run the market intelligence report always at the day's start."

### Customer Intelligence Report
Prompt: "Run the customer intelligence report on a weekly basis."

### Topic Research Skill
Prompt: "I want to start setting up and working more with local LLM models, and potentially want to do a video around it. Do some research on the easiest way to use these models in a good harness, and also look which of their models I could actually run locally on my MacBook realistically."

### Marketing Analytics Skill
Prompt: "Run the marketing analytics skill every day."

These prompts are designed to help you quickly get started with Claude Skills for marketing automation. Customize them as needed to fit your specific use cases.

### Common Pitfalls

## Common Pitfalls
When using Claude Skills for marketing automation, be aware of the following common pitfalls:
1. **Generic AI-Generated Content**: Avoid letting AI generate content entirely on its own. Always incorporate your unique insights and beliefs to ensure the content is not generic.
2. **Insufficient Data for Voice Skill**: The Voice Skill requires ample data to mimic your tone effectively. Ensure you provide enough examples, including email replies, social media content, and audio transcriptions.
3. **Broad Design Skills**: Keep design skills specific to one use case. Trying to make a skill too broad can result in inconsistent and low-quality outputs.
4. **Improper Connector Setup**: Ensure connectors like Apify and Firecrawl are properly set up for research tasks. Without these, you may not be able to scrape necessary data from social media and other websites.
5. **Lack of Human-in-the-Loop Processes**: Always incorporate human-in-the-loop processes to guide AI-generated content. This ensures the content aligns with your goals and preferences.
6. **Inconsistent Validation**: Regularly test and validate the outputs of each skill to ensure they meet your standards. This includes checking the tone of voice in copy, the visual consistency of designs, and the coherence of repurposed videos.

### Core Concepts

## Core Concepts
Claude Skills are reusable instruction sets that enable Claude to perform specific tasks efficiently. These skills can be customized to automate various marketing operations, including copywriting, design, video repurposing, and research. The Voice Skill is particularly valuable as it drafts copy in your tone of voice, adapting to different communication channels like email, LinkedIn, and social media. The Newsletter Skill helps create newsletters based on your unique insights and beliefs, ensuring the content is not generic. Design Skills automate the creation of presentations and social media carousels, making it easier to produce visually appealing content quickly. The Video Repurposing Skill cuts long-form videos into short clips suitable for social media platforms, adding captions and transitions automatically. Research Skills provide market intelligence and customer insights, helping you stay updated with industry trends and understand customer pain points and wins.

### Practical Guide

## Practical Guide
To effectively use Claude Skills for marketing automation, follow these steps:
1. **Set Up Claude Skills**: Download and install the necessary skills from the provided link. Ensure you have the required connectors like Apify and Firecrawl for research tasks.
2. **Customize Voice Skill**: Use the Voice Profile Builder Skill to create a voice guide tailored to your tone. Provide ample data, including email replies, social media content, and audio transcriptions, to train the skill effectively.
3. **Create Newsletters**: Utilize the Newsletter Skill to generate newsletters based on your unique insights. Use a values and beliefs document to inspire content and follow a human-in-the-loop process to guide the creation.
4. **Automate Designs**: Use the Instant UI Skill and Carousel Builder Skill to create presentations and social media carousels. Keep design skills specific to one use case for better results and ensure you have example images in the reference file for consistent style.
5. **Repurpose Videos**: Employ the Video Repurposing Skill to cut long-form videos into short clips. Use the code tab to run the skill and install necessary packages like FFmpeg, Whisper, and Remotion.
6. **Conduct Research**: Run the Market Intelligence Report and Customer Intelligence Report Skills to gather insights. Schedule these tasks to run automatically and customize the sources you want to track.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[11 Claude Skills That Automate My Entire Marketing](https://www.youtube.com/watch?v=x_EO0Dz1p7g)** by Ben AI