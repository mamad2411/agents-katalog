#!/usr/bin/env node
/**
 * Comprehensive Open WebUI test for CodebrewRouter
 * Updated with correct selectors based on Open WebUI structure
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const WEBUI_URL = process.env.WEBUI_URL || 'http://127.0.0.1:58370/';
const RESPONSE_TIMEOUT_MS = 30000; // Should complete within 30s to avoid hang
const MIN_RESPONSE_LENGTH = 50;

// Test configuration
const TEST_CASES = [
  {
    name: 'Dad Joke (General Knowledge)',
    prompt: 'tell me a dad joke',
    expectedKeywords: ['joke', 'dad'],
    unexpectedKeywords: ['error', 'fail'],
    minLength: 30,
    category: 'general'
  },
  {
    name: 'HttpClient in C# (Code Request)',
    prompt: 'can you create a httpclient in c# that will connect to www.yahoo.com',
    expectedKeywords: ['HttpClient', 'using', 'var'],
    unexpectedKeywords: ['error', 'fail'],
    minLength: 100,
    category: 'code'
  }
];

const ITERATIONS = 2; // Run each test 2 times

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
    this.log('INFO', 'Browser ready');
  }

  async navigateToWebUI() {
    this.log('INFO', 'Navigating to Open WebUI', { url: WEBUI_URL });
    try {
      await this.page.goto(WEBUI_URL, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await this.page.waitForTimeout(2000);
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
      // Wait for the contenteditable div (message input)
      await this.page.waitForSelector('[contenteditable="true"]', {
        timeout: 10000
      });
      this.log('DEBUG', 'Chat interface is ready (contenteditable found)');
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
      // Click on the contenteditable div to focus it
      const contentEditableSelector = '[contenteditable="true"]';
      await this.page.click(contentEditableSelector);
      this.log('DEBUG', 'Focused on input field');

      // Type the prompt
      await this.page.type(contentEditableSelector, prompt, { delay: 50 });
      this.log('DEBUG', 'Prompt typed into input field');

      // Press Enter to send
      await this.page.press(contentEditableSelector, 'Enter');
      this.log('DEBUG', 'Enter key pressed, waiting for response...');

      // Wait for response - look for new messages appearing in the chat
      // Open WebUI typically shows messages in divs with class containing "message"
      let responseReceived = false;
      let responseText = '';
      let attempts = 0;
      const maxAttempts = 60; // Check for up to 60 seconds (1s per check)
      let lastMessageCount = 0;

      while (!responseReceived && attempts < maxAttempts) {
        try {
          // Look for message containers - they typically have role="article" or class with "message"
          const messages = await this.page.$$('[role="article"]');
          const currentCount = messages.length;
          
          // If we have new messages, get the last one
          if (currentCount > lastMessageCount) {
            const lastMessage = messages[messages.length - 1];
            const text = await lastMessage.textContent();
            if (text && text.trim().length > MIN_RESPONSE_LENGTH) {
              responseText = text.trim();
              responseReceived = true;
              this.log('DEBUG', 'Response detected', { length: responseText.length, messageCount: currentCount });
              break;
            }
            lastMessageCount = currentCount;
          }
        } catch (e) {
          // Continue waiting
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
          error: `Timeout: Response did not arrive within ${maxAttempts}s window`
        };
      }

      if (elapsedMs > RESPONSE_TIMEOUT_MS) {
        this.log('WARN', 'Response took longer than ideal', { elapsedMs, idealMs: RESPONSE_TIMEOUT_MS });
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
      this.log('ERROR', 'Error sending prompt', { error: error.message, elapsedMs });
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

  async runAllTests() {
    try {
      await this.initialize();
      
      if (!await this.navigateToWebUI()) {
        this.log('ERROR', 'Cannot proceed - failed to load Open WebUI');
        return false;
      }

      if (!await this.waitForChatReady()) {
        this.log('WARN', 'Chat interface may not be fully ready, but attempting to proceed');
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

      // Summary
      this.log('INFO', '\n========== TEST SUMMARY ==========');
      this.log('INFO', `Passed: ${totalPassed}/${totalTests}`);
      this.log('INFO', `Pass rate: ${(totalPassed / totalTests * 100).toFixed(1)}%`);

      // Save detailed results
      this.saveResults();

      return totalPassed === totalTests;
    } catch (error) {
      this.log('ERROR', 'Unexpected error during test run', { error: error.message });
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
