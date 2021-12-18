import requests
import json

projectcache = []

def fetch_data(url):
    username = 'mlimper'
    token = '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'
    res = requests.get(url,auth=(username,token))
    #print(res.status_code)
    if res.status_code != 200:
        return []
    else:
        return res.json()


nrepo = 0
repo_teams = {}
my_repo_list = []

team_repos = {}

for npage in range(1,3):
    teams_url = 'https://api.github.com/orgs/wmo-im/teams?sort=name&page='+str(npage)
    print(teams_url)
    team_results = fetch_data(url=teams_url)
    print(len(team_results))
    for team in team_results:
        repo_list = []
        if "repositories_url" in team:
            repo_results = fetch_data(url=team["repositories_url"])
            for repo in repo_results:
                repo_list.append(repo["name"])
                if repo["name"] not in repo_teams:
                    repo_teams[repo["name"]] = [team["name"]]
                    nrepo += 1
                else:
                    repo_teams[repo["name"]].append(team["name"])
        team_repos[team["name"]] = repo_list

repo_list = []
for npage in range(1,3):
    repos_url = 'https://api.github.com/orgs/wmo-im/repos?public=true&sort=name&page='+str(npage)
    print(repos_url)
    repos_results = fetch_data(url=repos_url)
    print(len(repos_results))
    for repo in repo_results:
        teams=[]
        for team in team_repos:
            if repo["name"] in team_repos[team]:
                is_team_repo=True
                teams.append(repo["name"])
        repo_list.append({
                "name" : repo["name"],
                "description" : repo["description"],
                "html_url" : repo["html_url"],
                "teams" : teams
            })

# write result to wis_repo_data.json

with open("wis_repo_data.json","w") as myfile:
    json.dump(repo_list,myfile)

