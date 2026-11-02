from Movie import *
import random
import sys

class MovieList:

    def __init__(self, filename=None):  # constructor
        self.__list = []  # private list of Movie objects
        if filename is not None:
            file = open(filename, "r")
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                fields = line.split(";", 2)  # ID; Year; Title
                self.__list.append(Movie(int(fields[0]), int(fields[1]), fields[2]))
            file.close()

    def getSize(self):  # return the number of movies in the list
        return len(self.__list)

    def append(self, movie):  # add a movie at the end of the list
        self.__list.append(movie)

    def binarySearch(self, id):  # return the movie with the given ID (None if not found)
        low = 0
        high = len(self.__list) - 1
        while low <= high:
            mid = (low + high) // 2
            midID = self.__list[mid].getID()
            if midID == id:
                return self.__list[mid]
            elif midID < id:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def shuffle(self):  # randomly shuffle the list (Fisher-Yates)
        for i in range(len(self.__list) - 1, 0, -1):
            j = random.randint(0, i)
            self.__list[i], self.__list[j] = self.__list[j], self.__list[i]

    def save(self, filename):  # save the list using the same format as the database file
        file = open(filename, "w")
        for movie in self.__list:
            file.write(str(movie.getID()) + ";" + str(movie.getYear()) + ";" + movie.getTitle() + "\n")
        file.close()