#Standard Python libs
import collections, configparser, datetime, os, pickle, sqlite3, sys

#Site-libs
import tweepy

class Twitter(object):
    def __init__(self, botName):
        self.api = self.initializeAPI()
        self.botName = botName
        self.rawTweets = []
        self.cleanTweets = []

        if os.path.exists('twitter.pickle'):
            self.loadState()
        else:
            self.lastTweetId = 0

    def initializeAPI(self):
        config = configparser.ConfigParser()
        config.read('twitter.conf')

        if 'twitter' in config:
            if config.has_option('twitter', 'consumer_key'):
                consumer_key = config['twitter']['consumer_key']
            else:
                return None
            if config.has_option('twitter', 'consumer_secret'):
                consumer_secret = config['twitter']['consumer_secret']
            else:
                return None
            if config.has_option('twitter', 'access_token'):
                access_token = config['twitter']['access_token']
            else:
                return None
            if config.has_option('twitter', 'access_token_secret'):
                access_token_secret = config['twitter']['access_token_secret']
            else:
                return None
        else:
            return None

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def loadState(self):
        with open('twitter.pickle', 'rb') as f:
            self.lastTweetId = pickle.load(f)

    def saveState(self):
        with open('twitter.pickle', 'wb') as f:
            pickle.dump(self.lastTweetId, f)

    def getTweets(self):
        tweets = {}
        newTweets = []

        if self.lastTweetId:
            self.rawTweets += self.api.mentions_timeline(count=200, since_id=self.lastTweetId)
        else:
            self.rawTweets += self.api.mentions_timeline(count=200)

        for t in self.rawTweets:
            if t.id > self.lastTweetId:
                self.lastTweetId = t.id

            if t.user.screen_name in tweets:
                #Add datetime comparison here
                if tweets[t.user.screen_name][1] < t.created_at:
                    print('Overwriting old tweet from %s' % t.user.screen_name)
                    tweets[t.user.screen_name] = [t.text, t.created_at, False]
                else:
                    continue

            tweets[t.user.screen_name] = [t.text, t.created_at, False]


        for t in tweets:
            newTweets.append([t, self.cleanTweet(tweets[t][0]), tweets[t][1], tweets[t][2]])

        #Don't lose the lastTweetId!
        self.saveState()

        print('%d total new tweets from %d user(s). [%d actual tweets]' % (len(self.rawTweets), len(tweets.keys()), len(newTweets)))

        self.cleanTweets = newTweets

        return newTweets

    def sendTweet(self, msg, picFileName=None):
        if picFileName:
            return self.api.update_with_media(picFileName, msg)
        else:
            return self.api.update_status(msg)

    def cleanTweet(self, msg):
        #Remove whitespace around msg
        msg.strip()

        #Remove the botname
        msg.replace(self.botName, '')

        #Remove hashtags
        newMsg = ''
        for i in msg.split():
            if i[:1] == '@':
                pass
            elif i[:1] == '#':
                pass
            elif i.find('://') > -1:
                pass
            else:
                newMsg = newMsg.strip() + ' ' + i

        return newMsg.strip()

    def findTop5Votes(self):
        rawVotes = {}
        top5Votes = []

        for t in self.cleanTweets:
            if t[1] in rawVotes:
                rawVotes[t[1]] += 1
            else:
                rawVotes[t[1]] = 1

        return sorted(rawVotes.items(), key=lambda t: t[1])[:5]

    def top5ToString(self, top5):
        msg = 'Top 5 Votes:\n\n'

        for t in top5:
            msg += '"' + t[0] + '" - Votes: ' + str(t[1]) + '\n\n'

        if msg == 'Top 5 Votes:\n\n':
            msg = 'No votes submitted this round...\n\n'

        return msg

    def setSuccess(self, winningTweet):
        for t in self.cleanTweets:
            if t[1] == winningTweet:
                t[3] = True

    def resetTweets(self):
        self.rawTweets = []
        self.cleanTweets = []

    def logTweets(self):
        con = None

        try:
            con = sqlite3.connect('web/tweet.db')
            cur = con.cursor()
            for t in self.cleanTweets:
                cur.execute('''SELECT * FROM Player WHERE name=?;''', (t[0],))
                data = cur.fetchone()
                if data: #User exists in database, update their info
                    data = list(data)
                    #Update success
                    if t[3]:
                        data[2] += 1
                    #Update tweet count
                    data[3] += 1

                    #Check for a newer date
                    if t[2] > datetime.datetime.strptime(data[5], '%m/%d/%Y'):
                        data[5] = t[2].strftime('%m/%d/%Y')
                        data[4] += 1

                    #Update the existing entry
                    cur.execute('''UPDATE Player SET Success=?, Total=?, TotalDay=?, LastDay=? WHERE id=?;''', (data[2], data[3], data[4], data[5], data[0]))

                else: #Add user to DB
                    success = 1 if t[3] else 0
                    cur.execute('''INSERT INTO Player (Name, Success, Total, TotalDay, LastDay) VALUES(?, ?, 1, 1, ?);''', (t[0], success, t[2].strftime('%m/%d/%Y')))

                con.commit()

        except sqlite3.Error as e:
            print("Error: {}".format(e))
        finally:
            if con:
                con.close()
