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
        if data['commit'] != commit_dict['headcommit']:
            data['commit'] = commit_dict['headcommit']
            data['date'] = commit_dict['timestamp']
            data['version'] += 1
            jsonFile.seek(0)
            json.dump(data, jsonFile)
            jsonFile.truncate()


def main():
    root_dir = os.getcwd()
    repo = git.Repo(root_dir)
    mygit = repo.git

    git_added_files = mygit.diff("--cached", "--name-only").split("\n")

    for file in git_added_files:
        dir = get_file_directory(file)
        headcommit = repo.head.commit
        timestamp = time.strftime("%B %d, %Y", time.gmtime(headcommit.committed_date))
        commit_dict = {"headcommit": headcommit.__str__(), "timestamp": timestamp}
        if dir:
            update_version_file(f"{dir}/version.json", commit_dict)
        update_version_file(f"version.json", commit_dict)


main()
