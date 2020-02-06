
import git
from git import Git
from git import Repo
import os, shutil
import errno
import filecmp
from filecmp import dircmp



#commit_start = int(input("How many commits ago do you want to start the process with"))


localdirectory = "D:\\Documents\\Group research project\\Research tool test\\newest\\researchtool"
testinggiturl = "https://github.com/tigerater/researchtool.git"
gitdirectory = "D:\\Documents\\Group research project\\Research tool test\\original\\System_and_network_team20"
giturl = "https://github.com/tigerater/System_and_network_team20.git"


#print(list(repo.git.log(p=True)))





def add_diff_files(dcmp):
    for name in dcmp.right_only:
        print(name)
        origin = dcmp.right + "\\" + name
        destfolder = dcmp.left + "\\" + name
        destination = dcmp.left
        if os.path.isfile(origin):
            shutil.copy(origin, destination)
        else:
            shutil.copytree(origin, destfolder)
    for sub_dcmp in dcmp.subdirs.values():
        add_diff_files(sub_dcmp)

def delete_diff_files(dcmp):
    for name in dcmp.left_only:
        print(name)
        todelete = dcmp.left + "\\" + name
        if os.path.isfile(todelete):
            os.remove(todelete)
        else:
            shutil.rmtree(todelete)
    for sub_dcmp in dcmp.subdirs.values():
        delete_diff_files(sub_dcmp)

def merge_diff_files(dcmp):
    for name in dcmp.diff_files:
        print(name)
        origin = dcmp.right + "\\" + name
        destfolder = dcmp.left + "\\" + name
        destination = dcmp.left
        if os.path.isfile(origin):
            os.remove(destfolder)
            shutil.copy(origin, destination)
        else:
            shutil.rmtree(destfolder)
            shutil.copytree(origin, destfolder)
    for sub_dcmp in dcmp.subdirs.values():
        add_diff_files(sub_dcmp)


current_original_commit = 0


def main():
    #make sure the directory is empty
    if not os.listdir(gitdirectory):
        repo = git.Repo.clone_from(giturl, gitdirectory, branch = 'master')
        
    else:
        repo = git.Repo(gitdirectory)
        repo2 = git.Repo(localdirectory)
    originalrepo = Git(gitdirectory)
    commits = list(repo.iter_commits("master", max_count=100))
    tree = repo.head.commit.tree

    stay = True
    current_original_commit = 0

    print("quit to quit, current to check current commit sha, < for past one, > for future one, number for type commit number you want")
    while stay:
        
        userinput = input("input: ")
        if userinput == "quit":
            stay = False
        elif userinput == "current":
            print(repo.head.commit)
            print("commits in the past = "+ str(current_original_commit))
            continue
        elif userinput == ">":
            if current_original_commit > 0:
                current_original_commit-=1
            else:
                print("you tried to go out of range, this is the newest commit")
                continue
        elif userinput == "<":
            if current_original_commit < len(commits)-1:
                current_original_commit+=1
            else:
                print("you tried to go out of range, this is the oldest commit")
                continue
        elif userinput.isdigit():
            if int(userinput) < len(commits) and int(userinput) >= 0:
                current_original_commit = int(userinput)
            else:
                print("you tried to go out of range")
                continue
        else:
            print("sorry, not recognised try again")
            continue
        originalrepo.checkout(commits[current_original_commit])
        
        

        dcmp = dircmp(localdirectory, gitdirectory) 
        print("files and folders added:")
        add_diff_files(dcmp)
        print("files and folders removed:")
        delete_diff_files(dcmp)
        print("files and folders replaced:")
        merge_diff_files(dcmp)
        print("changes complete, starting commit number: " + str(current_original_commit) + " commit(s) from the newest commit. hash: " + str(commits[current_original_commit]))
        #try:
        repo2 = Repo(localdirectory)
        #repo2.git.push(force=True)
        #repo2.index.add('.')
        #repo2.git.add(update=True)
        repo2.git.add("-A")
        repo2.index.commit(str(current_original_commit))
        #repo2.git.commit('-m', 'test commit', author='tigerater@gmail.com')
        origin = repo2.remote(name='origin')
        origin.push()
        print("commit successful, pushing")
        #except:
            #print('Some error occured while pushing the code')  

        
        
    
main()

print("quitting")







"""
for c in commits:
    # reset to previous commit
    #repo.head.reset('HEAD~1', index = True, working_tree = True)
    repo.git.reset('--hard')
    # unique SHA key
    #sha = c.name_rev.split()[0] 
    #shutil.copytree(gitdirectory, localdirectory)
    print("ok")


#commits = repo.iter_commits('--all', max_count=100, since='10.days.ago', paths=path)

#repo location on drive here
#g = Git('D:\\testing')

def git_push(repo):
    #try:
        repo.git.add(update=True)
        repo.index.commit("tiger test")
        origin = repo.remote(name='origin')
        origin.push()
    #except:
        #print('Some error occured while pushing the code')    

git_push(repo)




#tag name here
#g.checkout('tag')
"""
