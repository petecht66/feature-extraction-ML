import re
import time
from datetime import datetime
from datetime import timedelta

url_pattern = re.compile(r'http\S+')
hashtag_pattern = re.compile(r'#\S+')
mention_pattern = re.compile(r'@\S+')
rule = re.compile(r'[^a-zA-Z0-9\s]')
# rule = re.compile(r'[^a-zA-Z\s]')
rule_all = re.compile(r'[^a-zA-Z0-9\s]')


class User():
    '''
    TwitterUser class can used to save a user
    Including userbased features
    '''
    #user_feature = []
    def __init__(self, tweet_json):
        self.user_json = tweet_json['user']
        self.id_str = self.user_json['id_str']
        self.screen_name = self.user_json['screen_name']
        self.name = self.user_json['name']
        self.created_at = self.json_date_to_stamp(self.user_json['created_at'])
        self.followers_count = self.get_followers_count()
        self.friends_count = self.get_friends_count()
        self.statuses_count = self.get_statuses_count()

    def json_date_to_stamp(self, json_date):
        '''
        exchange date from json format to timestamp(int)
        input:
            date from json
        output:
            int
        '''
        time_strpt = time.strptime(json_date, '%a %b %d %H:%M:%S +0000 %Y')
        stamp = int(time.mktime(time_strpt))
        return stamp

    def json_date_to_os(self, json_date):
        '''
        exchange date from json format to linux OS format
        input:
            date from json
        output:
            datetime
        '''
        time_strpt = time.strftime('%Y-%m-%d %H:%M:%S',
                                   time.strptime(json_date, '%a %b %d %H:%M:%S +0000 %Y'))
        os_time = datetime.strptime(str(time_strpt), '%Y-%m-%d %H:%M:%S')
        return os_time
    
    def get_screen_name(self):
        '''
        return user screen name
        '''
        return self.screen_name

    def get_followers_count(self):
        '''
        return follower count
        '''
        followers_count = self.user_json['followers_count']
        if followers_count == 0:
            followers_count = 1
        return followers_count

    def get_friends_count(self):
        '''
        return friends count
        '''
        friends_count = self.user_json['friends_count']
        if friends_count == 0:
            friends_count = 1
        return friends_count

    def get_statuses_count(self):
        '''
        return statuses count
        '''
        statuses_count = self.user_json['statuses_count']
        if statuses_count == 0:
            statuses_count = 1
        return statuses_count

    def get_user_age(self):
        '''
        Age of an account
        get age feature of an account, remember call this function all the time. Time exchange
        '''
        account_start_time = self.json_date_to_os(self.user_json['created_at'])
        now_time = datetime.now()
        account_age = (now_time-account_start_time).days
        if account_age == 0:
            account_age = 1
        return account_age

    def get_user_favourites(self):
        '''
        get user favourites count
        '''
        favourites_count = self.user_json['favourites_count']
        return favourites_count
    
    def get_user_lists(self):
        '''
        get user lists
        '''
        listed_count = self.user_json['listed_count']
        return listed_count
   
    def get_description_len(self):
        desc_text = self.user_json['description']
        # filter_text = self.text_filter(desc_text)
        if desc_text is None:
            return 0
        else:
            return len(desc_text)
    
    def text_filter(self, text):
        # filter email
        new_text = re.sub(url_pattern,' ',text)

        # filter hashtag
        #new_text = re.sub(hashtag_pattern,'',new_text)

        # filter mention
        new_text = re.sub(mention_pattern,' ',new_text)

        # . _ - link words together
        new_text = re.sub('\.|_|-', '', new_text)

        # keep
        new_text = re.sub(rule_all, ' ',new_text)
        # new_text = re.sub(rule, ' ',new_text)

        # filter \t \n
        new_text = re.sub('\t|\n|\r|\v',' ', new_text)
        # filter multi spaces
        new_text = re.sub(' +', ' ', new_text)

        # remove space of head or tail
        new_text = re.sub('^ | $','', new_text)

        return new_text

    def get_ratio_follow_friend(self):
        return self.get_followers_count()/self.get_friends_count()
    
