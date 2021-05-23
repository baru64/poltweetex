# https://github.com/seatgeek/fuzzywuzzy
from fuzzywuzzy import fuzz
import string


# Code for testing fuzzy search on tweets
randomTweets = ['sfajczyłam płytkę PCB, której w pełni działający egzemplarz miałam tylko jeden.',
                'Łukaszenka stał się zagrożeniem nie tylko dla obywateli swojego kraju, ale także dla bezpieczeństwa międzynarodowego. Jego akt państwowego terroryzmu wymaga natychmiastowej i zdecydowanej reakcji wszystkich europejskich rządów i instytucji.',
                'Podzielę się naiwnym życzeniem. Byłoby super gdybyśmy wsp. Białorusi się nie pokłócili. Gdybyśmy mówili jednym głosem.',
                'Łukaszenka, ty draniu, oddaj samolot!',
                'Podsumowanie ostatnich 6 lat w Polsce:',
                'Dlaczego prezes jeździ CZESKIM samochodem?!']

def splitIntoWords(lst):
    return lst.split(' ')


def searchForWordInSentence(searchWord, sentence, matchingRatio = 50):
    words = splitIntoWords(sentence)
    for word in words:
        ratio = fuzz.ratio(searchWord,word)
        if(ratio >matchingRatio):
            print("[Word:"+word+", Ratio:" + str(ratio)+"]")

def replacePolishSigns(sentence):
    polishSigns={'ą':'a','ć':'c','ę':'e','ł':'l','ń':'n','ó':'o','ś':'s','ż':'z','ź':'z'}
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    for sign in polishSigns:
        sentence = sentence.replace(sign,polishSigns[sign])
    return sentence

def removePutationMarks(sentence):
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    return sentence

def modifyTweets(tweet):
    tweet = tweet.lower()
    tweet = replacePolishSigns(tweet)
    tweet = removePutationMarks(tweet)
    return tweet





# Code for clearing data 
searchWord = 'samolot'
for tweet in randomTweets:
    tweet = modifyTweets(tweet)
    searchForWordInSentence(searchWord,tweet)
    


