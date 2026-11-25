---
title: Document Control Workflow Skill
description: Skill for document control management including registration, numbering, transmittal tracking, RFI processing, and records management
version: 1.0
frequency: Daily
success_rate: 95%
tags:
  - document-control-workflow
  - document-registration
  - transmittal-tracking
  - rfi-processing
  - records-management
  - 00900_document-control
docs:
  - docs_construct_ai/disciplines/00900_document-control/agent-data/domain-knowledge/00900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00900_document-control/agent-data/prompts/00900_AI-NATIVE-DOCUMENT-CONTROL-PROMPT.md
---

# Document Control Workflow Skill

## Overview

This skill provides capability for document control workflow management including document registration, numbering, transmittal processing, RFI tracking, and records management. It supports Document Control (00900) in their operational responsibilities.

## Triggers

- New document received for registration
- Transmittal processing required
- RFI received for processing
- Document status enquiry
- Records management action needed

## Prerequisites

- Access to EDMS
- Access to document numbering system
- Access to transmittal register
- Access to RFI register
- Document Control domain knowledge loaded

## Steps

### Step 1: Process Document
- Receive document via transmittal, email, or upload
- Assign document number using numbering rules
- Capture metadata (type, discipline, revision, originator)
- Log in document register

### Step 2: Route for Review
- Configure review workflow based on document type
- Route to appropriate reviewers
- Track review progress and deadlines
- Follow up on overdue reviews

### Step 3: Manage Transmittals
- Create transmittal with documents and recipients
- Track dispatch and receipt
- Monitor response deadlines
- Follow up on overdue responses
- Archive completed transmittals

### Step 4: Process RFIs
- Register RFI with unique number
- Route to appropriate discipline for response
- Track response progress and deadlines
- Verify response completeness
- Close out RFI and archive

### Step 5: Manage Records
- Apply retention schedules
- Archive documents per retention policy
- Prepare handover documentation
- Verify records completeness

## Success Criteria

- All documents registered with valid numbers
- All transmittals tracked with response monitoring
- All RFIs tracked from receipt to closeout
- Records retained per policy
- No overdue items unmonitored

## Pitfalls

- Do not release unapproved documents
- Do not distribute superseded revisions
- Do not bypass required review workflows
- Do not authorize records disposal without permission
- Do not lose or misplace project records

## Cross-References

- 00900 Document Control domain knowledge
- All engineering disciplines (document consumers)
- 00300 Construction discipline
- 02200 Quality Assurance discipline