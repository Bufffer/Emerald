
## Overview
The Emerald Project is an academic article recommendation system designed to provide personalized article suggestions based on user interests and reading history. The primary goal is to direct users to the most relevant academic articles in their fields of interest, enhancing their research and study experiences.

## Features
- **Data Source**: Utilizes pre-existing academic article datasets such as Inspec and Krapivin2009.
- **Data Preprocessing**:
  - Implements Natural Language Processing (NLP) techniques for text preprocessing using Python libraries such as NLTK or spaCy.
  - Preprocessing steps include removal of English stop words, punctuation, and stemming.
- **Vector Embeddings**:
  - Creates vector representations for articles and user profiles using FastText and SciBERT models.
- **Similarity Calculation**:
  - Uses Cosine Similarity to evaluate and recommend articles based on user profiles.
- **Recommendation Engine**:
  - Provides top 5 recommendations based on FastText and SciBERT vector representations.
  - Dynamically updates recommendations according to user interactions and feedback.
- **User Profile Management**:
  - Allows users to register, create, update, and manage their profiles.
  - Collects demographic information and academic interests during registration.
- **User Interface**:
  - Develops a user-friendly web interface with search and filtering capabilities.
- **Performance Evaluation**:
  - Calculates Precision and Recall values to assess recommendation performance.
  - Displays evaluation results on the interface.

## Technology Stack
- **Backend**: Flask framework for developing the web application.
- **Database**: MongoDB for data synchronization and storage.
- **Machine Learning & AI**: Python for implementing NLP and recommendation algorithms.

## Project Requirements
- **Deliverables**:
  - A comprehensive project report in IEEE format including flow diagrams, pseudocode, summary, introduction, methodology, experimental results, conclusion, references, and an ER diagram.
- **Submission**:
  - Projects must be submitted via edestek2.kocaeli.edu.tr by the specified deadline. Late submissions will not be accepted.

## Usage
- **Initial Recommendations**: Based on user’s specified interests during registration.
- **Dynamic Updates**: Continuously refines recommendations according to user feedback and reading history.
- **Feedback Mechanism**: Users can mark recommendations as relevant or not, influencing future suggestions.




## How to Run the Project
# Befaıre run the project you have to install cc.en.300.bin file for FastText model from [https://fasttext.cc/docs/en/crawl-vectors.html] then you have to add the file to root directory.

# then create a mongodb project and define MONGO_URI and SECRET_KEY in .env.



1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Bufffer/Emerald.git
   cd Emerald


2. **Create an virtual env**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt # Install Dependencies

2. **Run the Project**:
   ```sh
   python run.py
   # and the project will be running at http://127.0.0.1:5000.


## Images from the project

Sign In Page
![Login](https://github.com/Bufffer/Emerald/assets/30267871/290aed4f-15a2-400a-b9fa-39f1d6978783)

Sign Up Page
![Register](https://github.com/Bufffer/Emerald/assets/30267871/072a822d-cff5-4948-8587-df379db4f502)

Interesting Page
# After you enter your demographic information in Sign up, it will ask you for your interests. Here, the dataset I used was analyzed and the top 9 keywords in all articles were found.
![interests](https://github.com/Bufffer/Emerald/assets/30267871/c91ba8e6-b86e-415d-9312-713d097c7491)

Profile Page
# On this page you can edit your profile information after pressing edit.
![profile](https://github.com/Bufffer/Emerald/assets/30267871/9c81e53d-de86-4033-910f-798082b73b35)

Article Search Page
# On this page you can search for the keywords or phrases you want.
![articles](https://github.com/Bufffer/Emerald/assets/30267871/91017db9-605f-49a7-ac96-983efe8c2c41)

Recommendation Page
# This page is a recommendation system page that makes suggestions based on your interests and the articles you like.
![recomendations](https://github.com/Bufffer/Emerald/assets/30267871/3b579d3a-6d4a-46be-b52e-af17716abb33)

Article Detail Page
# On this page you can like and read articles. If you don't like it, it will not show you this kind of article again.
![articles_detail](https://github.com/Bufffer/Emerald/assets/30267871/5b56e236-ac34-4780-83ef-c71a9ffabe44)


