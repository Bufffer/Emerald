import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from models import Article  
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BartTokenizer, BartForConditionalGeneration
import spacy
from spacy.tokens import DocBin

nltk.download('stopwords')
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    doc = nlp(' '.join(filtered_tokens))
    lemmatized_tokens = ' '.join([token.lemma_ for token in doc])
    return lemmatized_tokens

def clean_text(text):
    text = text.replace("\t", " ").replace("\r", " ")
    text = ' '.join(text.split())
    return text

def extract_keyphrases(text, num_phrases=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_array = vectorizer.get_feature_names_out()
    tfidf_sorting = tfidf_matrix.toarray().flatten().argsort()[-num_phrases:]
    key_phrases = [feature_array[i] for i in tfidf_sorting]
    return key_phrases

model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def abstractive_keyphrases(text, num_phrases=5):
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    words = summary.split()
    key_phrases = sorted(set(words), key=words.index)
    return key_phrases[:num_phrases]

dataset_folder = 'Dataset'
for filename in os.listdir(dataset_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(dataset_folder, filename), 'r', encoding='utf-8') as file:
            content = file.read()
            parts = content.split('\n', 1)
            title = clean_text(parts[0].strip())
            abstract = clean_text(parts[1].strip()) if len(parts) > 1 else ''

            preprocessed_title = preprocess_text(title)
            preprocessed_abstract = preprocess_text(abstract)

            extractive_phrases = extract_keyphrases(preprocessed_abstract)
            abstractive_phrases = abstractive_keyphrases(preprocessed_abstract)

            article = Article(title=title, content=abstract, extractive_keyphrases=extractive_phrases, abstractive_keyphrases=abstractive_phrases)
            article.save()
