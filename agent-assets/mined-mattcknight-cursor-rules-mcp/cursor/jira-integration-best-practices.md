---
description: Industry best practices for JIRA integration and product requirements ingestion
globs: ["**/*"]
tags: [jira, integration, requirements, ingestion, mcp, automation]
priority: 7
version: 1.0.0
---

# JIRA Integration & Product Requirements Ingestion Best Practices

## Industry Standards Overview

### 1. JIRA Integration Architecture

**Industry Standard:** REST API integration with webhook support
**Cursor Recommendation:** MCP (Model Context Protocol) integration with AI-assisted analysis

#### MCP JIRA Server Configuration
```yaml
# .cursor/mcp-servers.yml
servers:
  jira:
    command: npx @modelcontextprotocol/server-jira
    args:
      - --jira-url=https://your-domain.atlassian.net
      - --jira-username=${JIRA_USERNAME}
      - --jira-api-token=${JIRA_API_TOKEN}
      - --jira-project-keys=PROJ,TEAM,APP
    env:
      JIRA_USERNAME: ${JIRA_USERNAME}
      JIRA_API_TOKEN: ${JIRA_API_TOKEN}
```

#### Available MCP JIRA Functions
```python
# Core JIRA Operations
mcp_jira_jira_ls_projects()                    # List accessible projects
mcp_jira_jira_get_project(projectKeyOrId)      # Get project details
mcp_jira_jira_ls_issues(**filters)             # List issues with filters
mcp_jira_jira_get_issue(issueIdOrKey)          # Get specific issue details
mcp_jira_jira_create_issue(**issue_data)      # Create new issues
mcp_jira_jira_add_comment(issueIdOrKey, body)  # Add comments
mcp_jira_jira_add_worklog(issueIdOrKey, **worklog)  # Log work time
mcp_jira_jira_ls_worklogs(issueIdOrKey)        # List work logs
```

### 2. Product Requirements Ingestion Patterns

**Industry Standard:** User story mapping and acceptance criteria extraction
**Cursor Recommendation:** AI-assisted requirements analysis with persona-based validation

#### Automated Requirements Ingestion Workflow
```python
# scripts/jira-requirements-ingester.py
import json
from datetime import datetime
from typing import List, Dict, Any

class JIRARequirementsIngester:
    def __init__(self, project_key: str):
        self.project_key = project_key
        self.ingestion_patterns = {
            'user_stories': r'As a (.+), I want (.+) so that (.+)',
            'acceptance_criteria': r'Given (.+), when (.+), then (.+)',
            'technical_requirements': r'(?:must|should|shall) (.+)',
            'business_rules': r'Business rule: (.+)'
        }
    
    def ingest_sprint_requirements(self, sprint_id: str) -> Dict[str, Any]:
        """Ingest all requirements from a JIRA sprint"""
        
        # Get sprint issues
        issues = self.get_sprint_issues(sprint_id)
        
        requirements = {
            'sprint_id': sprint_id,
            'ingestion_date': datetime.now().isoformat(),
            'user_stories': [],
            'acceptance_criteria': [],
            'technical_requirements': [],
            'business_rules': [],
            'dependencies': [],
            'risks': []
        }
        
        for issue in issues:
            issue_requirements = self.analyze_issue_requirements(issue)
            self.merge_requirements(requirements, issue_requirements)
        
        return requirements
    
    def analyze_issue_requirements(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single JIRA issue for requirements"""
        
        content = f"{issue.get('summary', '')} {issue.get('description', '')}"
        
        requirements = {
            'issue_key': issue['key'],
            'issue_type': issue['fields']['issuetype']['name'],
            'priority': issue['fields']['priority']['name'],
            'user_stories': self.extract_pattern(content, 'user_stories'),
            'acceptance_criteria': self.extract_pattern(content, 'acceptance_criteria'),
            'technical_requirements': self.extract_pattern(content, 'technical_requirements'),
            'business_rules': self.extract_pattern(content, 'business_rules'),
            'story_points': issue['fields'].get('customfield_10002', 0),
            'labels': issue['fields'].get('labels', []),
            'components': [c['name'] for c in issue['fields'].get('components', [])]
        }
        
        return requirements
    
    def extract_pattern(self, content: str, pattern_type: str) -> List[str]:
        """Extract requirements using regex patterns"""
        
        import re
        pattern = self.ingestion_patterns[pattern_type]
        matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
        return [match if isinstance(match, str) else ' '.join(match) for match in matches]
```

