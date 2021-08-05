from django.shortcuts import render
from django.views.generic import TemplateView
import tweepy
import json
import re
import pandas as pd

# Create your views here.
recentlySearchedList = []

class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		template_name = "index.html"
		return render(request, template_name, context=None)

def get_hashtags(request):
	data1 = request.GET['fulltextarea'].replace(" ", "").replace("#", "")
	data = re.sub(r'[^\w\s]','',data1)
	if not data:
		return render(request, 'index.html', context=None)
	#if not data in recentlySearchedList:
	recentlySearchedList.insert(0, data)
	#print(recentlySearchedList)
	recentlySearchedList1 = recentlySearchedList[:5]
	recentlySearchedResult = ', '.join(recentlySearchedList1)
	result = fetchTop5HashTags(data)
	context = {
		"searched_word": data,
		"top5mostused" : result,
		"recentlySearched": recentlySearchedResult
	}
	return render(request, 'index.html', context)

def fetchTop5HashTags(query):
	strOutput = "No Results"
	auth = tweepy.OAuthHandler("gpsQw4K7hOtWSp4nv5m3HuQIb", "OqAPHmMTavS8hXlVTHQezFM5zI3eCIntQSaUfipd2TFf3vFe2H")
	auth.set_access_token("117104019-oALkIdHmwvQgjPs42R8Appwc4lmxMbsBgS9aV3Ba", "gvFk4JYfNKSpqb2nQepypFHHsjrpIhghOJYQtTu7v5buf")
	api = tweepy.API(auth, wait_on_rate_limit=True, parser=tweepy.parsers.JSONParser())
	results = api.search(q=query, count=25, since="2020-10-01", tweet_mode='extended')
	if (results['statuses']):
		resultList = processResults(results)
		if (resultList):
			resultDataFrame = pd.DataFrame(resultList)
			resultDataFrame.rename(columns={0: 'tweetId', 1: 'url', 2:'screenName', 3:'Hashtag'}, inplace=True)
			resultValue = resultDataFrame['Hashtag'].value_counts()[:5].index.tolist()
			strOutput = ', '.join(resultValue)
	return strOutput

def processResults(results):
	resultList = []
	for tweet in results['statuses']:
		screenName = tweet['user']['screen_name']
		tweetId = tweet['id']
		url = "https://twitter.com/"+ screenName +"/status/" + "%s" %tweetId
		if(tweet['retweeted']):
			fullText = tweet['retweeted_status']['full_text']
		else:
			fullText = tweet['full_text']
		for word in fullText.split():
			if (word[0] == '#'):
				tempList = []
				tempList.append(tweetId)
				tempList.append(url)
				tempList.append(screenName)
				word1 = re.sub(r'[^\w\s]','',word)
				tempList.append("#"+word1)
				#hashtagList = word
				resultList.append(tempList)
	return resultList
