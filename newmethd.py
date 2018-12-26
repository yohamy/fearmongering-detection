import json
import nltk
nltk.download("punkt")
import operator, functools 
from collections import Counter
import sys
import string
from nltk.stem.snowball import SnowballStemmer
from pprint import pprint
stemmer = SnowballStemmer("english")



"""function that tokenizes each of the lists that are used 
	throughout this program, including the tweets, fearmongering 
	word relations and sympathetic word relations. Then stems 
	all words in each of these lists. Then returns a list of 
	word stems"""
def stemming(text):
		tweet_tokens = []
		tweet_stems = []
		for word in text:
			word.casefold()
			token = nltk.word_tokenize(word)
			tweet_tokens += token
		
		for token in tweet_tokens:
			stem = [stemmer.stem(token)]
			tweet_stems += stem
		return tweet_stems

"""function that counts the frequencies of fearmongering language 
	or sympathetic language within the tweets. The sublist refers 
	to list that the tweets are being compared to (fear mongering 
	and sympathetic word relations) Then returns the frequencies 
	of each word match"""
def frequency(text, sublist):
	freq = Counter()
	for z in text:
		if z in sublist:
			freq[z] += 1
	return freq



with open("twitter.json", "r") as source:
	trump_data = json.load(source)
	from string import punctuation
	
	#retrieves all the full_text (tweet) instances from the file
	get_values = functools.partial(map, operator.itemgetter('full_text'))
	tweets = list(map(operator.itemgetter("full_text"), trump_data))
	print(len(tweets), "tweets")


	trumplist= []
	trumplist = stemming(tweets)

	#strips most punctuations from the stemmed data
	strp = Counter(word.strip(punctuation) for line in trumplist for word in line.split())
	count = Counter(strp).most_common(60)
	print("60 most common words found in tweets", count)
	print("===="*10)


with open("fear_words.txt", "r") as source:
	
	#retrieves all fearmongering related words from file
	fear = stemming(source)
	print("These are fear mongering words", len(fear))
	print(fear)
	print("===="*10)
	
	

with open("sympathetic.txt", "r") as source:
	
	#retrieves all sympathetic related words from file
	sympathetic_words = stemming(source)
	print("These are sympathetic words", len(sympathetic_words))
	print(sympathetic_words)
	print("===="*10)


#Removes any shared stems in both lists
for i in fear:
	if i in sympathetic_words:
		fear.remove(i)
		sympathetic_words.remove(i)



#creates a counter of fear words in the tweets
fear_freq = frequency(trumplist, fear)

print("These are fear mongering words found in tweets", fear_freq)
print("===="*10)


#creates a counter of sympathetic words in the tweets
sym_freq = frequency(trumplist, sympathetic_words)

print("These are sympathetic words found in tweets", sym_freq)
print("===="*10)

		




