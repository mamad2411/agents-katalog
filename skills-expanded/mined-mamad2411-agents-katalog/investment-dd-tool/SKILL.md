# Investment Due Diligence Tool - AWS Lambda + Claude Architecture

# Project Context
You are working on an Investment Due Diligence Tool with AWS Lambda + Claude API.
- Backend: AWS Lambda functions with Claude API for market research agents
- Frontend: React with Material-UI and Redux for state management  
- Database: DynamoDB for data persistence
- Orchestration: AWS Step Functions to coordinate Lambda agents
- Deployment: Full AWS serverless stack

# Architecture Principles
- Each agent is a separate Lambda function that returns scored results (0-10)
- Free data sources only (Reddit API, Census Bureau, Google Patents, etc.)
- Real-time progress updates via WebSocket API Gateway
- Comprehensive PMF (Product-Market Fit) scoring system

# Lambda Function Patterns
Each agent Lambda should:
1. Accept business idea input via event parameter
2. Research using free external APIs
3. Use Claude API for analysis and scoring
4. Return structured JSON with score, breakdown, confidence, reasoning
5. Include comprehensive error handling
6. Log progress for monitoring

# When generating Lambda functions:
1. Always include proper error handling and try/catch blocks
2. Add comprehensive CloudWatch logging
3. Include input validation for event parameters
4. Use AWS SDK v3 with proper client initialization
5. Implement timeout handling
6. Follow established Lambda function structure
7. Include relevant unit tests
8. Consider cold start optimization

# When generating React components:
1. Use Material-UI components consistently
2. Integrate with AWS API Gateway via axios
3. Handle loading states for asynchronous Lambda calls
4. Display real-time progress from WebSocket updates
5. Show detailed scoring breakdowns
6. Implement error boundaries for AWS service failures
