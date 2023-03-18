from flask import Flask, render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pivot_table = pickle.load(open('pivot_table.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=[f"Author: {author}" for author in popular_df['Book-Author'].values],
                           image=list(popular_df['Image-URL-M'].values),
                           votes=[f"Votes: {vote}" for vote in popular_df['num_rating'].values],
                           ratings=[f"Rating: {rating:.1f}" for rating in popular_df['avg_rating'].values],
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # found_books = pivot_table.index[pivot_table.index.str.contains(user_input, case=False)]
    # if len(found_books) == 0:
    #     return render_template('recommend.html', message='Name not found. Please try again.')
    # index_new = np.where(pivot_table.index==found_books[0])[0][0]
    if user_input not in pivot_table.index:
        return render_template('recommend.html', message='Name not found. Please try again.')
    index_new = np.where(pivot_table.index==user_input)[0][0]
    similar_book_recommend = sorted(list(enumerate(similarity_score[index_new])),key=lambda x:x[1],reverse=True)[1:6]
    data = []
    for items in similar_book_recommend:
        book =[]
        temp_df = books[books['Book-Title'] == pivot_table.index[items[0]]]
        book.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        book.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        book.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(book)
    print(data)
    return render_template('recommend.html', data=data)

if __name__=='__main__':
    app.run(debug=True)