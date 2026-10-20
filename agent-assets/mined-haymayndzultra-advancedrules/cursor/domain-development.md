# Domain Development Guidelines

## 🎯 Technology Domain Selection

### Frontend Development Domains

#### React Ecosystem
- **Use When**: Building interactive web applications, SPAs, component-based UIs
- **Best For**: Complex user interfaces, state management, reusable components
- **Key Technologies**: React, Next.js, TypeScript, Tailwind CSS
- **Apply Rule**: [domains/frontend/react.mdc](mdc:.cursor/rules/domains/frontend/react.mdc)

#### Vue.js Ecosystem
- **Use When**: Building progressive web applications, simple to complex UIs
- **Best For**: Rapid prototyping, gradual adoption, enterprise applications
- **Key Technologies**: Vue 3, Composition API, Vite, Pinia
- **Apply Rule**: [domains/frontend/vue.mdc](mdc:.cursor/rules/domains/frontend/vue.mdc)

#### Modern CSS Frameworks
- **Use When**: Building responsive, modern web applications
- **Best For**: Rapid UI development, consistent design systems
- **Key Technologies**: Tailwind CSS, CSS Grid, Flexbox, CSS Variables
- **Apply Rule**: [domains/frontend/tailwind.mdc](mdc:.cursor/rules/domains/frontend/tailwind.mdc)

#### HTMX & Progressive Enhancement
- **Use When**: Building dynamic web applications without heavy JavaScript
- **Best For**: Server-rendered applications, progressive enhancement
- **Key Technologies**: HTMX, Alpine.js, server-side rendering
- **Apply Rule**: [domains/frontend/htmx.mdc](mdc:.cursor/rules/domains/frontend/htmx.mdc)

### Backend Development Domains

#### Python & FastAPI
- **Use When**: Building modern, fast web APIs, data processing applications
- **Best For**: Rapid API development, machine learning integration, data science
- **Key Technologies**: Python 3.11+, FastAPI, Pydantic, SQLAlchemy
- **Apply Rule**: [domains/backend/fastapi.mdc](mdc:.cursor/rules/domains/backend/fastapi.mdc)

#### Node.js & Express
- **Use When**: Building scalable web applications, real-time features
- **Best For**: Full-stack JavaScript development, microservices, real-time apps
- **Key Technologies**: Node.js 18+, Express.js, TypeScript, Prisma
- **Apply Rule**: [domains/backend/node-express.mdc](mdc:.cursor/rules/domains/backend/node-express.mdc)

#### Go Development
- **Use When**: Building high-performance, concurrent applications
- **Best For**: Microservices, CLI tools, system programming, cloud-native apps
- **Key Technologies**: Go 1.21+, Gin/Echo frameworks, Go modules
- **Apply Rule**: [domains/backend/go.mdc](mdc:.cursor/rules/domains/backend/go.mdc)

#### Java & Spring
- **Use When**: Building enterprise applications, microservices
- **Best For**: Large-scale applications, enterprise integration, long-term maintenance
- **Key Technologies**: Java 17+, Spring Boot 3.x, Maven/Gradle
- **Apply Rule**: [domains/backend/java.mdc](mdc:.cursor/rules/domains/backend/java.mdc)

### Mobile Development Domains

#### React Native
- **Use When**: Building cross-platform mobile applications
- **Best For**: Rapid mobile development, code sharing between platforms
- **Key Technologies**: React Native, Expo, TypeScript, React Navigation
- **Apply Rule**: [domains/mobile/react-native.mdc](mdc:.cursor/rules/domains/mobile/react-native.mdc)

#### Flutter
- **Use When**: Building high-performance cross-platform applications
- **Best For**: Native performance, custom UI components, Google ecosystem
- **Key Technologies**: Flutter 3.x, Dart, Material Design, Cupertino
- **Apply Rule**: [domains/mobile/flutter.mdc](mdc:.cursor/rules/domains/mobile/flutter.mdc)

### Specialized Domains

#### AI & Machine Learning
- **Use When**: Building intelligent applications, data analysis tools
- **Best For**: Predictive analytics, natural language processing, computer vision
- **Key Technologies**: Python, TensorFlow, PyTorch, scikit-learn
- **Apply Rule**: [domains/specialized/ai-ml.mdc](mdc:.cursor/rules/domains/specialized/ai-ml.mdc)

#### Blockchain Development
- **Use When**: Building decentralized applications, smart contracts
- **Best For**: DeFi applications, NFT platforms, blockchain integration
- **Key Technologies**: Solidity, Rust, Web3.js, Hardhat
- **Apply Rule**: [domains/specialized/blockchain.mdc](mdc:.cursor/rules/domains/specialized/blockchain.mdc)

## 🔧 Domain Selection Guidelines

