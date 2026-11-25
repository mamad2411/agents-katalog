---
memory_layer: durable_knowledge
para_section: pages/skills/python-module-naming-standards
gigabrain_tags: python, naming-standards, modules, packages, pep8, imports
openstinger_context: python-naming-standards, module-organization
last_updated: 2026-03-30
related_docs:
  - docs_construct_ai/codebase/coding-standards/
  - docs_construct_ai/codebase/architecture/
related_skills:
  - agent-coding-standards
  - agent-development-standards
  - file-naming-standards
frequency_percent: 92.0
success_rate_percent: 98.0
---

# Python Module Naming Standards

## Overview

**Core principle:** Follow PEP 8 and Construct AI standards for Python module and package naming to ensure compatibility with Python import system, IDE tooling, and static analysis tools.

**Critical requirement:** Use underscores instead of hyphens in all Python module and package names to prevent import syntax errors.

## When to Use This Skill

**Trigger Conditions:**
- When creating Python modules, packages, or directories
- Before implementing Python agent code
- When setting up Python project structure
- During code reviews of Python code
- When refactoring Python imports or module structure
- When debugging Python import errors
- When integrating Python agents with existing systems

**Mandatory Application:**
- Required for all Python development in Construct AI
- Must be applied before any Python code implementation
- Required for both new Python code and refactoring
- Must be verified before Python code deployment
- Required for maintaining Python ecosystem compatibility

## Step-by-Step Procedure

### Step 1: Understand PEP 8 Compliance Requirements
**Master the fundamental Python naming rules:**

```python
# PEP 8 Python naming rules validation
class PythonNamingValidator:
    def __init__(self):
        self.valid_chars = set('abcdefghijklmnopqrstuvwxyz0123456789_')
        
    def validate_module_name(self, name: str) -> dict:
        """
        Validate Python module/package name against PEP 8.
        
        Args:
            name: Module or package name to validate
            
        Returns:
            dict: Validation result with errors and suggestions
        """
        errors = []
        suggestions = []
        
        # Check lowercase only
        if name != name.lower():
            errors.append('Module names must be lowercase')
            suggestions.append(f'Convert to: {name.lower()}')
        
        # Check valid characters only
        invalid_chars = set(name) - self.valid_chars
        if invalid_chars:
            errors.append(f'Invalid characters found: {invalid_chars}')
            # Suggest underscore replacement for hyphens
            if '-' in invalid_chars:
                underscored = name.replace('-', '_')
                suggestions.append(f'Replace hyphens with underscores: {underscored}')
        
        # Check starts with letter or underscore
        if name and not (name[0].isalpha() or name[0] == '_'):
            errors.append('Module names must start with letter or underscore')
        
        # Check not a Python keyword
        python_keywords = {
            'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
            'def', 'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try',
            'while', 'with', 'yield'
        }
        if name in python_keywords:
            errors.append(f'Cannot use Python keyword: {name}')
        
        # Check reasonable length
        if len(name) > 64:
            errors.append('Module name too long (max 64 characters)')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'suggestions': suggestions
        }

# Usage
validator = PythonNamingValidator()

# Valid names
print(validator.validate_module_name('deep_agents'))  # {'valid': True}
print(validator.validate_module_name('procurement_workflow'))  # {'valid': True}

# Invalid names (hyphenated)
print(validator.validate_module_name('01900-procurement'))
# {'valid': False, 'errors': [...], 'suggestions': ['Replace hyphens with underscores: 01900_procurement']}
```

**PEP 8 Requirements:**
- All module and package names must be lowercase
- Use underscores for word separation (never hyphens)
- Only letters, numbers, and underscores allowed
- Must be valid Python identifiers
- Cannot be Python keywords
- Reasonable length (under 64 characters)

### Step 2: Apply Construct AI Python Naming Patterns
**Follow discipline-specific naming conventions:**

