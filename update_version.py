#!/bin/python3
import git
import os
import json
import time

root_dir = os.getcwd()
repo = git.Repo(root_dir)
mygit = repo.git

# print(mygit.status())
changedFiles = [ item.a_path for item in repo.index.diff(None) ]
print(changedFiles)
print(repo.untracked_files)

directories = ["A", "B", "C", "D", "E"]
print(mygit.status("A"))
headcommit = repo.head.commit

with open("version.json", "r+") as jsonFile:
    data = json.load(jsonFile)
    data['commit'] = headcommit.__str__()
    data['date'] = time.strftime("%B %d, %Y", time.gmtime(headcommit.committed_date))
    data['version'] += 1
    jsonFile.seek(0)
    json.dump(data, jsonFile)
    jsonFile.truncate()
