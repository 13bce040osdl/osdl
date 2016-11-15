import re
from collections import Counter
from sys import argv

nearby_keys = {
	'a': 'qwsz',
	'b': 'vghn',
	'c': 'xdfv',
	'd': 'erfcxs',
	'e': 'rdsw',
	'f': 'rtgvcd',
	'g': 'tyhbvf',
	'h': 'yujnbg',
	'i': 'ujklo',
	'j': 'uikmnh',
	'k': 'iolmj',
	'l': 'opk',
	'm': 'njk',
	'n': 'bhjm',
	'o': 'iklp',
	'p': 'ol',
	'q': 'wa',
	'r': 'edft',
	's': 'wedxza',
	't': 'rfgy',
	'u': 'yhji',
	'v': 'cfgb',
	'w': 'qase',
	'x': 'zsdc',
	'y': 'tghu',
	'z': 'asx'
}

mistaken_chars = {
	'a': 'e',
	'b': '',
	'c': ['k', 'ch'],
	'd': '',
	'e': ['i', 'a'],
	'f': '',
	'g': '',
	'h': '',
	'i': ['ee', 'y'],
	'j': '',
	'k': ['c'],
	'l': '',
	'm': '',
	'n': '',
	'o': '',
	'p': '',
	'q': '',
	'r': '',
	's': ['sh'],
	't': '',
	'v': 'w',
	'u': ['o','oo'],
	'w': 'v',
	'x': '',
	'y': 'i',
	'z': ''
}

def get_words(text):
	return re.findall(r'\w+', text.lower())

fname = 'corpus'
f = open(fname)
words = Counter(get_words(f.read()))

def Pr(word):
	return words[word] / sum(words.values())

def correct_me(word, n=5):
	l = list(probable_words(word))
	l.sort(key=Pr, reverse=True)
	return l[:n]

def probable_words(word): 
	return (dictionary([word]) or dictionary(distance1(word)) or dictionary(distance2(word)) or [word])

def dictionary(arr): 
	return set(w for w in arr if w in words)

def distance1(word):
	alphabets = "abcdefghijklmnopqrstuvwxyz"
	two_words     = [(word[:i], word[i:]) for i in range(len(word)+1)]
	insert_char    = [x + c + y for x, y in two_words for c in alphabets]
	delete_char    = [x + y[1:] for x, y in two_words if y]
	replace_char   = [x + c + y[1:] for x, y in two_words if y for c in nearby_keys[y[0]]]
	replace_char_new = [x + c + y[1:] for x, y in two_words if y for c in mistaken_chars[y[0]]]
	replace_char.extend(replace_char_new)
	swap_char = [x + y[1] + y[0] + y[2:] for x, y in two_words if len(y)>1]
	return set(delete_char + swap_char + replace_char + insert_char)

def distance2(word): 
    return set(d2 for d1 in distance1(word) for d2 in distance1(d1))
    
print(probable_words(argv[1]))
