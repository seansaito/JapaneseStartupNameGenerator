from PyDictionary import PyDictionary
dictionary=PyDictionary()


def get_synonym (word):

    synonyms = dictionary.synonym(word)
    syns = synonyms[:]
    for i in synonyms:
        newlist = dictionary.synonym(i)
        for j in newlist:
            syns.append(j)


    return list(set(syns))

print get_synonym("enraged")
