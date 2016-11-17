from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from HTMLParser import HTMLParser
import time


#consumer key, secret and access secret and token

ckey = "PflO21BLCT42HrCOQwbpKB3eN"
csecret = "ntXQRqvIuP6whGA5sMtzE7cXDE4lrtF5UomFOB5gkx8LqnvwQS"
atoken = "791739710582304768-d3ik2cTyqJKKVRbND3DRJ2QNIr9f8EC"
asecret = "LYC9QmArsFcpA8LjD6UQ40TZl8LX2yQXQ3kX9lYZ1ILj9"

#a rough bounding box of USA, Hawaii, and Alaska
UNITED_STATES = [-125.9,24.1,-66.3,49.3]
HAWAII = [-161.03,18.27,-154.06,22.86]
ALASKA = [-168.09,52.02,-140.8,71.76]

dict ={
		'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09', 
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
}

class listener(StreamListener):
	
	
	
	
	def on_data(self, data):
		tweet = json.loads(HTMLParser().unescape(data))
		try:
			hashtags = str([hashtag['text'] for hashtag in tweet['entities']['hashtags']])
			
#			coordinates is NULL if disabled. An if statement is needed to use the data when available		
			if tweet['coordinates']:
				geo_location = str(tweet['coordinates']['coordinates'])
				geo_location_long = geo_location.split("[")[1].split(",")[0]
				geo_location_lat = geo_location.split(", ")[1].split("]")[0]

			else:
				geo_location_lat = 'empty'
				geo_location_long = ''
				
			if(geo_location_lat != 'empty'):
				geo = 'point(' + geo_location_lat + ',' + geo_location_long + ')'
			else:
				geo = "''"
			
			date = str(tweet['created_at'])
			date_year = date[26:30]
			date_month = dict[date[4:7]]
			date_day = date[8:10]
			full_date = str(date_year + '-' + date_month + '-' + date_day)
			 
			print "INSERT INTO LargeTable VALUES" + '(' + '"' + hashtags + '",' + "''"+ ', ' + geo + ', ' + full_date + ');'
			
			return True
			
#		this exception is for if the keyerror is there are no entities	
		except KeyError:
			pass
			
				
	def on_error(self, status_code):
		 print >> sys.stderr, 'Encountered error with status code:', status_code
		 return True # Don't kill the stream

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream

		
#Necessary authentication from twitter app to use API	
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations = UNITED_STATES+HAWAII+ALASKA) #filters within bound box of USA, including Hawaii and Alaska

		
