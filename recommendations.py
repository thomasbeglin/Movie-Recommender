# Imports
import importlib
from math import sqrt


# Reload script
# Reload the module
def reload(): importlib.reload()


# This is the nested dictionary that stores the scores that movie critics have given
critics = {
    'Lisa Rose': {'Lady In The Water': 2.5, 'Snakes On A Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5,
                  'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
    'Gene Seymour': {'Lady In The Water': 3.0, 'Snakes On A Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0,
                     'You, Me and Dupree': 3.5, 'The Night Listener': 3.0},
    'Michael Phillips': {'Lady In The Water': 2.5, 'Snakes On A Plane': 3.0, 'Superman Returns': 3.5,
                         'The Night Listener': 4.0},
    'Claudia Puig': {'Snakes On A Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 4.0,
                     'You, Me and Dupree': 2.5, 'The Night Listener': 4.5},
    'Mick LaSalle': {'Lady In The Water': 3.0, 'Snakes On A Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0,
                     'You, Me and Dupree': 2.0, 'The Night Listener': 3.0},
    'Jack Matthews': {'Lady In The Water': 3.0, 'Snakes On A Plane': 4.0, 'Superman Returns': 5.0,
                      'You, Me and Dupree': 3.5, 'The Night Listener': 3.0},
    'Toby': {'Snakes On A Plane': 4.5, 'Superman Returns': 4.0,
             'You, Me and Dupree': 1.0}}


# We now want to see how similar the preferences of different people are, AKA their similarity score
# The two ways of calculating this that I will try here are the Euclidean Distance Score, and the Pearson Correlation Score

# Euclidean Distance Calculator
def sim_distance(prefs, person1, person2):
    # First get list of all movies both people have ranked
    sm = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            sm[item] = 1
    # Return 0 if there are no movies in common
    if len(sm) == 0: return 0
    print(sm)
    sumValues = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in sm])

    return 1 / (1 + sqrt(sumValues))


# Function for calculating the Pearson Correlation Score
def sim_pearson(prefs, person1, person2):
    sm = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            sm[item] = 1

    arrayLen = len(sm)
    if arrayLen == 0: return 0
    # Add up all the movie scores for each person
    person1Sum = sum([prefs[person1][item] for item in sm])
    person2Sum = sum([prefs[person2][item] for item in sm])

    # Add up all the squares of the movie scores for each person
    person1SumSquare = sum([pow(prefs[person1][item], 2) for item in sm])
    person2SumSquare = sum([pow(prefs[person2][item], 2) for item in sm])

    # Add up all the products of the scores each person gave each movie
    totalSumProduct = sum([prefs[person1][item] * prefs[person2][item] for item in sm])

    num = totalSumProduct - (person1Sum * person2Sum / arrayLen)
    den = sqrt((person1SumSquare - pow(person1Sum, 2) / arrayLen) * (person2SumSquare - pow(person2Sum, 2) / arrayLen))
    # Make sure we don't get any math errors!
    if den == 0: return 0

    return num / den


# Function that will take a given person, and recommend them top movies that they might not have seen yet
def movie_recommend(primaryUser, movieDictionary, similarity=sim_pearson):
    totalScores = {}
    totalNoReviews = {}

    for person in movieDictionary:
        if person == primaryUser: continue
        sim = similarity(critics, primaryUser, person)
        if sim <= 0: continue

        for movie in movieDictionary[person]:
            if movie not in movieDictionary[primaryUser] or movieDictionary[primaryUser][movie]==0:
                totalScores.setdefault(movie, 0)
                totalScores[movie] += movieDictionary[person][movie] * sim
                totalNoReviews.setdefault(movie, 0)
                totalNoReviews[movie] += sim

    finalList = []
    for finalMovie in totalScores:
        finalList.append((totalScores[finalMovie] / totalNoReviews[finalMovie], finalMovie))

    finalList.sort()
    finalList.reverse()
    print(finalList)
    return finalList


def main():
    print(movie_recommend('Toby', critics))


if __name__ == "__main__":
    main()
