---
name: jinja2-templates
description: Write safe, readable Jinja2 templates for Ansible and configuration generation.
---

# Jinja2 templates

An undefined variable aborts the whole play mid-run, and a plaintext secret in a template leaks into rendered files and logs. Guarding optionals with `| default()` and keeping logic out of templates makes failures predictable and reviewable.

## Variable safety

- Always use the `| default()` filter for optional variables: `{{ optional_var | default('fallback') }}`.
- Document all referenced variables in the task's `vars:` or the role's `defaults/main.yml`.
- Never assume a variable exists without `| default()`.
- Use `| default(omit)` to skip optional config blocks entirely.

## Structure and logic

- Templates render; keep logic in Ansible tasks or the calling code.
- Use `{%- if condition -%}` (with `-`) to strip whitespace and avoid formatting issues.
- Avoid complex Jinja2 logic; if you need loops or conditionals, move to a task.
- Use `{% include %}` for reusable template fragments, not copy-paste.

## Embedded data

- Use `| to_json` or `| to_yaml` for structured data embedded in templates.
- Example: `"environment": {{ my_dict | to_json }}` for JSON config files.
- Always validate the output after adding filters; YAML/JSON syntax errors are common.

## Secrets in templates

- Never put plaintext secrets in templates; use `vault`, `aws_ssm_parameter`, or `lookup()` in the task.
- If a template renders a secret, apply `no_log: true` to the task.
- Document the expected secret variable name in `defaults/main.yml` with a comment.

## Style

- Use two spaces for indentation, consistent with Ansible.
- Comment complex template logic; explain *why*, not *what*.
- Keep template files under 100 lines; extract if longer.

## Examples

```jinja2
{# BAD — variable used without default; crashes if optional_port is undefined #}
listen = {{ optional_port }}
environment = {{ config_dict }}

{# GOOD — safe defaults; structured data serialized with filter #}
listen = {{ optional_port | default(8080) }}
environment = {{ config_dict | to_json }}
```

```jinja2
{# BAD — complex logic inside the template #}
{% for item in items %}
  {% if item.type == "web" and item.enabled %}
    ...
  {% endif %}
{% endfor %}

{# GOOD — filter in the task, template stays declarative #}
{% for item in web_items %}
  ...
{% endfor %}
```