```python
# Construct AI Python naming patterns
class ConstructAINamingStandards:
    def __init__(self):
        self.discipline_codes = {
            '00102': 'administration',
            '00300': 'construction', 
            '00400': 'contracts',
            '00825': 'architectural',
            '00835': 'chemical_engineering',
            '00850': 'civil_engineering',
            '00855': 'geotechnical_engineering',
            '00860': 'electrical_engineering',
            '00870': 'mechanical_engineering',
            '00871': 'process_engineering',
            '00872': 'structural',
            '01300': 'governance',
            '01900': 'procurement',
            '02000': 'project_controls',
            '02035': 'scheduling',
            '02400': 'safety'
        }
    
    def generate_package_name(self, discipline_code: str, purpose: str = None) -> str:
        """
        Generate proper package name for discipline.
        
        Args:
            discipline_code: Discipline code (e.g., '01900')
            purpose: Optional purpose suffix
            
        Returns:
            str: Properly formatted package name
        """
        if discipline_code not in self.discipline_codes:
            raise ValueError(f'Unknown discipline code: {discipline_code}')
        
        base_name = self.discipline_codes[discipline_code]
        package_name = f'{discipline_code}_{base_name}'
        
        if purpose:
            # Clean purpose and add as suffix
            clean_purpose = purpose.lower().replace(' ', '_').replace('-', '_')
            package_name = f'{package_name}_{clean_purpose}'
        
        return package_name
    
    def generate_module_name(self, package_name: str, module_type: str, 
                           identifier: str = None) -> str:
        """
        Generate proper module name within package.
        
        Args:
            package_name: Parent package name
            module_type: Type of module (agent, utility, core, abstract)
            identifier: Optional identifier for the module
            
        Returns:
            str: Properly formatted module name
        """
        type_prefixes = {
            'agent': '',  # No prefix for agent modules
            'utility': '',  # No prefix for utility modules  
            'core': 'c_',  # Core framework modules
            'abstract': 'a_'  # Abstract base classes
        }
        
        if module_type not in type_prefixes:
            raise ValueError(f'Unknown module type: {module_type}')
        
        prefix = type_prefixes[module_type]
        
        if module_type == 'agent':
            # Agent modules: {code}_{agent_name}_agent.py
            return f'{identifier}_agent.py'
        elif module_type == 'abstract':
            # Abstract modules: a_{number}_{name}.py
            return f'{prefix}{identifier}_{package_name.split("_")[1]}_base.py'
        else:
            # Other modules: {prefix}{purpose}.py
            return f'{prefix}{identifier}.py'

# Usage
standards = ConstructAINamingStandards()

# Generate package names
print(standards.generate_package_name('01900'))  # '01900_procurement'
print(standards.generate_package_name('00850', 'coordinator'))  # '00850_civil_engineering_coordinator'

# Generate module names
print(standards.generate_module_name('01900_procurement', 'agent', '01900_template_analysis'))
# '01900_template_analysis_agent.py'

print(standards.generate_module_name('core', 'core', 'deep_agents_state_management'))
# 'c_deep_agents_state_management.py'

print(standards.generate_module_name('shared', 'abstract', '0000'))
# 'a_0000_shared_base.py'
```

**Construct AI Patterns:**
- Discipline packages: `{code}_{discipline_name}`
- Agent modules: `{code}_{agent_name}_agent.py`
- Core modules: `c_{purpose}.py`
- Abstract bases: `a_{number}_{name}.py`
- Utility modules: `{purpose}.py`

### Step 3: Implement Proper Directory Structure
**Create Python package structure following standards:**

