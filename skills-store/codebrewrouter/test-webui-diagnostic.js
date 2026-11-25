#!/usr/bin/env node
/**
 * Diagnostic script to explore Open WebUI structure
 */

import { chromium } from 'playwright';

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    console.log('Navigating to Open WebUI...');
    await page.goto('http://127.0.0.1:58370/', { waitUntil: 'domcontentloaded', timeout: 15000 });
    
    console.log('Waiting 3 seconds for page to stabilize...');
    await page.waitForTimeout(3000);

    // Take a screenshot
    await page.screenshot({ path: 'webui-diagnostic.png' });
    console.log('Screenshot saved: webui-diagnostic.png');

    // Get page title
    const title = await page.title();
    console.log(`\nPage title: ${title}`);

    // Get all textarea and input elements
    console.log('\n=== Searching for input elements ===');
    const textareas = await page.$$('textarea');
    console.log(`Found ${textareas.length} textarea elements`);
    
    const inputs = await page.$$('input[type="text"]');
    console.log(`Found ${inputs.length} text input elements`);

    // Search for chat-related divs
    console.log('\n=== Searching for chat elements ===');
    const chatElements = await page.$$('[class*="chat"], [class*="message"], [class*="input"], [role="textbox"]');
    console.log(`Found ${chatElements.length} chat-related elements`);

    // Get all buttons
    console.log('\n=== Searching for buttons ===');
    const buttons = await page.$$('button');
    console.log(`Found ${buttons.length} buttons`);
    
    const sendButtons = await page.$$('button[aria-label*="send" i], button:has-text("Send")');
    console.log(`Found ${sendButtons.length} potential send buttons`);

    // Get all input-like elements with different selectors
    console.log('\n=== Searching with broader selectors ===');
    const allInputs = await page.$$('[contenteditable="true"]');
    console.log(`Found ${allInputs.length} contenteditable elements`);

    const divInputs = await page.$$('div[role="textbox"]');
    console.log(`Found ${divInputs.length} div role="textbox" elements`);

    // Look for message input area
    console.log('\n=== Searching for message input area ===');
    const messageForms = await page.$$('form, [class*="message-input"], [class*="chat-input"]');
    console.log(`Found ${messageForms.length} form/message elements`);

    // Try to find elements by text content
    console.log('\n=== Searching by visible text ===');
    const elements = await page.$$('*');
    let foundPromptRelated = false;
    
    for (const el of elements.slice(0, 100)) {
      const text = await el.textContent();
      if (text && (text.includes('message') || text.includes('ask') || text.includes('prompt'))) {
        const tag = await el.evaluate(e => e.tagName);
        console.log(`Found "${text.substring(0, 50)}..." in ${tag}`);
        foundPromptRelated = true;
        break;
      }
    }

    if (!foundPromptRelated) {
      console.log('No obvious prompt-related text found');
    }

    // Get full HTML structure (first 2000 chars)
    console.log('\n=== Page HTML (first 2000 characters) ===');
    const html = await page.content();
    console.log(html.substring(0, 2000));

    console.log('\n=== Diagnostics complete ===');
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
}

main();
