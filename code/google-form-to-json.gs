/**
 * Google Apps Script to extract Google Form responses as JSON
 * 
 * Setup Instructions:
 * 1. Go to script.google.com
 * 2. Create a new project
 * 3. Copy this code into the script editor
 * 4. Replace 'YOUR_FORM_ID' with your actual Google Form ID
 * 5. Run the main function to test
 */

// Configuration - Replace with your form ID
const FORM_ID = 'YOUR_FORM_ID'; // Get this from your form URL

/**
 * Main function to extract form responses as JSON
 */
function extractFormResponsesAsJSON() {
  try {
    // Get the form
    const form = FormApp.openById(FORM_ID);
    
    // Get all responses
    const responses = form.getResponses();
    
    // Get form items (questions) for mapping
    const formItems = form.getItems();
    
    // Create a mapping of item IDs to question titles
    const itemMapping = {};
    formItems.forEach(item => {
      itemMapping[item.getId()] = item.getTitle();
    });
    
    // Process responses
    const jsonData = responses.map((response, index) => {
      const responseData = {
        responseId: response.getId(),
        timestamp: response.getTimestamp(),
        respondentEmail: response.getRespondentEmail(),
        answers: {}
      };
      
      // Get all item responses
      const itemResponses = response.getItemResponses();
      
      itemResponses.forEach(itemResponse => {
        const itemId = itemResponse.getItem().getId();
        const questionTitle = itemMapping[itemId] || 'Unknown Question';
        const answer = itemResponse.getResponse();
        
        // Handle different types of responses
        if (Array.isArray(answer)) {
          responseData.answers[questionTitle] = answer;
        } else {
          responseData.answers[questionTitle] = answer;
        }
      });
      
      return responseData;
    });
    
    // Log the JSON data
    console.log('Form Responses as JSON:');
    console.log(JSON.stringify(jsonData, null, 2));
    
    // Optionally save to a Google Sheet
    saveToSheet(jsonData);
    
    return jsonData;
    
  } catch (error) {
    console.error('Error extracting form responses:', error);
    throw error;
  }
}

/**
 * Save the JSON data to a Google Sheet
 */
function saveToSheet(jsonData) {
  try {
    // Create or get the spreadsheet
    const spreadsheet = SpreadsheetApp.create('Form Responses JSON Export');
    const sheet = spreadsheet.getActiveSheet();
    
    // Add headers
    sheet.getRange(1, 1).setValue('Response ID');
    sheet.getRange(1, 2).setValue('Timestamp');
    sheet.getRange(1, 3).setValue('Email');
    sheet.getRange(1, 4).setValue('JSON Data');
    
    // Add data
    jsonData.forEach((response, index) => {
      const row = index + 2;
      sheet.getRange(row, 1).setValue(response.responseId);
      sheet.getRange(row, 2).setValue(response.timestamp);
      sheet.getRange(row, 3).setValue(response.respondentEmail);
      sheet.getRange(row, 4).setValue(JSON.stringify(response.answers, null, 2));
    });
    
    // Auto-resize columns
    sheet.autoResizeColumns(1, 4);
    
    console.log('Data saved to spreadsheet:', spreadsheet.getUrl());
    
  } catch (error) {
    console.error('Error saving to sheet:', error);
  }
}

/**
 * Get form responses for a specific date range
 */
function extractFormResponsesByDateRange(startDate, endDate) {
  try {
    const form = FormApp.openById(FORM_ID);
    const responses = form.getResponses();
    
    const filteredResponses = responses.filter(response => {
      const responseDate = response.getTimestamp();
      return responseDate >= startDate && responseDate <= endDate;
    });
    
    console.log(`Found ${filteredResponses.length} responses between ${startDate} and ${endDate}`);
    
    // Process the filtered responses (same logic as main function)
    const formItems = form.getItems();
    const itemMapping = {};
    formItems.forEach(item => {
      itemMapping[item.getId()] = item.getTitle();
    });
    
    const jsonData = filteredResponses.map(response => {
      const responseData = {
        responseId: response.getId(),
        timestamp: response.getTimestamp(),
        respondentEmail: response.getRespondentEmail(),
        answers: {}
      };
      
      const itemResponses = response.getItemResponses();
      itemResponses.forEach(itemResponse => {
        const itemId = itemResponse.getItem().getId();
        const questionTitle = itemMapping[itemId] || 'Unknown Question';
        const answer = itemResponse.getResponse();
        
        if (Array.isArray(answer)) {
          responseData.answers[questionTitle] = answer;
        } else {
          responseData.answers[questionTitle] = answer;
        }
      });
      
      return responseData;
    });
    
    console.log('Filtered Form Responses as JSON:');
    console.log(JSON.stringify(jsonData, null, 2));
    
    return jsonData;
    
  } catch (error) {
    console.error('Error extracting filtered form responses:', error);
    throw error;
  }
}

/**
 * Export responses to a downloadable JSON file
 */
function exportResponsesAsJSONFile() {
  try {
    const jsonData = extractFormResponsesAsJSON();
    
    // Create a blob with the JSON data
    const blob = Utilities.newBlob(
      JSON.stringify(jsonData, null, 2),
      'application/json',
      'form_responses.json'
    );
    
    // Save to Google Drive
    const file = DriveApp.createFile(blob);
    
    console.log('JSON file created:', file.getUrl());
    console.log('File ID:', file.getId());
    
    return file;
    
  } catch (error) {
    console.error('Error creating JSON file:', error);
    throw error;
  }
}

/**
 * Get form metadata and structure
 */
function getFormMetadata() {
  try {
    const form = FormApp.openById(FORM_ID);
    
    const metadata = {
      formId: form.getId(),
      title: form.getTitle(),
      description: form.getDescription(),
      isAcceptingResponses: form.isAcceptingResponses(),
      hasProgressBar: form.hasProgressBar(),
      isQuiz: form.isQuiz(),
      questions: []
    };
    
    const items = form.getItems();
    items.forEach(item => {
      const questionData = {
        id: item.getId(),
        title: item.getTitle(),
        type: item.getType().toString(),
        helpText: item.getHelpText()
      };
      
      metadata.questions.push(questionData);
    });
    
    console.log('Form Metadata:');
    console.log(JSON.stringify(metadata, null, 2));
    
    return metadata;
    
  } catch (error) {
    console.error('Error getting form metadata:', error);
    throw error;
  }
}
