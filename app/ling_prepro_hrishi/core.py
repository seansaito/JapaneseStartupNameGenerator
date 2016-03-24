import fuzzy

def fingerprint_word(word):
    return "%s%02d" % (fuzzy.Soundex(5)(word)[1:],(len(fuzzy.nysiis(word))))
