import pandas as pd
import config
import requests

#TODO- actor race, add ratings from combination of different sources, topics of the winning movies (how to determine if they were topical when released)


##globals
all_casts = [] #list of list of tuples (actor name, cast no) for each film
all_budgets = []
all_titles = []
all_keywords = [] # list of list of keywords for each film
all_actors = [] #list of names
# FULL CAST/GENDERS FOR EACH: 2 - guy, 1 - girl, ignore 0s (unfortunately makes for small margin of error)
all_actor_genders = [] #list of genders (added in order)

def get_movie_ids(filename):
    df = pd.read_csv(filename, usecols = ["Const"])
    return df



def get_details(movie_id):
    call ='https://api.themoviedb.org/3/movie/' + str(movie_id) + '?api_key=' + config.MY_KEY + '&language=en-US'
    r = requests.get(call)
    budget = r.json().get('budget')
    title = r.json().get('original_title')
    all_budgets.append(budget)
    all_titles.append(title)

def get_cast(movie_id):
    call = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/credits?api_key=' + config.MY_KEY
    r = requests.get(call)
    cast = r.json().get('cast')
    # iterate through cast
    cast_for_movie = []
    for item in cast:
        actor_name = item.get('name')
        cast_for_movie.append((actor_name, item.get('cast_id')))  # adding cast[(actor_name, rank_of_appearance)]
        if actor_name not in all_actors:
            all_actors.append(actor_name)
            all_actor_genders.append(item.get('gender')) #add actor name and gender to list
    all_casts.append(cast_for_movie)

def get_keywords(movie_id):
    call = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/keywords?api_key=' + config.MY_KEY
    r = requests.get(call)
    keywords = r.json().get('keywords')
    movie_keywords = []
    for item in keywords:
        word = item.get('name')
        movie_keywords.append(word) # add all keywords for this film
    all_keywords.append(movie_keywords)

def main():
    movies = get_movie_ids("data/BestPictureAcademyAward.csv")

    for Const in movies.itertuples(): #for each movie title
        movie_id = (Const[1])
        get_cast(movie_id)
        get_details(movie_id)
        get_keywords(movie_id)
    movies['Title'] = all_titles
    movies['Cast'] = all_casts
    movies['Budget'] = all_budgets
    movies['Keywords'] = all_keywords
    actors = pd.DataFrame(all_actors, columns=['Name'])
    actors['Gender'] = all_actor_genders

    #print final dataframes
    print(movies.head())
    print(actors.head())

    movies.to_csv('data/FilmData.csv', header=True)

if __name__ == '__main__':
    main()
