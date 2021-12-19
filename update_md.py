import requests
import json

from dotenv import load_dotenv
load_dotenv()
import os

username = os.environ.get("username")
token = os.environ.get("personal-access-token")

def fetch_data(url):
    res = requests.get(url,auth=(username,token))
    #res = requests.get(url)
    if res.status_code != 200:
        print(res.status_code)
        return []
    else:
        return res.json()

team_list = []
team_children = {}
team_repos = {}

org_name = "wmo-im"
for npage in range(1,3):
    teams_url = f'https://api.github.com/orgs/{org_name}/teams?sort=name&page={str(npage)}'
    print(teams_url)
    team_results = fetch_data(url=teams_url)
    print(len(team_results))
    for team in team_results:
        repo_list = []
        member_list = []
        team_parent = None
        team_obj = { 
            "name": team["name"] , 
            "description": team["description"],
            "html_url": team["html_url"], 
            "members_url": f'https://api.github.com/orgs/{org_name}/teams/{team["slug"]}/members'
        }
        if team["parent"]:
            team_parent = {}
            team_parent["name"] = team["parent"]["name"]
            team_parent["description"] = team["parent"]["name"]
            if team_parent["name"] in team_children:
                team_children[team_parent["name"]].append( team_obj )
            else:
                team_children[team_parent["name"]] = [ team_obj ]
        if "repositories_url" in team:
            repo_results = fetch_data(url=team["repositories_url"])
            for repo in repo_results:
                repo_list.append({ 
                    "name": repo["name"],
                    "description": repo["description"],
                    "html_url": repo["html_url"]
                    })
        team_obj["repo_list"] = repo_list
        team_obj["parent"] = team_parent
        team_list.append(team_obj)
        team_repos[team["name"]] = repo_list

# write new repos/repos.md
with open("teams/index.md","w") as myfile:
    myfile.write(f'# WMO-IM GitHub Teams\n')
    myfile.write(f' \n')
    # first run over all teams and create links for all teams without parents
    #for team in team_list:
    #    team_title = str(team["name"]).replace(" ","-")
    #    if team["parent"] == None:
    #        myfile.write(f'[{team_title}](#{team_title}) \n')
    #        myfile.write(f' \n')
    # now run over team-list again and create paragraphs
    for team in team_list:
        #team_title = str(team["name"]).replace(" ","-")
        #myfile.write(f'## {team_title}\n')
        myfile.write(f'## [{team["name"]}]({team["html_url"]})\n')
        myfile.write(f' \n')
        if "description" in team and team["description"] != "":
            myfile.write(f'{team["description"]}\n')
        else: 
            myfile.write(f'Missing team description\n')
        myfile.write(f' \n')
        if len(team["repo_list"]) != 0: 
            myfile.write(f'#### GitHub repositories: \n')
            for repo in team["repo_list"]:
                myfile.write(f'* [{repo["name"]}]({repo["html_url"]}): ')
                if repo["description"] :
                    myfile.write(f'{repo["description"]}\n')
                else: 
                    myfile.write(f'Missing description\n')
            myfile.write(f' \n')
        if team["name"] in team_children:
            myfile.write(f'#### Sub-teams:\n')
            for child in team_children[team["name"]]:
                myfile.write(f'* [{child["name"]}]({child["html_url"]}): ')
                if "description" in child:
                    myfile.write(f'{child["description"]}\n')
                else: 
                    myfile.write(f'Missing team description\n')
            myfile.write(f' \n')
                #if len(team["repo_list"]) != 0: 
                #    myfile.write(f'GitHub repositories: \n')
                #    for repo in team["repo_list"]:
                #        myfile.write(f'- [{repo["name"]}]({repo["html_url"]}): ')
                #        if repo["description"] :
                #            myfile.write(f'{repo["description"]}\n')
                #        else: 
                #            myfile.write(f'Missing description\n')
                #    myfile.write(f' \n')




