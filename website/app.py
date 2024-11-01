from flask import Flask, render_template, request
import pickle
import os
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load data files
BASE_DIR = os.path.dirname(__file__)
popular_df = pickle.load(open(os.path.join(BASE_DIR, 'templates', 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(BASE_DIR, 'templates', 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join(BASE_DIR, 'templates', 'books.pkl'), 'rb'))
similarity_score = pickle.load(open(os.path.join(BASE_DIR, 'templates', 'similarity_score.pkl'), 'rb'))

@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        image=list(popular_df['Image-URL-M'].values),
        author=list(popular_df['Book-Author'].values),
        book_rating=list(popular_df['num_ratings'].values),
        avg_rating=list(popular_df['avg_ratings'].values)
    )

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        user_input = request.form.get('book_title')
        
        # Debugging print statement
        print("User input:", user_input)
        
        try:
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:7]

            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                data.append(item)
            
            # Debugging print statement to verify 'data'
            print("Data:", data)
        except IndexError:
            data = [["No results found", "N/A", "https://via.placeholder.com/150"]]

        return render_template('search.html', data=data)
    
    # If GET request is made, show an empty search form or redirect
    return render_template('search.html', data=[])




if __name__ == '__main__':
    app.run(debug=True)
