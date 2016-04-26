# You must have pymarkovchain in your path
# https://github.com/TehMillhouse/PyMarkovChain
from pymarkovchain import MarkovChain
import glob
import os
import tweepy


# wordpoolGen will generate a list of words from all available .txt.files in the working directory
def wordpool_generator():
	wordpool = []

	# The following iterator will run through all .txt file in the directory
	# print the name and replace newlines with spaces
	for file in glob.glob("*.txt"):
		print(file)
		wordpool.append(open(file).read().replace('\n', ' '))

	# Next, the function will put all texts in one string and remove numbers
	wordpool = ' '.join(wordpool)
	wordpool = ''.join([i for i in wordpool if not i.isdigit()])
	return wordpool

# databaseGen will generate and dumb a database.
def database_generator(markovChain, wordpool):
		markovChain.generateDatabase(wordpool)
		markovChain.dumpdb()

# stringGen will generate a string, based on the markov database.
def string_generator(markovChain):
	while True:
		markovString = markovChain.generateString()
		
		# The function will keep generating new strings
		# until it makes a string longer than 50 characters and shorter than 140 (Twitter limit)
		if len(markovString) > 50 and len(markovString) < 140:
			return markovString

# twitterPoster posts the string to Twitter
# See http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/ for details
def twitter_poster(string):
	#enter the corresponding information from your Twitter application:
	CONSUMER_KEY = 'consumerkey'#keep the quotes, replace this with your consumer key
	CONSUMER_SECRET = 'consumersecret'#keep the quotes, replace this with your consumer secret key
	ACCESS_KEY = 'accesskey'#keep the quotes, replace this with your access token
	ACCESS_SECRET = 'accesssecret'#keep the quotes, replace this with your access token secret
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	api.update_status(string)

# The main script will 
# 1. connect to a Markov database
# 2. generate a word pool and a database if it doesn't exist already
# 3. generate a string from the markovChain
# 4. post the string to Twitter
if __name__ == '__main__':
	databaseName = 'database.db'
	markovChain = MarkovChain(databaseName)
	if not os.path.isfile(databaseName):
		wordpool = wordpool_generator(); database_generator(markovChain, wordpool)
	else:
		print('Database already exists, skipping database creation...')
	string = string_generator(markovChain)
	twitter_poster(string)
