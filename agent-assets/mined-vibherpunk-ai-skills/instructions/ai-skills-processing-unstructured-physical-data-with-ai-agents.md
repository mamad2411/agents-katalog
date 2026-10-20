# Copilot Instructions: Processing Unstructured Physical Data With Ai Agents
Description: This skill enables AI agents to efficiently process and analyze unstructured physical data (e.g., video recordings, sensor data, robot telemetry) using data harnesses, Pydantic schemas, and execution engines. It covers data modeling, distributed computing, and incremental updates to handle large-scale, complex datasets.

## Overview
Processing unstructured physical data (e.g., video recordings, sensor data) is a complex task due to the sheer volume and complexity of the data. This skill teaches you how to build a **data harness** that enables AI agents to efficiently process, analyze, and query such data. Key components include **Pydantic schemas** for data modeling, **execution engines** for distributed computing, and **incremental updates** to avoid redundant processing.

For a deeper dive into the core concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Install the Required Tools**: Install the necessary libraries and tools, such as Pydantic and DataChain.
   ```bash
   pip install pydantic datachain
   ```
2. **Define Pydantic Schemas**: Create schemas to model your unstructured data. This ensures consistency and enables efficient querying.
   ```python
   from pydantic import BaseModel

   class VideoFrame(BaseModel):
       file_path: str
       frame_id: int
       timestamp: float
       class_id: int
       confidence_score: float
       bounding_box: dict
   ```
3. **Set Up the Execution Engine**: Configure a distributed computing engine (e.g., Dask) to process data in parallel.
   ```python
   from dask import distributed

   client = distributed.Client()
   ```
4. **Process Data Incrementally**: Use incremental updates to avoid reprocessing data that has already been analyzed.
   ```python
   def process_file(file_path):
       # Process the file and return results
       return VideoFrame(file_path=file_path, frame_id=1, timestamp=0.0, class_id=1, confidence_score=0.9, bounding_box={})

   results = client.map(process_file, file_paths)
   ```
5. **Query the Database**: Use SQL-like queries to retrieve insights from the processed data.
   ```sql
   SELECT COUNT(*) FROM video_frames WHERE class_id = 1;
   ```
6. **Validate and Test**: Run tests to ensure the accuracy and efficiency of your data processing pipeline.
   ```python
   def test_video_frame():
       frame = VideoFrame(file_path='video.mp4', frame_id=1, timestamp=0.0, class_id=1, confidence_score=0.9, bounding_box={})
       assert frame.class_id == 1
   ```

For detailed examples and code snippets, refer to [Code Examples](references/code_examples.md).

## Best Practices
- **Use Pydantic Schemas**: Pydantic ensures data consistency and simplifies schema management. Avoid using JSON files or SQL databases directly.
- **Leverage Distributed Computing**: Use execution engines like Dask to process large datasets efficiently.
- **Implement Incremental Updates**: Avoid redundant processing by using incremental updates and checkpoints.

## Common Pitfalls
- **Ignoring Data Modeling**: Skipping schema definition leads to inconsistent data and inefficient queries.
- **Overlooking Distributed Computing**: Processing large datasets sequentially is slow and resource-intensive.
- **Failing to Validate**: Without proper testing, errors in data processing can go unnoticed.

For a practical guide on avoiding these pitfalls, see [Practical Guide](references/practical_guide.md).

## Validation Steps
1. **Schema Validation**: Ensure all data adheres to the defined Pydantic schemas.
2. **Query Accuracy**: Verify that SQL queries return accurate results.
3. **Performance Testing**: Measure the efficiency of the distributed computing engine.
4. **Incremental Update Testing**: Confirm that incremental updates work as expected.

## References
For further reading, consult the following documents:
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)

## Reference Guides

### Code Examples

# Code Examples

## Introduction
This document provides concrete code examples for processing unstructured physical data using AI agents. It covers data modeling, distributed computing, and incremental updates.

## Data Modeling with Pydantic
Define schemas for your data using Pydantic. For example, a schema for video frames might look like this:
```python
from pydantic import BaseModel

class VideoFrame(BaseModel):
    file_path: str
    frame_id: int
    timestamp: float
    class_id: int
    confidence_score: float
    bounding_box: dict
```

## Distributed Computing with Dask
Set up a distributed computing engine using Dask:
```python
from dask import distributed

client = distributed.Client()
```
Process files in parallel:
```python
def process_file(file_path):
    # Process the file and return results
    return VideoFrame(file_path=file_path, frame_id=1, timestamp=0.0, class_id=1, confidence_score=0.9, bounding_box={})

results = client.map(process_file, file_paths)
```

## Incremental Updates
Implement incremental updates to avoid redundant processing:
```python
def process_file(file_path):
    # Process the file and return results
    return VideoFrame(file_path=file_path, frame_id=1, timestamp=0.0, class_id=1, confidence_score=0.9, bounding_box={})

results = client.map(process_file, file_paths)
```

## Conclusion
These code examples demonstrate how to process unstructured physical data efficiently using AI agents.

### Core Concepts

# Core Concepts

## Introduction
Unstructured physical data, such as video recordings, sensor data, and robot telemetry, presents unique challenges due to its complexity and volume. This document outlines the core concepts required to process such data efficiently using AI agents.

## Data Harness
A **data harness** is a framework that enables AI agents to interact with unstructured physical data. It includes tools for data modeling, distributed computing, and incremental updates. The harness ensures that agents can process, analyze, and query data efficiently.

## Pydantic Schemas
**Pydantic** is a Python library for data validation and settings management. It allows you to define schemas that model your unstructured data, ensuring consistency and enabling efficient querying. For example, a schema for video frames might include fields like `file_path`, `frame_id`, `timestamp`, `class_id`, `confidence_score`, and `bounding_box`.

## Execution Engine
An **execution engine** is responsible for processing data in a distributed manner. Tools like **Dask** allow you to parallelize data processing tasks, making it possible to handle large datasets efficiently.

## Incremental Updates
**Incremental updates** ensure that only new or modified data is processed, avoiding redundant computations. This is crucial for maintaining efficiency, especially when dealing with large datasets.

## Conclusion
Understanding these core concepts is essential for building effective data harnesses that enable AI agents to process unstructured physical data efficiently.

### Practical Guide

# Practical Guide

## Introduction
This guide provides practical tips and best practices for processing unstructured physical data using AI agents. It covers common pitfalls and how to avoid them.

## Best Practices
1. **Use Pydantic Schemas**: Always define schemas for your data using Pydantic. This ensures consistency and simplifies schema management.
2. **Leverage Distributed Computing**: Use execution engines like Dask to process large datasets efficiently. Avoid sequential processing, which can be slow and resource-intensive.
3. **Implement Incremental Updates**: Use incremental updates to avoid redundant processing. This is especially important when dealing with large datasets.

## Common Pitfalls
1. **Ignoring Data Modeling**: Skipping schema definition leads to inconsistent data and inefficient queries. Always define schemas for your data.
2. **Overlooking Distributed Computing**: Processing large datasets sequentially is slow and resource-intensive. Always use distributed computing tools.
3. **Failing to Validate**: Without proper testing, errors in data processing can go unnoticed. Always validate your data and queries.

## Conclusion
Following these best practices and avoiding common pitfalls will help you build efficient and reliable data processing pipelines for unstructured physical data.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[When Agents Meet Physical Data: The Other Physics of Agent Harnesses - Dmitry Petrov, DataChain](https://www.youtube.com/watch?v=bUJgirn4_yc)** by AI Engineer