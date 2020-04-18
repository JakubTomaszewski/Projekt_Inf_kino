import pandas as pd


class BadGatewayException(Exception):
    def __init__(self):
        super().__init__('Incorrect URL')


def get_movie_titles(url):
    try:
        # Loading movie data
        movies_df = pd.read_csv(url)
    except Exception:  # if the url is incorrect raise an exception
        raise BadGatewayException

    # Getting only the titles column and some rows
    movie_titles = movies_df.loc[60:, 'Film']
    # Dropping duplicate rows
    movie_titles = movie_titles.drop_duplicates()
    # Transforming it to a numpy array
    movie_titles_array = movie_titles.values
    return movie_titles_array
