---
name: figmalint-design-system-auditing
description: AI-powered Figma plugin for auditing components for design system compliance, accessibility, and developer readiness
triggers:
  - audit my Figma component for design system compliance
  - analyze Figma components for accessibility issues
  - detect design tokens and hard-coded values in Figma
  - generate component documentation from Figma
  - fix design token usage in Figma components
  - export Figma component specs for developers
  - check Figma component readiness score
  - integrate FigmaLint into my workflow
---

# FigmaLint Design System Auditing Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection

## Overview

FigmaLint is an AI-powered Figma plugin that audits components for design system compliance, accessibility standards (WCAG), and developer handoff readiness. It analyzes components, detects design tokens vs hard-coded values, identifies missing interactive states, and generates structured documentation for developer handoff or AI code generation.

**Key capabilities:**
- Multi-provider AI analysis (Anthropic Claude, OpenAI GPT, Google Gemini)
- Design token detection and auto-fix binding
- Accessibility auditing (contrast, touch targets, focus indicators)
- Component state coverage analysis
- Auto-fix for tokens and layer naming
- Export to Markdown, AI Prompt, or JSON

## Installation

### From Figma Community

```bash
# Install directly from Figma Community
# Visit: https://www.figma.com/community/plugin/1521241390290871981/figmalint
# Click "Install" button
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/southleft/figmalint.git
cd figmalint

# Install dependencies
npm install

# Build the plugin
npm run build

# In Figma Desktop App:
# Plugins > Development > Import plugin from manifest
# Select manifest.json from the project root
```

### Development Commands

```bash
npm run dev          # Development build with watch mode
npm run build        # Production build
npm run lint         # TypeScript type checking
npm run clean        # Clean build artifacts
```

## Architecture Overview

FigmaLint follows a modular architecture:

```
src/
├── code.ts                      # Plugin entry point
├── types.ts                     # TypeScript definitions
├── api/
│   ├── claude.ts                # Prompt construction
│   └── providers/               # AI provider implementations
│       ├── anthropic.ts
│       ├── openai.ts
│       └── google.ts
├── core/
│   ├── component-analyzer.ts    # Component analysis
│   ├── token-analyzer.ts        # Token detection
│   └── consistency-engine.ts    # Design system checks
├── fixes/
│   ├── token-fixer.ts           # Auto-fix token binding
│   └── naming-fixer.ts          # Layer renaming
└── utils/
    └── figma-helpers.ts         # Figma API utilities
```

## Configuration

### API Provider Setup

FigmaLint supports three AI providers. Set up API keys using environment variables:

```typescript
// API keys are stored in Figma's local storage per provider
// Never hardcode keys in code

// For Anthropic Claude
process.env.ANTHROPIC_API_KEY

// For OpenAI GPT
process.env.OPENAI_API_KEY

// For Google Gemini
process.env.GOOGLE_API_KEY
```

### Provider Configuration

```typescript
// src/api/providers/types.ts
export interface AIProvider {
  id: string;
  name: string;
  models: AIModel[];
  call: (request: AIRequest) => Promise<AIResponse>;
  parseKey?: (key: string) => boolean;
}

// Available providers
const PROVIDERS = {
  anthropic: {
    models: ['claude-opus-4.5', 'claude-sonnet-4.5', 'claude-haiku-4.5']
  },
  openai: {
    models: ['gpt-5.2', 'gpt-5.2-pro', 'gpt-5-mini']
  },
  google: {
    models: ['gemini-3-pro', 'gemini-2.5-pro', 'gemini-2.5-flash']
  }
};
```

## Core Functionality

### Component Analysis

```typescript
// src/core/component-analyzer.ts
import { analyzeComponent } from './core/component-analyzer';

// Analyze a Figma component
async function analyzeComponentNode(node: ComponentNode) {
  const analysis = await analyzeComponent(node, {
    includeTokens: true,
    includeAccessibility: true,
    includeStates: true,
    includeNaming: true
  });
  
  return {
    metadata: analysis.metadata,
    tokens: analysis.tokenAnalysis,
    states: analysis.statesCoverage,
    accessibility: analysis.accessibilityChecks,
    readiness: analysis.readinessScore
  };
}
```

