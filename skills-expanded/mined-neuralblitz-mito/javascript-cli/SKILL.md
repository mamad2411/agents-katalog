---
name: javascript-cli
description: Building CLI applications with Node.js, Inquirer, and Commander
license: MIT
metadata:
  audience: javascript-developers
  category: cli-development
---

# Skill: JavaScript/Node.js CLI

## What I do
Build command-line interface applications using Node.js and JavaScript/TypeScript. Focus on Inquirer for interactive prompts, Commander for argument parsing, and Chalk for terminal styling.

## When to use me
When building Node.js CLI tools, automation scripts, scaffolding tools, or interactive command-line applications.

## Core Packages

| Package | Purpose |
|---------|---------|
| `@inquirer/prompts` | Interactive prompts |
| `commander` | CLI argument parsing |
| `chalk` | Terminal string styling |
| `yargs` | CLI builder |
| `oclif` | Enterprise CLI framework |
| `picocolors` | Fast color library |

## Installation
```bash
npm install @inquirer/prompts commander chalk
# or
pnpm add @inquirer/prompts commander chalk
```

## Inquirer Prompts

### Modern @inquirer/prompts API
```javascript
import { input, select, confirm, checkbox } from '@inquirer/prompts';

// Simple input
const name = await input({
  message: "What's your name?",
  default: "Anonymous"
});

// Selection
const framework = await select({
  message: "Choose a framework:",
  choices: [
    { name: "React", value: "react" },
    { name: "Vue", value: "vue" },
    { name: "Svelte", value: "svelte" }
  ]
});

// Confirmation
const proceed = await confirm({
  message: "Do you want to continue?",
  default: true
});

// Multiple selection
const features = await checkbox({
  message: "Select features:",
  choices: ["Auth", "Database", "Testing", "Deployment"],
  default: ["Auth", "Testing"]
});
```

### Complete Example
```javascript
import { input, select, confirm } from '@inquirer/prompts';
import { cyan, bold } from 'chalk';

async function createProject() {
  console.log(bold.cyan('Project Creator'));
  console.log('-------------------\n');

  const name = await input({
    message: 'Project name:',
    validate: (value) => /^[a-z0-9-]+$/.test(value) 
      ? true 
      : 'Use lowercase letters, numbers, and hyphens only'
  });

  const template = await select({
    message: 'Choose a template:',
    choices: [
      { name: 'JavaScript', value: 'js' },
      { name: 'TypeScript', value: 'ts' },
      { name: 'Node.js API', value: 'api' }
    ]
  });

  const useTesting = await confirm({
    message: 'Include testing framework?',
    default: true
  });

  console.log(`\nCreating ${name} with ${template} template...`);
  if (useTesting) {
    console.log('Adding testing support...');
  }
  console.log(bold.green('Done!'));
}

createProject().catch(console.error);
```

### Legacy Inquirer.js API
```javascript
import inquirer from 'inquirer';

const answers = await inquirer.prompt([
  {
    type: 'input',
    name: 'name',
    message: 'Project name:',
    default: 'my-project'
  },
  {
    type: 'list',
    name: 'framework',
    message: 'Choose framework:',
    choices: ['React', 'Vue', 'Angular', 'Svelte']
  },
  {
    type: 'confirm',
    name: 'typescript',
    message: 'Use TypeScript?',
    default: true
  },
  {
    type: 'checkbox',
    name: 'features',
    message: 'Select features:',
    choices: ['Router', 'State Management', 'Testing', 'CSS Framework']
  }
]);
```

## Commander.js

### Basic Usage
```javascript
import { Command } from 'commander';

const program = new Command();

program
  .name('myapp')
  .description('My awesome CLI application')
  .version('1.0.0');

program
  .command('init')
  .description('Initialize a new project')
  .argument('<name>', 'Project name')
  .option('-t, --template <type>', 'Project template', 'default')
  .action((name, options) => {
    console.log(`Initializing ${name} with ${options.template} template`);
  });

program
  .command('build')
  .description('Build the project')
  .option('-p, --prod', 'Production build')
  .option('-w, --watch', 'Watch mode')
  .action((options) => {
    console.log('Building...', options);
  });

program.parse();
```

### Nested Subcommands
```javascript
import { Command } from 'commander';

const program = new Command();

// config group
program
  .command('config')
  .description('Configuration commands')
  .addCommand(
    new Command('set')
      .argument('<key>', 'Config key')
      .argument('<value>', 'Config value')
      .action((key, value) => {
        console.log(`Setting ${key} = ${value}`);
      })
  )
  .addCommand(
    new Command('get')
      .argument('<key>', 'Config key')
      .action((key) => {
        console.log(`Getting ${key}`);
      })
  )
  .addCommand(
    new Command('list')
      .action(() => {
        console.log('Listing all config');
      })
  );

program.parse();
```

