import numpy as np
from bson.objectid import ObjectId
from Emerald.models import db

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0
    return dot_product / (norm_vec1 * norm_vec2)

def get_recommendations(user_email, vector_type='fasttext'):
    users_collection = db["Users"]
    articles_collection = db["Articles"]

    user = users_collection.find_one({"email": user_email})
    if not user:
        raise ValueError(f"User with email {user_email} not found.")

    if vector_type == 'fasttext':
        user_vector = np.array(user["fasttext_vector"])
    elif vector_type == 'scibert':
        user_vector = np.array(user["scibert_vector"])
    else:
        raise ValueError("Invalid vector type")

    recommendations = []
    for article in articles_collection.find():
        if vector_type == 'fasttext':
            article_vector = np.array(article["fasttext_vector"])
            # article_vector = np.array(article["fasttext_vector"])
        elif vector_type == 'scibert':
            article_vector = np.array(article["scibert_vector"])

        similarity = cosine_similarity(user_vector, article_vector)
        recommendations.append((article, similarity))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:5]

