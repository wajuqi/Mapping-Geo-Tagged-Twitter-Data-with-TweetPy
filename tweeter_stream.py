import sys, arcpy, datetime, tweepy

# Copy and paste your 4 security keys from the identification.txt file
consumer_key = "XXX"
consumer_secret = "XXX"
access_token = "XXX"
access_token_secret = "XXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Set the path of your tweets collection table
table = r'tweets\tweets_template.dbf'


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:

            # 1. Get all of our data from tweets
            user = status.user.screen_name
            tweet = status.text
            coord_x = status.coordinates['coordinates'][0]
            coord_y = status.coordinates['coordinates'][1]
            date_utc = status.created_at
            h_m_s_utc = (str(status.created_at.hour)) + ':' + (str(status.created_at.minute)) + ':' + (
                str(status.created_at.second))
            date_est = datetime.datetime.now()
            h_m_s_est = (str(date_est.hour)) + ':' + (str(date_est.minute)) + ':' + (str(date_est.second))

            # 2. Create an Insert Cursor to insert each tweet and its attributes to our collection table.
            # Create insert cursor for table
            rows = arcpy.InsertCursor(table)
            # Add a new row to rows
            row = rows.newRow()
            # Put each attribute to its corresponding column
            row.user_name = user
            row.tweet = tweet
            row.coord_x = coord_x
            row.coord_y = coord_y
            row.date_utc = date_utc
            row.h_m_s_utc = h_m_s_utc
            row.date_est = date_est
            row.h_m_s_est = h_m_s_est
            # Insert this attribute to collection table
            rows.insertRow(row)
            # Delete cursor and row objects to remove locks on the data
            del row, rows

            # 3. Print on the screen the users and tweets
            print
            user
            print
            tweet

        except:
            # If there are no coordinates for a tweet, then pass
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

# ----------------Script execution----------------
listener = tweepy.streaming.Stream(auth, CustomStreamListener())

# Change the values to track what you have chosen to map
listener.filter(track=[' thanksgiving ', '#thanksgiving'])
