def getGoodWords ():

	wordfile = open ("words.txt", "r")
	wordList = []
	for word in wordfile:
		word = word.strip("\n")
		wordList.append (word)
	return wordList

def getBadWords ():

	wordfile = open ("badwords.txt", "r")
	wordList = []
	for word in wordfile:
		word = word.strip("\n")
		wordList.append (word)
	return wordList

print getBadWords()