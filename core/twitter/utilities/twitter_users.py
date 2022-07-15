import ast 
from flask import (url_for, request)

class TwitterUsersUtils:
    def get(self, tweet_user_doc):
        start = ast.literal_eval(request.form.get("start", "0"))
        limit = ast.literal_eval(request.form.get("length", "10"))
        
        initial_pipeline = self.__get_initial_pipeline()
        filtered_pipeline = self.__get_filtered_query(initial_pipeline)
        ordered_pipeline = self.__get_ordered_pipeline(filtered_pipeline)
        
        page = int(start/limit) + 1
        offset = (page - 1) * limit

        db_result = self.__get_db_result(ordered_pipeline, tweet_user_doc, offset, limit)
        user_data = self.__format_paginated_query(db_result)
        filtered_record_details = list(tweet_user_doc.aggregate(
            filtered_pipeline + [
                {
                    '$facet': {
                        'totalCount': [
                            {
                                '$count': 'count'
                            }
                        ]
                    }
                }
            ]))[0]['totalCount']
        return {
            "data": user_data,
            "recordsTotal": tweet_user_doc.count(),
            "recordsFiltered": filtered_record_details[0]['count'] if filtered_record_details else 0, 
        }	

    def __get_initial_pipeline(self):
        return  [
                    { 
                        "$addFields": { 
                            "userObjId": { "$toObjectId": "$_id" } } 
                    },
                    {
                        '$lookup': {
                            'from': "tweet",
                            'localField': "userObjId",
                            'foreignField': "user",
                            'as': "related_tweets"
                        }
                    },
                    {
                        "$addFields": {
                            "tweet_count": {
                                "$size": "$related_tweets"
                            }
                        } 
                    }
                ]
    def __get_db_result(self, ordered_pipeline, tweet_user_doc, offset, limit):
        final_pipeline = ordered_pipeline + [
            {
                "$project": {
                    'user_id': 1,
                    'name': 1,
                    'verified': 1,
                    'followers_count': 1,
                    'friends_count': 1,
                    'statuses_count': 1,
                    'favourites_count': 1,
                    'tweet_count': 1,
                }
            },
            {
                '$skip': offset,
            },
            {
                '$limit': limit,
            }
        ]
        return tweet_user_doc.aggregate(final_pipeline)

    def __get_filtered_query(self, initial_pipeline):
        searched_value = request.form.get("search[value]", "")
        if searched_value.strip():
            return initial_pipeline + [
                {
                    "$match": {
                        "$or": [
                            {
                                'name': searched_value,
                            },
                            {
                                '$expr': {
                                    '$eq': [
                                        {
                                            '$toString': "$user_id"
                                        },
                                        searched_value,
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        return initial_pipeline

    def __get_ordered_pipeline(self, filtered_pipeline):
        column_index    = request.form.get("order[0][column]")
        order_dir       = request.form.get("order[0][dir]", "")
        column_name     = request.form.get(f"columns[{column_index}][data]")
        if column_name:
            return filtered_pipeline + [
                {
                    "$sort": {
                        column_name: 1 if order_dir == "asc" else -1,
                    }
                }
            ]
        return filtered_pipeline

    def __format_paginated_query(self, db_result):
        user_data = [] 
        for user_details in db_result:
            user_data.append({
                'user_id': user_details['user_id'],
                'name': user_details['name'],
                'verified': user_details['verified'],
                'tweet_count': user_details['tweet_count'],
                'followers_count': user_details['followers_count'],
                'friends_count': user_details['friends_count'],
                'statuses_count': user_details['statuses_count'],
                'favourites_count': user_details['favourites_count'],
                "action": f'''<a class="dropdown-item" href="{url_for('twitter.tweets')}">
                        <i class="fa fa-twitter" aria-hidden="true"></i>    
                    </a>''',
            })
        return user_data