#### Persona-Based Requirements Analysis
```bash
# Requirements Analysis Workflow
@persona-product-manager analyze JIRA sprint PROJ-123
- Extract user stories and acceptance criteria
- Identify business value and user impact
- Map to product roadmap priorities
- Validate against business objectives

@persona-technical-product-manager analyze technical feasibility
- Extract technical requirements from user stories
- Identify system dependencies and constraints
- Estimate implementation complexity
- Create technical implementation roadmap

@persona-solution-architect design system integration
- Map requirements to system architecture
- Identify integration points and APIs
- Design data flow and system interactions
- Create technical specifications

@persona-developer create implementation plan
- Break down user stories into tasks
- Identify code modules and components
- Estimate development effort
- Create development sequence

@persona-qa-engineer create testing strategy
- Map acceptance criteria to test cases
- Identify test scenarios and edge cases
- Create test automation plan
- Define quality gates and metrics
```

### 3. Requirements Documentation Standards

**Industry Standard:** User story format with acceptance criteria
**Cursor Recommendation:** Enhanced with technical specifications and implementation guidance

#### Requirements Document Template
```markdown
# Requirements: [JIRA-Ticket-Key] - [Title]

## Issue Information
- **Key:** [JIRA-123]
- **Type:** [Story/Bug/Task]
- **Priority:** [High/Medium/Low]
- **Story Points:** [1-8]
- **Sprint:** [Sprint Name]
- **Assignee:** [Name]

## User Story
**As a** [user type]  
**I want** [functionality]  
**So that** [business value]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Technical Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Business Rules
- [Rule 1]
- [Rule 2]

## Dependencies
- **Blocks:** [List of blocked tickets]
- **Blocked by:** [List of blocking tickets]
- **Related:** [List of related tickets]

## Implementation Notes
- [Technical consideration 1]
- [Technical consideration 2]

## Testing Strategy
- [Test scenario 1]
- [Test scenario 2]

## Definition of Done
- [ ] Code implemented and reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] QA testing completed
- [ ] Product owner acceptance
```

### 4. Automated JIRA State Management

**Industry Standard:** Webhook-based automation and CI/CD integration
**Cursor Recommendation:** AI-assisted state transitions with context awareness

