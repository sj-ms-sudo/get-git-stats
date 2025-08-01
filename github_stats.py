import requests
import json
from collections import defaultdict
import argparse
import matplotlib.pyplot as plt
import os
def plot_graph(username,repo_count,followers,following,language_count):
    fig ,axs = plt.subplots(1,3,figsize=(12,4))
    plt.suptitle(f"Github profile summary {username}")
    bars0 = axs[0].bar("Number of repos",repo_count,color = '#5DADE2')
    axs[0].set_title("Repo count")
    axs[0].set_ylabel("Number of repos")
    for bar in bars0:
        height = bar.get_height()
        axs[0].text(bar.get_x()+bar.get_width()/2,height,str(height),ha = 'center',va = 'bottom')
    values = [followers,following]
    colors = ['#58D68D' if followers >0 else '#000000','#F5B041'if following >0 else '#000000']
    bars1 = axs[1].bar(["Followers","Following"],values,color=colors)
    axs[1].set_title("Followers and Following")
    axs[1].set_ylabel("Number of users")
    for bar in bars1:
        height = bar.get_height()
        label = str(int(height)) if height>0 else"0"
        axs[1].text(bar.get_x()+bar.get_width()/2,height+0.5,label,ha='center',va='bottom')
    labels = []
    size = []
    for k , v in language_count.items():
        labels.append(k)
        size.append(v)
    colors = plt.cm.tab20.colors[:len(labels)]
    axs[2].pie(size,labels=labels,autopct='%1.1f%%',colors=colors,startangle=170)
    axs[2].set_title("Languages used")
    axs[2].axis('equal')
    #plt.tight_layout(rect=[0,0,1,0.92])
    plt.show()
def get_details(headers , url,u_name,flag):
    url = f"{url}{u_name}"
    session = requests.Session()
    language_count = defaultdict(int)
    response = session.get(url,headers= headers)
    if response.status_code ==401:
        print(f"Error : username {u_name} not found")
        exit()
    elif not response.ok:
        print(f"Error {response.status_code} - {response.reason}")
        exit()
    followers = response.json()["followers"]
    following = response.json()["following"]
    username= response.json()["login"]
    repo = response.json()["repos_url"]
    repo_response=session.get(repo)
    repo_count = 0
    for r in repo_response.json():
        repo_count+=1
        language_count[r["language"]]+=1
    if flag:
        plot_graph(username,repo_count,followers,following,language_count)
    else:
        print(f"Username : {username}")
        print(f"Number of repos : {repo_count}")
        print(f"Followers : {followers}")
        print(f"Following : {following}")
        print(".... Languages Used ....")
        for k,v in language_count.items():
            print(f"{k} : {v} repos")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Find the details of a github account")
    parser.add_argument("-u","--username",help = "Specify the username")
    parser.add_argument("-g","--graph",action ="store_true",help = "Specify to plot graph or leave if text is needed")
    args = parser.parse_args()
    u_name = args.username
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        exit()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.github.com/users/"
    get_details(headers,url,u_name,args.graph)