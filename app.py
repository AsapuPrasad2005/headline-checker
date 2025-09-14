# 1. Import required libraries
from flask import Flask, request, jsonify, send_from_directory
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os
import requests
from bs4 import BeautifulSoup

# 2. Initialize Flask app
app = Flask(__name__, static_folder='.')

# 3. Tiny demo dataset for training
data = [
    ("The government approved a new health policy today", "REAL"),
    ("Scientists discovered water on Mars", "REAL"),
    ("Celebrity adopts alien baby, sources confirm", "FAKE"),
    ("Miracle cure for aging found; doctors shocked", "FAKE"),
    ("Local mayor launches education reform", "REAL"),
    ("Eat this fruit and lose 10kg overnight", "FAKE"),
    ("New study shows coffee linked to longer life", "REAL"),
    ("World will end next week says prophecy", "FAKE"),
    ("President signs new law on education", "REAL"),
    ("Aliens spotted in New York city", "FAKE")
]

# 4. Separate dataset into texts and labels
texts = [t for t, _ in data]
labels = [l for _, l in data]

# 5. Create and train ML pipeline
pipeline = make_pipeline(
    TfidfVectorizer(max_features=2000, stop_words='english'),
    LogisticRegression()
)
pipeline.fit(texts, labels)

# 6. Function to fetch article text if input is a URL
def fetch_article_text(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text.strip()
    except Exception as e:
        print("Error fetching article:", e)
        return None

# 7. API endpoint: /predict
@app.route('/predict', methods=['POST'])
def predict():
    req = request.get_json()
    if not req or 'text' not in req:
        return jsonify({'error': 'No text provided'}), 400

    text_input = req['text'].strip()

    # If input is a URL, fetch article content
    if text_input.startswith('http://') or text_input.startswith('https://'):
        fetched_text = fetch_article_text(text_input)
        if not fetched_text:
            return jsonify({'error': 'Could not fetch article from URL'}), 400
        text_input = fetched_text

    if not text_input:
        return jsonify({'error': 'Empty text'}), 400

    # Predict label `and probability
    pred = pipeline.predict([text_input])[0]
    probs = pipeline.predict_proba([text_input])[0]
    classes = pipeline.named_steps['logisticregression'].classes_
    prob_for_pred = float(probs[list(classes).index(pred)])

    return jsonify({'label': pred, 'probability': prob_for_pred})

# 8. Serve frontend index.html
@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

# 9. Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