#### Automated State Transition Rules
```python
# scripts/jira-state-manager.py
class JIRAStateManager:
    def __init__(self):
        self.transition_rules = {
            'To Do': {
                'triggers': ['new_issue_created', 'sprint_started'],
                'conditions': ['has_assignee', 'has_story_points'],
                'actions': ['notify_assignee', 'update_sprint_status']
            },
            'In Progress': {
                'triggers': ['branch_created', 'work_started'],
                'conditions': ['has_active_branch', 'has_worklog_entry'],
                'actions': ['update_worklog', 'notify_team']
            },
            'Code Review': {
                'triggers': ['pull_request_created'],
                'conditions': ['pr_approved', 'tests_passing'],
                'actions': ['assign_reviewer', 'start_review_timer']
            },
            'Testing': {
                'triggers': ['pr_merged', 'deployed_to_staging'],
                'conditions': ['has_test_plan', 'qa_assigned'],
                'actions': ['notify_qa', 'create_test_execution']
            },
            'Done': {
                'triggers': ['qa_approved', 'product_owner_accepted'],
                'conditions': ['all_criteria_met', 'documentation_updated'],
                'actions': ['close_issue', 'update_velocity']
            }
        }
    
    def process_state_transition(self, issue_key: str, trigger: str, context: Dict[str, Any]):
        """Process automated state transition based on trigger and context"""
        
        current_state = self.get_issue_status(issue_key)
        transition_rule = self.transition_rules.get(current_state, {})
        
        if trigger in transition_rule.get('triggers', []):
            if self.check_conditions(transition_rule.get('conditions', []), context):
                self.execute_actions(transition_rule.get('actions', []), issue_key, context)
                self.transition_issue(issue_key, self.get_next_state(current_state))
    
    def check_conditions(self, conditions: List[str], context: Dict[str, Any]) -> bool:
        """Check if transition conditions are met"""
        
        for condition in conditions:
            if condition == 'has_assignee':
                if not context.get('assignee'):
                    return False
            elif condition == 'has_active_branch':
                if not context.get('branch_name'):
                    return False
            elif condition == 'pr_approved':
                if not context.get('pr_approved'):
                    return False
            # Add more condition checks as needed
        
        return True
    
    def execute_actions(self, actions: List[str], issue_key: str, context: Dict[str, Any]):
        """Execute transition actions"""
        
        for action in actions:
            if action == 'notify_assignee':
                self.notify_assignee(issue_key, context)
            elif action == 'update_worklog':
                self.update_worklog(issue_key, context)
            elif action == 'assign_reviewer':
                self.assign_reviewer(issue_key, context)
            # Add more action implementations as needed
```

#### Git-JIRA Integration Hooks
```bash
#!/bin/bash
# .git/hooks/post-commit

# JIRA Integration Hook
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_HASH=$(git rev-parse HEAD)
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

# Extract JIRA ticket from commit message
JIRA_TICKET=$(echo "$COMMIT_MSG" | grep -oE '[A-Z]+-[0-9]+' | head -1)

if [ ! -z "$JIRA_TICKET" ]; then
    # Update JIRA with commit information
    curl -X POST "https://your-domain.atlassian.net/rest/api/3/issue/$JIRA_TICKET/comment" \
        -H "Authorization: Basic $(echo -n $JIRA_USERNAME:$JIRA_API_TOKEN | base64)" \
        -H "Content-Type: application/json" \
        -d "{
            \"body\": {
                \"type\": \"doc\",
                \"version\": 1,
                \"content\": [
                    {
                        \"type\": \"paragraph\",
                        \"content\": [
                            {
                                \"type\": \"text\",
                                \"text\": \"Commit: $COMMIT_HASH\"
                            }
                        ]
                    },
                    {
                        \"type\": \"paragraph\",
                        \"content\": [
                            {
                                \"type\": \"text\",
                                \"text\": \"Branch: $BRANCH_NAME\"
                            }
                        ]
                    },
                    {
                        \"type\": \"paragraph\",
                        \"content\": [
                            {
                                \"type\": \"text\",
                                \"text\": \"Message: $COMMIT_MSG\"
                            }
                        ]
                    }
                ]
            }
        }"
    
    # Log work time if this is a significant commit
    if [[ "$COMMIT_MSG" =~ (feature|bugfix|major) ]]; then
        # Estimate work time based on commit size
        COMMIT_SIZE=$(git diff --stat HEAD~1 HEAD | tail -1 | awk '{print $4}')
        WORK_TIME="30m"  # Default estimate
        
        if [ "$COMMIT_SIZE" -gt 100 ]; then
            WORK_TIME="2h"
        elif [ "$COMMIT_SIZE" -gt 50 ]; then
            WORK_TIME="1h"
        fi
        
        # Log work time to JIRA
        curl -X POST "https://your-domain.atlassian.net/rest/api/3/issue/$JIRA_TICKET/worklog" \
            -H "Authorization: Basic $(echo -n $JIRA_USERNAME:$JIRA_API_TOKEN | base64)" \
            -H "Content-Type: application/json" \
            -d "{
                \"timeSpent\": \"$WORK_TIME\",
                \"started\": \"$(date -u +%Y-%m-%dT%H:%M:%S.000+0000)\",
                \"comment\": \"Work logged automatically from commit $COMMIT_HASH\"
            }"
    fi
fi
```

