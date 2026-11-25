---
name: prestashop-console-commands
description: Skill for creating CLI console commands in PrestaShop 8 and 9 using Symfony Console.
---

# PrestaShop Console Commands Skill

This skill explains how to add custom CLI commands to your module, which can be executed via `bin/console`.

## 1. Technical Guide

### Creating the Command Class
Command classes must be located in `src/Command/` and extend `Symfony\Component\Console\Command\Command`.

```php
namespace MyModule\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class MyCustomCommand extends Command
{
    protected function configure()
    {
        $this
            ->setName('mymodule:task')
            ->setDescription('Performs a custom task')
            ->addOption('force', 'f', null, 'Force the task');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $output->writeln('Task started...');
        // Your logic here
        $output->writeln('Task finished!');
        return 0; // Success
    }
}
```

### Registering the Command
Commands must be registered as services in `config/services.yml` with the `console.command` tag.

```yaml
services:
    MyModule\Command\MyCustomCommand:
        tags:
            - { name: 'console.command' }
```

## 2. Professional Development Guide

### Using Legacy Core in CLI
To use legacy classes (like `Configuration` or `Db`), ensure you have initialized the context if necessary, although Symfony commands in PS usually have access to the service container.

```php
protected function execute(InputInterface $input, OutputInterface $output): int
{
    $db = \Db::getInstance();
    $shopId = (int)\Configuration::get('PS_SHOP_DEFAULT');
    // ...
}
```

### Best Practices
- **Return Codes**: Always return `0` for success and non-zero (like `1`) for errors.
- **Output Formatting**: Use `<info>`, `<error>`, and `<comment>` tags for colored output.
- **Dependency Injection**: Use constructor injection to get services instead of calling the global container.

## 3. User Guide

### How to execute
Access your terminal in the PrestaShop root directory and run:

```bash
php bin/console mymodule:task --force
```

## Rules & Best Practices
- **Namespace**: Ensure the namespace in the PHP file matches your module structure.
- **Header Licensing**: Always include the Ecom Experts license header.
- **Timeouts**: For long-running tasks, use `set_time_limit(0)` and consider implementing progress bars.
