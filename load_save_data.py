import numpy as np
# from meta_data import get_movie_titles


def create_seats_array(movies, num_rows, num_seats):
    '''Creates an array made of zeros representing a free cinema hall'''
    for movie in movies:
        # Creating seats array
        seats_array = np.zeros([num_rows, num_seats], dtype=np.int8)

        # Adding report info to the file
        txt_info = f'Tytuł: {movie}\n' + '+'*45 + f'\nliczba osób: {int(seats_array.sum())}\n'
        movie = movie.replace(':', '')  # Replacing special characters for a valid filename
        # Saving the zeros array
        np.savetxt(f'.\movies\{movie}.csv', seats_array, delimiter=',', fmt='%1d', header=txt_info)


def get_csv_data(chosen_movie):
    '''Loads the cinema hall array from a csv file'''
    if chosen_movie is not None:
        chosen_movie = chosen_movie.replace(':', '')  # Replacing special characters for a valid filename
        try:
            movie_array = np.genfromtxt(f'.\movies\{chosen_movie}.csv', delimiter=',', skip_header=4)
            return movie_array
        except FileNotFoundError:  # if the file does not exist
            create_seats_array([chosen_movie], rows, seats)


def save_csv_data(chosen_movie, seats_array):
    '''Saves the cinema hall array into a csv file'''
    if seats_array is not None and chosen_movie is not None:
        # Adding report info to the file
        txt_info = f'Tytuł: {chosen_movie}\n' + '+'*45 + f'\nliczba osób: {int(seats_array.sum())}\n'
        chosen_movie = chosen_movie.replace(':', '')  # Replacing special characters for a valid filename
        np.savetxt(f'.\movies\{chosen_movie}.csv', seats_array, delimiter=',', fmt='%1d', header=txt_info)


rows = 7
seats = 30


# url = 'https://gist.githubusercontent.com/tiangechen/b68782efa49a16edaf07dc2cdaa855ea/raw/0c794a9717f18b094eabab2cd6a6b9a226903577/movies.csv'
#
# # Getting an array of movie titles
# movie_list = get_movie_titles(url)
# # Creating an zeros array for each movie
# create_seats_array(movie_list, rows, seats)