### Token Detection

```typescript
// src/core/token-analyzer.ts
import { analyzeTokens } from './core/token-analyzer';

interface TokenAnalysis {
  tokensByType: {
    colors: Array<{ name: string; value: string; boundNodes: string[] }>;
    spacing: Array<{ name: string; value: number; boundNodes: string[] }>;
    typography: Array<{ name: string; fontFamily: string; fontSize: number }>;
    effects: Array<{ name: string; type: string }>;
    borders: Array<{ name: string; strokeWeight: number }>;
  };
  hardCodedValues: {
    colors: Array<{ nodeId: string; value: string; property: string }>;
    spacing: Array<{ nodeId: string; value: number; property: string }>;
  };
  tokenAdoptionRate: number;
}

async function detectTokens(node: ComponentNode): Promise<TokenAnalysis> {
  return analyzeTokens(node, {
    includeLocalVariables: true,
    includeLibraryVariables: true,
    includeStyles: true,
    deduplicatePerNode: true
  });
}
```

### Auto-Fix Token Binding

```typescript
// src/fixes/token-fixer.ts
import { bindHardCodedValueToToken } from './fixes/token-fixer';

interface TokenBindingOptions {
  searchLocal: boolean;
  searchLibraries: boolean;
  fuzzyMatch: boolean;
  propertyAwareScoring: boolean;
}

// Bind a hard-coded color to a design token
async function fixColorToken(nodeId: string, hardCodedColor: string) {
  const result = await bindHardCodedValueToToken({
    nodeId,
    property: 'fills',
    hardCodedValue: hardCodedColor,
    tokenType: 'color',
    options: {
      searchLocal: true,
      searchLibraries: true,
      fuzzyMatch: true,
      propertyAwareScoring: true
    }
  });
  
  if (result.success) {
    console.log(`Bound to token: ${result.tokenName}`);
  }
}

// Bind spacing values
async function fixSpacingToken(nodeId: string, hardCodedSpacing: number) {
  await bindHardCodedValueToToken({
    nodeId,
    property: 'paddingLeft',
    hardCodedValue: hardCodedSpacing,
    tokenType: 'spacing',
    options: {
      searchLocal: true,
      searchLibraries: true,
      fuzzyMatch: true,
      propertyAwareScoring: true
    }
  });
}
```

### Layer Naming Auto-Fix

```typescript
// src/fixes/naming-fixer.ts
import { suggestLayerName, applyLayerRename } from './fixes/naming-fixer';

type NamingStrategy = 'semantic' | 'bem' | 'prefix' | 'kebab' | 'camel' | 'snake';

// Detect generic names and suggest semantic alternatives
async function fixLayerNaming(node: SceneNode, strategy: NamingStrategy = 'semantic') {
  const suggestion = suggestLayerName(node, strategy);
  
  if (suggestion.isGeneric) {
    console.log(`Generic name detected: "${suggestion.currentName}"`);
    console.log(`Suggested: "${suggestion.suggestedName}"`);
    
    // Apply the rename
    await applyLayerRename(node.id, suggestion.suggestedName);
  }
}

// Recognizes 30+ semantic layer types:
// icon, button, label, badge, avatar, card, header, footer,
// navigation, sidebar, modal, dropdown, input, checkbox, etc.
```

### Accessibility Auditing

```typescript
// Accessibility checks included in component analysis
interface AccessibilityChecks {
  contrastRatio: {
    pass: boolean;
    ratio: number;
    wcagLevel: 'AA' | 'AAA' | 'fail';
  };
  touchTargets: {
    pass: boolean;
    minSize: number;
    actualSize: { width: number; height: number };
  };
  focusIndicators: {
    pass: boolean;
    hasVisibleFocus: boolean;
  };
  fontSize: {
    pass: boolean;
    minSize: number;
    actualSize: number;
  };
}

async function checkAccessibility(node: ComponentNode) {
  const analysis = await analyzeComponent(node);
  const { accessibilityChecks } = analysis;
  
  if (!accessibilityChecks.contrastRatio.pass) {
    console.warn(`Contrast ratio: ${accessibilityChecks.contrastRatio.ratio} (fail)`);
  }
  
  if (!accessibilityChecks.touchTargets.pass) {
    console.warn(`Touch target too small: ${accessibilityChecks.touchTargets.actualSize.width}x${accessibilityChecks.touchTargets.actualSize.height}`);
  }
}
```

