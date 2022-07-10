#!/bin/python3
import git
import os
import json
import time

def get_file_directory(file):
    dir = file.split('/')[0]
    if dir in ["A", "B", "C", "D", "E"]:
        return dir

def update_version_file(file, headcommit):
    with open(file, "r+") as jsonFile:
        data = json.load(jsonFile)
        if data['commit'] != headcommit.__str__():
            data['commit'] = headcommit.__str__()
            data['date'] = time.strftime("%B %d, %Y", time.gmtime(
            headcommit.committed_date))
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
            headcommit = mygit.rev_list("HEAD", dir)
            update_version_file(f"{dir}/version.json", headcommit)
        else:
            headcommit = repo.head.commit
            update_version_file(f"version.json", headcommit)

main()
