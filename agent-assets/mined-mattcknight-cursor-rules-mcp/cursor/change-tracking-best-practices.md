---
description: Industry best practices for change tracking, history, and learning capture
globs: ["**/*"]
tags: [change-tracking, history, learning-capture, automation, metrics]
priority: 4
version: 1.0.0
---

# Change Tracking & History Best Practices

## Industry Standards Overview

### 1. Git-Based Change Tracking (Foundation)

**Industry Standard:** Git provides the technical foundation for change tracking
**Cursor Recommendation:** Enhanced with Jira ticket-prefixed commit messages and automated workflows

#### 🔴 MANDATORY Commit Message Format

**ALL commit messages MUST start with Jira ticket number:**

```bash
# Format: [PROJECT_KEY]-[NUMBER] Brief description
PROJ-1234 Add user authentication with JWT tokens

- Implemented JWT token generation and validation
- Added user login and registration endpoints
- Created middleware for token verification
- Updated API documentation with auth examples

Related: PROJ-4567, PROJ-7890
Closes: PROJ-1234
```

#### ❌ FORBIDDEN Commit Formats

**NEVER use these formats:**
- ❌ Conventional commits: `feat(auth): add JWT token validation`
- ❌ Semantic commits: `fix(api): resolve memory leak`
- ❌ Type prefixes: `feature: add authentication`, `bugfix: fix issue`
- ❌ Component prefixes: `[API] Add authentication`
- ❌ Format with type: `PROJ-1234 -feature [API] Add authentication`

### 2. Automated Change Detection

**Industry Standard:** CI/CD pipelines with automated triggers
**Cursor Recommendation:** AI-assisted change detection with learning capture

#### Implementation Pattern
```yaml
# .github/workflows/change-detection.yml
name: Automated Change Detection

on:
  push:
    branches: [main, develop]
  pull_request:
    types: [opened, synchronize]

jobs:
  change-detection:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for comparison
      
      - name: Detect Changes
        run: |
          # Detect significant changes
          if git diff --name-only HEAD~1 HEAD | grep -E '\.(py|js|ts|md)$'; then
            echo "SIGNIFICANT_CHANGES=true" >> $GITHUB_ENV
          fi
      
      - name: Trigger Learning Capture
        if: env.SIGNIFICANT_CHANGES == 'true'
        run: |
          # Trigger AI learning capture
          curl -X POST "${{ secrets.AI_WEBHOOK_URL }}" \
            -H "Content-Type: application/json" \
            -d '{
              "action": "capture_learning",
              "commit": "${{ github.sha }}",
              "author": "${{ github.actor }}",
              "files_changed": "'$(git diff --name-only HEAD~1 HEAD | tr '\n' ',' | sed 's/,$//')'"
            }'
```

#### AI-Assisted Change Detection
```python
# scripts/ai-change-detector.py
import subprocess
import json
from datetime import datetime

def detect_significant_changes():
    """Detect changes that warrant learning capture"""
    
    # Get commit details
    commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    commit_message = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode().strip()
    files_changed = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD']).decode().strip().split('\n')
    
    # Analyze change significance
    significant_patterns = [
        r'\.cursor/rules/',  # Rule changes
        r'docs/learnings/',  # Learning documents
        r'docs/recommendations/',  # Recommendations
        r'architecture',  # Architecture changes
        r'refactor',  # Refactoring
        r'breaking',  # Breaking changes
    ]
    
    significant_changes = []
    for file in files_changed:
        for pattern in significant_patterns:
            if re.search(pattern, file, re.IGNORECASE):
                significant_changes.append(file)
                break
    
    if significant_changes:
        trigger_learning_capture({
            'commit_hash': commit_hash,
            'commit_message': commit_message,
            'significant_files': significant_changes,
            'timestamp': datetime.now().isoformat()
        })

def trigger_learning_capture(change_data):
    """Trigger AI learning capture for significant changes"""
    
    learning_prompt = f"""
    Analyze the following changes and create a learning document:
    
    Commit: {change_data['commit_hash']}
    Message: {change_data['commit_message']}
    Files: {', '.join(change_data['significant_files'])}
    
    Please create a learning document following the format:
    - Context: What led to these changes?
    - Problem: What challenge was being solved?
    - Solution: How was it implemented?
    - Lessons Learned: What insights emerged?
    - Recommendations: What should be done next?
    """
    
    # Send to AI for processing
    # Implementation would call AI API to generate learning document
```

### 3. Delta Visualization

**Industry Standard:** Git diff tools and change visualization
**Cursor Recommendation:** AI-enhanced delta analysis with context