### Options
```javascript
program
  .command('deploy')
  .option('-e, --env <env>', 'Environment', 'production')
  .option('-r, --replicas <count>', 'Number of replicas', '1')
  .option('--dry-run', 'Dry run mode')
  .option('-v, --verbose', 'Verbose output')
  .action((options) => {
    console.log('Deploying to:', options.env);
    console.log('Replicas:', options.replicas);
    if (options.dryRun) console.log('DRY RUN MODE');
    if (options.verbose) console.log('Verbose output enabled');
  });
```

## Chalk Styling

### Basic Usage
```javascript
import chalk from 'chalk';

// Text styling
console.log(chalk.red('Error message'));
console.log(chalk.green('Success!'));
console.log(chalk.yellow('Warning'));
console.log(chalk.blue('Info'));

// Combinations
console.log(chalk.bold.cyan('Title'));
console.log(chalk.bgRed.white('Highlighted'));
console.log(chalk.underline('Underlined'));

// Template literals
console.log(`
  ${chalk.green('✓')} Success: Operation completed
  ${chalk.red('✗')} Error: Something went wrong
  ${chalk.yellow('⚠')} Warning: Check configuration
`);

// Custom themes
const theme = {
  title: chalk.bold.blue,
  subtitle: chalk.cyan,
  success: chalk.green,
  error: chalk.red,
  warning: chalk.yellow
};

console.log(theme.title('My Application'));
console.log(theme.subtitle('Version 1.0.0'));
```

### Dynamic Colors
```javascript
// RGB
console.log(chalk.rgb(255, 128, 0)('Orange text'));

// Hex
console.log(chalk.hex('#FF8800')('Orange text'));

// Custom gradient
console.log(chalk.hex('#FF0000')('Red') + 
            chalk.hex('#FFFF00')('Yellow') + 
            chalk.hex('#00FF00')('Green'));
```

## Complete CLI Example

```javascript
#!/usr/bin/env node
import { Command } from 'commander';
import { input, select, confirm } from '@inquirer/prompts';
import chalk from 'chalk';
import fs from 'fs/promises';
import path from 'path';

const program = new Command();

program
  .name('project-cli')
  .description('Project scaffolding CLI')
  .version('1.0.0');

// init command with prompts
program
  .command('init')
  .description('Initialize a new project')
  .action(async () => {
    console.log(chalk.bold.cyan('\n Project Creator \n'));
    
    const projectName = await input({
      message: 'Project name:',
      validate: (v) => v.length > 0 || 'Name is required'
    });

    const template = await select({
      message: 'Choose template:',
      choices: [
        { name: 'JavaScript (ESM)', value: 'js' },
        { name: 'TypeScript', value: 'ts' },
        { name: 'Node.js API', value: 'api' }
      ]
    });

    const addTesting = await confirm({
      message: 'Add testing?',
      default: true
    });

    console.log(chalk.yellow('\nCreating project...'));
    
    // Create project structure
    await fs.mkdir(projectName, { recursive: true });
    
    const pkg = {
      name: projectName,
      version: '0.1.0',
      type: 'module',
      scripts: {
        test: addTesting ? 'node --test' : undefined
      }
    };

    await fs.writeFile(
      path.join(projectName, 'package.json'),
      JSON.stringify(pkg, null, 2)
    );

    console.log(chalk.green(`\n✓ Project ${projectName} created!`));
  });

program.parse();
```

## Testing

### With Prompts Mocking
```javascript
import { jest } from '@jest/globals';

// Mock inquirer for testing
jest.mock('@inquirer/prompts', () => ({
  input: jest.fn().mockResolvedValue('test-project'),
  select: jest.fn().mockResolvedValue('ts'),
  confirm: jest.fn().mockResolvedValue(true)
}));

test('creates project with prompts', async () => {
  await createProject();
  expect(fs.mkdir).toHaveBeenCalledWith('test-project', expect.any(Object));
});
```

## Shell Completion

```bash
# Bash
myapp completion bash > /etc/bash_completion.d/myapp

# Zsh
myapp completion zsh > ~/.zsh/completions/_myapp

# Fish
myapp completion fish > ~/.config/fish/completions/myapp.fish
```

## Best Practices

1. **Use ESM modules** (`"type": "module"`) for modern imports
2. **Validate inputs** with Inquirer's `validate` option
3. **Use Commander** for argument parsing, Inquirer for prompts
4. **Color wisely** - respect `--no-color` flag
5. **Handle errors gracefully** - clear error messages
6. **Exit codes** - use `process.exit(1)` for errors
7. **Shebang** for executable CLIs: `#!/usr/bin/env node`
8. **Bin field** in package.json for CLI entry point