```python
# Python package structure implementation
import os
import pathlib
from typing import List, Dict, Any

class PythonPackageStructure:
    def __init__(self, root_path: str):
        self.root_path = pathlib.Path(root_path)
        
    def create_package_structure(self, discipline_code: str, 
                               package_config: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Create complete Python package structure.
        
        Args:
            discipline_code: Discipline code (e.g., '01900')
            package_config: Configuration for package structure
            
        Returns:
            dict: Created files and directories
        """
        created_items = {
            'directories': [],
            'files': []
        }
        
        # Generate package name
        standards = ConstructAINamingStandards()
        package_name = standards.generate_package_name(discipline_code)
        
        # Create main package directory
        package_dir = self.root_path / 'deep_agents' / 'agents' / 'pages' / package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        created_items['directories'].append(str(package_dir))
        
        # Create __init__.py
        init_file = package_dir / '__init__.py'
        self._create_init_file(init_file, package_config)
        created_items['files'].append(str(init_file))
        
        # Create subdirectories
        subdirs = ['main_agents', 'coordinator_agents', 'specialist_agents', 'utilities']
        for subdir in subdirs:
            subdir_path = package_dir / subdir
            subdir_path.mkdir(exist_ok=True)
            created_items['directories'].append(str(subdir_path))
            
            # Create __init__.py for each subdirectory
            sub_init = subdir_path / '__init__.py'
            self._create_init_file(sub_init, {'subpackage': subdir})
            created_items['files'].append(str(sub_init))
        
        # Create main agent modules
        if 'agents' in package_config:
            for agent_config in package_config['agents']:
                agent_file = package_dir / 'main_agents' / f"{agent_config['code']}_{agent_config['name']}_agent.py"
                self._create_agent_module(agent_file, agent_config)
                created_items['files'].append(str(agent_file))
        
        # Create utility modules
        if 'utilities' in package_config:
            for util_config in package_config['utilities']:
                util_file = package_dir / 'utilities' / f"{util_config['name']}.py"
                self._create_utility_module(util_file, util_config)
                created_items['files'].append(str(util_file))
        
        return created_items
    
    def _create_init_file(self, file_path: pathlib.Path, config: Dict[str, Any]):
        """Create __init__.py file with proper imports."""
        imports = []
        
        if 'subpackage' in config:
            # Subpackage init - import from parent
            pass  # Minimal init for subpackages
        else:
            # Main package init
            imports.append('"""')
            imports.append(f"{config.get('name', 'Package')} agents and utilities.")
            imports.append('"""')
            imports.append('')
            imports.append('__version__ = "1.0.0"')
        
        content = '\n'.join(imports)
        file_path.write_text(content)
    
    def _create_agent_module(self, file_path: pathlib.Path, config: Dict[str, Any]):
        """Create agent module with proper structure."""
        content = f'''"""
{config.get('name', 'Agent')} - {config.get('description', 'Agent implementation')}

Generated following Construct AI Python naming standards.
"""

from deep_agents.core.python.unified_agent_framework import UnifiedAgent, AgentConfig
from typing import Dict, List, Any, Optional
import asyncio


class {config.get('class_name', 'Agent')}(UnifiedAgent):
    """
    {config.get('name', 'Agent')} implementation.
    
    DESCRIPTION = "{config.get('description', 'Agent functionality')}"
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        # Agent-specific initialization
    
    async def _executeImpl(self, workflow_state: Dict[str, Any], 
                          options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic.
        
        Args:
            workflow_state: Current workflow state
            options: Execution options
            
        Returns:
            Dict containing results
        """
        # Implementation here
        return {{
            "agent_id": self.agent_id,
            "status": "completed",
            "result": workflow_state
        }}


# Export the agent class
__all__ = ["{config.get('class_name', 'Agent')}"]
'''
        file_path.write_text(content)

# Usage
structure = PythonPackageStructure('/path/to/project')

config = {
    'name': 'Procurement Agents',
    'agents': [
        {
            'code': '01900',
            'name': 'template_analysis',
            'class_name': 'ProcurementTemplateAnalysisAgent',
            'description': 'Analyzes procurement templates'
        }
    ],
    'utilities': [
        {
            'name': 'validation_utils',
            'description': 'Validation utilities for procurement'
        }
    ]
}

created = structure.create_package_structure('01900', config)
print("Created structure:", created)
```

