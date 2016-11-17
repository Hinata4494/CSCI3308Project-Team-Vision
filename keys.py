from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#consumer key, secret and access key and token

ckey = "PflO21BLCT42HrCOQwbpKB3eN"
csecret = "ntXQRqvIuP6whGA5sMtzE7cXDE4lrtF5UomFOB5gkx8LqnvwQS"
atoken = "791739710582304768-d3ik2cTyqJKKVRbND3DRJ2QNIr9f8EC"
asecret = "LYC9QmArsFcpA8LjD6UQ40TZl8LX2yQXQ3kX9lYZ1ILj9"


class listener(StreamListener):

    def on_data(self, data):
        print(data)
        return(True)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#"])
