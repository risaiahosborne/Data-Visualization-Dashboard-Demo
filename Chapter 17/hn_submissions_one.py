from operator import itemgetter

import requests

# Make an API call and check the response
def get_repos_info():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url)

    return f"Status code: {r.status_code}"

def loop_ids():
        
    submission_ids = r.json()
    submission_dicts = []
    
    for submission_id in submission_ids[:30]:
        # Make a new API call for each submission
        url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
        r = requests.get(url)
        print(f"id: {submission_id}\\tstatus: {r.status_code}")
        response_dict = r.json()
        
        if not response_dict: # for articles with no comments
            continue
        #Build a dictionary for each article. 
        submission_dict = {
            'title': response_dict.get('title', "Nothing Available"),
            'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict.get('descendants', 0), #Default is 0 for articles with no comments
                        }
        submission_dicts.append(submission_dict)
        
    submission_dicts = sorted(
        submission_dicts, key = itemgetter('comments'), reverse= True
    )
    
def print_descriptions():
    for submission_dict in submission_dicts:
        print(f"\nTitle: {submission_dict['title']}")
        print(f"Discussion: {submission_dict['hn_link']}")
        print(f"Comments: {submission_dict['comments']}")
        

    
get_repos_info()
print_descriptions()