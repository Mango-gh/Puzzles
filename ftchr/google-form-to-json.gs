/**
 * Minimal Google Apps Script: return raw Google Form responses as JSON
 */

// Replace with your actual Google Form ID
const FORM_ID = '1FAIpQLSd0HN_RQWmlOZ2CvPf5JhRVJbANBxrKEZxAh3zT9GPIP7l8jA';

function doGet(e) {
  try {
    const jsonData = getRawResponses();
    return ContentService
      .createTextOutput(JSON.stringify(jsonData, null, 2))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ error: true, message: error.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getRawResponses() {
  const form = FormApp.openById(FORM_ID);
  const responses = form.getResponses();
  const items = form.getItems();

  // Map item IDs to titles for readable keys
  const idToTitle = {};
  items.forEach(function(item) {
    idToTitle[item.getId()] = item.getTitle();
  });

  // Define explicit vs implicit questions
  const explicitQuestions = [
    "Name(Need not be real)",
    "Whats your gender? (More coming soon)",
    "What is your age?",
    "What city do you live in?",
    "What are you looking for?",
    "Do you want children in the future?",
    "Do you smoke?",
    "Do you drink alcohol?",
    "Which of these hobbies or interests do you enjoy? "
  ];

  // Build array of raw response objects
  const jsonData = responses.map(function(response) {
    const explicit = {};
    const implicit = {};
    
    response.getItemResponses().forEach(function(ir) {
      const itemId = ir.getItem().getId();
      const key = idToTitle[itemId] || String(itemId);
      const val = ir.getResponse();
      const answer = Array.isArray(val) ? val : val;
      
      if (explicitQuestions.includes(key)) {
        explicit[key] = answer;
      } else {
        implicit[key] = answer;
      }
    });

    return {
      responseId: response.getId(),
      timestamp: response.getTimestamp(),
      respondentEmail: response.getRespondentEmail(),
      explicit: explicit,
      implicit: implicit
    };
  });

  return jsonData;
}
