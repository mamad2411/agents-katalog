---
name: agent-plugin-implementation-extension
description: Implement custom agents in TypeScript as VS Code extensions for complex workflows that require custom tools, dynamic behavior, or programmatic agent registration.
---

# Agent Implementation: Extension

## Specialization

Develop a VS Code extension in TypeScript to register custom agents programmatically when agents require:
- Custom tools (beyond built-in and MCP).
- Dynamic agent behavior (runtime decisions, state management).
- Language model selection or model-switching logic.
- Tight integration with VS Code APIs (editors, workspace, commands).

## Supporting Activities

- Scaffold VS Code extension project (TypeScript, webpack, build pipeline).
- Implement agent registration via `vscode.lm.registerAgent()`.
- Define custom tools using `LanguageModelToolDefinition` interface.
- Handle tool invocation and result streaming.
- Manage agent state and multi-turn conversations.
- Debug and test agent behavior in VS Code.
- Package and publish extension as VSIX.

## Workflow

1. **Scaffold VS Code extension project**:
   - Prerequisites: Node.js 18+, npm, TypeScript compiler (`tsc`).
   - Initialize project:
     ```bash
     npm init -y
     npm install --save-dev @types/vscode @vscode/vsce typescript webpack webpack-cli ts-loader
     npm install vscode-languageclient  # If using language server
     ```
   - Create `src/extension.ts` entry point.
   - Create `tsconfig.json`:
     ```json
     {
       "compilerOptions": {
         "target": "ES2020",
         "module": "commonjs",
         "lib": ["ES2020"],
         "outDir": "./out",
         "rootDir": "./src",
         "strict": true,
         "esModuleInterop": true,
         "skipLibCheck": true,
         "forceConsistentCasingInFileNames": true
       },
       "include": ["src/**/*"],
       "exclude": ["node_modules"]
     }
     ```
   - Create `webpack.config.js` for bundling:
     ```javascript
     const path = require('path');

     module.exports = {
       target: 'node',
       entry: './src/extension.ts',
       output: {
         path: path.resolve(__dirname, 'out'),
         filename: 'extension.js',
         libraryTarget: 'commonjs2'
       },
       externals: {
         vscode: 'commonjs vscode'
       },
       resolve: {
         extensions: ['.ts', '.js']
       },
       module: {
         rules: [
           {
             test: /\.ts$/,
             use: 'ts-loader',
             exclude: /node_modules/
           }
         ]
       },
       devtool: 'source-map'
     };
     ```
   - Create `package.json` contribution point:
     ```json
     {
       "name": "my-agent-extension",
       "displayName": "My Custom Agent",
       "version": "1.0.0",
       "publisher": "mycompany",
       "engines": {
         "vscode": "^1.90.0"
       },
       "activationEvents": ["onLanguage:*"],
       "main": "./out/extension.js",
       "contributes": {
         "chatParticipants": [
           {
             "id": "my-agent",
             "name": "My Agent",
             "description": "Custom workflow automation"
           }
         ]
       },
       "scripts": {
         "vscode:prepublish": "webpack --mode production",
         "compile": "webpack --mode development",
         "watch": "webpack --mode development --watch"
       }
     }
     ```

2. **Define custom tool schema**:
   - Create tool metadata using `LanguageModelToolDefinition`:
     ```typescript
     const myTool: vscode.LanguageModelToolDefinition = {
       name: 'my-custom-tool',
       description: 'Analyzes code for security issues',
       inputSchema: {
         type: 'object' as const,
         properties: {
           filePath: {
             type: 'string',
             description: 'Path to the file to analyze'
           },
           checkType: {
             type: 'string',
             enum: ['vulnerability', 'performance', 'style'],
             description: 'Type of security check'
           }
         },
         required: ['filePath']
       }
     };
     ```

3. **Implement tool handler**:
   - Implement `ILanguageModelTool` interface:
     ```typescript
     class MyCustomTool implements vscode.ILanguageModelTool {
       async invoke(
         invocation: vscode.LanguageModelToolInvocationOptions,
         token: vscode.CancellationToken
       ): Promise<vscode.LanguageModelToolResult> {
         const { filePath, checkType } = invocation.input as Record<string, string>;

         // Input validation
         if (!filePath || typeof filePath !== 'string') {
           return {
             content: [{ type: 'text', text: 'Error: Invalid filePath' }]
           };
         }

         try {
           // Fetch and analyze file
           const uri = vscode.Uri.file(filePath);
           const fileContent = await vscode.workspace.fs.readFile(uri);
           const text = new TextDecoder().decode(fileContent);

           // Perform analysis
           const issues = analyzeForVulnerabilities(text, checkType);

           // Return results
           return {
             content: [{
               type: 'text',
               text: JSON.stringify(issues, null, 2)
             }]
           };
         } catch (error) {
           return {
             content: [{
               type: 'text',
               text: `Error analyzing file: ${error instanceof Error ? error.message : String(error)}`
             }]
           };
         }
       }
     }
     ```

4. **Implement agent handler**:
   - Implement `vscode.ChatAgentStream` handler:
     ```typescript
     class MyAgent implements vscode.IChatAgentImplementation {
       async invoke(
         request: vscode.ChatAgentRequest,
         progress: (parts: vscode.ChatProgress[]) => void,
         history: vscode.ChatAgentHistoryEntry[],
         token: vscode.CancellationToken
       ): Promise<vscode.ChatAgentResult> {
         // Validate request
         if (!request.prompt || request.prompt.length === 0) {
           return {
             exitCode: 1,
             message: 'No prompt provided'
           };
         }

         // Process user prompt (1-10 tool calls typical)
         progress([{
           kind: vscode.ChatAgentProgressKind.MarkdownContent,
           content: '📋 Analyzing code...'
         }]);

         // Invoke custom tool
         const toolResult = await this.invokeTool('my-custom-tool', {
           filePath: extractFilePathFromPrompt(request.prompt)
         });

         // Return result
         return {
           exitCode: 0,
           message: toolResult
         };
       }
     }
     ```

