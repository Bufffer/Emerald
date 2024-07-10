# vector_embeddings.py
import fasttext
from transformers import BertModel, BertTokenizer
from models import Article, User, db
import numpy as np
import torch

# Modellerin yüklenmesi
fasttext_model = fasttext.load_model('cc.en.300.bin')
scibert_model = BertModel.from_pretrained('allenai/scibert_scivocab_uncased')
scibert_tokenizer = BertTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')

def get_fasttext_vector(text):
    return fasttext_model.get_sentence_vector(text)

def get_scibert_vector(text):
    inputs = scibert_tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = scibert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

def process_articles():
    articles_collection = db["Articles"]
    articles = articles_collection.find()
    for article in articles:
        article_text = article["article_content"]
        fasttext_vector = get_fasttext_vector(article_text)
        scibert_vector = get_scibert_vector(article_text)
        articles_collection.update_one(
            {"_id": article["_id"]},
            {"$set": {"fasttext_vector": fasttext_vector.tolist(), "scibert_vector": scibert_vector.tolist()}}
        )

def process_users():
    users_collection = db["Users"]
    users = users_collection.find()
    for user in users:
        interests_text = ', '.join(user["interests"])
        fasttext_vector = get_fasttext_vector(interests_text)
        scibert_vector = get_scibert_vector(interests_text)
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"fasttext_vector": fasttext_vector.tolist(), "scibert_vector": scibert_vector.tolist()}}
        )

if __name__ == "__main__":
    process_articles()
    process_users()
