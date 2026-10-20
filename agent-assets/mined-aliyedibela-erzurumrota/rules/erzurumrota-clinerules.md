FINAL OUTPUT FORMATTING RULES

CRITICAL: Your final output MUST strictly adhere to the following format. This supersedes all other formatting instructions.

    XML-ONLY RESPONSE: Your entire response MUST be a single, valid XML block. It must start directly with an opening tag (e.g., <tool_name>) and end with a closing tag (e.g., </tool_name>).
    NO PREFIX/SUFFIX: There must be absolutely no text, characters, or any other content before the opening XML tag or after the closing XML tag. This includes, but is not limited to, <thinking> tags.

Correct Example:

<tool_name>
  <parameter>value</parameter>
</tool_name>

Incorrect Example:

<thinking>I need to use a tool.</thinking>
<tool_name>
  <parameter>value</parameter>
</tool_name>


WHEN YOU CHANGE FILE USE REPLACE_IN_FILE NOT WRITE FILE