### Component State Detection

```typescript
// Detect missing interactive states
interface StatesCoverage {
  detected: string[];
  missing: string[];
  variants: Array<{
    name: string;
    properties: Record<string, string>;
  }>;
}

async function checkComponentStates(node: ComponentSetNode) {
  const analysis = await analyzeComponent(node);
  const { statesCoverage } = analysis;
  
  console.log('Detected states:', statesCoverage.detected);
  // Example: ['default', 'hover', 'pressed']
  
  console.log('Missing states:', statesCoverage.missing);
  // Example: ['focus', 'disabled', 'active']
  
  // Interactive states checked:
  // hover, focus, disabled, pressed, active, selected, error, loading
}
```

### AI-Powered Description Generation

```typescript
// Generate structured component description
interface ComponentDescription {
  summary: string;
  sections: {
    purpose: string;
    behavior: string;
    composition: string;
    usage: string;
    codeGenerationNotes: string;
  };
  nestedComponents: string[];
  currentDescription: string;
  matches: boolean;
}

async function generateDescription(node: ComponentNode, provider: string, model: string, apiKey: string) {
  const prompt = buildDescriptionPrompt(node);
  
  const response = await callAIProvider({
    provider,
    model,
    apiKey,
    prompt,
    systemPrompt: 'You are a design systems expert generating component documentation.'
  });
  
  return {
    summary: response.summary,
    sections: response.sections,
    nestedComponents: response.nestedComponents,
    matches: node.description === response.generatedDescription
  };
}
```

### Export Formats

```typescript
// Export component documentation
type ExportFormat = 'markdown' | 'ai-prompt' | 'json';

async function exportComponent(node: ComponentNode, format: ExportFormat) {
  const analysis = await analyzeComponent(node);
  
  switch (format) {
    case 'markdown':
      // Comprehensive documentation for design system sites
      return generateMarkdownExport(analysis);
      
    case 'ai-prompt':
      // Structured spec for AI code generation
      return generateAIPromptExport(analysis);
      
    case 'json':
      // Complete analysis data for programmatic use
      return JSON.stringify(analysis, null, 2);
  }
}

// Markdown export includes:
// - Component metadata and variants table
// - Properties API reference
// - Interactive states (pass/fail status)
// - Design token breakdown (tokens vs hard-coded)
// - Accessibility audit results
// - Component readiness score
// - AI interpretation
```

### Design Systems Chat

```typescript
// Multi-turn conversational interface
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

interface ChatContext {
  componentId: string;
  analysis: ComponentAnalysis;
  conversationHistory: ChatMessage[];
}

async function askAboutComponent(question: string, context: ChatContext) {
  const prompt = buildChatPrompt(question, context);
  
  const response = await callAIProvider({
    provider: context.provider,
    model: context.model,
    apiKey: process.env[`${context.provider.toUpperCase()}_API_KEY`],
    prompt,
    conversationHistory: context.conversationHistory
  });
  
  // Update conversation history
  context.conversationHistory.push(
    { role: 'user', content: question, timestamp: Date.now() },
    { role: 'assistant', content: response, timestamp: Date.now() }
  );
  
  return response;
}
```

## Common Patterns

### Full Component Audit Workflow