class Tweet():
    '''
    TwitterTweet class can used to save a tweet
    '''
    def __init__(self, tweet_json):
        self.tweet_json = tweet_json
        self.user = User(tweet_json)


        self.text = tweet_json['text']
        self.timestr = self.json_date_to_stamp(tweet_json['created_at'])
        self.tid_str = self.tweet_json['id_str']

    def json_date_to_stamp(self, json_date):
        '''
        exchange date from json format to timestamp(int)
        input:
            date from json
        output:
            int
        '''
        time_strpt = time.strptime(json_date, '%a %b %d %H:%M:%S +0000 %Y')
        stamp = int(time.mktime(time_strpt))
        return stamp
    
    def get_id(self):
        return self.tid_str

    def is_en(self):
        return self.tweet_json["lang"]=="en"

    def get_create_at(self):
        '''
        get create at
        '''
        return self.timestr

    def get_retweet_count(self):
        '''
        Get retweet count, handling both original tweets and retweets.
        '''
        # If this is a retweet, extract retweet_count from the original tweet
        if 'retweeted_status' in self.tweet_json:
            return self.tweet_json['retweeted_status'].get('retweet_count', 0)
        # Otherwise, use the retweet_count of the tweet itself
        return self.tweet_json.get('retweet_count', 0)


    def get_hashtag_count(self):
        '''
        get number of hashtags
        '''
        hashtags = self.tweet_json['entities']['hashtags']
        return len(hashtags)

    def get_mention_count(self):
        '''
        get number of hashtags
        '''
        mentions = self.tweet_json['entities']['user_mentions']
        return len(mentions)

    def get_url_count(self):
        '''
        get number of urls
        '''
        urls = self.tweet_json['entities']['urls']
        return len(urls)

    def get_text_len(self):
        '''
        return chars of text
        '''
        return len(self.text)

    def get_text_digits(self):
        '''
        return number of digits in tweet
        '''
        count_digits = 0
        for ch in self.text:
            if ord(ch)>=48 and ord(ch)<=57:
                count_digits = count_digits+1
        return count_digits

    def get_retweeted_favorites_count(self):
        # Check if this tweet is a retweet and has 'retweeted_status'
        if 'retweeted_status' in self.tweet_json:
            # If so, access the 'favorite_count' from the original tweet
            return self.tweet_json['retweeted_status'].get('favorite_count', 0)
        else:
            # If not a retweet or 'favorite_count' is not present, return 0 or another default value
            return 0

    def get_average_word_length(self):
        # Determine the average number of letters in each word
        words = self.text.split()
        num_words = len(words)
        if len(words) == 0: # avoid division by zero
            return 0
        total_length = 0
        for word in words: # loop through each word
            total_length += len(word) # add the number of letters to the total
        average_length = total_length / num_words # find average length
        return average_length

    def get_capitalized_words_count(self):
        # Determine number of words that are fully capitalized
        capitalization_count = 0
        words = self.text.split()
        if len(words) == 0:
            return 0
        for word in words: # loop through each word
            if word.isupper():
                capitalization_count += 1 # increment by one if the word is fully capitalized
        return capitalization_count

    def get_repeats_count(self):
        # Determine number of words that are repeated
        words = self.text.split()
        if len(words) == 0:
            return 0
        repeat_count = 0
        seen = []
        for word in words: # loop through each word
            lowercase = word.lower() # lowercase the word
            if lowercase in seen:
                repeat_count += 1 # increment by one if word has been seen
            else:
                seen.append(lowercase) # append to array if not seen yet
        return repeat_count

    def get_capital_lowercase_ratio(self):
        # Calculate ratio of capital words to lowercase words
        capitalization_count = 0
        lowercase_count = 0
        words = self.text.split()
        if len(words) == 0:
            return 0
        for word in words: # loop through each word
            if word.isupper(): # check if word is fully capitalized
                capitalization_count += 1 # increment by one if true
            if word.islower(): # check if word is fully lowercase
                lowercase_count += 1 # increment by one if lowercase
        ratio = capitalization_count / lowercase_count # return ratio of two counts
        return ratio

    def get_tweet_features(self):
        feature_list = []
        feature_list.append(self.user.get_user_age())           # 1
        feature_list.append(self.user.get_description_len())    # 2
        feature_list.append(self.user.get_followers_count())    # 3
        feature_list.append(self.user.get_friends_count())      # 4
        feature_list.append(self.user.get_user_favourites())    # 5
        feature_list.append(self.user.get_user_lists())         # 6
        feature_list.append(self.user.get_statuses_count())     # 7
        feature_list.append(self.get_hashtag_count())           # 8
        feature_list.append(self.get_mention_count())           # 9
        feature_list.append(self.get_url_count())               # 10
        feature_list.append(self.get_text_len())                # 11
        feature_list.append(self.get_text_digits())             # 12     
        feature_list.append(self.get_retweeted_favorites_count()) #13
        feature_list.append(self.get_average_word_length())       # 14
        feature_list.append(self.get_capitalized_words_count())   # 15
        feature_list.append(self.get_repeats_count())           # 16
        feature_list.append(self.get_capital_lowercase_ratio())   # 17
        return feature_list
