# AqAI Backend

This folder contains the artificial intelligence backend part of the AqAI website. It is an API server developed using Flask.

## Features

- AI chat API
- Services API
- Contact form processing

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

## API Endpoints

### Chat API
- **URL**: `/api/chat`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "message": "Hello, what is artificial intelligence?"
  }
  ```
- **Successful Response**:
  ```json
  {
    "response": "Artificial intelligence refers to computer systems designed to mimic human intelligence.",
    "status": "success"
  }
  ```

### Services API
- **URL**: `/api/services`
- **Method**: `GET`
- **Successful Response**:
  ```json
  [
    {
      "id": 1,
      "title": "AI Solutions",
      "description": "We develop custom artificial intelligence models and solutions for your business.",
      "icon": "fa-robot"
    },
    ...
  ]
  ```

### Contact API
- **URL**: `/api/contact`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "John Smith",
    "email": "john@example.com",
    "message": "I would like to learn more about your AI solutions."
  }
  ```
- **Successful Response**:
  ```json
  {
    "message": "Your message has been received successfully. We will get back to you as soon as possible.",
    "status": "success"
  }
  ```

## Folder Structure

```
ai/
├── app.py              # Main application file
├── model.py            # AI model
├── requirements.txt    # Dependencies
├── data/               # Data files
│   ├── contacts.json   # Contact forms
│   └── responses.json  # Custom responses (optional)
└── README.md           # This file
```

## Training the AI Model

The current AI model is a simple rule-based system that uses keyword matching to categorize user messages and provide appropriate responses. You can train or customize this model in several ways:

### 1. Adding Custom Responses

The easiest way to customize the AI is by creating or editing the `data/responses.json` file:

```json
{
  "greetings": [
    "Custom greeting message 1",
    "Custom greeting message 2"
  ],
  "custom_category": [
    "Custom category response 1",
    "Custom category response 2"
  ]
}
```

These responses will be loaded automatically when the application starts.

### 2. Adding New Categories

To add new categories of responses:

1. Add your new category and responses to the `data/responses.json` file
2. Modify the `_categorize_message` method in `model.py` to recognize this new category:

```python
def _categorize_message(self, message):
    # Existing categories...
    
    # Add your new category
    elif any(word in message for word in ["keyword1", "keyword2", "keyword3"]):
        return "your_new_category"
    
    else:
        return "unknown"
```

### 3. Implementing a More Advanced Model

For a more sophisticated AI model, you can replace the current implementation with:

- **Machine Learning Model**: Implement a text classification model using libraries like scikit-learn, TensorFlow, or PyTorch
- **Integration with External APIs**: Connect to services like OpenAI's GPT, Google's Vertex AI, or other NLP services
- **Custom NLP Pipeline**: Build a more advanced natural language processing pipeline with entity recognition, intent classification, etc.

To implement a machine learning model, you would need to:

1. Collect training data (example conversations)
2. Preprocess the text data
3. Train a classification model
4. Integrate the model into the `generate_response` method

Example of integrating a simple machine learning model:

```python
# In model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

class AIModel:
    def __init__(self):
        # Load the trained model and vectorizer
        self.vectorizer = joblib.load('data/vectorizer.pkl')
        self.classifier = joblib.load('data/classifier.pkl')
        self.responses = self._load_responses()
        
    def generate_response(self, user_message):
        # Preprocess the message
        processed_message = self._preprocess_message(user_message)
        
        # Vectorize the message
        message_vector = self.vectorizer.transform([processed_message])
        
        # Predict the category
        category = self.classifier.predict(message_vector)[0]
        
        # Select a response from the category
        if category in self.responses:
            response = random.choice(self.responses[category])
        else:
            response = random.choice(self.responses["unknown"])
            
        return response
```

## Customization

To customize the AI model:

1. Create a `data/responses.json` file:
```json
{
  "greetings": [
    "Custom greeting message 1",
    "Custom greeting message 2"
  ],
  "custom_category": [
    "Custom category response 1",
    "Custom category response 2"
  ]
}
```

2. Customize the `_categorize_message` method in the `model.py` file. 