### 5. Requirements Quality Assurance

**Industry Standard:** Definition of Done and acceptance criteria validation
**Cursor Recommendation:** AI-assisted quality assessment with persona-based validation

#### Requirements Quality Checklist
```markdown
## Requirements Quality Checklist

### User Story Quality
- [ ] **User Role:** Clear definition of user type
- [ ] **Functionality:** Specific, measurable functionality
- [ ] **Business Value:** Clear benefit to user/business
- [ ] **Acceptance Criteria:** Complete and testable
- [ ] **Story Points:** Appropriate estimation

### Technical Quality
- [ ] **Technical Requirements:** Clear and implementable
- [ ] **Dependencies:** Identified and documented
- [ ] **Integration Points:** Defined and validated
- [ ] **Performance Criteria:** Specified if applicable
- [ ] **Security Considerations:** Addressed if applicable

### Business Quality
- [ ] **Business Rules:** Complete and validated
- [ ] **Compliance:** Regulatory requirements addressed
- [ ] **Risk Assessment:** Risks identified and mitigated
- [ ] **Stakeholder Approval:** All stakeholders aligned
- [ ] **Success Metrics:** Measurable outcomes defined
```

#### AI-Assisted Requirements Validation
```python
# scripts/requirements-validator.py
class RequirementsValidator:
    def __init__(self):
        self.validation_rules = {
            'user_story_format': r'As a (.+), I want (.+) so that (.+)',
            'acceptance_criteria_format': r'Given (.+), when (.+), then (.+)',
            'technical_requirements_format': r'(?:must|should|shall) (.+)',
            'definition_of_done': [
                'code implemented',
                'tests written',
                'documentation updated',
                'reviewed',
                'deployed'
            ]
        }
    
    def validate_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Validate requirements against quality standards"""
        
        validation_results = {
            'overall_score': 0,
            'issues': [],
            'recommendations': [],
            'quality_metrics': {}
        }
        
        # Validate user story format
        user_story_score = self.validate_user_story_format(requirements.get('user_story', ''))
        validation_results['quality_metrics']['user_story_score'] = user_story_score
        
        # Validate acceptance criteria
        ac_score = self.validate_acceptance_criteria(requirements.get('acceptance_criteria', []))
        validation_results['quality_metrics']['acceptance_criteria_score'] = ac_score
        
        # Validate technical requirements
        tech_score = self.validate_technical_requirements(requirements.get('technical_requirements', []))
        validation_results['quality_metrics']['technical_requirements_score'] = tech_score
        
        # Calculate overall score
        validation_results['overall_score'] = (user_story_score + ac_score + tech_score) / 3
        
        return validation_results
    
    def validate_user_story_format(self, user_story: str) -> float:
        """Validate user story follows standard format"""
        
        import re
        pattern = self.validation_rules['user_story_format']
        match = re.search(pattern, user_story, re.IGNORECASE)
        
        if match:
            # Check completeness of each part
            user_role = match.group(1).strip()
            functionality = match.group(2).strip()
            business_value = match.group(3).strip()
            
            score = 0
            if len(user_role) > 5: score += 0.33
            if len(functionality) > 10: score += 0.33
            if len(business_value) > 10: score += 0.34
            
            return score
        
        return 0.0
    
    def validate_acceptance_criteria(self, criteria: List[str]) -> float:
        """Validate acceptance criteria quality"""
        
        if not criteria:
            return 0.0
        
        total_score = 0
        for criterion in criteria:
            # Check if criterion is testable
            if any(word in criterion.lower() for word in ['given', 'when', 'then', 'should', 'must']):
                total_score += 1
            elif len(criterion) > 20:  # Substantial criterion
                total_score += 0.5
        
        return min(total_score / len(criteria), 1.0)
```

### 6. Requirements Traceability

**Industry Standard:** Requirements traceability matrix
**Cursor Recommendation:** AI-assisted traceability with automated impact analysis

