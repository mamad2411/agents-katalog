# Project: XML Generator Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - myxml() - that allows you to create simple XML output.
- The output from a function will always be a string.
- Examples:
  - Input myxml('foo') gives output: <foo></foo>
  - Input myxml('foo', 'bar') gives output: <foo>bar</foo>
  - Input myxml('foo', 'bar', a=1, b=2, c=3) gives output: <foo a="1" b="2" c="3">bar</foo>
- How myxml() handles parameters:
  - First parameter: name of the XML tag.
  - Second argument: content placed between opening and closing XML tags.
  - Name-value pair arguments: turned into attributes inside the opening tag.
- Use Pythonic conventions.

## Exercise notes
- Consider plain parameters, parameters with defaults and keyword argument parameters (**kwargs).