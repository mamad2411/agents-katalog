# Claude Code Sub-Agents - Gestion Emballages v2

This directory contains 22 specialized Claude Code sub-agents configured for the Blue Whale Portal (Gestion Emballages v2) project. Each agent is properly formatted for Claude Code recognition and automatic delegation.

## 🚀 Usage

The agents should now be automatically recognized by Claude Code. You can:

1. **Check agent availability**:
   ```bash
   /agents
   ```

2. **Request specific agent**:
   ```
   Use the backend-specialist subagent to implement the order analytics API
   ```

3. **Let Claude choose automatically** - Claude will automatically delegate to appropriate agents based on task requirements.

## 📋 Available Agents (22)

### 🎯 **Coordination & Context**
- **multi-agent-coordinator** - Orchestrates complex multi-step tasks
- **context-manager** - Project knowledge and business requirements

### 🏗️ **Core Development** 
- **architecture-analyst** - System design and technical decisions
- **backend-specialist** - NestJS, TypeORM, business logic
- **frontend-developer** - Angular 18, responsive UI
- **database-expert** - PostgreSQL optimization and schema design
- **testing-engineer** - Comprehensive testing strategies

### 🔧 **Infrastructure & Operations**
- **devops-engineer** - Docker, CI/CD, deployment automation  
- **security-auditor** - Security assessment, GDPR compliance
- **api-designer** - RESTful API design and documentation
- **performance-optimizer** - Performance across all layers
- **monitoring-specialist** - System observability and alerting

### 🎨 **Quality & User Experience**
- **ui-ux-designer** - User experience and design system
- **documentation-writer** - Technical documentation and guides
- **code-reviewer** - Code quality and standards compliance
- **business-logic-analyst** - Domain modeling and business rules

### 🛠️ **Specialized Services**
- **migration-specialist** - Data migrations and system upgrades
- **dependency-manager** - Package management and security updates
- **refactoring-specialist** - Code improvement and technical debt
- **error-handling-specialist** - System resilience and error recovery
- **i18n-specialist** - Internationalization (French/English)
- **compliance-auditor** - Regulatory compliance and audit prep

## 🔧 **Agent Configuration**

Each agent is configured with:
- **YAML front matter** with name, description, and tools
- **Project-specific context** for Gestion Emballages v2
- **Appropriate tool access** based on specialization
- **Clear responsibilities** and success criteria

## 🎯 **Common Usage Patterns**

### **Complex Feature Development**
1. **multi-agent-coordinator** → Task breakdown and orchestration
2. **context-manager** → Business requirement validation  
3. **architecture-analyst** → Technical design decisions
4. Parallel execution with **backend-specialist**, **frontend-developer**, **database-expert**
5. **testing-engineer** → Quality assurance
6. **documentation-writer** → Documentation updates

### **Performance Issues**
1. **performance-optimizer** → Bottleneck identification
2. **database-expert** → Query optimization
3. **backend-specialist** → API improvements
4. **frontend-developer** → UI performance
5. **monitoring-specialist** → Performance tracking

### **Security Reviews**
1. **security-auditor** → Vulnerability assessment
2. **compliance-auditor** → Regulatory compliance
3. **code-reviewer** → Security code review
4. **architecture-analyst** → Security architecture

## ⚡ **Quick Test**

To verify the agents are working:

```bash
# Check if agents are recognized
/agents

# Test a simple delegation
Use the context-manager subagent to explain the Blue Whale Portal business model
```

## 📚 **Project Context**

All agents are pre-configured with knowledge of:
- **System**: Blue Whale Portal - B2B Supply Chain Management
- **Architecture**: NestJS + Angular 18 + PostgreSQL + MinIO + Docker
- **Business Domain**: Agricultural packaging procurement
- **User Roles**: ADMIN, MANAGER, HANDLER, STATION, SUPPLIER
- **Key Features**: Multi-supplier cart, order management, contract system

## 🎉 **Ready to Use!**

Your agents are now properly configured and should be automatically recognized by Claude Code. Try the `/agents` command to verify they're working correctly.

---
*These agents provide comprehensive coverage for enterprise-grade B2B platform development with specialized expertise for every aspect of the Gestion Emballages v2 project.*