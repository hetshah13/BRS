import streamlit as st
import pandas as pd
import numpy as np

# Load the data and models
popular_df1 = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_score = pd.read_pickle('similarity_score.pkl')

# Streamlit app
st.title('Book Recommendation System')

def display_top_50_books():
    st.header('Top 50 Books')
    num_cols = 4  # Number of columns for the grid
    for i in range(0, min(50, len(popular_df1)), num_cols):
        cols = st.columns(num_cols)
        for j, col in enumerate(cols):
            if i + j < len(popular_df1):
                col.image(popular_df1.iloc[i + j]['Image-URL-M'], width=150)
                col.write(f"**Title**: {popular_df1.iloc[i + j]['Book-Title']}")
                col.write(f"**Author**: {popular_df1.iloc[i + j]['Book-Author']}")
                col.write(f"**Votes**: {popular_df1.iloc[i + j]['num_ratings']}")
                col.write(f"**Rating**: {popular_df1.iloc[i + j]['avg_ratings']:.2f}")

def display_book_recommendation():
    st.header('Find Your Next Favorite Book')
    user_input = st.text_input('Enter a Book Title')

    if user_input:
        try:
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:11]

            st.subheader('Recommended Books')
            num_cols = 4  # Number of columns for the grid
            for i in range(0, len(similar_items), num_cols):
                cols = st.columns(num_cols)
                for j, col in enumerate(cols):
                    if i + j < len(similar_items):
                        temp_df = books[books['Book-Title'] == pt.index[similar_items[i + j][0]]]
                        col.image(temp_df['Image-URL-M'].values[0], width=150)
                        col.write(f"**Title**: {temp_df['Book-Title'].values[0]}")
                        col.write(f"**Author**: {temp_df['Book-Author'].values[0]}")
        except IndexError:
            st.write("Book not found in the dataset.")

def main():
    # Create a select box for the menu
    menu = st.sidebar.selectbox("Menu", ["Top 50 Books", "Book Recommendation"])

    if menu == "Top 50 Books":
        display_top_50_books()
    elif menu == "Book Recommendation":
        display_book_recommendation()

if __name__ == "__main__":
    main()
