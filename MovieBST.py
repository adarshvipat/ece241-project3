# Marcelo Goluboff, 35118548
# Adarsh Vipat, 35116645

from Movie import *
from MovieList import *
import random


class Node:
    def __init__(self, movie, index=0):  # constructor
        self.movie = movie  # Movie object stored in the node
        self.left = None
        self.right = None
        self.index = index  # level-order position (root is 0)


class MovieBST:

    def __init__(self, filename=None):  # constructor
        self.__root = None
        self.__size = 0  # private number of items
        if filename is not None:
            file = open(filename, "r")
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                fields = line.split(";", 2)  # ID; Year; Title
                self.insert(Movie(int(fields[0]), int(fields[1]), fields[2]))
            file.close()

    def getSize(self):  # return the number of movies in the BST
        return self.__size

    def insert(self, movie):  # insert a movie, the tree is sorted by ID
        if self.__root is None:
            self.__root = Node(movie, 0)
            self.__size += 1
        else:
            self.__insert(self.__root, movie)

    def __insert(self, node, movie):  # private recursive auxiliary method for insert
        if movie.getID() < node.movie.getID():
            if node.left is None:
                node.left = Node(movie, 2 * node.index + 1)
                self.__size += 1
            else:
                self.__insert(node.left, movie)
        elif movie.getID() > node.movie.getID():
            if node.right is None:
                node.right = Node(movie, 2 * node.index + 2)
                self.__size += 1
            else:
                self.__insert(node.right, movie)
        else:  # same ID already in the tree, replace the movie
            node.movie = movie

    def search(self, id):  # return the movie with the given ID (None if not found)
        current = self.__root
        while current is not None:
            currentID = current.movie.getID()
            if id == currentID:
                return current.movie
            elif id < currentID:
                current = current.left
            else:
                current = current.right
        return None

    def displayInOrder(self): 
        print("Display in order " + str(self.__size) + " items by ID")
        self.__displayInOrder(self.__root)

    def __displayInOrder(self, node): 
        if node is not None:
            self.__displayInOrder(node.left)
            print(node.movie)
            self.__displayInOrder(node.right)

    def show(self):  
        print("The BSTree looks like:")
        self.__show(self.__root, 0)

    def __show(self, node, level): 
        if node is not None:
            self.__show(node.right, level + 1)
            print(" " * 6 * level + str(node.movie.getID()) + "(" + str(node.index) + ")")
            self.__show(node.left, level + 1)

    def extractListInOrder(self, word):
        print("Begin sublist extraction for word:" + word + " using in-order traversal")
        userList = MovieList()
        self.__extractListInOrder(self.__root, word.lower(), userList)
        return userList

    def __extractListInOrder(self, node, word, userList):
        if node is not None:
            self.__extractListInOrder(node.left, word, userList)
            for titleWord in node.movie.getTitle().split():
                if titleWord.lower() == word:
                    userList.append(node.movie)
                    break
            self.__extractListInOrder(node.right, word, userList)
