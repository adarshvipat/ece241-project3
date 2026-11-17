# Marcelo Goluboff, 35118548
# Adarsh Vipat, 35116645

from Movie import *
from MovieList import *
from Queue import *
import random
import tkinter


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
        self.__maxIndex = 0  # private largest level-order index in the tree
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
                if node.left.index > self.__maxIndex:
                    self.__maxIndex = node.left.index
            else:
                self.__insert(node.left, movie)
        elif movie.getID() > node.movie.getID():
            if node.right is None:
                node.right = Node(movie, 2 * node.index + 2)
                self.__size += 1
                if node.right.index > self.__maxIndex:
                    self.__maxIndex = node.right.index
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

    def getMaxIndex(self):  # return the largest level-order index used in the tree
        return self.__maxIndex

    def getMaxLevel(self):  # return the deepest level of the tree (root is at level 0)
        # level of index i is floor(log2(i+1)), computed exactly with integers
        return (self.__maxIndex + 1).bit_length() - 1

    def displayLevelOrder(self):  # display level by level, return the level-order list
        if self.__root is None:
            return []
        levelList = [None] * (self.__maxIndex + 1)
        queue = Queue(self.__size)  # the queue never holds more than all the nodes
        queue.enqueue(self.__root)
        while not queue.isEmpty():
            node = queue.dequeue()  # visit the node
            print(node.movie)
            levelList[node.index] = node.movie
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)
        return levelList

    @staticmethod
    def plotBST(listDB):  # plot the complete binary tree, highlight the existing movies
        if len(listDB) == 0:
            return
        maxLevel = len(listDB).bit_length() - 1  # level of the last index (root is 0)
        nbNodes = 2 ** (maxLevel + 1) - 1  # number of nodes of the complete binary tree
        nbLeaves = 2 ** maxLevel

        width = 1000
        height = 80 + 60 * maxLevel
        margin = 20
        radius = 4

        # tkinter coordinates of each node of the complete binary tree
        x = [0] * nbNodes
        y = [0] * nbNodes
        first = nbLeaves - 1  # index of the first node of the bottom level
        for i in range(first, nbNodes):  # bottom level is evenly spaced
            if nbLeaves == 1:
                x[i] = width / 2
            else:
                x[i] = margin + (i - first) * (width - 2 * margin) / (nbLeaves - 1)
        for i in range(first - 1, -1, -1):  # a parent sits in the middle of its children
            x[i] = (x[2 * i + 1] + x[2 * i + 2]) / 2
        for i in range(nbNodes):
            level = (i + 1).bit_length() - 1
            y[i] = 30 + 60 * level

        def exists(i):  # True if a movie is stored at index i
            return i < len(listDB) and listDB[i] is not None

        root = tkinter.Tk()
        root.title("BST")
        canvas = tkinter.Canvas(root, width=width, height=height, bg="white")
        canvas.pack()

        # connections: grey ones first so the blue ones stay on top
        for color in ["grey", "blue"]:
            for i in range(1, nbNodes):
                parent = (i - 1) // 2
                used = exists(i) and exists(parent)
                if (color == "blue") == used:
                    canvas.create_line(x[parent], y[parent], x[i], y[i], fill=color)

        # nodes
        for i in range(nbNodes):
            if exists(i):
                color = "blue"
            else:
                color = "grey"
            canvas.create_oval(x[i] - radius, y[i] - radius, x[i] + radius, y[i] + radius,
                               fill=color, outline="black")

        root.mainloop()
