---
name: c4-architecture-diagrams
description: Create comprehensive C4 model diagrams for software architecture documentation using Context, Container, Component, and Code levels to visualize system structure and relationships
---

# C4 Architecture Diagrams

Create clear, hierarchical software architecture diagrams using the C4 model (Context, Container, Component, Code). Focus on different levels of abstraction to communicate system design to various stakeholders.

## Examples

### Level 1: Context Diagram
```mermaid
graph TB
    subgraph "System Context"
        User[👤 Token Holders<br/>Transfer tokens, check balances]
        Issuer[🏛️ Token Issuer<br/>Mint new tokens]
        Auditor[👨‍💼 Auditor<br/>Monitor compliance]
        Reserve[🏦 Reserve Custodian<br/>Hold backing assets]
    end
    
    System[📊 Reserve Token System<br/>Manages reserve-backed tokens]
    
    Blockchain[⛓️ Ethereum Blockchain<br/>Decentralized ledger]
    Explorer[🔍 Block Explorer<br/>Transaction visibility]
    
    User --> System
    Issuer --> System
    Auditor --> System
    Reserve --> System
    System --> Blockchain
    Auditor --> Explorer
    User --> Explorer
```

### Level 2: Container Diagram
```mermaid
graph TB
    subgraph "Reserve Token System"
        Smart[📜 Smart Contract<br/>Solidity | EVM<br/>Token logic + reserve checks]
        Events[📢 Event System<br/>Blockchain logs<br/>Compliance monitoring]
    end
    
    subgraph "External Systems"
        Reserve[🏦 Reserve Wallet<br/>EOA/Multisig<br/>Holds backing assets]
        Oracle[🔮 Price Oracle<br/>Chainlink (future)<br/>Real-time pricing]
    end
    
    User[👤 Users] --> Smart
    Smart --> Reserve
    Smart --> Events
    Smart -.-> Oracle
    Auditor[👨‍💼 Auditor] --> Events
```

### Level 3: Component Diagram
```mermaid
graph TB
    subgraph "RwaToken Contract"
        ERC20[📋 ERC20 Interface<br/>Standard token functions]
        Access[🔐 Access Control<br/>onlyIssuer modifier]
        Reserve[🏦 Reserve Checker<br/>Backing validation]
        Events[📢 Event Emitter<br/>Compliance logging]
        
        ERC20 --> Reserve
        ERC20 --> Access
        Reserve --> Events
    end
    
    subgraph "State Management"
        Balances[(💰 Balances<br/>mapping)]
        Supply[(📊 Total Supply<br/>uint256)]
        Allowances[(✅ Allowances<br/>nested mapping)]
    end
    
    ERC20 --> Balances
    ERC20 --> Supply
    ERC20 --> Allowances
```

### Level 4: Code Diagram
```mermaid
graph TB
    subgraph "transfer() Function Flow"
        Start([transfer called])
        CheckReserve{Reserve >= Supply?}
        CheckBalance{Balance >= Amount?}
        UpdateState[Update balances]
        EmitEvent[Emit Transfer event]
        EmitReserve[Emit ReserveChecked]
        Success([Return true])
        Fail([Revert])
        
        Start --> CheckReserve
        CheckReserve -->|No| Fail
        CheckReserve -->|Yes| CheckBalance
        CheckBalance -->|No| Fail
        CheckBalance -->|Yes| UpdateState
        UpdateState --> EmitEvent
        UpdateState --> EmitReserve
        EmitEvent --> Success
    end
```

## Guidelines

### C4 Model Levels
1. **Context (Level 1)**: System boundary and external actors
2. **Container (Level 2)**: High-level technology choices
3. **Component (Level 3)**: Internal structure of containers
4. **Code (Level 4)**: Class/function level detail

### Diagram Design Principles
- Use consistent shapes and colors for entity types
- Include technology choices (Solidity, EVM, etc.)
- Show data flow direction with arrows
- Add brief descriptions for each element
- Focus on one abstraction level per diagram

### Stakeholder Targeting
- **Context**: Business stakeholders, product managers
- **Container**: Architects, senior developers
- **Component**: Development team, technical leads
- **Code**: Developers working on specific modules

### Mermaid Best Practices
- Use subgraphs to group related components
- Include emojis for visual clarity
- Add technology stack annotations
- Show both synchronous and asynchronous relationships
- Use different arrow styles for different interaction types

### Documentation Structure
```
docs/architecture/
├── c4-context.md        # Level 1 diagrams
├── c4-container.md      # Level 2 diagrams  
├── c4-component.md      # Level 3 diagrams
└── c4-code.md          # Level 4 diagrams
```

### Common Patterns for Blockchain
- Smart contracts as containers
- External accounts as actors
- Blockchain as external system
- Events as communication mechanism
- Gas costs as non-functional constraints