#!/bin/python3
import git
import os
import json
import time

def get_file_directory(file):
    dir = file.split('/')[0]
    if dir in ["A", "B", "C", "D", "E"]:
        return dir

def update_version_file(file, commit_dict):
    with open(file, "r+") as jsonFile:
        data = json.load(jsonFile)
        headcommit, timestamp = commit_dict['headcommit'], commit_dict['timestamp']
        if data['commit'] != headcommit:
            data['commit'] = headcommit
            data['date'] = timestamp
            data['version'] += 1
            jsonFile.seek(0)
            json.dump(data, jsonFile)
            jsonFile.truncate()

def main():
    root_dir = os.getcwd()
    repo = git.Repo(root_dir)
    mygit = repo.git

    changedFiles = [ item.a_path for item in repo.index.diff(None) ]
    untracked_files = repo.untracked_files

    modified_or_new = changedFiles + untracked_files

    for file in modified_or_new:
        dir = get_file_directory(file)
        if dir:
            headcommit = mygit.rev_list("HEAD", dir).split()[-1]
            timestamp = mygit.show("-s", "--format=%cd", "--date=format:%B %d, %Y", headcommit).split("\n")[-1]
            commit_dict = {"headcommit": headcommit, "timestamp": timestamp}
            update_version_file(f"{dir}/version.json", commit_dict)
        else:
            headcommit = repo.head.commit
            timestamp = time.strftime("%B %d, %Y", time.gmtime(headcommit.committed_date))
            commit_dict = {"headcommit": headcommit.__str__(), "timestamp": timestamp}
            update_version_file(f"version.json", commit_dict)

main()
