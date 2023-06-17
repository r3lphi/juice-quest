articles = ["the", "to", "a", "an"]
vowels = ["a", "e", "i", "o", "u"]
pronouns = ["i", "my", "you", "your", "he", "his", "she", "her", "they", "their"]

def parsing_remove_list_articles(words):
    newList = []
    for word in words:
        if word in articles:
            continue
        newList.append(word)
    return newList

def parsing_generate_articled(words, uppercaseWhitelist=[]):
    built = ""
    k = 0
    for word in words:
        if k == len(words) - 1 and len(words) > 1:
            built += "and "

        if word not in uppercaseWhitelist:
            word = word.lower()

        if word[0] in vowels:
            built += ("an " + word)
        else:
            built += ("a " + word)
        
        if k < len(words) - 1:
            built += ", "

        k += 1
    built += "."
    return built
def parsing_ownerize(word):
    if word in pronouns:
        return word
    return word + "'s"