#### Traceability Matrix Generation
```python
# scripts/traceability-matrix.py
class TraceabilityMatrix:
    def __init__(self):
        self.traceability_data = {
            'requirements': {},
            'test_cases': {},
            'code_components': {},
            'documentation': {}
        }
    
    def generate_matrix(self, project_key: str) -> Dict[str, Any]:
        """Generate requirements traceability matrix"""
        
        # Get all requirements
        requirements = self.get_project_requirements(project_key)
        
        # Build traceability matrix
        matrix = {
            'project_key': project_key,
            'generation_date': datetime.now().isoformat(),
            'requirements': {},
            'coverage_metrics': {}
        }
        
        for req in requirements:
            req_key = req['key']
            matrix['requirements'][req_key] = {
                'summary': req['summary'],
                'test_cases': self.find_linked_test_cases(req_key),
                'code_components': self.find_linked_code(req_key),
                'documentation': self.find_linked_docs(req_key),
                'dependencies': self.find_dependencies(req_key),
                'impact_analysis': self.analyze_impact(req_key)
            }
        
        # Calculate coverage metrics
        matrix['coverage_metrics'] = self.calculate_coverage_metrics(matrix['requirements'])
        
        return matrix
    
    def find_linked_test_cases(self, requirement_key: str) -> List[str]:
        """Find test cases linked to requirement"""
        
        # Query JIRA for linked test cases
        # Implementation would use JIRA API to find linked issues
        return []
    
    def find_linked_code(self, requirement_key: str) -> List[str]:
        """Find code components linked to requirement"""
        
        # Search git commits for requirement references
        # Implementation would search commit messages and code comments
        return []
    
    def analyze_impact(self, requirement_key: str) -> Dict[str, Any]:
        """Analyze impact of requirement changes"""
        
        return {
            'affected_components': [],
            'risk_level': 'low',
            'effort_estimate': '1-2 days',
            'dependencies': []
        }
```

## Implementation Roadmap

### Phase 1: Foundation Setup (Week 1-2)
- [ ] Configure MCP JIRA server
- [ ] Set up authentication and permissions
- [ ] Create basic requirements ingestion scripts
- [ ] Establish requirements documentation templates

### Phase 2: Automation Development (Week 3-4)
- [ ] Implement automated requirements analysis
- [ ] Create persona-based validation workflows
- [ ] Build state management automation
- [ ] Develop quality assessment tools

### Phase 3: Integration & Testing (Week 5-6)
- [ ] Integrate with existing git workflows
- [ ] Test with real JIRA projects
- [ ] Validate requirements quality metrics
- [ ] Refine automation rules

### Phase 4: Advanced Features (Week 7-8)
- [ ] Implement traceability matrix generation
- [ ] Create impact analysis tools
- [ ] Build requirements analytics dashboard
- [ ] Develop predictive requirements insights

### Phase 5: Optimization & Training (Week 9-10)
- [ ] Optimize performance and accuracy
- [ ] Train team on new workflows
- [ ] Gather feedback and iterate
- [ ] Document best practices and lessons learned

## Success Metrics

### Requirements Quality Metrics
- **Completeness:** % of requirements with complete acceptance criteria
- **Clarity:** Average readability score of requirements
- **Traceability:** % of requirements with full traceability
- **Validation:** % of requirements validated by personas

### Process Efficiency Metrics
- **Ingestion Speed:** Time from JIRA creation to analysis completion
- **Validation Time:** Time to validate requirements quality
- **State Transition:** Time for automated state changes
- **Traceability:** Time to generate traceability matrix

### Business Impact Metrics
- **Requirements Accuracy:** % of requirements implemented as specified
- **Change Impact:** Time to assess impact of requirement changes
- **Stakeholder Satisfaction:** Feedback scores on requirements quality
- **Delivery Predictability:** Accuracy of effort estimates

---

**Last Updated:** 2025-10-27  
**Version:** 1.0.0  
**Maintained By:** AI Research Team  
**Review Cycle:** Monthly