### Project Requirements Analysis
1. **Performance Requirements**: High-performance → Go/Rust, Scalable → Java/Node.js
2. **Team Expertise**: Match technology to team skills and experience
3. **Time Constraints**: Rapid development → Python/FastAPI, React/Next.js
4. **Scalability Needs**: Microservices → Go/Java, Monolith → Python/Node.js
5. **Integration Requirements**: Enterprise → Java/Spring, Modern APIs → FastAPI/Express

### Technology Stack Combinations

#### Full-Stack JavaScript
- **Frontend**: React/Next.js + TypeScript + Tailwind CSS
- **Backend**: Node.js + Express + TypeScript + Prisma
- **Database**: PostgreSQL + Redis
- **Apply Rules**: [domains/frontend/react.mdc](mdc:.cursor/rules/domains/frontend/react.mdc) + [domains/backend/node-express.mdc](mdc:.cursor/rules/domains/backend/node-express.mdc)

#### Python Data Science Stack
- **Backend**: Python + FastAPI + SQLAlchemy
- **ML/AI**: TensorFlow/PyTorch + scikit-learn
- **Frontend**: HTMX + Alpine.js + Tailwind CSS
- **Apply Rules**: [domains/backend/fastapi.mdc](mdc:.cursor/rules/domains/backend/fastapi.mdc) + [domains/specialized/ai-ml.mdc](mdc:.cursor/rules/domains/specialized/ai-ml.mdc)

#### Enterprise Java Stack
- **Backend**: Java + Spring Boot + JPA
- **Frontend**: Vue.js + TypeScript + Tailwind CSS
- **Database**: PostgreSQL + Redis
- **Apply Rules**: [domains/backend/java.mdc](mdc:.cursor/rules/domains/backend/java.mdc) + [domains/frontend/vue.mdc](mdc:.cursor/rules/domains/frontend/vue.mdc)

## 📚 Domain Rule Application

### Automatic Application
Domain rules are automatically applied based on:
- File extensions (`.ts`, `.py`, `.go`, `.java`)
- Project configuration in [package.json](mdc:package.json)
- Directory structure in [FOLDER_STRUCTURE.md](mdc:FOLDER_STRUCTURE.md)

### Manual Application
Apply specific domain rules when:
- Starting new projects in specific technologies
- Migrating between technology stacks
- Implementing domain-specific features
- Following technology best practices

### Rule Priority
1. **Specific Domain Rules**: Technology-specific guidelines
2. **Universal Standards**: [domains/frontend/coding-standards.mdc](mdc:.cursor/rules/domains/frontend/coding-standards.mdc)
3. **Project Standards**: [code-quality-standards.mdc](mdc:.cursor/rules/code-quality-standards.mdc)

## 🚀 Implementation Workflow

### 1. Technology Selection
- Analyze project requirements
- Consider team expertise
- Evaluate performance needs
- Review integration requirements

### 2. Domain Rule Application
- Apply relevant domain rules
- Configure development environment
- Set up project structure
- Initialize technology stack

### 3. Development Execution
- Follow domain-specific patterns
- Apply technology best practices
- Use appropriate testing frameworks
- Implement security measures

### 4. Quality Assurance
- Run domain-specific tests
- Apply security scanning
- Validate performance metrics
- Review code quality

## 📊 Technology Decision Matrix

| Requirement | Frontend | Backend | Mobile | Specialized |
|-------------|----------|---------|---------|-------------|
| Rapid Prototyping | React + Tailwind | FastAPI | React Native | Python + ML |
| High Performance | Vue + Vite | Go | Flutter | Rust + ML |
| Enterprise Scale | React + TypeScript | Java + Spring | Native Android | Java + ML |
| Real-time Features | HTMX + Alpine | Node.js + Socket.io | React Native | Python + WebSockets |
| Data Science | HTMX + Charts | Python + FastAPI | React Native | Python + Jupyter |

## 🔍 Reference Materials

### Documentation
- [README.md](mdc:README.md) - Framework overview
- [FOLDER_STRUCTURE.md](mdc:FOLDER_STRUCTURE.md) - Project structure
- [FRAMEWORK_SUMMARY.md](mdc:FRAMEWORK_SUMMARY.md) - Framework capabilities

### Domain Rules Directory
- `.cursor/rules/domains/` - All domain-specific rules
- `.cursor/rules/domains/frontend/` - Frontend technology rules
- `.cursor/rules/domains/backend/` - Backend technology rules
- `.cursor/rules/domains/mobile/` - Mobile development rules
- `.cursor/rules/domains/specialized/` - Specialized technology rules

### Tools & Scripts
- `tools/run_role.py` - Execute AI personas with domain context
- `tools/quickstart.py` - Run complete development pipeline
- Domain-specific tooling in each technology directory
