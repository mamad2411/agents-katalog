---
name: astronomer-llms
description: 'Read and navigate Astronomer documentation using llms.txt context. You MUST load this skill when asked to read Astronomer documentation or Airflow documentation hosted by Astronomer.'
license: MIT
---

# Skill: astronomer-llms (Astronomer Docs)

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- When needing to read or reference Astronomer or Airflow documentation.
- When searching for Astronomer-specific Airflow deployment, orchestration, or DAG guidelines.
- When you are prompted to check `astronomer.io/docs` for information.

## WHEN NOT TO USE

- When you are writing Airflow DAGs (use `apache-airflow-dags` instead).
- When interacting with Airflow APIs (use `apache-airflow-api` instead).

## Core Process

1. **Use `llmstxt` conventions**: Astronomer provides an `llms.txt` file which is highly optimized for LLMs.
2. **Fetch the context**: Utilize the `webfetch` tool to retrieve the context files.
3. **Primary References**:
   - `https://www.astronomer.io/llms.txt`: The index of all LLM-friendly documentation.
   - `https://www.astronomer.io/docs/llms.txt`: The index specifically for Astronomer documentation.

## Best Practices

- Always prefer reading from `llms.txt` over scraping individual HTML pages, as `llms.txt` paths return markdown optimized for your context window.
- When looking for specific DAG authoring techniques, use the references in the `llms.txt` to find the correct `.md` documentation page.

## References

- [Astronomer LLMs.txt](https://www.astronomer.io/llms.txt)
- [Astronomer Docs LLMs.txt](https://www.astronomer.io/docs/llms.txt)

## Related Skills

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- **apache-airflow-dags**:
  You MUST load this skill when asked to write, refactor, or structure Airflow DAGs.
- **llmstxt**:
  You MUST load this skill when reading websites, llms.txt, or when creating/updating that file.
