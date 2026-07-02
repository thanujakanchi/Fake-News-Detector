# Fake News Detector

A Flask-based web application that detects whether a news statement is **Real** or **Fake** using Machine Learning and AI-powered verification through the Groq API.



## Project Overview

Fake News Detector helps users verify the authenticity of news claims. The system combines a trained Machine Learning model with AI analysis to provide accurate predictions and explanations.

Users simply enter a news statement, and the application analyzes the text and returns:

* Real or Fake prediction
* Confidence score
* AI-generated explanation
* News category (when available)



## Features

* Fake news detection using Machine Learning
* AI-powered analysis with Groq API
* Confidence score for predictions
* User-friendly web interface
* Fast and accurate text classification
* Trained using real and fake news datasets
* Responsive design



## Technologies Used

* Python
* Flask
* Scikit-learn
* Pandas
* HTML
* CSS
* JavaScript
* Groq API


## Installation


Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project directory.

```env
GROQ_API_KEY=your_groq_api_key
FLASK_SECRET_KEY=your_secret_key
FLASK_DEBUG=True
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```



## How It Works

1. User enters a news statement.
2. The system preprocesses the text.
3. The Machine Learning model predicts whether the news is Real or Fake.
4. The Groq API analyzes the statement and generates an explanation.
5. The final result, confidence score, and reasoning are displayed to the user.



## Dataset

The project uses publicly available fake and real news datasets containing thousands of news articles for training the Machine Learning model.



## Future Improvements

* Improve model accuracy
* Support multiple languages
* Real-time fact-checking from trusted sources
* Mobile application
* Voice input support
* User authentication and history



Machine Learning Project
