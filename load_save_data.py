import numpy as np
from meta_data import get_movie_titles


def create_seats_array(movies, num_rows, num_seats):
    '''Creates an array made of zeros representing a free cinema hall'''
    for movie in movies:
        # Creating seats array
        seats_array = np.zeros([num_rows, num_seats], dtype=np.int8)
        movie = movie.replace(':', '')
        np.savetxt(f'.\movies\{movie}.csv', seats_array, delimiter=',', fmt='%1d')


def get_csv_data(chosen_movie):
    '''Loads the cinema hall array from a csv file'''
    if chosen_movie is not None:
        chosen_movie = chosen_movie.replace(':', '')
        movie_array = np.genfromtxt(f'.\movies\{chosen_movie}.csv', delimiter=',')
        return movie_array


def save_csv_data(chosen_movie, seats_array):
    '''Saves the cinema hall array into a csv file'''
    if seats_array is not None and chosen_movie is not None:
        chosen_movie = chosen_movie.replace(':', '')
        np.savetxt(f'.\movies\{chosen_movie}.csv', seats_array, delimiter=',', fmt='%1d')


rows = 7
seats = 30


# url = 'https://gist.githubusercontent.com/tiangechen/b68782efa49a16edaf07dc2cdaa855ea/raw/0c794a9717f18b094eabab2cd6a6b9a226903577/movies.csv'
#
# # Getting an array of movie titles
# movie_list = get_movie_titles(url)
# # Creating an zeros array for each movie
# create_seats_array(movie_list, rows, seats)
