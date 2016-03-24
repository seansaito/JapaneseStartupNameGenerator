from global_vars import script_dir
import os

good_words = os.path.join(script_dir, "words.txt")
bad_words = os.path.join(script_dir, "badwords.txt")

def getGoodWords ():

	wordfile = open (good_words, "r")
	wordList = []
	for word in wordfile:
		word = word.strip("\n")
		wordList.append (word)
	return wordList

def getBadWords ():

	wordfile = open (bad_words, "r")
	wordList = []
	for word in wordfile:
		word = word.strip("\n")
		wordList.append (word)
	return wordList

# print getBadWords()
