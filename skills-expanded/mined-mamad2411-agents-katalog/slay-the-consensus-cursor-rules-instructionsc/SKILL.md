---
description: 
globs: 
alwaysApply: true
---
# Crypto Spire MVP Development Guide

## Project Overview

You will help develop "Crypto Spire," a roguelike deck-building game inspired by Slay the Spire that integrates blockchain technology. Players sign messages with crypto wallets to select themed decks, battle through procedurally generated runs, and mint fusion NFT cards upon successful completion.

This prompt will guide you through sequential development of the MVP. Complete each step before proceeding to the next. Request clarification if needed before moving forward.

## Development Stages Overview

1. **Frontend Project Setup**
2. **Game Core Implementation**
3. **Blockchain Integration**
4. **Backend Development**
5. **Integration & Testing**

## Detailed Development Steps

### Stage 1: Frontend Project Setup

#### Step 1.1: Create React Project
- Set up a new React project using Create React App or Vite
- Install necessary dependencies:
  - `ethers` for blockchain interaction
  - `phaser` for game rendering
  - `@privy-io/react-auth` or `@dynamic-labs/sdk-react` for wallet connection
- Set up basic folder structure
- Initialize Git repository

#### Step 1.2: Create Basic UI Components
- Create the main application layout
- Implement a wallet connection component
- Design the network selection UI
- Create placeholder screens for:
  - Home/Welcome
  - Deck Selection
  - Game Map
  - Battle View
  - Rest Site
  - Fusion Card Creation

#### Step 1.3: Set Up Asset Pipeline
- Create placeholder card art
- Define a unified style guide
- Set up asset loading system

### Stage 2: Game Core Implementation

#### Step 2.1: Implement Card System
- Define the card data structure
- Create card rendering components
- Implement card effects system
- Create the base starter decks for each network theme

#### Step 2.2: Build Core Game State Management
- Implement game state reducer
- Create game initialization logic
- Design save/load functionality for in-progress runs

#### Step 2.3: Create Map Generation
- Implement procedural map generation
- Create path selection mechanics
- Design node types (battle, rest, etc.)

#### Step 2.4: Implement Battle System
- Create turn-based combat system
- Implement card playing mechanics
- Build enemy AI
- Design health and energy systems
- Create battle resolution logic

#### Step 2.5: Build Rest Sites
- Implement healing mechanics
- Design rest site UI

#### Step 2.6: Create Boss Battles
- Design boss enemy types
- Implement special boss mechanics
- Create victory/defeat conditions

### Stage 3: Blockchain Integration

#### Step 3.1: Implement Wallet Connection
- Add wallet connection using AppKit
- Create account linking system
- Implement multi-chain authentication
- Set up session management
- Test connection across multiple networks

#### Step 3.2: Develop Signature Verification
- Implement message signing for network selection
- Create signature verification utilities
- Design secure message format

#### Step 3.3: Create Smart Contract
- Develop FusionCardNFT contract
- Write deployment scripts
- Test contract functionality
- Deploy to test network

#### Step 3.4: Implement NFT Minting
- Create card fusion selection UI
- Implement NFT metadata generation
- Build minting transaction handling
- Design success/failure states

### Stage 4: Backend Development

#### Step 4.1: Set Up API Structure
- Create Express/Node.js server
- Implement API routes structure
- Set up database connections
- Create authentication middleware

#### Step 4.2: Implement Game Service
- Build game state management
- Create run persistence
- Implement game logic validation

#### Step 4.3: Develop User Management
- Create user profiles
- Implement card collection storage
- Design run history tracking

#### Step 4.4: Build Signature Verification Service
- Implement multi-network signature verification
- Create signature storage and validation
- Build network-to-deck mapping

#### Step 4.5: Create Blockchain Service
- Implement NFT minting service
- Create blockchain transaction monitoring
- Build event listening for NFT updates

### Stage 5: Integration & Testing

#### Step 5.1: Connect Frontend and Backend
- Implement API service in frontend
- Create authentication flow
- Test data synchronization

#### Step 5.2: Integrate Game Flow
- Connect all game screens
- Implement proper state transitions
- Test complete game loop

#### Step 5.3: Polish User Experience
- Add animations and transitions
- Improve visual feedback
- Implement sound effects
- Create helpful tooltips and guides

#### Step 5.4: Test End-to-End
- Test complete user journey
- Verify blockchain interactions
- Validate game mechanics
- Check for edge cases

## Development Guidelines

### Code Organization
- Use domain-driven folder structure
- Implement clean architecture principles
- Separate game logic from UI and blockchain code
- Use TypeScript for type safety

### Frontend Patterns
- Use React hooks for state management
- Consider Redux for global state
- Implement component composition
- Use CSS modules or styled-components for styling

### Blockchain Integration

- Should use AppKit 
- Abstract blockchain interactions behind service interfaces
- Handle network errors gracefully
- Implement transaction confirmation UI
- Cache blockchain data when appropriate
- Minimize on-chain transactions

### Backend Considerations
- Implement proper authentication
- Create comprehensive API documentation
- Use environment variables for configuration
- Implement logging and monitoring
- Design for horizontal scaling

## Development Sequence

For each component or feature:

1. First, create a basic implementation focused on functionality
2. Write tests to verify correct behavior
3. Refactor for code quality and performance
4. Document the implementation
5. Move to the next component only after current one is verified working

## Output Format

For each development step:
1. Explain your approach
2. Show the relevant code files
3. Explain how to test functionality
4. Note any potential issues or future improvements

## Getting Started

Begin with Stage 1: Frontend Project Setup. For the first deliverable, create:

1. The project structure
2. Basic component hierarchy
3. Initial wallet connection component

Show your work as you complete each step, explaining design decisions as you go.