import bcrypt
from flask import render_template, jsonify, request, redirect, url_for, session
from Emerald import app
import requests
from Emerald.models import User, db
import re
from functools import wraps
from bson.objectid import ObjectId
from Emerald.recomendattion import get_recommendations  
import numpy as np
from Emerald.models import fasttext_model

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')  
        user_collection = db['Users']
        user = user_collection.find_one({'email': {'$regex': '^' + re.escape(email) + '$', '$options': 'i'}})
        if user and bcrypt.checkpw(password, user['password']):
            session['email'] = email
            return redirect(url_for('profile', email=email))
        else:
            return "Kullanıcı adı veya parola yanlış!"
    return render_template('auth/Login.html')

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = hash_password(request.form['password'])
        interests = request.form.getlist('interests')
        
        user_collection = db['Users']
        existing_user = user_collection.find_one({'email': email})
        
        if existing_user:
            return jsonify({"error": "This email is already registered."}), 400
        
        new_user = User(username=username, lastname=lastname, email=email, password=password, interests=interests)
        new_user.save() 
        return jsonify({"success": "User registered successfully."}), 200  
    return render_template('auth/Register.html')


@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('profile', email=session['email']))
    else:
        return redirect(url_for('login'))
    
@app.route("/profile/<email>")
@login_required
def profile(email):
    user_collection = db['Users']
    user = user_collection.find_one({'email': email})
    if user:
        return render_template("users/Profile.html", user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/article_detail/<article_id>")
def article_detail(article_id):
    article = db['Articles'].find_one({'_id': ObjectId(article_id)})
    if article is None:
        return "Article not found", 404
    # recommendations_fasttext = get_article_recommendations(article_id, 'fasttext')
    # recommendations_scibert = get_article_recommendations(article_id, 'scibert')
    
    return render_template("article_detail.html", article=article)

@app.route("/searcharticles", methods=["GET", "POST"])
def search_articles():
    if request.method == "POST":
        search_query = request.form.get("search")
        articles_collection = db['Articles']
        articles = articles_collection.find(
            {"$text": {"$search": search_query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(20)
        return render_template("articles/SearchArticle.html", articles=articles)
    return render_template("articles/SearchArticle.html", articles=[])


@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password").encode('utf-8')  
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())  

        user_collection = db['Users']
        user_collection.update_one({"email": email}, {"$set": {
            "username": name,
            "lastname": lastname,
            "email": email,
            "password": hashed_password
        }})

        return redirect(url_for("profile", email=email))

@app.route("/recommendations", methods=["GET"])
@login_required
def recommendations():
    user_email = session['email']
    recommendations_fasttext = get_recommendations(user_email, 'fasttext')
    recommendations_scibert = get_recommendations(user_email, 'scibert')

    # Precision değerini hesapla
    response = requests.get(url_for('calculate_performance', _external=True))
    precision_data = response.json()
    precision = precision_data['precision']
    
    return render_template("articles/Recomendation.html", 
                           recommendations_fasttext=recommendations_fasttext,
                           recommendations_scibert=recommendations_scibert,
                           precision=precision)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    user_email = session.get('email')
    data = request.get_json()
    article_id = data.get('article_id')
    interest = data.get('interest')

    feedback_collection = db['Feedback']
    feedback_collection.insert_one({
        'user_email': user_email,
        'article_id': article_id,
        'interest': interest
    })

    # Kullanıcı ilgi alanlarını güncelle
    update_user_interest_vector(user_email, interest, article_id)
    
    return jsonify({"message": "Feedback received"}), 200

def update_user_interest_vector(user_email, interest, article_id):
    user = db['Users'].find_one({'email': user_email})
    article = db['Articles'].find_one({'_id': ObjectId(article_id)})
    
    if not user or not article:
        return
    user_fasttext_vector = np.array(user.get('fasttext_vector', np.zeros(fasttext_model.get_dimension())))
    user_scibert_vector = np.array(user.get('scibert_vector', np.zeros(768)))
    article_fasttext_vector = np.array(article.get('fasttext_vector', np.zeros(fasttext_model.get_dimension())))
    article_scibert_vector = np.array(article.get('scibert_vector', np.zeros(768)))

    if interest == 'interested':
        new_fasttext_vector = (user_fasttext_vector * len(user.get('interests', [])) + article_fasttext_vector) / (len(user.get('interests', [])) + 1)
        new_scibert_vector = (user_scibert_vector * len(user.get('interests', [])) + article_scibert_vector) / (len(user.get('interests', [])) + 1)
    else:
        new_fasttext_vector = (user_fasttext_vector * len(user.get('interests', [])) - article_fasttext_vector) / (len(user.get('interests', [])) - 1) if len(user.get('interests', [])) > 1 else np.zeros(fasttext_model.get_dimension())
        new_scibert_vector = (user_scibert_vector * len(user.get('interests', [])) - article_scibert_vector) / (len(user.get('interests', [])) - 1) if len(user.get('interests', [])) > 1 else np.zeros(768)

    db['Users'].update_one(
        {'email': user_email},
        {'$set': {
            'fasttext_vector': new_fasttext_vector.tolist(),
            'scibert_vector': new_scibert_vector.tolist()
        }}
    )


@app.route('/calculate_performance')
def calculate_performance():
    feedbacks = list(db['Feedback'].find())
    tp = sum(1 for f in feedbacks if f['interest'] == 'interested')
    fp = sum(1 for f in feedbacks if f['interest'] == 'not_interested')

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0

    return jsonify({"precision": precision}), 200