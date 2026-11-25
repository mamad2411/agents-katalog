# Chapter 12: Domain-Specific Prompting - Cursor Rules

## Chapter Context

This chapter teaches domain-specific prompting - embedding industry knowledge, terminology, and workflows into prompts. Students learn to create expert personas and build specialized AI systems for specific domains.

## Key Concepts

### 1. Generic vs. Domain-Specific
- Generic: general knowledge, surface-level
- Domain-specific: expert knowledge, deep insights
- Context and terminology matter
- Domain workflows important

### 2. Expert Personas
- Define expert role and experience
- Specialization areas
- Domain knowledge
- Professional tone
- Industry standards

### 3. Domain Documentation
- Technical documentation
- API documentation
- User guides
- Domain-specific formats
- Industry standards

### 4. Domain Code Generation
- Industry patterns
- Best practices
- Domain constraints
- Code standards
- Framework conventions

### 5. Domain Code Review
- Domain-specific checks
- Industry standards
- Security considerations
- Performance requirements
- Compliance requirements

## Important Code Patterns

### Domain Expert Persona
```python
domain_expert = """
You are a senior IoT engineer with 15 years of experience in 
industrial automation. You specialize in:
- Predictive maintenance systems
- Sensor calibration and diagnostics
- Network protocols (MQTT, CoAP, LoRaWAN)
- Safety-critical systems (IEC 61508)

When analyzing issues, consider:
- Safety implications first
- Production uptime impact
- Cost-effectiveness
- Harsh operating environments
"""
```

### Domain-Specific Analysis
```python
prompt = f"""
As {domain_expert}, analyze this IoT issue:

{problem_description}

Provide analysis focusing on:
- Industry-specific KPIs
- Safety and regulatory implications
- Operational efficiency
- Actionable insights for IoT context
"""
```

## Common Mistakes to Avoid

1. **Too generic**: Always add domain context
2. **Wrong persona**: Match expert to task
3. **Missing terminology**: Use domain language
4. **No workflows**: Include domain processes
5. **Ignoring standards**: Follow industry standards

## Integration Points

- **Chapters 9-11**: Applies prompting strategies to domains
- **Chapter 13**: Agents can be domain-specific
- **Chapter 17**: Web apps for domain use cases

## Related Chapters

- **Chapters 9-11**: Prompting strategies (applied to domains)
- **Chapter 13**: Agents (can be domain-specific)
- **Chapter 17**: Web applications (domain interfaces)
