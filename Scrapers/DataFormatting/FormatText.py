# This function converts input string into lower case string with first char
# of each SENTENCE capitalised.

def FormatSentence(sentence):
    sentence = sentence.replace(
        ".", "SPECIAL_CHAR").replace("\n", "SPECIAL_CHAR")
    sentenceList = sentence.split("SPECIAL_CHAR")
    newString = ""
    for val in sentenceList:
        newString += val.strip().capitalize() + ". "
    return newString.strip().replace(". .", ".")  # Remove duplicated full stops


# This function converts input string into lower case string with first char
# of each WORD capitalised.
# The start of each word is identified by (1) space
# (2) starting bracket (3) Next char after -
# This function also makes sure there is spacing around @ and -, if exist
# This function fixes misaligned brackets and output will be (XY)
# (XY) and ( XY ) are not considered misaligned brackets. (XY ) or ( XY) are considered misaligned.

def FormatTitle(title):
    haveReplacedBrack = False
    if(not " ( " in title):
        haveReplacedBrack = True
        title = title.replace("(", " ( ")
    if(not " ) " in title):
        title = title.replace(")", ") ")
    if(not " - " in title):
        title = title.replace(
            "-", " - ")
    if(not " @ " in title):
        title = title.replace(
            "@", " @ ")
    titleList = title.split()
    newString = ""
    for val in titleList:
        newString += val.strip().capitalize() + " "

    if(haveReplacedBrack):
        newString = newString.replace("( ", "(").replace(" )", ")")
    return newString.strip()
