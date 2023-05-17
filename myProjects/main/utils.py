import requests 
from flask import current_app
import os
import json

def get_leetcode():
    leetcode_data = requests.get('https://leetcode-stats-api.herokuapp.com/Th3BossC').json()
    return leetcode_data 



def dict_to_file(leetcode):
    leetcode['easyLen'] = "%.2f" % (leetcode['easySolved']/leetcode['totalEasy'] * 100)
    leetcode['mediumLen'] = "%.2f" % (leetcode['mediumSolved']/leetcode['totalMedium'] * 100)
    leetcode['hardLen'] = "%.2f" % (leetcode['hardSolved']/leetcode['totalHard'] * 100)
    
    del leetcode['status']
    del leetcode['message']
    del leetcode['acceptanceRate']
    del leetcode['ranking']
    del leetcode['contributionPoints']
    del leetcode['reputation']
    del leetcode['submissionCalendar']
    with open(os.path.join(current_app.root_path + '/static/leetcode.json'), 'w') as outfile:
        json.dump(leetcode, outfile)


# "status": "success",
#   "message": "retrieved",
#   "totalSolved": 360,
#   "totalQuestions": 1735,
#   "easySolved": 146,
#   "totalEasy": 458,
#   "mediumSolved": 196,
#   "totalMedium": 904,
#   "hardSolved": 21,
#   "totalHard": 368,
#   "acceptanceRate": 50.92,
#   "ranking": 47657,
#   "contributionPoints": 2534,
#   "reputation": 1,
#   "submissionCalendar": {}
