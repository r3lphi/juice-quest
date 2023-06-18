import inflect

articles = ["the", "to", "a", "an"]
vowels = ["a", "e", "i", "o", "u"]
pronouns = ["i", "my", "you", "your", "he", "his", "she", "her", "they", "their"]

infEngine = inflect.engine()

def parsing_remove_articles(str):
    for word in str.split():
        if word in articles:
            return parsing_remove_articles(str[:str.index(word)] + str[str.index(word) + len(word) + 1:])
    return str

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

def parsing_get_article(word):
    if word[0] in vowels:
        return "an"
    return "a"

def parsing_ownerize(word, gamedata):
    if word in pronouns:
        return word
    if word == gamedata.name:
        return "your"
    return word + "'s"

def parsing_generate_quantity(word, quantity):
    if quantity == 1:
        if word[0] in vowels:
            return "an "
        else:
            return "a "
    elif quantity <= 12:
        match quantity:
            case 6:
                return "half-a-dozen "
            case 12:
                return "a dozen "
            case _:
                return f"{infEngine.number_to_words(quantity)} "
    else:
        return "a lot of "


def parsing_rough_compare(a, b):
    if not b:
        return False
    for word in b.lower().split():
        if word in a.lower().split():
            continue
        return False
    return True

