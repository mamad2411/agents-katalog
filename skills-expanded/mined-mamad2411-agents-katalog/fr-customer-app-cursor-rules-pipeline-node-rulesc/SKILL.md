---
description: 
globs: app/pipelines/**/*.py
alwaysApply: false
---
---
description: 
globs: app/pipelines/**/*.py
alwaysApply: false
---
# Pipeline Transformation and Development Guide

This guide provides the necessary steps and best practices for transforming the existing pipeline structure to other pipelines and creating new pipeline nodes.

## Table of Contents
- [0. Creating a New Pipeline Node](mdc:#0-creating-a-new-pipeline-node)
- [1. Basic Structure](mdc:#1-basic-structure)
- [2. Node Structure](mdc:#2-node-structure)
- [3. Error Handling](mdc:#3-error-handling)
- [4. Logging](mdc:#4-logging)
- [5. Supabase Operations](mdc:#5-supabase-operations)
- [6. Status Management](mdc:#6-status-management)
- [7. Task Context Usage](mdc:#7-task-context-usage)
- [8. Security and Validation](mdc:#8-security-and-validation)
- [9. Performance](mdc:#9-performance)
- [10. Real Pipeline Example](mdc:#10-real-pipeline-example)

## 0. Creating a New Pipeline Node

This section provides a step-by-step guide for creating a new pipeline node.

### 0.1. Determining the Node Type

The first step in creating a node is determining its type based on the function it will perform:

1. **Standard Node**: For general operations such as data retrieval, processing, transformation, or saving
2. **LLM Node**: For operations requiring interaction with AI models (GPT, Claude, etc.)

### 0.2. Creating a New Standard Node

Below is a sample template for a standard node. You can start by copying and editing it:

```python
import logging
from core.base import Node
from core.task import TaskContext
from core.enums import NodeStatus
from services.supabase_service import SupabaseClient

logger = logging.getLogger(__name__)

class MyNewNode(Node):
    def process(self, task_context: TaskContext) -> TaskContext:
        """
        Explain the operation the node will perform here
        
        Args:
            task_context: Pipeline task context
            
        Returns:
            TaskContext: Updated task context
        """
        logger.info(f"Starting process for {self.__class__.__name__}")
        
        try:
            # Check the status of the previous node (if applicable)
            status, error = self.get_previous_node_status(task_context)
            if status in [NodeStatus.FAILED, NodeStatus.SKIPPED]:
                logger.warning(f"Previous node {status.value}. Skipping current node.")
                return self.update_task_context(task_context, NodeStatus.SKIPPED)
                
            # Get necessary data from previous nodes
            input_data = task_context.nodes.get("PreviousNodeName", {}).get("key_name")
            
            # Validate input data and raise specific exceptions for expected errors
            if not input_data:
                error_msg = "Required input data 'key_name' not found in PreviousNodeName"
                logger.error(error_msg)
                raise ValueError(error_msg) # Raise exception
                
            # Main processing code - call helper methods if needed
            result = self.do_work(input_data) # Errors in helper methods will propagate up
            
            # Return successful result
            logger.info("Successfully completed process")
            return self.update_task_context(
                task_context,
                NodeStatus.SUCCESS,
                my_result=result
            )
            
        except Exception as e:
            # Centralized error handling for all exceptions
            error_msg = str(e) # Use the exception's message directly
            # Use logger.exception to log the error and stack trace
            logger.exception(f"Error in {self.__class__.__name__}: {error_msg}") 
            return self.update_task_context(task_context, NodeStatus.FAILED, error=error_msg)
    
    def do_work(self, input_data):
        """Helper method that performs the main work. Avoid try-except here."""
        # Processing code
        # If an error occurs here, let it propagate to the process method's except block
        processed_data = input_data # Placeholder
        return processed_data

### 0.3. Creating a New LLM Node

You can use the following template to create an LLM node:

```python
from core.llm import LLMNode
from core.task import TaskContext
from pydantic import BaseModel, Field
from core.llm_output import LLMOutput
import logging
from services.prompt_loader import PromptManager
from services.llm_factory import LLMFactory
from typing import Optional, Dict, List, Any
from core.enums import NodeStatus

logger = logging.getLogger(__name__)

class MyNewLLMNode(LLMNode):
    class ContextModel(BaseModel):
        # Schema for data to be retrieved from previous nodes
        input_data: Dict[str, Any] = Field(
            description="Input data to analyze",
            default_factory=dict
        )
        
    class ResponseModel(BaseModel):
        # Expected response schema from the LLM
        markdown_response: Optional[str] = Field(
            None, 
            description="Human-readable output in markdown format"
        )
        structured_data: Optional[Dict[str, Any]] = Field(
            None,
            description="Structured output data"  
        )
        key_points: Optional[List[str]] = Field(
            None,
            description="List of key points",
            min_items=3,
            max_items=10
        )

    def get_context(self, task_context: TaskContext) -> ContextModel:
        """
        Retrieves necessary data from the task context
        """
        # Get data from the previous node
        input_data = task_context.nodes.get("PreviousNodeName", {}).get("key_name")
        
        # Data validation
        if not input_data:
            raise ValueError("Required input data not found in task context")
        
        # Create context model
        self.context_model = self.ContextModel(input_data=input_data)
        logger.info("Successfully prepared context for LLM")
        return self.context_model

    def create_completion(self, context: ContextModel) -> ResponseModel:
        """
        Create LLM completion
        """
        # Create LLM instance
        llm = LLMFactory("openai")  # or "claude", "llama", etc.
        
        # Load prompt - Name of the .prompt file in PromptManager
        prompt = PromptManager.get_prompt("my_prompt_name")
        
        # Prepare messages
        self.messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": str(context.input_data)}
        ]

        # Get response from LLM
        self.response_model, self.completion = llm.create_completion(
            response_model=self.ResponseModel,
            messages=self.messages
        )
        
        logger.info("Successfully generated LLM response")
        return self.response_model

    def process(self, task_context: TaskContext) -> TaskContext:
        """
        Main processing method
        """
        logger.info(f"Starting process for {self.__class__.__name__}")

        try:
            # 1. Check previous node status (if not the first node)
            status, error = self.get_previous_node_status(task_context)
            if status in [NodeStatus.FAILED, NodeStatus.SKIPPED]:
                logger.warning(f"Previous node {status.value}. Skipping current node.")
                return self.update_task_context(task_context, NodeStatus.SKIPPED)

            # 2. Main processing code
            # ...

            # 3. Return successful result
            return self.update_task_context(
                task_context,
                NodeStatus.SUCCESS,
                result_data=result
            )

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error in {self.__class__.__name__}: {error_msg}")
            return self.update_task_context(task_context, NodeStatus.FAILED, error=error_msg)

    def llm_output(self) -> LLMOutput:
        """
        Configure LLM output format
        """
        return LLMOutput(     
            node_pipeline="my_pipeline_name",
            node_name=self.node_name,
            model_name=self.completion.model,
            role_name="system",
            prompt=self.messages,
            input=self.context_model.model_dump_json(),
            output=self.completion.model_dump_json(),
            structured_data=self.response_model.model_dump()
        )
```

### 0.4. Creating a Prompt File (for LLM Node)

Steps to create a prompt file for the LLM node:

1. Create a new file named `my_prompt_name.prompt` under the `prompts/` directory
2. Write the prompt content in the following format:

```
<instruction>
Write detailed instructions for the LLM here. Task purpose, expected output format, constraints, etc.
</instruction>

<context>
Input data will be in this section. Think of this section as a template; actual data will be placed here during the LLM call.
</context>

<output_format>
Specify the output format here. It must be compatible with the ResponseModel.

Example:
{
  "markdown_response": "...",
  "structured_data": {
    "key1": "value1",
    "key2": "value2"
  },
  "key_points": [
    "Point 1",
    "Point 2",
    "Point 3"
  ]
}
</output_format>
```

### 0.5. Adding the New Node to the Pipeline

After creating your node, add it to the pipeline:

1. Open the `__init__.py` file in the pipeline folder
2. Import your node
3. Add the node to the pipeline's node list:

```python
from typing import List
from core.pipeline import Pipeline
from core.base import BaseNode
from .node1 import Node1
from .node2 import Node2
from .my_new_node import MyNewNode

class MyPipeline(Pipeline):
    """Pipeline definition"""
    
    name = "my_pipeline"
    version = "1.0.0"
    
    def get_nodes(self) -> List[BaseNode]:
        return [
            Node1(),
            Node2(),
            MyNewNode()  # Add the new node
        ]
```

### 0.6. Checklist

Use this checklist when creating a new node:

- [ ] Is the node class name descriptive?
- [ ] Is the appropriate base class selected? (`Node` or `LLMNode`)
- [ ] Is a docstring added?
- [ ] Is the previous node status checked? (Skip for the first node in the pipeline)
- [ ] Are all input data validated?
- [ ] Is logger usage correct?
- [ ] Is error handling done appropriately?
- [ ] Is the task context update correct?
- [ ] Are ContextModel and ResponseModel defined for LLM nodes?
- [ ] Is the prompt prepared? (for LLM nodes)

## 1. Basic Structure

Each pipeline folder should contain the following basic files:

```
pipeline_name/
├── __init__.py
├── node1.py
├── node2.py
└── node3.py
```

## 2. Node Structure

### 2.1. Base Class Selection

Choose the appropriate base class based on your node type:

- For nodes using LLM: `LLMNode`
- For other nodes: `Node`

### 2.2. Basic Methods

The basic method structure required in every node:

```python
def process(self, task_context: TaskContext) -> TaskContext:
    """
    Main processing method with centralized error handling.
    """
    logger.info(f"Starting process for {self.__class__.__name__}")

    try:
        # 1. Check previous node status (if not the first node)
        status, error = self.get_previous_node_status(task_context)
        if status in [NodeStatus.FAILED, NodeStatus.SKIPPED]:
            logger.warning(f"Previous node {status.value}. Skipping current node.")
            return self.update_task_context(task_context, NodeStatus.SKIPPED)

        # 2. Validate inputs and perform core logic
        # Example: Get and validate data
        required_value = task_context.some_method_to_get_data("some_key")
        if not required_value:
            error_msg = "Required data 'some_key' is missing or invalid."
            logger.error(error_msg)
            raise ValueError(error_msg) # Raise specific exception

        # Call helper methods or perform operations directly
        result = self._perform_action(required_value) # Errors propagate up

        # 3. Return successful result
        logger.info("Successfully completed process")
        return self.update_task_context(
            task_context,
            NodeStatus.SUCCESS,
            result_data=result
        )

    except Exception as e:
        # Centralized handling for all exceptions
        error_msg = str(e) # Use the exception's message
        logger.exception(f"Error in {self.__class__.__name__}: {error_msg}") # Log error and stack trace
        return self.update_task_context(
            task_context, NodeStatus.FAILED, error=error_msg
        )

def _perform_action(self, data):
    """Helper method example. Avoid try-except here."""
    # Business logic
    # Let exceptions propagate up to the process method
    processed_result = data # Placeholder
    return processed_result
```

### 2.3. Additional Requirements for LLM Nodes

Required structure for LLM nodes:

```python
import json # Added import

class MyLLMNode(LLMNode):
    # 1. Context Model definition - Schema for data from previous nodes
    class ContextModel(BaseModel):
        linkedin_analysis: Optional[Dict[str, Any]] = Field(
            description="LinkedIn analysis data",
            default=None
        )
        website_analysis: Optional[Dict[str, Any]] = Field(
            description="Website analysis data",
            default=None
        )

    # 2. Response Model definition - Expected response schema from LLM
    class ResponseModel(BaseModel):
        # You can model complex data structures using nested models
        class CompanyProfile(BaseModel):
            name: Optional[str] = Field(description="Company name", default=None)
            industry: Optional[list[str]] = Field(description="Primary and secondary industries", default_factory=list)
            # ... other fields

        # Main model fields
        markdown_formated_response: Optional[str] = Field(
            description="Human-readable summary in Markdown format",
            min_length=200,
            default=None
        )
        company_profile: Optional[CompanyProfile] = Field(description="Basic company information", default=None)
        key_insights: Optional[List[str]] = Field(
            description="List of 3-5 most important insights",
            min_items=3,
            max_items=5,
            default_factory=list
        )

    # 3. Context retrieval method - Get data from previous nodes and validation
    def get_context(self, task_context: TaskContext) -> ContextModel:
        # Get data from previous nodes
        linkedin_analysis = task_context.nodes.get("AnalyseLinkedIn", {}).get("linkedin_analysis")
        website_analysis = task_context.nodes.get("AnalyseWebsite", {}).get("website_analysis")

        # Data validation
        if not linkedin_analysis and not website_analysis:
            raise ValueError("No analysis data found in task context")

        # Create context model
        self.context_model = self.ContextModel(
            linkedin_analysis=linkedin_analysis,
            website_analysis=website_analysis
        )

        logger.info("Successfully prepared context for LLM")
        return self.context_model

    # 4. Create LLM completion
    def create_completion(self, context: ContextModel) -> ResponseModel:
        # Create LLM instance
        llm = LLMFactory("openai")

        # Load prompt
        prompt = PromptManager.get_prompt("prompt_name")

        # Prepare messages
        self.messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(context.model_dump())} # Use json.dumps
        ]

        # Get response from LLM
        self.response_model, self.completion = llm.create_completion(
            response_model=self.ResponseModel,
            messages=self.messages
        )

        logger.info("Successfully generated LLM response")
        return self.response_model

    # 5. Main processing method
    def process(self, task_context: TaskContext) -> TaskContext:
        try:
            logger.info("Starting LLM process")

            # Check previous node status
            status, error = self.get_previous_node_status(task_context)
            if status in [NodeStatus.FAILED, NodeStatus.SKIPPED]:
                logger.warning(f"Previous node {status.value}. Skipping current node.")
                return self.update_task_context(task_context, NodeStatus.SKIPPED)

            # Prepare context and get LLM response
            context = self.get_context(task_context)
            self.response_model = self.create_completion(context)

            logger.info("Successfully completed LLM process")

            # Update task context
            return self.update_task_context(
                task_context,
                NodeStatus.SUCCESS,
                result=self.response_model.model_dump()
            )
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error in LLM process: {error_msg}")
            return self.update_task_context(task_context, NodeStatus.FAILED, error=error_msg)

    # 6. LLM output format
    def llm_output(self) -> LLMOutput:
        return LLMOutput(
            node_pipeline="pipeline_name",
            node_name=self.node_name,
            model_name=self.completion.model,
            role_name="system",
            prompt=self.messages,
            input=self.context_model.model_dump_json(),
            output=self.completion.model_dump_json(),
            structured_data=self.response_model.model_dump()
        )
```

Important points for LLM Nodes:

1. **Context Model**
   * The schema for data from previous nodes should be clearly defined.
   * Default values should be set for optional fields.
   * Descriptive descriptions should be used in Field definitions.

2. **Response Model**
   * The expected response format from the LLM should be modeled in detail.
   * Complex data structures can be defined using nested models.
   * Validation rules (like min_length, min_items) can be added for fields.
   * Default values and factory methods should be used.

3. **Context Preparation**
   * Null checks should be performed when retrieving data from previous nodes.
   * Meaningful errors should be raised in case of missing data.
   * Context model validation is done automatically.

4. **LLM Operations**
   * Prompts should be managed via PromptManager.
   * Context data should be sent in JSON format.
   * The LLM response should be received as structured data.

5. **Error Handling**
   * Appropriate logging should be done at each stage.
   * Errors should be caught and recorded in the task context.
   * Errors from previous nodes should be checked.

6. **Output Format**
   * All details of the LLM operation (prompt, input, output) should be recorded.
   * Structured data should be stored separately.
   * Model and node information should be completely filled.

## 3. Error Handling

Points to consider for error handling in each node:

- ✅ **Centralized Handling**: Implement a single `try...except Exception as e:` block within the `process` method to handle all potential errors originating from that node, including errors from helper methods it calls.
- ⬆️ **Raise Specific Exceptions**: For predictable error conditions within the `try` block (e.g., missing required data, invalid input), raise specific, informative exceptions like `ValueError`. Do **not** call `update_task_context` and return directly from these checks.
  ```python
  if not required_data:
      error_msg = "Required data X is missing."
      logger.error(error_msg)
      raise ValueError(error_msg) # Let the central handler catch this
  ```
- ➡️ **Use Exception Message**: In the central `except Exception as e:` block, use `error_msg = str(e)` to capture the message from the caught exception (whether it was explicitly raised or unexpected).
- 📜 **Log with Stack Trace**: Use `logger.exception(f"Error message: {error_msg}")` within the central `except` block. This logs the error message along with the full stack trace, which is crucial for debugging.
- 🚫 **Avoid Try-Except in Helpers**: Do **not** use `try...except` blocks in helper methods called by `process`. Allow exceptions from helper methods to propagate up to the central handler in `process`. This keeps error handling logic consolidated.
- ➡️ **Update Context in Except**: The central `except` block is the *only* place where `update_task_context(..., status=NodeStatus.FAILED, error=error_msg)` should be called for failures.
- ⏭️ **Check Previous Node Status**: Always check the status of the preceding node at the beginning of the `process` method (unless it's the first node) and return `update_task_context(..., status=NodeStatus.SKIPPED)` if the previous node failed or was skipped. This check should happen *before* the main `try` block.

Example of the recommended structure:

```python
def process(self, task_context: TaskContext) -> TaskContext:
    logger.info(f"Starting process for {self.__class__.__name__}")

    # Check previous node status first
    status, error = self.get_previous_node_status(task_context)
    if status in [NodeStatus.FAILED, NodeStatus.SKIPPED]:
        logger.warning(f"Previous node {status.value}. Skipping current node.")
        return self.update_task_context(task_context, NodeStatus.SKIPPED)

    try:
        # --- Main Logic ---
        # Get data
        input_data = self._get_input(task_context) 
        
        # Validate data (raise specific error if invalid)
        if not input_data:
             raise ValueError("Input data is missing.")

        # Perform work (errors in _do_work propagate up)
        result = self._do_work(input_data)

        # Return success
        logger.info("Successfully completed process")
        return self.update_task_context(
            task_context, NodeStatus.SUCCESS, result=result
        )

    except Exception as e:
        # --- Central Error Handler ---
        error_msg = str(e)
        logger.exception(f"Error in {self.__class__.__name__}: {error_msg}") # Log stack trace
        return self.update_task_context(
            task_context, NodeStatus.FAILED, error=error_msg
        )

def _get_input(self, task_context):
    # No try-except here
    # ... logic to get data ...
    return data

def _do_work(self, data):
    # No try-except here
    # ... logic to process data ...
    return result
```

## 4. Logging

Logging structure to be used in each node:

```python
import logging
logger = logging.getLogger(__name__)

# Info logs
logger.info("Starting process")

# Debug logs
logger.debug("Detailed information")

# Error logs
logger.error(f"Error occurred: {error_msg}")

# Warning logs
logger.warning("Warning message")
```

## 5. Supabase Operations

Example structure for Supabase operations:

```python
from services.supabase_service import SupabaseClient

# Create client
supabase = SupabaseClient.get_client()

# Read data
response = (
    supabase.table("table_name")
    .select("field1, field2")
    .eq("id", some_id)
    .execute()
)

# Update data
supabase.table("table_name") \
    .update({"status": "new_status"}) \
    .eq("id", some_id) \
    .execute()
```

## 6. Status Management

Recommendations for status management:

- The start and end statuses of each pipeline should be clearly defined.
- Status changes should be logged.
- Helper methods should be used for status updates.

```python
def _update_status(self, id: str, status: str) -> None:
    """
    Status update helper method
    """
    try:
        supabase = SupabaseClient.get_client()
        supabase.table("table_name").update({"status": status}).eq("id", id).execute()
        logger.info(f"[ID {id}] Updated status to {status}")
    except Exception as e:
        logger.error(f"[ID {id}] Failed to update status")
```