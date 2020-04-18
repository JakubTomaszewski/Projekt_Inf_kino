import pandas as pd


def get_movie_titles(url):
    movies_df = pd.read_csv(url)
    movie_titles_array = movies_df.loc[65:, 'Film'].values
    return movie_titles_array
