# models.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import fasttext
import numpy as np
from transformers import AutoTokenizer, AutoModel

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.Users

# Modellerin yüklenmesi
fasttext_model = fasttext.load_model('cc.en.300.bin')
scibert_model_name = "allenai/scibert_scivocab_uncased"
scibert_tokenizer = AutoTokenizer.from_pretrained(scibert_model_name)
scibert_model = AutoModel.from_pretrained(scibert_model_name)

class User:
    def __init__(self, username, lastname, email, password, interests=None):
        self.username = username
        self.lastname = lastname
        self.email = email
        self.password = password
        self.interests = interests if interests else []
        self.fasttext_vector = self.get_fasttext_vector()
        self.scibert_vector = self.get_scibert_vector()

    def save(self):
        users_collection = db["Users"]
        user_data = {
            "username": self.username,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password,
            "interests": self.interests,
            "fasttext_vector": self.fasttext_vector.tolist(),
            "scibert_vector": self.scibert_vector.tolist()
        }
        users_collection.insert_one(user_data)

    def get_fasttext_vector(self):
        total_vector = np.zeros(fasttext_model.get_dimension())
        for interest in self.interests:
            total_vector += fasttext_model.get_sentence_vector(interest)
        return total_vector / len(self.interests) if self.interests else np.zeros(fasttext_model.get_dimension())

    def get_scibert_vector(self):
        total_vector = np.zeros(768)
        for interest in self.interests:
            inputs = scibert_tokenizer(interest, return_tensors="pt", truncation=True, padding=True, max_length=512)
            outputs = scibert_model(**inputs)
            total_vector += outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
        return total_vector / len(self.interests) if self.interests else np.zeros(768)

class Article:
    def __init__(self, title, content, extractive_keyphrases, abstractive_keyphrases):
        self.title = title
        self.content = content
        self.extractive_keyphrases = extractive_keyphrases
        self.abstractive_keyphrases = abstractive_keyphrases
        self.fasttext_vector = self.get_fasttext_vector()
        self.scibert_vector = self.get_scibert_vector()

    def save(self):
        articles_collection = db["Articles"]
        article_data = {
            "article_title": self.title,
            "article_content": self.content,
            "extractive_keyphrases": self.extractive_keyphrases,
            "abstractive_keyphrases": self.abstractive_keyphrases,
            "fasttext_vector": self.fasttext_vector.tolist(),
            "scibert_vector": self.scibert_vector.tolist()
        }
        articles_collection.insert_one(article_data)

    def get_fasttext_vector(self):
        words = self.content.split()
        total_vector = np.sum([fasttext_model.get_sentence_vector(word) for word in words], axis=0)
        return total_vector / len(words) if words else np.zeros(fasttext_model.get_dimension())

    def get_scibert_vector(self):
        inputs = scibert_tokenizer(self.content, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = scibert_model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

class Recommendation:
    def __init__(self, user_id, article_id, score):
        self.user_id = user_id
        self.article_id = article_id
        self.score = score

    def save(self):
        recommendations_collection = db["Recommendations"]
        recommendation_data = {
            "user_id": self.user_id,
            "article_id": self.article_id,
            "score": self.score
        }
        recommendations_collection.insert_one(recommendation_data)

db['Articles'].create_index([("article_title", "text"), ("article_content", "text")])