---
description: 
globs: 
alwaysApply: false
---
# Gmail API Testing Instructions for Google OAuth

**Subject**: OAuth Verification Response - Step-by-Step Gmail API Testing Instructions  
**Project ID**: omnii-462003 (31768914670)

Dear Google Verification Team,

Thank you for reviewing our OAuth application. We have addressed the testing concerns and provide the following detailed instructions to test our Gmail API integration.

## Application Overview

**Omnii** is an AI-powered productivity assistant that helps users manage their Gmail, Calendar, Contacts, and Tasks through natural language commands. Our application uses Gmail API to analyze user emails and provide intelligent productivity assistance.

## 🔧 Recent Technical Updates

We have **fixed the quick action functionality** that may have caused issues during your previous testing:
- ✅ Fixed non-responsive quick action buttons
- ✅ Added visual feedback for API calls  
- ✅ Enhanced user interface clarity
- ✅ Improved error handling and connection status

## 📋 How to Test Gmail API Integration

### **Application Access**
- **URL**: [Your production app URL]
- **Test Environment**: Use a Gmail account with recent emails for comprehensive testing

### **Method 1: Quick Actions Panel (Recommended)**

1. **Sign in** with Google OAuth (will request Gmail permissions)
2. **Locate the Quick Actions Panel** on the right sidebar (desktop) or in the Actions tab (mobile)
3. **Look for** the "⚡ Quick Actions" section with Gmail, Calendar, Contacts, and Tasks buttons
4. **Click the "Gmail" button** (envelope icon) labeled "Check latest emails"
   - **Expected Result**: AI fetches and displays your recent emails with analysis
   - **Visual Feedback**: Button shows loading spinner during processing
   - **AI Response**: Provides email summary, actionable insights, and task suggestions

### **Method 2: Natural Language Commands**

Type any of these commands in the chat input field:
- `"check my latest emails"`
- `"fetch my emails"`  
- `"show me my inbox"`
- `"get my recent emails"`
- `"search my emails for [keyword]"`

### **Method 3: Advanced Email Functions**

Test additional Gmail API capabilities:
- **Email Composition**: `"compose a new email"`
- **Email Organization**: `"show my unread emails"`
- **Label Management**: `"create a label called 'Important'"`
- **Email Analysis**: `"find emails from last week about meetings"`

## 🎯 Gmail API Usage & Scopes

### **OAuth Scopes We Request**
- `https://mail.google.com/` - Full Gmail access for comprehensive email management
- `https://www.googleapis.com/auth/gmail.readonly` - Read emails for analysis
- `https://www.googleapis.com/auth/gmail.compose` - Create draft emails
- `https://www.googleapis.com/auth/gmail.send` - Send emails on user's behalf  
- `https://www.googleapis.com/auth/gmail.modify` - Organize emails with labels
- `https://www.googleapis.com/auth/gmail.labels` - Manage email labels and categories

### **How We Use Gmail Data**

#### **1. AI-Powered Email Analysis**
- Extract actionable tasks from email content
- Identify urgent emails requiring immediate attention
- Suggest optimal response times based on sender patterns
- Analyze communication patterns for productivity insights

#### **2. Smart Email Management**
- Help compose contextually appropriate replies
- Organize emails with intelligent labeling suggestions
- Extract meeting details for calendar integration
- Update contact information from email signatures

#### **3. Productivity Enhancement**
- Convert emails to actionable tasks
- Identify follow-up requirements
- Suggest email templates for common responses
- Provide email scheduling recommendations

## 🔒 Data Privacy & Security

### **Data Processing**
- Email content is analyzed in real-time for AI insights
- No permanent storage of sensitive email content
- Only metadata required for AI context is temporarily cached
- All processing happens server-side with encrypted communication

### **User Control**
- Users can disconnect Gmail access anytime via Google Account settings
- All Gmail actions require explicit user approval before execution
- Granular permissions allow limiting specific functionalities
- Complete data deletion available upon request

## 🧠 AI Context Enhancement

### **Why We Need Comprehensive Gmail Access**

Our AI assistant requires full Gmail access to:

1. **Understand User Context**: Analyze communication patterns to provide personalized assistance
2. **Extract Actionable Items**: Identify tasks, deadlines, and follow-ups from email conversations
3. **Provide Intelligent Suggestions**: Recommend responses, scheduling, and organization strategies
4. **Maintain Conversation Continuity**: Reference previous email threads for context-aware assistance
5. **Enable Proactive Assistance**: Anticipate user needs based on email content and patterns

### **User Experience Enhancement**

The comprehensive Gmail integration enables:
- **Natural Language Email Management**: Users can request email actions in plain English
- **Smart Prioritization**: AI identifies and highlights important emails
- **Automated Task Creation**: Convert email requests into actionable items
- **Intelligent Scheduling**: Extract meeting details and suggest optimal times
- **Context-Aware Responses**: Generate appropriate replies based on conversation history

## 🚀 Expected Testing Experience

### **Typical User Flow**
1. User clicks Gmail quick action or types email-related command
2. AI instantly connects to Gmail API using user's OAuth token
3. Real-time email fetching and analysis occurs
4. AI provides summary with actionable insights
5. User can ask follow-up questions or request email actions
6. AI helps compose responses or take organizational actions

### **What You Should See**
- **Immediate Response**: Fast email fetching and display
- **AI Analysis**: Intelligent summary of email content
- **Actionable Insights**: Task suggestions and follow-up recommendations
- **Visual Feedback**: Loading states and processing indicators
- **Context Awareness**: References to previous emails and conversations

## 📧 Recommended Test Scenarios

### **Basic Functionality**
1. **Email Retrieval**: Test with account containing 10+ recent emails
2. **Email Analysis**: Use account with mix of personal and work emails  
3. **Task Extraction**: Test with emails containing action items
4. **Contact Integration**: Test with emails from various senders

### **Advanced Features**
1. **Email Composition**: Request AI to help draft professional emails
2. **Label Management**: Test creating and applying email labels
3. **Search Functionality**: Search for specific emails or topics
4. **Integration Testing**: Test Calendar event extraction from emails

## 🛠️ Troubleshooting

### **If Quick Actions Don't Respond**
- Ensure you're signed in with Google OAuth
- Check that Gmail permissions were granted during sign-in
- Try refreshing the page and re-testing
- Look for any connection status indicators

### **If Commands Don't Work**
- Verify the command is typed correctly in the chat input
- Ensure WebSocket connection is active (check connection status)
- Try alternative command phrasing
- Check browser console for any error messages

## 📞 Support Contact

If you encounter any issues during testing or need additional clarification, please contact:

**Technical Contact**: [Your contact information]  
**Email**: [Your email]  
**Response Time**: Within 24 hours

We are committed to ensuring smooth OAuth verification and appreciate your thorough review of our application.

---

**Best regards,**  
Omnii Development Team  
[Date]