#### Before/After Comparison Framework
```markdown
# Delta Analysis Template

## Change Summary
**Commit:** [hash]  
**Date:** [timestamp]  
**Author:** [name]  
**Jira Ticket:** [PROJ-1234]

## Before State
```diff
- [Previous code/configuration]
- [Previous structure]
- [Previous behavior]
```

## After State
```diff
+ [New code/configuration]
+ [New structure]
+ [New behavior]
```

## Impact Analysis
- **Files Changed:** [count]
- **Lines Added:** [count]
- **Lines Removed:** [count]
- **Breaking Changes:** [yes/no]
- **Dependencies Affected:** [list]

## Learning Insights
- [Key insight 1]
- [Key insight 2]
- [Pattern identified]
```

#### Automated Delta Generation
```python
# scripts/delta-analyzer.py
import subprocess
import json
from datetime import datetime

def generate_delta_analysis(commit_hash):
    """Generate comprehensive delta analysis for a commit"""
    
    # Get commit details
    commit_info = subprocess.check_output([
        'git', 'show', '--stat', '--pretty=format:%H|%an|%ae|%ad|%s', commit_hash
    ]).decode().strip()
    
    # Get file changes
    files_changed = subprocess.check_output([
        'git', 'diff', '--name-status', f'{commit_hash}~1', commit_hash
    ]).decode().strip().split('\n')
    
    # Generate diff for each file
    deltas = []
    for file_change in files_changed:
        if file_change:
            status, file_path = file_change.split('\t', 1)
            diff_content = subprocess.check_output([
                'git', 'diff', f'{commit_hash}~1', commit_hash, '--', file_path
            ]).decode()
            
            deltas.append({
                'file': file_path,
                'status': status,
                'diff': diff_content,
                'lines_added': len([l for l in diff_content.split('\n') if l.startswith('+')]),
                'lines_removed': len([l for l in diff_content.split('\n') if l.startswith('-')])
            })
    
    return {
        'commit_hash': commit_hash,
        'timestamp': datetime.now().isoformat(),
        'deltas': deltas,
        'summary': {
            'files_changed': len(deltas),
            'total_lines_added': sum(d['lines_added'] for d in deltas),
            'total_lines_removed': sum(d['lines_removed'] for d in deltas)
        }
    }
```

### 4. Learning Metrics & Quality Tracking

**Industry Standard:** Code quality metrics and documentation coverage
**Cursor Recommendation:** AI-assisted learning quality assessment

#### Learning Metrics Dashboard
```python
# scripts/learning-metrics.py
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

class LearningMetrics:
    def __init__(self, learnings_dir="docs/learnings"):
        self.learnings_dir = Path(learnings_dir)
    
    def calculate_metrics(self, days=30):
        """Calculate learning capture metrics for the last N days"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        learnings = self.get_recent_learnings(cutoff_date)
        
        metrics = {
            'period_days': days,
            'total_learnings': len(learnings),
            'learnings_per_day': len(learnings) / days,
            'quality_scores': self.assess_quality(learnings),
            'coverage_areas': self.analyze_coverage(learnings),
            'trends': self.analyze_trends(learnings)
        }
        
        return metrics
    
    def assess_quality(self, learnings):
        """Assess quality of learning documents"""
        
        quality_criteria = {
            'has_context': 0,
            'has_problem': 0,
            'has_solution': 0,
            'has_lessons': 0,
            'has_recommendations': 0,
            'has_examples': 0,
            'has_related_links': 0
        }
        
        for learning in learnings:
            content = learning.read_text()
            
            if '## Context' in content: quality_criteria['has_context'] += 1
            if '## Problem' in content: quality_criteria['has_problem'] += 1
            if '## Solution' in content: quality_criteria['has_solution'] += 1
            if '## Lessons Learned' in content: quality_criteria['has_lessons'] += 1
            if '## Recommendations' in content: quality_criteria['has_recommendations'] += 1
            if '```' in content: quality_criteria['has_examples'] += 1
            if '## Related' in content: quality_criteria['has_related_links'] += 1
        
        # Convert to percentages
        total = len(learnings)
        return {k: (v / total * 100) if total > 0 else 0 for k, v in quality_criteria.items()}
    
    def analyze_coverage(self, learnings):
        """Analyze coverage areas in learnings"""
        
        coverage_areas = {
            'architecture': 0,
            'development': 0,
            'testing': 0,
            'deployment': 0,
            'documentation': 0,
            'process': 0,
            'tools': 0
        }
        
        for learning in learnings:
            content = learning.read_text().lower()
            
            if any(word in content for word in ['architecture', 'design', 'system']):
                coverage_areas['architecture'] += 1
            if any(word in content for word in ['code', 'implementation', 'development']):
                coverage_areas['development'] += 1
            if any(word in content for word in ['test', 'testing', 'qa']):
                coverage_areas['testing'] += 1
            if any(word in content for word in ['deploy', 'deployment', 'ci/cd']):
                coverage_areas['deployment'] += 1
            if any(word in content for word in ['documentation', 'docs', 'readme']):
                coverage_areas['documentation'] += 1
            if any(word in content for word in ['process', 'workflow', 'procedure']):
                coverage_areas['process'] += 1
            if any(word in content for word in ['tool', 'tooling', 'automation']):
                coverage_areas['tools'] += 1
        
        return coverage_areas