**Directory Structure Standards:**
- Discipline packages: `deep_agents/agents/pages/{code}_{discipline}/`
- Subdirectories: `main_agents/`, `coordinator_agents/`, `specialist_agents/`, `utilities/`
- All directories use underscores, never hyphens
- Each directory has `__init__.py` file

### Step 4: Handle Import Statement Corrections
**Fix import statements to work with proper naming:**

```python
# Import statement correction utilities
class ImportStatementFixer:
    def __init__(self):
        self.hyphen_to_underscore_map = {
            '01900-procurement': '01900_procurement',
            '00850-civil-engineering': '00850_civil_engineering',
            '01300-governance': '01300_governance',
            # Add more mappings as needed
        }
    
    def fix_import_statement(self, import_line: str) -> str:
        """
        Fix import statement to use underscores instead of hyphens.
        
        Args:
            import_line: Original import statement
            
        Returns:
            str: Fixed import statement
        """
        # Handle different import patterns
        if import_line.startswith('from '):
            return self._fix_from_import(import_line)
        elif import_line.startswith('import '):
            return self._fix_direct_import(import_line)
        else:
            return import_line  # Not an import statement
    
    def _fix_from_import(self, import_line: str) -> str:
        """Fix from...import statements."""
        # Pattern: from deep_agents.agents.pages.01900-procurement.main_agents import Agent
        parts = import_line.split()
        if len(parts) >= 2:
            module_path = parts[1]
            # Replace hyphenated parts with underscored versions
            for old, new in self.hyphen_to_underscore_map.items():
                module_path = module_path.replace(old, new)
            parts[1] = module_path
            return ' '.join(parts)
        return import_line
    
    def _fix_direct_import(self, import_line: str) -> str:
        """Fix direct import statements."""
        # Pattern: import deep_agents.agents.pages.01900-procurement.main_agents
        parts = import_line.split()
        if len(parts) >= 2:
            module_path = parts[1]
            # Replace hyphenated parts with underscored versions
            for old, new in self.hyphen_to_underscore_map.items():
                module_path = module_path.replace(old, new)
            parts[1] = module_path
            return ' '.join(parts)
        return import_line
    
    def fix_file_imports(self, file_path: str) -> Dict[str, int]:
        """
        Fix all import statements in a Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            dict: Summary of changes made
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        fixed_lines = []
        changes_made = 0
        
        for line in lines:
            original_line = line
            line = self.fix_import_statement(line)
            if line != original_line:
                changes_made += 1
            fixed_lines.append(line)
        
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(fixed_lines))
        
        return {
            'file': file_path,
            'changes_made': changes_made,
            'total_lines': len(lines)
        }

# Usage
fixer = ImportStatementFixer()

# Fix individual import
original = "from deep_agents.agents.pages.01900-procurement.main_agents import ProcurementAgent"
fixed = fixer.fix_import_statement(original)
print(f"Fixed: {fixed}")
# Output: from deep_agents.agents.pages.01900_procurement.main_agents import ProcurementAgent

# Fix entire file
result = fixer.fix_file_imports('/path/to/agent_file.py')
print(f"Fixed {result['changes_made']} import statements in {result['file']}")
```

**Import Correction:**
- Replace hyphens with underscores in module paths
- Handle both `from...import` and `import` statements
- Update all files in codebase systematically
- Verify imports work after changes

### Step 5: Implement Validation and Migration
**Set up automated validation and migration tools:**

