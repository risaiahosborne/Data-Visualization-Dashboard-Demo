import requests
import plotly.express as px

# Make an API call 
url = "https://api.github.com/search/repositories"
url += "?q=language:java+sort:stars+stars:>10000" #only look for repositories with 10000 stars or more

headers = {"Accept": "application/vnd.github.v3+json"} #v3 on github update if necessary
r = requests.get(url, headers = headers)  #requests call to the api passing the url and predefined header
print(f"Status code: {r.status_code}") #200 == success

#Convert response obj to dict and process overall results
response_dict = r.json() 
print(f"Complete results: {not response_dict['incomplete_results']}")

#Process results
#print(response_dict.keys())

#print(f"Total repositores: {response_dict['total_count']}")
#print(f"Complete results: {not response_dict['incomplete_results']}")

#Explore information about the repositories and process infromation
repo_dicts = response_dict['items']
repo_links, stars, hover_texts = [], [], []
#print(f"Repositores returned: {len(repo_dicts)}")

#print("\nSelected information about each repository:")
for repo_dict in repo_dicts:
    #print(f"Name: {repo_dict['name']}")
    #print(f"Owner: {repo_dict['owner']['login']}")
    #print(f"Stars: {repo_dict['stargazers_count']}")
    #print(f"Repository: {repo_dict['html_url']}")
    #print(f"Created: {repo_dict['created_at']}")
    #print(f"Updated: {repo_dict['updated_at']}")
    #print(f"Description: {repo_dict['description']}")
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url']
    repo_link = f"<a href = '{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)
    
    stars.append(repo_dict['stargazers_count'])
    
    #Build hover texts.
    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    hover_text = f"{owner}<br />{description}"
    hover_texts.append(hover_text)

#Examine the first repository
#repo_dict = repo_dicts[0]
#print(f"\nKeys: {len(repo_dict)}")
#for key in sorted(repo_dict.keys()):
    #print(key)

#Visualization
title = "Most-Starred Java Projects on GitHub"
labels = {'x': 'Repository', 'y': 'Stars'}
fig = px.bar(
    x = repo_links, y = stars, title = title, labels = labels,
             hover_name = hover_texts,
            )

fig.update_layout(
    title_font_size = 28, xaxis_title_font_size = 20, 
    yaxis_title_font_size = 20,
                )

fig.update_traces(marker_color = 'SteelBlue', marker_opacity = 0.6)

fig.show()