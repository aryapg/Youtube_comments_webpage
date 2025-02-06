# YouTube Comments Sentiment Analyzer Web App

This project consists of a **backend** Python script that retrieves YouTube video comments, performs sentiment analysis, and a **frontend** React-based web application that displays the sentiment analysis results interactively.

## Installation and Setup

### 1. Clone the Repository
Clone both the backend and frontend repository:
```bash
git clone https://github.com/aryapg/Youtube-Comments-Sentiment-Analyzer.git
cd Youtube-Comments-Sentiment-Analyzer

### 2. Backend Setup (Python)

#### Install Required Dependencies
Ensure you have Python 3.6 or higher installed. Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

#### Configure API Key
1. Obtain a YouTube Data API key from the Google Cloud Console.
2. Open the `youtube_comments_sentiment.py` file in a text editor.
3. Locate the `api_key` variable and replace `"YOUR_API_KEY"` with your actual API key:
```python
api_key = "YOUR_API_KEY"
```

#### Run the Sentiment Analyzer Backend
```bash
python youtube_comments_sentiment.py
```
Enter the YouTube video ID when prompted.

### 3. Frontend Setup (React)

#### Install Dependencies
Navigate to the frontend directory and install the required dependencies:
```bash
cd ../Youtube_Comments_Sentiment_Analyzer
npm install
```

#### Run the Web Application
```bash
npm start
```
The app will open in your browser at `http://localhost:3000/`.

## Requirements

### Backend (Python)
* Python 3.6 or higher
* pandas
* google-api-python-client
* scikit-learn
* textblob
* nltk
* emoji
* gensim
* matplotlib
* numpy

### Frontend (React)
* Node.js and npm installed
* React
* React Bootstrap (if used in the project)

## File Descriptions
* **youtube_comments_sentiment.py**: Backend script for sentiment analysis.
* **requirements.txt**: Lists required Python packages.
* **Frontend React files**: Contains the UI and logic for interacting with the backend.

## Acknowledgments
This project utilizes the YouTube Data API v3 and various machine learning libraries for sentiment analysis, along with React for frontend development.