```

#### Learning Quality Checklist
```markdown
## Learning Document Quality Checklist

### Content Quality (Required)
- [ ] **Context:** Clear description of the situation
- [ ] **Problem:** Specific challenge or issue identified
- [ ] **Solution:** Detailed approach taken
- [ ] **Lessons Learned:** Key insights extracted
- [ ] **Recommendations:** Actionable next steps

### Technical Quality (Recommended)
- [ ] **Examples:** Concrete code or configuration examples
- [ ] **Before/After:** Clear comparison showing change
- [ ] **Related Links:** References to related documents
- [ ] **Metrics:** Quantifiable results or improvements
- [ ] **Anti-patterns:** What to avoid

### Formatting Quality (Required)
- [ ] **Proper Headers:** Clear section organization
- [ ] **Code Blocks:** Properly formatted with language tags
- [ ] **Lists:** Well-structured bullet points
- [ ] **Links:** Working internal and external links
- [ ] **Metadata:** Proper YAML frontmatter
```

### 5. Cross-Reference Linking

**Industry Standard:** Documentation linking and knowledge graphs
**Cursor Recommendation:** AI-assisted relationship mapping

#### Automated Cross-Reference Generation
```python
# scripts/cross-reference-generator.py
import re
import json
from pathlib import Path
from collections import defaultdict

class CrossReferenceGenerator:
    def __init__(self, docs_dir="docs"):
        self.docs_dir = Path(docs_dir)
        self.references = defaultdict(list)
    
    def generate_cross_references(self):
        """Generate cross-references between documents"""
        
        # Scan all documents
        all_docs = list(self.docs_dir.rglob("*.md"))
        
        for doc in all_docs:
            content = doc.read_text()
            doc_id = str(doc.relative_to(self.docs_dir))
            
            # Find references to other documents
            references = self.find_document_references(content, all_docs)
            
            # Find references to commits
            commit_refs = self.find_commit_references(content)
            
            # Find references to issues/tickets
            issue_refs = self.find_issue_references(content)
            
            self.references[doc_id] = {
                'document_references': references,
                'commit_references': commit_refs,
                'issue_references': issue_refs
            }
        
        return self.references
    
    def find_document_references(self, content, all_docs):
        """Find references to other documents"""
        
        references = []
        doc_names = [d.stem for d in all_docs]
        
        for doc_name in doc_names:
            # Look for various reference patterns
            patterns = [
                rf'\b{doc_name}\b',
                rf'\[{doc_name}\]',
                rf'`{doc_name}`',
                rf'"{doc_name}"'
            ]
            
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    references.append(doc_name)
                    break
        
        return list(set(references))
    
    def find_commit_references(self, content):
        """Find references to git commits"""
        
        commit_pattern = r'[a-f0-9]{7,40}'
        return re.findall(commit_pattern, content)
    
    def find_issue_references(self, content):
        """Find references to issues/tickets"""
        
        issue_pattern = r'[A-Z]+-\d+'
        return re.findall(issue_pattern, content)
```

#### Cross-Reference Template
```markdown
# Cross-Reference Network

## Document Relationships
```mermaid
graph TD
    A[Learning: Evolution Chat to Persona AI] --> B[Persona Framework Synthesis]
    A --> C[AI Research Project Adaptation]
    B --> D[Template Generation Guidelines]
    C --> D
    D --> E[Cursor Rules Structure Best Practices]
```

## Related Changes
- **Commits:** [list of related commits]
- **Issues:** [list of related JIRA tickets]
- **Documents:** [list of related documents]
- **Personas:** [list of affected personas]

## Impact Chain
1. [Initial change] → [Secondary change] → [Final outcome]
2. [Pattern identified] → [Template created] → [Best practice established]
```

### 6. Template Automation

**Industry Standard:** Automated documentation generation
**Cursor Recommendation:** AI-assisted template generation from git commits

#### Automated Learning Document Generation
```python
# scripts/auto-learning-generator.py
import subprocess
import json
from datetime import datetime
from pathlib import Path

