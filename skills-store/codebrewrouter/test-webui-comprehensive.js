#!/usr/bin/env node
/**
 * Comprehensive Open WebUI test for CodebrewRouter
 * 
 * Tests:
 * 1. General knowledge (dad joke) - should be fast, not routing to code-heavy model
 * 2. Code request (HttpClient in C#) - should complete successfully
 * 3. Response validation - checks for content quality
 * 4. Timeout detection - ensures no hangs
 * 5. Multiple iterations - catches flakiness
 * 6. Multi-turn conversation - validates state management
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const WEBUI_URL = process.env.WEBUI_URL || 'http://127.0.0.1:58370/';
const TIMEOUT_MS = 60000; // 60 second timeout for responses
const RESPONSE_TIMEOUT_MS = 30000; // Should complete within 30s to avoid hang
const MIN_RESPONSE_LENGTH = 50;

// Test configuration
const TEST_CASES = [
  {
    name: 'Dad Joke (General Knowledge)',
    prompt: 'tell me a dad joke',
    expectedKeywords: ['dad', 'joke', 'joke'],
    unexpectedKeywords: ['error', 'null', 'undefined', 'error:', 'fail'],
    minLength: 30,
    category: 'general'
  },
  {
    name: 'HttpClient in C# (Code Request)',
    prompt: 'can you create a httpclient in c# that will connect to www.yahoo.com',
    expectedKeywords: ['HttpClient', 'using', 'var', 'new', 'www.yahoo.com', 'C#'],
    unexpectedKeywords: ['error', 'fail', 'cannot', 'not supported'],
    minLength: 150,
    category: 'code'
  }
];

const ITERATIONS = 3; // Run each test 3 times to catch flakiness

class WebUITester {
  constructor() {
    this.browser = null;
    this.page = null;
    this.results = [];
    this.logs = [];
    this.startTime = Date.now();
  }

  log(level, message, data = null) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      message,
      data: data || {}
    };
    this.logs.push(logEntry);
    const prefix = `[${timestamp}] [${level}]`;
    if (data) {
      console.log(`${prefix} ${message}`, data);
    } else {
      console.log(`${prefix} ${message}`);
    }
  }

  async initialize() {
    this.log('INFO', 'Launching browser...');
    this.browser = await chromium.launch();
    this.page = await this.browser.newPage();
    
    // Setup event listeners for network/error detection
    this.page.on('framenavigated', (frame) => {
      this.log('DEBUG', 'Frame navigated', { url: frame.url() });
    });

    this.page.on('response', (response) => {
      if (response.status() >= 400) {
        this.log('WARN', `HTTP error response: ${response.status()}`, { url: response.url() });
      }
    });

    this.log('INFO', 'Browser ready');
  }

  async navigateToWebUI() {
    this.log('INFO', 'Navigating to Open WebUI', { url: WEBUI_URL });
    try {
      await this.page.goto(WEBUI_URL, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await this.page.waitForTimeout(2000); // Wait for UI to stabilize
      this.log('INFO', 'Successfully navigated to Open WebUI');
      return true;
    } catch (error) {
      this.log('ERROR', 'Failed to navigate to Open WebUI', { error: error.message });
      return false;
    }
  }

  async waitForChatReady() {
    this.log('DEBUG', 'Waiting for chat interface to be ready...');
    try {
      // Wait for the input field or send button to appear
      await this.page.waitForSelector('textarea, input[type="text"], button[aria-label*="Send"]', {
        timeout: 10000
      });
      this.log('DEBUG', 'Chat interface is ready');
      return true;
    } catch (error) {
      this.log('WARN', 'Chat interface may not be fully ready', { error: error.message });
      return false;
    }
  }

  async sendPrompt(prompt) {
    this.log('INFO', 'Sending prompt to chat', { prompt });
    const startTime = Date.now();

    try {
      // Find the textarea or input field
      const inputSelector = 'textarea, input[type="text"]';
      await this.page.fill(inputSelector, prompt);
      this.log('DEBUG', 'Prompt filled in input field');

      // Find and click the send button
      // Try multiple selectors for the send button
      const sendButtonSelectors = [
        'button[aria-label*="Send"]',
        'button:has-text("Send")',
        'button[data-testid="send"]',
        'button.send',
        'form button:last-child'
      ];

      let clicked = false;
      for (const selector of sendButtonSelectors) {
        try {
          const button = await this.page.$(selector);
          if (button) {
            await button.click();
            clicked = true;
            this.log('DEBUG', 'Send button clicked', { selector });
            break;
          }
        } catch (e) {
          // Continue to next selector
        }
      }

      if (!clicked) {
        this.log('WARN', 'Could not find send button, trying Enter key');
        await this.page.press(inputSelector, 'Enter');
      }

      this.log('DEBUG', 'Prompt submitted, waiting for response...');

      // Wait for response - look for new messages appearing
      // The response typically appears in a message container
      const responseSelector = '[role="article"], [class*="message"], [class*="response"], [class*="chat-message"]';
      
      let responseReceived = false;
      let responseText = '';
      let attempts = 0;
      const maxAttempts = 30; // Check for 30 seconds (1s per check)

      while (!responseReceived && attempts < maxAttempts) {
        try {
          const messages = await this.page.$$(responseSelector);
          if (messages.length > 0) {
            const lastMessage = messages[messages.length - 1];
            const text = await lastMessage.textContent();
            if (text && text.trim().length > MIN_RESPONSE_LENGTH) {
              responseText = text.trim();
              responseReceived = true;
              this.log('DEBUG', 'Response detected', { length: responseText.length });
              break;
            }
          }
        } catch (e) {
          this.log('DEBUG', 'Still waiting for response...', { attempt: attempts + 1 });
        }

        await this.page.waitForTimeout(1000);
        attempts++;
      }

      const elapsedMs = Date.now() - startTime;

      if (!responseReceived) {
        this.log('ERROR', 'Timeout waiting for response', { elapsedMs, maxWaitMs: maxAttempts * 1000 });
        return {
          success: false,
          responseText: '',
          elapsedMs,
          error: 'Timeout: Response did not arrive within timeout window'
        };
      }

      if (elapsedMs > RESPONSE_TIMEOUT_MS) {
        this.log('WARN', 'Response arrived but took longer than ideal', { elapsedMs, idealMs: RESPONSE_TIMEOUT_MS });
      }

      this.log('INFO', 'Response received successfully', { elapsedMs });
      return {
        success: true,
        responseText,
        elapsedMs,
        error: null
      };
    } catch (error) {
      const elapsedMs = Date.now() - startTime;
      this.log('ERROR', 'Error sending prompt or waiting for response', { error: error.message, elapsedMs });
      return {
        success: false,
        responseText: '',
        elapsedMs,
        error: error.message
      };
    }
  }

  validateResponse(response, testCase) {
    const validationResult = {
      lengthValid: false,
      hasExpectedKeywords: false,
      noUnexpectedKeywords: true,
      qualityScore: 0,
      issues: []
    };

    const text = response.responseText.toLowerCase();

    // Check length
    if (text.length >= testCase.minLength) {
      validationResult.lengthValid = true;
    } else {
      validationResult.issues.push(`Response too short (${text.length} < ${testCase.minLength})`);
    }

    // Check for expected keywords
    const foundKeywords = testCase.expectedKeywords.filter(kw => 
      text.includes(kw.toLowerCase())
    );
    if (foundKeywords.length > 0) {
      validationResult.hasExpectedKeywords = true;
    } else {
      validationResult.issues.push(`No expected keywords found. Looked for: ${testCase.expectedKeywords.join(', ')}`);
    }

    // Check for unexpected keywords
    const unexpectedFound = testCase.unexpectedKeywords.filter(kw => 
      text.includes(kw.toLowerCase())
    );
    if (unexpectedFound.length > 0) {
      validationResult.noUnexpectedKeywords = false;
      validationResult.issues.push(`Found unexpected keywords: ${unexpectedFound.join(', ')}`);
    }

    // Calculate quality score (0-100)
    let score = 0;
    if (validationResult.lengthValid) score += 25;
    if (validationResult.hasExpectedKeywords) score += 50;
    if (validationResult.noUnexpectedKeywords) score += 25;
    validationResult.qualityScore = score;

    return validationResult;
  }

  async runTestCase(testCase, iteration) {
    this.log('INFO', `\n========== Test: ${testCase.name} (Iteration ${iteration}/${ITERATIONS}) ==========`);
    
    const response = await this.sendPrompt(testCase.prompt);
    const validation = this.validateResponse(response, testCase);

    const result = {
      testCase: testCase.name,
      iteration,
      ...response,
      validation
    };

    this.results.push(result);

    // Log detailed results
    this.log('INFO', `Response time: ${response.elapsedMs}ms`);
    this.log('INFO', `Response quality score: ${validation.qualityScore}/100`);
    
    if (!response.success) {
      this.log('ERROR', `FAILED: ${response.error}`);
    } else if (validation.qualityScore < 100) {
      this.log('WARN', `Partial success (quality: ${validation.qualityScore}/100)`, {
        issues: validation.issues
      });
    } else {
      this.log('INFO', 'PASSED: Response valid and complete');
    }

    return response.success && validation.qualityScore === 100;
  }

  async runMultiTurnTest() {
    this.log('INFO', '\n========== Multi-Turn Conversation Test ==========');
    this.log('INFO', 'Sending first joke request...');

    const response1 = await this.sendPrompt('tell me a funny joke');
    if (!response1.success) {
      this.log('ERROR', 'Failed to get first joke');
      return false;
    }

    const joke1 = response1.responseText;
    this.log('INFO', 'First joke received, sending second joke request...');

    // Clear input and send second request
    const inputSelector = 'textarea, input[type="text"]';
    await this.page.fill(inputSelector, '');

    const response2 = await this.sendPrompt('tell me a different funny joke');
    if (!response2.success) {
      this.log('ERROR', 'Failed to get second joke');
      return false;
    }

    const joke2 = response2.responseText;

    // Validate that jokes are different
    if (joke1 === joke2) {
      this.log('WARN', 'Multi-turn test: Jokes appear to be identical (possible caching or model issue)');
      return false;
    }

    this.log('INFO', 'PASSED: Multi-turn conversation working, jokes are different');
    return true;
  }

  async runAllTests() {
    try {
      await this.initialize();
      
      if (!await this.navigateToWebUI()) {
        this.log('ERROR', 'Cannot proceed - failed to load Open WebUI');
        return false;
      }

      if (!await this.waitForChatReady()) {
        this.log('WARN', 'Chat interface may not be fully ready, attempting to proceed');
      }

      let totalPassed = 0;
      let totalTests = 0;

      // Run each test case multiple times
      for (const testCase of TEST_CASES) {
        for (let i = 1; i <= ITERATIONS; i++) {
          totalTests++;
          const passed = await this.runTestCase(testCase, i);
          if (passed) totalPassed++;

          // Wait between iterations to avoid overwhelming the system
          if (i < ITERATIONS) {
            await this.page.waitForTimeout(2000);
          }
        }
      }

      // Run multi-turn test
      totalTests++;
      const multiTurnPassed = await this.runMultiTurnTest();
      if (multiTurnPassed) totalPassed++;

      // Summary
      this.log('INFO', '\n========== TEST SUMMARY ==========');
      this.log('INFO', `Passed: ${totalPassed}/${totalTests}`);
      this.log('INFO', `Pass rate: ${(totalPassed / totalTests * 100).toFixed(1)}%`);

      // Save detailed results
      this.saveResults();

      return totalPassed === totalTests;
    } catch (error) {
      this.log('ERROR', 'Unexpected error during test run', { error: error.message, stack: error.stack });
      return false;
    } finally {
      if (this.browser) {
        await this.browser.close();
      }
    }
  }

  saveResults() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const reportPath = path.join(__dirname, `test-results-${timestamp}.json`);
    
    const report = {
      timestamp: new Date().toISOString(),
      duration: Date.now() - this.startTime,
      url: WEBUI_URL,
      results: this.results,
      logs: this.logs,
      summary: {
        totalTests: this.results.length,
        passed: this.results.filter(r => r.success).length,
        failed: this.results.filter(r => !r.success).length
      }
    };

    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    this.log('INFO', `Results saved to: ${reportPath}`);
  }
}

// Run the tests
async function main() {
  console.log('🧪 CodebrewRouter Open WebUI Comprehensive Test Suite');
  console.log('====================================================\n');

  const tester = new WebUITester();
  const success = await tester.runAllTests();

  process.exit(success ? 0 : 1);
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
