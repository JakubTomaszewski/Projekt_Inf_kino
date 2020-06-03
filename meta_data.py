import pandas as pd


def get_movie_titles(url: str):
    try:
        # Loading movie data
        movies_df = pd.read_csv(url)
        # Getting only the titles column and some rows
        movie_titles = movies_df.loc[60:, 'Film']
        # Dropping duplicate rows
        movie_titles = movie_titles.drop_duplicates()
        # Transforming it to a numpy array
        movie_titles_array = movie_titles.values
        return movie_titles_array
    except FileNotFoundError:
        print('File or URL could not be found')
    except ValueError:
        print('Incorrect path')