```typescript
async function auditComponent(componentNode: ComponentNode) {
  // 1. Analyze component
  const analysis = await analyzeComponent(componentNode, {
    includeTokens: true,
    includeAccessibility: true,
    includeStates: true,
    includeNaming: true
  });
  
  // 2. Check readiness score
  console.log(`Readiness Score: ${analysis.readinessScore}/100`);
  
  // 3. Identify issues
  const issues = [];
  
  if (analysis.tokenAnalysis.hardCodedValues.colors.length > 0) {
    issues.push(`${analysis.tokenAnalysis.hardCodedValues.colors.length} hard-coded colors`);
  }
  
  if (analysis.statesCoverage.missing.length > 0) {
    issues.push(`Missing states: ${analysis.statesCoverage.missing.join(', ')}`);
  }
  
  if (!analysis.accessibilityChecks.contrastRatio.pass) {
    issues.push('Contrast ratio fails WCAG standards');
  }
  
  // 4. Auto-fix issues
  if (analysis.tokenAnalysis.hardCodedValues.colors.length > 0) {
    for (const hardCoded of analysis.tokenAnalysis.hardCodedValues.colors) {
      await bindHardCodedValueToToken({
        nodeId: hardCoded.nodeId,
        property: hardCoded.property,
        hardCodedValue: hardCoded.value,
        tokenType: 'color'
      });
    }
  }
  
  // 5. Export documentation
  const markdown = await exportComponent(componentNode, 'markdown');
  const aiPrompt = await exportComponent(componentNode, 'ai-prompt');
  
  return { analysis, issues, markdown, aiPrompt };
}
```

### Batch Token Fixing

```typescript
async function fixAllTokens(componentNode: ComponentNode) {
  const analysis = await analyzeComponent(componentNode);
  const { hardCodedValues } = analysis.tokenAnalysis;
  
  // Fix all hard-coded colors
  for (const color of hardCodedValues.colors) {
    await bindHardCodedValueToToken({
      nodeId: color.nodeId,
      property: color.property,
      hardCodedValue: color.value,
      tokenType: 'color',
      options: {
        searchLocal: true,
        searchLibraries: true,
        fuzzyMatch: true,
        propertyAwareScoring: true
      }
    });
  }
  
  // Fix all hard-coded spacing
  for (const spacing of hardCodedValues.spacing) {
    await bindHardCodedValueToToken({
      nodeId: spacing.nodeId,
      property: spacing.property,
      hardCodedValue: spacing.value,
      tokenType: 'spacing',
      options: {
        searchLocal: true,
        searchLibraries: true,
        fuzzyMatch: true,
        propertyAwareScoring: true
      }
    });
  }
  
  console.log('All tokens fixed');
}
```

### Custom Accessibility Audit

```typescript
interface CustomAccessibilityRules {
  minContrastRatio: number;
  minTouchTargetSize: number;
  minFontSize: number;
  requireFocusIndicator: boolean;
}

async function customAccessibilityAudit(
  node: ComponentNode,
  rules: CustomAccessibilityRules
) {
  const analysis = await analyzeComponent(node);
  const results = [];
  
  // Contrast ratio
  if (analysis.accessibilityChecks.contrastRatio.ratio < rules.minContrastRatio) {
    results.push({
      type: 'contrast',
      severity: 'error',
      message: `Contrast ratio ${analysis.accessibilityChecks.contrastRatio.ratio} is below ${rules.minContrastRatio}`
    });
  }
  
  // Touch target size
  const { width, height } = analysis.accessibilityChecks.touchTargets.actualSize;
  if (width < rules.minTouchTargetSize || height < rules.minTouchTargetSize) {
    results.push({
      type: 'touch-target',
      severity: 'error',
      message: `Touch target ${width}x${height} is below minimum ${rules.minTouchTargetSize}px`
    });
  }
  
  // Font size
  if (analysis.accessibilityChecks.fontSize.actualSize < rules.minFontSize) {
    results.push({
      type: 'font-size',
      severity: 'warning',
      message: `Font size ${analysis.accessibilityChecks.fontSize.actualSize}px is below ${rules.minFontSize}px`
    });
  }
  
  // Focus indicator
  if (rules.requireFocusIndicator && !analysis.accessibilityChecks.focusIndicators.hasVisibleFocus) {
    results.push({
      type: 'focus',
      severity: 'error',
      message: 'Component missing visible focus indicator'
    });
  }
  
  return results;
}
```

