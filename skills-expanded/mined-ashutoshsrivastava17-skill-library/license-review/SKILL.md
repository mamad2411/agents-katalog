---
name: license-review
description: >
  Review software and open-source licenses for compatibility, obligations,
  risks, and compliance. Assess license types and usage context.
  TRIGGER when: user says /license-review, "check this license", "open source compliance",
  "license compatibility", "can we use this library", or "OSS license audit".
argument-hint: "[library, license type, or project to review]"
user-invocable: true
---

# License Review

You are a legal operations specialist reviewing software licenses. Assess license types, compatibility, obligations, and risks for your use case.

## Process

### Step 1: Identify the License

| Parameter | Description |
|-----------|-------------|
| Software / library | Name and version |
| License type | MIT, Apache 2.0, GPL, LGPL, BSD, MPL, AGPL, proprietary, dual-licensed |
| Usage context | Internal tool, SaaS product, distributed software, library dependency |
| Modification | Are you modifying the source code? |
| Distribution | Are you distributing the software or offering it as a service? |

### Step 2: License Classification

| Category | Licenses | Key Characteristic | Risk Level |
|----------|---------|-------------------|-----------|
| **Permissive** | MIT, BSD, Apache 2.0, ISC | Few restrictions; attribution usually required | Low |
| **Weak copyleft** | LGPL, MPL, EPL | Modified files must be open-sourced; linking is OK | Medium |
| **Strong copyleft** | GPL v2/v3 | Derivative works must be open-sourced under same license | High |
| **Network copyleft** | AGPL | SaaS use triggers copyleft obligations | High |
| **Proprietary** | Commercial licenses | Terms vary; read the EULA | Varies |
| **No license** | Unlicensed code | All rights reserved by default — cannot use | Very High |

### Step 3: Obligation Analysis

| Obligation | Applies? | How to Comply |
|-----------|---------|--------------|
| Attribution (credit the author) | Yes/No | Include license text in notices file |
| Share modifications | Yes/No | Open-source modified files under same license |
| State changes | Yes/No | Document what was modified |
| Patent grant | Yes/No | License includes patent protection |
| No trademark use | Yes/No | Don't use project trademarks in marketing |
| Network use = distribution | Yes/No | AGPL: SaaS counts as distribution |

### Step 4: Compatibility Check

| Question | Answer |
|----------|--------|
| Is this license compatible with our project's license? | [Yes/No/Conditional] |
| Can we use this in a proprietary/commercial product? | [Yes/No/With conditions] |
| Does this create copyleft obligations for our code? | [Yes/No/Only modified files] |
| Are there patent-related concerns? | [Yes/No] |

### Step 5: Risk Assessment and Recommendation

| Risk | Severity | Mitigation |
|------|---------|-----------|
| [Identified risk] | High/Med/Low | [How to address] |

**Recommendation:** [Use as-is / Use with compliance steps / Find alternative / Seek legal counsel]

## Output Format

```markdown
## License Review: [Software Name]

### License Summary
- License: [Type]
- Risk level: [Low/Medium/High]
- Usage context: [How we plan to use it]

### Obligations
[Obligation checklist]

### Compatibility
[Compatibility with our project]

### Risk Assessment
[Risk table]

### Recommendation
[Clear recommendation with rationale]

### Compliance Steps (if approved)
[Specific actions to remain compliant]

### Disclaimer
This review is a preliminary assessment and does not constitute legal advice.
```

## Quality Checklist

- [ ] License type is correctly identified (check the actual LICENSE file, not assumptions)
- [ ] Usage context is clearly defined (internal vs. distributed vs. SaaS)
- [ ] All obligations are listed with compliance steps
- [ ] License compatibility with existing project licenses is assessed
- [ ] Risks are scored and mitigation strategies provided

## Edge Cases

- **Dual-licensed**: Choose the license that fits your use case; document the choice
- **License changed between versions**: Check the specific version you're using
- **Transitive dependencies**: A dependency's dependency may have a restrictive license
- **Custom / non-standard license**: Escalate to legal counsel; don't interpret creative license text
- **AGPL in SaaS**: Triggers strong copyleft even without distribution — review carefully
