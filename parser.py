articles = ["the", "to", "a", "an"]

def parser_remove_list_articles(_list):
    newList = list[str]
    for word in _list:
        if word in articles:
            continue
        newList.append(word)
    return newList