## Troubleshooting

### API Provider Issues

```typescript
// Verify API key format
function validateApiKey(provider: string, key: string): boolean {
  const patterns = {
    anthropic: /^sk-ant-/,
    openai: /^sk-/,
    google: /^[A-Za-z0-9_-]+$/
  };
  
  return patterns[provider]?.test(key) ?? false;
}

// Test provider connection
async function testProviderConnection(provider: string, apiKey: string) {
  try {
    const response = await callAIProvider({
      provider,
      model: 'default',
      apiKey,
      prompt: 'Test',
      systemPrompt: 'Reply with "OK"'
    });
    return { success: true, response };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

### Token Binding Issues

```typescript
// Debug token search
async function debugTokenSearch(hardCodedValue: string, tokenType: string) {
  const localVars = await figma.variables.getLocalVariablesAsync();
  const libraryVars = await figma.variables.getLibraryVariablesAsync();
  
  console.log(`Searching for ${tokenType} matching:`, hardCodedValue);
  console.log(`Local variables: ${localVars.length}`);
  console.log(`Library variables: ${libraryVars.length}`);
  
  // Search with fuzzy matching
  const matches = findMatchingTokens(hardCodedValue, tokenType, {
    variables: [...localVars, ...libraryVars],
    fuzzyMatch: true,
    propertyAwareScoring: true
  });
  
  console.log('Matches found:', matches);
  return matches;
}
```

### Performance Optimization

```typescript
// Batch analyze multiple components
async function batchAnalyze(componentNodes: ComponentNode[]) {
  const results = await Promise.all(
    componentNodes.map(node => 
      analyzeComponent(node, {
        includeTokens: true,
        includeAccessibility: false, // Skip for performance
        includeStates: true,
        includeNaming: false
      })
    )
  );
  
  return results;
}

// Cache analysis results
const analysisCache = new Map<string, ComponentAnalysis>();

async function getCachedAnalysis(node: ComponentNode) {
  const cacheKey = `${node.id}-${node.lastModified}`;
  
  if (analysisCache.has(cacheKey)) {
    return analysisCache.get(cacheKey);
  }
  
  const analysis = await analyzeComponent(node);
  analysisCache.set(cacheKey, analysis);
  
  return analysis;
}
```

### Error Handling

```typescript
async function safeAnalyze(node: ComponentNode) {
  try {
    return await analyzeComponent(node);
  } catch (error) {
    if (error.message.includes('API key')) {
      console.error('API key invalid or missing');
      return { error: 'Invalid API key' };
    }
    
    if (error.message.includes('rate limit')) {
      console.error('Rate limit exceeded, retrying in 60s');
      await new Promise(resolve => setTimeout(resolve, 60000));
      return safeAnalyze(node);
    }
    
    if (error.message.includes('node not found')) {
      console.error('Component node deleted or inaccessible');
      return { error: 'Node not found' };
    }
    
    throw error;
  }
}
```

## Integration Examples

### CI/CD Pipeline Integration

```typescript
// Export component specs for automated testing
async function exportForCI(componentSetId: string) {
  const node = await figma.getNodeByIdAsync(componentSetId) as ComponentSetNode;
  const analysis = await analyzeComponent(node);
  
  return {
    componentId: node.id,
    componentName: node.name,
    readinessScore: analysis.readinessScore,
    tokenAdoption: analysis.tokenAnalysis.tokenAdoptionRate,
    accessibilityPasses: Object.values(analysis.accessibilityChecks).every(c => c.pass),
    missingStates: analysis.statesCoverage.missing,
    exportedAt: new Date().toISOString()
  };
}
```

### Design System Documentation Sync

```typescript
// Sync to external documentation platform
async function syncToDocumentation(componentNode: ComponentNode, platform: string) {
  const markdown = await exportComponent(componentNode, 'markdown');
  
  // Send to documentation platform API
  await fetch(`https://api.${platform}.com/components`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.DOCS_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: componentNode.name,
      content: markdown,
      updatedAt: new Date().toISOString()
    })
  });
}
```
