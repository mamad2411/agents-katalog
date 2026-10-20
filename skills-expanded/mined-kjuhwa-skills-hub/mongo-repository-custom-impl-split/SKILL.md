---
tags: [backend, mongo, repository, custom, impl, split]
name: spring-data-mongo-repository-custom-split
description: Standard 3-file split for MongoRepository — the base interface, a *Custom interface for handwritten queries, and a *Impl class that uses MongoTemplate — so complex queries live beside the CRUD without breaking derived-query inference.
trigger: a repository needs both Spring Data CRUD / derived queries AND complex MongoTemplate-based aggregations or dynamic Criteria
source_project: lucida-cm
version: 1.0.0
category: backend
---

See `content.md`.