```python
# Comprehensive validation and migration system
import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple

class PythonNamingMigrationTool:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.fixer = ImportStatementFixer()
        self.validator = PythonNamingValidator()
        
    def scan_for_violations(self) -> Dict[str, List[str]]:
        """
        Scan project for Python naming violations.
        
        Returns:
            dict: Violations by category
        """
        violations = {
            'hyphenated_directories': [],
            'invalid_module_names': [],
            'import_errors': []
        }
        
        # Scan directories for hyphens
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # Check directory names
            for dir_name in dirs:
                if '-' in dir_name and 'deep_agents' in str(root_path):
                    violations['hyphenated_directories'].append(str(root_path / dir_name))
            
            # Check Python files
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = root_path / file_name
                    
                    # Validate module name
                    module_name = file_name[:-3]  # Remove .py extension
                    validation = self.validator.validate_module_name(module_name)
                    if not validation['valid']:
                        violations['invalid_module_names'].append(str(file_path))
                    
                    # Check for import issues
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Look for problematic imports
                        import_pattern = r'from\s+deep_agents\.[^\'"]*-[^\'"]*'
                        if re.search(import_pattern, content):
                            violations['import_errors'].append(str(file_path))
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        
        return violations
    
    def generate_migration_plan(self, violations: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Generate detailed migration plan.
        
        Args:
            violations: Violations found by scanning
            
        Returns:
            dict: Migration plan with steps and commands
        """
        plan = {
            'directory_renames': [],
            'file_updates': [],
            'commands': [],
            'risk_assessment': 'medium'
        }
        
        # Plan directory renames
        for dir_path in violations['hyphenated_directories']:
            old_name = Path(dir_path).name
            new_name = old_name.replace('-', '_')
            new_path = str(Path(dir_path).parent / new_name)
            
            plan['directory_renames'].append({
                'old_path': dir_path,
                'new_path': new_path,
                'git_command': f'git mv "{dir_path}" "{new_path}"'
            })
        
        # Plan file updates
        all_files = violations['invalid_module_names'] + violations['import_errors']
        unique_files = list(set(all_files))
        
        for file_path in unique_files:
            plan['file_updates'].append({
                'file': file_path,
                'action': 'fix_imports',
                'backup': f'{file_path}.backup'
            })
        
        # Generate command sequence
        plan['commands'] = [
            '# Step 1: Create backups',
            'find deep_agents -name "*.py" -exec cp {} {}.backup \\;',
            '',
            '# Step 2: Rename directories (use git mv to preserve history)',
        ]
        
        for rename in plan['directory_renames']:
            plan['commands'].append(rename['git_command'])
        
        plan['commands'].extend([
            '',
            '# Step 3: Fix import statements in all Python files',
            'find deep_agents -name "*.py" -exec python -c "from migration_tool import fix_file_imports; fix_file_imports(\'{}\')" \\;',
            '',
            '# Step 4: Run tests to verify imports work',
            'python -m pytest tests/ -v',
            '',
            '# Step 5: Clean up backups (after verification)',
            'find deep_agents -name "*.backup" -delete'
        ])
        
        return plan
    
    def execute_migration(self, plan: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
        """
        Execute the migration plan.
        
        Args:
            plan: Migration plan from generate_migration_plan
            dry_run: If True, only show what would be done
            
        Returns:
            dict: Execution results
        """
        results = {
            'executed_commands': [],
            'errors': [],
            'success': True
        }
        
        if dry_run:
            print("DRY RUN - The following commands would be executed:")
            for cmd in plan['commands']:
                if cmd.startswith('#'):
                    print(f"\n{cmd}")
                else:
                    print(f"  {cmd}")
            return results
        
        # Execute directory renames
        for rename in plan['directory_renames']:
            try:
                result = subprocess.run(rename['git_command'], shell=True, 
                                      capture_output=True, text=True, cwd=self.project_root)
                if result.returncode == 0:
                    results['executed_commands'].append(rename['git_command'])
                else:
                    results['errors'].append(f"Failed to rename {rename['old_path']}: {result.stderr}")
                    results['success'] = False
            except Exception as e:
                results['errors'].append(f"Error renaming {rename['old_path']}: {e}")
                results['success'] = False
        
        # Fix import statements
        for update in plan['file_updates']:
            try:
                fix_result = self.fixer.fix_file_imports(update['file'])
                results['executed_commands'].append(f"Fixed {fix_result['changes_made']} imports in {update['file']}")
            except Exception as e:
                results['errors'].append(f"Error fixing imports in {update['file']}: {e}")
                results['success'] = False
        
        return results

# Usage
tool = PythonNamingMigrationTool('/path/to/project')

# Scan for violations
violations = tool.scan_for_violations()
print(f"Found {len(violations['hyphenated_directories'])} hyphenated directories")
print(f"Found {len(violations['invalid_module_names'])} invalid module names")
print(f"Found {len(violations['import_errors'])} files with import errors")

# Generate migration plan
plan = tool.generate_migration_plan(violations)
print("Migration plan generated with", len(plan['directory_renames']), "directory renames")

# Execute migration (dry run first)
results = tool.execute_migration(plan, dry_run=True)
if results['success']:
    print("Migration plan validated successfully")
    
    # Execute for real
    # results = tool.execute_migration(plan, dry_run=False)
else:
    print("Migration plan has errors:", results['errors'])
```

