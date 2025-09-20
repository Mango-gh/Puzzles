# Google Form to JSON Export Script

This Google Apps Script extracts responses from your Google Form and converts them to JSON format.

## Setup Instructions

### 1. Get Your Form ID
1. Open your Google Form
2. Look at the URL: `https://docs.google.com/forms/d/FORM_ID/edit`
3. Copy the `FORM_ID` part (the long string between `/d/` and `/edit`)

### 2. Create the Script
1. Go to [script.google.com](https://script.google.com)
2. Click "New Project"
3. Delete the default code and paste the contents of `google-form-to-json.gs`
4. Replace `'YOUR_FORM_ID'` with your actual form ID
5. Save the project (Ctrl+S or Cmd+S)

### 3. Run the Script
1. In the script editor, select the `extractFormResponsesAsJSON` function from the dropdown
2. Click the "Run" button (▶️)
3. Grant permissions when prompted
4. Check the "Executions" tab to see the results

## Available Functions

### `extractFormResponsesAsJSON()`
- **Purpose**: Main function to extract all form responses as JSON
- **Output**: Logs JSON to console and optionally saves to Google Sheet
- **Usage**: Run this function to get all responses

### `extractFormResponsesByDateRange(startDate, endDate)`
- **Purpose**: Extract responses within a specific date range
- **Parameters**: 
  - `startDate`: Date object (e.g., `new Date('2024-01-01')`)
  - `endDate`: Date object (e.g., `new Date('2024-12-31')`)
- **Usage**: Call with specific dates to filter responses

### `exportResponsesAsJSONFile()`
- **Purpose**: Creates a downloadable JSON file in Google Drive
- **Output**: Creates a file named `form_responses.json` in your Google Drive
- **Usage**: Run to get a downloadable JSON file

### `getFormMetadata()`
- **Purpose**: Get information about the form structure
- **Output**: Returns form title, description, questions, etc.
- **Usage**: Run to understand your form's structure

## JSON Output Format

The script outputs JSON in this format:

```json
[
  {
    "responseId": "unique_response_id",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "respondentEmail": "user@example.com",
    "answers": {
      "What's your name?": "John Doe",
      "What's your age?": "25",
      "What are your hobbies?": ["Reading", "Gaming", "Cooking"],
      "Rate your experience": "5"
    }
  }
]
```

## Features

- ✅ Extracts all form responses
- ✅ Maps question IDs to readable question titles
- ✅ Handles different answer types (text, multiple choice, checkboxes)
- ✅ Includes timestamps and respondent emails
- ✅ Optional Google Sheet export
- ✅ Optional JSON file download
- ✅ Date range filtering
- ✅ Form metadata extraction
- ✅ Error handling and logging

## Troubleshooting

### Permission Errors
- Make sure you're the owner of the form or have edit access
- Grant all requested permissions when running the script

### Form ID Issues
- Double-check that you've replaced `'YOUR_FORM_ID'` with the correct ID
- The form ID is the long string in your form's URL

### No Responses Found
- Make sure your form has responses
- Check that the form is accepting responses
- Verify you have the correct form ID

### Script Execution Errors
- Check the "Executions" tab in the script editor for detailed error messages
- Make sure all required permissions are granted

## Example Usage

```javascript
// Get all responses
const allResponses = extractFormResponsesAsJSON();

// Get responses from last month
const lastMonth = new Date();
lastMonth.setMonth(lastMonth.getMonth() - 1);
const recentResponses = extractFormResponsesByDateRange(lastMonth, new Date());

// Export as downloadable file
const jsonFile = exportResponsesAsJSONFile();

// Get form information
const formInfo = getFormMetadata();
```

## Customization

You can modify the script to:
- Change the JSON output format
- Add additional data fields
- Filter responses by specific criteria
- Export to different formats
- Send data to external APIs

## Support

If you encounter issues:
1. Check the script execution logs
2. Verify your form ID is correct
3. Ensure you have proper permissions
4. Test with a simple form first

