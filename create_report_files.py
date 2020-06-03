from load_save_data import create_seats_array
from meta_data import get_movie_titles

# Setting the cinema hall size
rows = 7
seats = 30

# Creating empty report files
# URL with movie data
url = 'https://gist.githubusercontent.com/tiangechen/b68782efa49a16edaf07dc2cdaa855ea/raw/0c794a9717f18b094eabab2cd6a6b9a226903577/movies.csv'

# Getting an array of movie titles
movie_list = get_movie_titles(url)
if movie_list is not None:
    # Creating an zeros array for each movie
    create_seats_array(movie_list, rows, seats)