5. **Register agent and tools in extension activation**:
   - Update `src/extension.ts`:
     ```typescript
     import * as vscode from 'vscode';

     export async function activate(context: vscode.ExtensionContext) {
       // Register custom tool
       const myTool = new MyCustomTool();
       context.subscriptions.push(
         vscode.lm.registerToolDefinition(
           { name: 'my-custom-tool', description: '...' },
           myTool
         )
       );

       // Register agent
       const myAgent = new MyAgent();
       context.subscriptions.push(
         vscode.lm.registerAgent(
           'my-agent',
           {
             id: 'my-agent',
             name: 'My Agent',
             description: 'Custom workflow automation',
             tools: ['my-custom-tool', 'search', 'read'],
             model: 'GPT-5.2 (copilot)',
             modes: [vscode.ChatMode.Ask]
           },
           myAgent
         )
       );

       console.log('My Agent extension activated');
     }

     export function deactivate() {}
     ```

6. **Test in VS Code**:
   - Compile:
     ```bash
     npm run compile
     ```
   - Launch debug session:
     ```bash
     Press F5 or Run → Start Debugging
     ```
   - A new VS Code window opens with extension running.
   - Test: Open Chat, select agent, send prompt.
   - Verify: Agent responds, tools are invoked, results are correct.

7. **Implement error handling and logging**:
   - Use VS Code's Output channel:
     ```typescript
     const outputChannel = vscode.window.createOutputChannel('My Agent');
     outputChannel.appendLine('Agent started');
     ```
   - Wrap tool invocation in try-catch:
     ```typescript
     try {
       // Tool logic
     } catch (error) {
       outputChannel.appendLine(`Tool error: ${error}`);
       return { content: [{ type: 'text', text: 'Tool failed' }] };
     }
     ```

8. **Validation and testing**:
   - **Unit test**: Tool logic (input validation, output format).
   - **Integration test**: Agent invokes tool and produces expected output.
   - **E2E test**: Multi-turn agent conversation in VS Code Chat.
   - **Performance test**: Tool execution time < 1s (typical SLA).

## Inputs

- Agent design with tool requirements and workflow logic (from agent-plugin-design skill).
- Custom tool specifications (name, input schema, output format).
- VS Code API requirements (editors, workspace, commands).
- TypeScript knowledge and extension development experience.

## Required Outputs

- VS Code extension scaffolded (package.json, tsconfig.json, webpack.config.js, src/extension.ts).
- Custom tool definitions (LanguageModelToolDefinition with input schema).
- Tool handler implementation (ILanguageModelTool with invoke() method).
- Agent handler implementation (IChatAgentImplementation with invoke() method).
- Agent registration in extension activation (vscode.lm.registerAgent()).
- Compiled extension (VSIX package for distribution).
- Tests: unit, integration, E2E test coverage.
- Documentation: README with extension purpose, tool descriptions, usage examples.

## Done Criteria

- Extension scaffolding is complete (all config files present and valid).
- Custom tools have explicit input schemas (JSON schema format).
- Tool handlers validate input and return consistent output format.
- Agent handler successfully invokes tools and processes results.
- Extension compiles without errors (`npm run compile` succeeds).
- Extension loads in VS Code debug session (F5).
- Agent appears in Chat agent selector.
- Agent responds to prompts and invokes tools correctly.
- Tests pass (unit, integration, E2E).
- VSIX package builds successfully (`vsce package`).

## Validation Checklist

- [ ] `package.json` has valid `contributes.chatParticipants` entry.
- [ ] `tsconfig.json` has `strict: true` and targets `ES2020`.
- [ ] `webpack.config.js` bundles extension correctly (checks `out/extension.js`).
- [ ] Custom tool input schema is valid JSON schema.
- [ ] Tool handler validates all input fields (no assumptions).
- [ ] Tool handler returns `LanguageModelToolResult` with `content` array.
- [ ] Agent handler implements `IChatAgentImplementation` interface correctly.
- [ ] Agent registration uses `vscode.lm.registerAgent()` with correct parameters.
- [ ] Extension loads without errors in debug session (F5).
- [ ] Agent is selectable in Chat and responds to prompts.
- [ ] Tool invocation succeeds and produces expected output.
- [ ] Error cases handled gracefully (tool fails, input invalid, etc.).

## References

- [VS Code Extension API Reference](https://code.visualstudio.com/api/references/vscode-api)
- [Language Model API Documentation](https://code.visualstudio.com/docs/copilot/agents/overview)
- [Chat Agent Implementation Guide](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Tool Definition and Invocation](https://code.visualstudio.com/docs/copilot/agents/agent-tools)
- [VS Code Extension Development Guide](https://code.visualstudio.com/api/get-started/your-first-extension)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## Trigger Conditions

Invoke this skill when any of the following is true:

- Custom tools are needed beyond built-in and MCP.
- Agent requires dynamic behavior or runtime decisions.
- Extension integration with VS Code APIs is required (editors, workspace, commands).
- Agent needs model selection or behavior tuning via TypeScript code.
- Complex multi-turn workflows require programmatic state management.
