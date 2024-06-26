import sys
import subprocess
import numpy as np
import pandas as pd

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    install('scikit-learn')
    from sklearn.metrics.pairwise import cosine_similarity


data = {
    'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
    'movie_id': [1, 2, 3, 1, 2, 4, 1, 3, 4, 2, 3, 4],
    'rating': [5, 4, 3, 4, 5, 2, 3, 5, 4, 4, 3, 5]
}

df = pd.DataFrame(data)


user_movie_matrix = df.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
print("User-Movie Matrix:\n", user_movie_matrix)


user_similarity = cosine_similarity(user_movie_matrix)
print("User Similarity:\n", user_similarity)


def get_recommendations(user_id, num_recommendations=3):
    user_index = user_id - 1  
    similar_users = list(enumerate(user_similarity[user_index]))
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)
    
    recommendations = []
    user_rated_movies = set(df[df['user_id'] == user_id]['movie_id'])
    
    for similar_user in similar_users:
        if similar_user[0] == user_index:
            continue
        
        similar_user_id = similar_user[0] + 1
        similar_user_movies = df[df['user_id'] == similar_user_id]
        
        for _, row in similar_user_movies.iterrows():
            if row['movie_id'] not in user_rated_movies and row['movie_id'] not in recommendations:
                recommendations.append(row['movie_id'])
            
            if len(recommendations) >= num_recommendations:
                return recommendations
    
    return recommendations


user_id = int(input("Enter your user ID: "))


recommendations = get_recommendations(user_id)
print(f"Recommendations for User {user_id}:\n", recommendations)