class AutoLearningGenerator:
    def __init__(self, learnings_dir="docs/learnings"):
        self.learnings_dir = Path(learnings_dir)
    
    def generate_from_commit(self, commit_hash):
        """Generate learning document from git commit"""
        
        # Get commit details
        commit_info = self.get_commit_info(commit_hash)
        
        # Analyze changes
        changes = self.analyze_changes(commit_hash)
        
        # Generate learning document
        learning_doc = self.create_learning_document(commit_info, changes)
        
        # Save document
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_auto_learning_{commit_hash[:7]}.md"
        filepath = self.learnings_dir / filename
        filepath.write_text(learning_doc)
        
        return filepath
    
    def get_commit_info(self, commit_hash):
        """Get detailed commit information"""
        
        info = subprocess.check_output([
            'git', 'show', '--pretty=format:%H|%an|%ae|%ad|%s|%b', commit_hash
        ]).decode().strip()
        
        parts = info.split('|', 5)
        return {
            'hash': parts[0],
            'author': parts[1],
            'email': parts[2],
            'date': parts[3],
            'subject': parts[4],
            'body': parts[5] if len(parts) > 5 else ''
        }
    
    def analyze_changes(self, commit_hash):
        """Analyze what changed in the commit"""
        
        # Get file changes
        files_changed = subprocess.check_output([
            'git', 'diff', '--name-status', f'{commit_hash}~1', commit_hash
        ]).decode().strip().split('\n')
        
        # Categorize changes
        categories = {
            'rules': [],
            'documentation': [],
            'code': [],
            'configuration': [],
            'tests': []
        }
        
        for file_change in files_changed:
            if file_change:
                status, file_path = file_change.split('\t', 1)
                
                if '.cursor/rules' in file_path:
                    categories['rules'].append((file_path, status))
                elif file_path.startswith('docs/'):
                    categories['documentation'].append((file_path, status))
                elif file_path.endswith(('.py', '.js', '.ts', '.java')):
                    categories['code'].append((file_path, status))
                elif file_path.endswith(('.json', '.yaml', '.yml', '.toml')):
                    categories['configuration'].append((file_path, status))
                elif 'test' in file_path.lower():
                    categories['tests'].append((file_path, status))
        
        return categories
    
    def create_learning_document(self, commit_info, changes):
        """Create learning document from commit analysis"""
        
        # Determine learning type based on changes
        if changes['rules']:
            learning_type = "Rule Structure Change"
        elif changes['documentation']:
            learning_type = "Documentation Update"
        elif changes['code']:
            learning_type = "Code Implementation"
        else:
            learning_type = "General Change"
        
        # Generate document content
        doc_content = f"""# Learning: {learning_type} - {commit_info['subject']}

**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Commit:** {commit_info['hash'][:7]}  
**Author:** {commit_info['author']}  
**Type:** {learning_type}

## Context

This learning was automatically generated from commit {commit_info['hash'][:7]}.

**Commit Message:** {commit_info['subject']}

**Commit Body:**
```
{commit_info['body']}
```

## Changes Made

### Rule Changes
{self.format_file_changes(changes['rules'])}

### Documentation Changes
{self.format_file_changes(changes['documentation'])}

### Code Changes
{self.format_file_changes(changes['code'])}

### Configuration Changes
{self.format_file_changes(changes['configuration'])}

### Test Changes
{self.format_file_changes(changes['tests'])}

## Problem

[AI Analysis: What problem was this commit solving?]

## Solution

[AI Analysis: How was the problem addressed?]

## Lessons Learned

- [AI Analysis: Key insight 1]
- [AI Analysis: Key insight 2]
- [AI Analysis: Key insight 3]

## Recommendations

- [AI Analysis: Recommendation 1]
- [AI Analysis: Recommendation 2]

## Related

- **Commit:** {commit_info['hash']}
- **Author:** {commit_info['author']}
- **Date:** {commit_info['date']}

---

*This document was automatically generated from git commit analysis.*
"""
        
        return doc_content
    
    def format_file_changes(self, file_changes):
        """Format file changes for display"""
        
        if not file_changes:
            return "None"
        
        formatted = []
        for file_path, status in file_changes:
            status_symbol = {
                'A': '➕',
                'M': '✏️',
                'D': '❌',
                'R': '🔄'
            }.get(status, '📝')
            
            formatted.append(f"- {status_symbol} `{file_path}`")
        
        return '\n'.join(formatted)
```

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Implement Jira ticket-prefixed commit message validation
- [ ] Set up automated change detection
- [ ] Create learning metrics dashboard
- [ ] Establish quality checklist

### Phase 2: Automation (Week 3-4)
- [ ] Deploy AI-assisted change detection
- [ ] Implement delta visualization
- [ ] Create cross-reference generator
- [ ] Build template automation

### Phase 3: Optimization (Week 5-6)
- [ ] Refine learning quality metrics
- [ ] Optimize cross-reference accuracy
- [ ] Enhance template generation
- [ ] Create learning analytics dashboard

### Phase 4: Integration (Week 7-8)
- [ ] Integrate with existing workflows
- [ ] Train team on new processes
- [ ] Monitor and iterate
- [ ] Document best practices

---

**Last Updated:** 2025-10-27  
**Version:** 1.0.0  
**Maintained By:** AI Research Team  
**Review Cycle:** Monthly
