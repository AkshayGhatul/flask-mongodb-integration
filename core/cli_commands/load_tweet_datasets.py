import click, os
from flask import json
from flask import current_app
from core.user.documents import Tweet, TweetUser

@current_app.cli.command("load_tweet_datasets")
@click.command()
def load_tweet_datasets():
    # Tweet.objects().all().delete()
    # TweetUser.objects().all().delete()
    # return
    filename = os.path.join(current_app.root_path, 'datasets', 'NintendoTweets.json')
    with open(filename) as test_file:
        for line in test_file:
            if line.strip() != "":
                data = json.loads(line)
                if 'id' in data:
                    user_details = data.pop('user')
                    user_id = user_details.pop('id')
                    try:
                        tweet_user = TweetUser.objects(user_id=user_id).get()
                    except:
                        tweet_user = TweetUser(**user_details, user_id=user_id)
                        tweet_user.save()
                    tweet_id = data.pop('id')
                    tweet = Tweet(**data, tweet_id=tweet_id, user=tweet_user)
                    tweet.save()
        print("Done..")