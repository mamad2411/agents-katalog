# Cursor Rules for Web3 Wallet App

## NO PLACEHOLDERS POLICY
- **NEVER** use placeholder values like "0.5", "100.0", "mock data", "demo purposes", etc.
- **NEVER** use placeholder text like "Lorem ipsum", "Sample text", "TODO", etc.
- **ALWAYS** implement real functionality that works with actual blockchain data
- **ALWAYS** use real API calls, real contract interactions, real balance fetching

## CODE QUALITY STANDARDS
- All functions must be fully implemented with real logic
- All data must come from actual sources (blockchain, APIs, user input)
- All error handling must be comprehensive and user-friendly
- All loading states must reflect actual operations

## WEB3 SPECIFIC RULES
- Balance fetching must use real blockchain RPC calls
- Transaction functions must use proper gas estimation
- Contract interactions must use correct ABI and contract addresses
- Network switching must work with actual network configurations
- Wallet creation must use real Privy wallet creation

## UI/UX STANDARDS
- All text must be meaningful and contextual
- All buttons must perform real actions
- All forms must have proper validation
- All error messages must be helpful and actionable
- All loading states must indicate real progress

## FORBIDDEN PATTERNS
- Mock data or demo values
- Placeholder text or content
- TODO comments without implementation
- Hardcoded fake values
- Non-functional buttons or links
- Placeholder images or icons without real alternatives

## REQUIRED IMPLEMENTATIONS
- Real balance fetching from blockchain
- Real transaction sending with proper validation
- Real error handling with user feedback
- Real loading states for all async operations
- Real network switching functionality
- Real wallet creation and management

## REVIEW CHECKLIST
Before any code is considered complete:
- [ ] No placeholder values anywhere
- [ ] All functions are fully implemented
- [ ] All data comes from real sources
- [ ] All error cases are handled
- [ ] All loading states work properly
- [ ] All user interactions are functional
- [ ] All blockchain interactions are real