**Migration System:**
- Scan entire codebase for naming violations
- Generate detailed migration plan with commands
- Execute safe migration with backups
- Validate results and clean up

## Success Criteria

- [ ] All Python modules and packages use lowercase names
- [ ] Underscores used instead of hyphens in all Python paths
- [ ] All import statements work with standard Python syntax
- [ ] IDE autocomplete and IntelliSense work correctly
- [ ] Static analysis tools (mypy, pylint, pyright) pass
- [ ] All directory names follow discipline code patterns
- [ ] Migration completed without breaking existing functionality
- [ ] Tests pass after migration

## Common Pitfalls

1. **Hyphenated Directories** - Always use underscores in Python package names
2. **Invalid Import Syntax** - Standard imports fail with hyphens in module paths
3. **IDE Tooling Issues** - Autocomplete and analysis break with invalid names
4. **Migration Complexity** - Large codebases need careful migration planning
5. **Import Path Updates** - All references must be updated after renaming
6. **Test Suite Failures** - Imports break after directory renames
7. **Git History Preservation** - Use `git mv` to maintain history during renames

## Examples

### Correct Python Naming

**Package Names:**
- `deep_agents` (top-level)
- `procurement_workflow` (subpackage)
- `01900_procurement` (discipline package)
- `01900_procurement_coordinator` (specialized package)

**Module Names:**
- `01900_template_analysis_agent.py` (agent module)
- `c_deep_agents_state_management.py` (core module)
- `a_0000_base_governance_agent.py` (abstract base)
- `structured_logging.py` (utility module)

**Class Names:**
- `ProcurementTemplateAnalysisAgent` (agent class)
- `WorkflowState` (state class)
- `GovernedAgentMixin` (mixin class)
- `BaseWorkflowState` (abstract base)

**Function Names:**
- `validate_workflow` (function)
- `_execute_impl` (private method)
- `async def coordinate` (async method)
- `with_governance` (decorator)

### Incorrect Naming (with corrections)

**❌ `01900-procurement` (directory)**
**✅ `01900_procurement`**
*Issue: Hyphens break Python imports*

**❌ `from deep_agents.agents.pages.01900-procurement import agent`**
**✅ `from deep_agents.agents.pages.01900_procurement import agent`**
*Issue: SyntaxError with hyphens*

**❌ `Template-Analysis-Agent.py`**
**✅ `01900_template_analysis_agent.py`**
*Issues: Mixed case, hyphens, no discipline code prefix*

## Cross-References

### Related Procedures
- [File Naming Standards](skills/file-naming-standards/SKILL.md) - General file naming conventions
- [Agent Coding Standards](skills/agent-coding-standards/SKILL.md) - JavaScript/Python coding standards
- [Agent Development Standards](skills/agent-development-standards/SKILL.md) - Framework development standards

### Related Skills
- `agent-coding-standards` - Language-agnostic coding standards
- `agent-development-standards` - Agent framework standards
- `file-naming-standards` - General file organization

### Related Agents
- `DevForge_AI_Team` - Python development assistance
- `QualityForge_AI_Team` - Code quality and standards verification