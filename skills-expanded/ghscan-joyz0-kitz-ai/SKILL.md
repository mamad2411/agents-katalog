---
name: config-system-design
description: Provides a comprehensive configuration system with JSON5 support, schema validation, environment variable substitution, and hot-reloading capabilities. Enables modular, secure, and maintainable configuration management for complex applications.
---

# config-system-design

## Description

Provides a comprehensive configuration system with JSON5 support, schema validation, environment variable substitution, and hot-reloading capabilities. Enables modular, secure, and maintainable configuration management for complex applications.

## Triggers

- **Use when:** You need a robust configuration system that supports environment variables, schema validation, and hot-reloading for a complex application.
- **Do NOT use when:** You're building a simple script or application that only requires basic configuration files without advanced features.

## Input

- `config_path`: string (Path to the main configuration file)
- `schema_definition`: object (Zod schema definition for validation)
- `default_values`: object (Default configuration values)
- `env_vars`: object (Environment variables for substitution)

## Output

- `config`: object (Fully validated and resolved configuration)
- `status`: boolean (Success status)
- `errors`: array (Validation errors, if any)
- `reload_watcher`: object (Hot-reload watcher instance)

## Steps

1. **Read Configuration**: Load the main config file and any included files using JSON5 parsing.
2. **Resolve Environment Variables**: Substitute `${VAR}` placeholders with actual environment values.
3. **Merge Configurations**: Deep merge included files and apply runtime overrides.
4. **Apply Defaults**: Add default values for missing configuration keys.
5. **Validate Schema**: Use Zod to validate the complete configuration against the schema.
6. **Setup Hot-Reload**: Start file watcher for configuration changes.
7. **Return Result**: Provide the validated configuration and status.

## Failure Strategy

- If configuration file is missing, use default values and warn the user.
- If schema validation fails, provide detailed error messages with paths to invalid fields.
- If environment variables are missing, log warnings and use fallback values if available.
- If hot-reload setup fails, disable hot-reload and continue with static configuration.

## Key Features

- **JSON5 Support**: Allows comments, trailing commas, and other syntax improvements
- **Schema Validation**: Strict validation using Zod to catch errors early
- **Environment Variable Substitution**: Securely inject environment variables
- **Modular Configuration**: Support for including other config files
- **Hot-Reloading**: Automatically apply configuration changes without restart
- **Configuration Auditing**: Track changes and maintain backups

## Implementation References

- **File Structure**: See references/config-system/file-structure.md
- **Schema Definitions**: See references/config-system/schema-examples.md
- **Hot-Reload Implementation**: See references/config-system/hot-reload.md
- **Security Best Practices**: See references/config-system/security.md
