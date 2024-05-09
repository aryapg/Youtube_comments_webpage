from flask import Flask, request, jsonify, send_file
import pandas as pd
import emoji
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from flask_cors import CORS
from textblob import TextBlob

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)
api_key = "AIzaSyBtpjwDRl5oP1RJgANjgMOAZaXYAwIM_Q4"
youtube = None  # Initialized later in the code

def initialize_youtube_api():
    global youtube
    from googleapiclient.discovery import build
    youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=2500  # Adjust as per your requirements
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        request = youtube.commentThreads().list_next(request, response)
    return comments

def remove_emojis(text):
    text_without_emojis = emoji.demojize(text)
    return re.sub(r':[a-z_]+:', '', text_without_emojis)

def preprocess_text(text):
    text = remove_emojis(text)
    text = ''.join([c for c in str(text) if c.isprintable()])
    text = re.sub(r'[^\w\s]', '', text.lower().strip())
    return text

lancaster = LancasterStemmer()
stop_words = set(nltk.corpus.stopwords.words('english'))

@app.route('/', methods=['POST'])
def index():
    video_id = request.json.get('video_id')
    if video_id:
        initialize_youtube_api()
        comments_texts = get_video_comments(video_id)
        df = pd.DataFrame({
            'Comment': comments_texts,
        })
        df['Comment'] = df['Comment'].apply(preprocess_text)

        df['Comment'] = df['Comment'].apply(lambda x: word_tokenize(str(x)))
        df['Comment'] = df['Comment'].apply(lambda tokens: [word for word in tokens if word.lower() not in stop_words])
        df['Comment'] = df['Comment'].apply(lambda tokens: [lancaster.stem(token) for token in tokens])
        df['Comment'] = df['Comment'].apply(lambda tokens: ' '.join(tokens))

        df['Label'] = df['Comment'].apply(lambda x: TextBlob(x).sentiment.polarity)
        df['Label'] = df['Label'].apply(lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral')

        neutral_count = (df['Label'] == 'neutral').sum()
        rows_to_delete = min(200, neutral_count)
        indices_to_delete = df[df['Label'] == 'neutral'].index[:rows_to_delete]
        df = df.drop(indices_to_delete)

        output_file = 'Final.xlsx'
        df.to_excel(output_file, index=False)

        X_train, X_test, y_train, y_test = train_test_split(df['Comment'], df['Label'], test_size=0.2, random_state=42)

        vectorizer = TfidfVectorizer()
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        rf_classifier = RandomForestClassifier(n_estimators=800, criterion="gini", class_weight={"negative":5, "neutral":2, "positive":2}, max_depth=140, min_samples_split=6, min_samples_leaf=2, max_leaf_nodes=110, bootstrap=False)
        rf_classifier.fit(X_train_tfidf, y_train)

        y_train_pred = rf_classifier.predict(X_train_tfidf)
        accuracy_rf = accuracy_score(y_train, y_train_pred)
        print(df.describe)
        print(f'Random Forest Classifier Training Accuracy: {accuracy_rf:.2f}')

        y_pred_rf = rf_classifier.predict(X_test_tfidf)
        accuracy_rf = accuracy_score(y_test, y_pred_rf)
        print(f'Random Forest Classifier Accuracy: {accuracy_rf:.2f}')

        report = classification_report(y_test, y_pred_rf, output_dict=True)

        # Calculate percentages from the Excel file
        excel_data = pd.read_excel(output_file)
        total_comments = len(excel_data)
        positive_percentage = (excel_data['Label'] == 'positive').sum() / total_comments * 100
        neutral_percentage = (excel_data['Label'] == 'neutral').sum() / total_comments * 100
        negative_percentage = (excel_data['Label'] == 'negative').sum() / total_comments * 100

        return jsonify({
            'report': report,
            'positive_percentage': positive_percentage,
            'neutral_percentage': neutral_percentage,
            'negative_percentage': negative_percentage,
        })

    return jsonify({'error': 'Invalid request, video_id not provided'})

@app.route('/download')
def download_file():
    path = "Final.xlsx"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
