import numpy as np
from bson.objectid import ObjectId
from Emerald.models import db
from Emerald.recomendattion import cosine_similarity

def get_article_recommendations(article_id, vector_type='fasttext', num_recommendations=5):
    articles_collection = db["Articles"]

    current_article = articles_collection.find_one({'_id': ObjectId(article_id)})
    if not current_article:
        raise ValueError("Article not found.")

    current_vector = np.array(current_article[f"{vector_type}_vector"])

    recommendations = []
    for article in articles_collection.find({'_id': {'$ne': ObjectId(article_id)}}):  
        article_vector = np.array(article[f"{vector_type}_vector"])
        similarity = cosine_similarity(current_vector, article_vector)
        recommendations.append((article, similarity))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:num_recommendations]
