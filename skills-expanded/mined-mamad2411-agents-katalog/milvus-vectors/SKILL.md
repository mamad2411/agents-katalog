---
name: milvus-vectors
description: Scalable vector database with Milvus
version: 1.0.0
tags: [ai, vectors, database, embeddings, search]
---

# Milvus – Vector Database at Scale

Milvus is a purpose-built vector database for AI applications,
capable of handling billions of vectors with sub-second search.

- **GitHub**: github.com/milvus-io/milvus (35 000+ ⭐)
- **License**: Apache-2.0
- **Security**: Linux Foundation AI project. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{MILVUS_HOST}}` | Milvus server host |
| `{{MILVUS_PORT}}` | Milvus server port (default: 19530) |

## Usage Examples

### Create a collection (via pymilvus)

```bash
python3 -c "
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
connections.connect(host='{{MILVUS_HOST}}', port='{{MILVUS_PORT}}')
fields = [
    FieldSchema('id', DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema('embedding', DataType.FLOAT_VECTOR, dim=768)
]
schema = CollectionSchema(fields)
col = Collection('my_collection', schema)
print('Collection created:', col.name)
"
```

## AI Agent Tips

- Supports multiple index types: IVF, HNSW, DiskANN, GPU indexes.
- Hybrid search combines vector similarity with scalar filtering.
- Cloud-native with horizontal scaling via Kubernetes.
- Integrates with LangChain, LlamaIndex, and Haystack.
