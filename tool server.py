
import git
from git import Git
from git import Repo
import os, shutil
import errno
import filecmp
from filecmp import dircmp
import time



#commit_start = int(input("How many commits ago do you want to start the process with"))

#below: the url and directory which you want to clone into
localdirectory = "D:\\Documents\\Group research project\\MAIN NEW\\serverfinal"
testinggiturl = "https://github.com/Research-Project-COMP0031/serverfinal.git"
#below: url and directory of the project you want to clone (for the directoy replace \ with \\)
gitdirectory = "D:\\Documents\\Group research project\\4bigprojects\\server"
giturl = "https://github.com/nextcloud/server.git"


#print(list(repo.git.log(p=True)))



#iteration not working, need to create empty folder instead of copying over, TODO
def add_diff_files(dcmp):
    for name in dcmp.right_only:
        #print(name)
        origin = dcmp.right + "\\" + name
        destfolder = dcmp.left + "\\" + name
        destination = dcmp.left
        if os.path.isfile(origin):
            shutil.copy(origin, destination)
        else:
            shutil.copytree(origin, destfolder)
        #dcmp = dircmp(localdirectory, gitdirectory) 
    for sub_dcmp in dcmp.subdirs.values():
        #print("tiger")
        add_diff_files(sub_dcmp)

def delete_diff_files(dcmp):
    for name in dcmp.left_only:
        #print(name)
        todelete = dcmp.left + "\\" + name
        if os.path.isfile(todelete):
            os.remove(todelete)
        else:
            shutil.rmtree(todelete)
    for sub_dcmp in dcmp.subdirs.values():
        delete_diff_files(sub_dcmp)

def merge_diff_files(dcmp):
    for name in dcmp.diff_files:
        #print(name)
        origin = dcmp.right + "\\" + name
        destfolder = dcmp.left + "\\" + name
        destination = dcmp.left
        if os.path.isfile(origin):
            os.remove(destfolder)
            shutil.copy(origin, destination)
        else:
            shutil.rmtree(destfolder)
            os.mkdir(destfolder)
    for sub_dcmp in dcmp.subdirs.values():
        merge_diff_files(sub_dcmp)


current_original_commit = 0

def main():
    #make sure the directory is empty
    if not os.listdir(gitdirectory):
        repo = git.Repo.clone_from(giturl, gitdirectory, branch = 'master')
        
    else:
        repo = git.Repo(gitdirectory)
        repo2 = git.Repo(localdirectory)
    originalrepo = Git(gitdirectory)
    commits = list(repo.iter_commits("master", max_count=1000000))
    tree = repo.head.commit.tree

    
    
    print(originalrepo.branch())
    
    stay = True
    current_original_commit = 0

    print("quit to quit, current to check current commit sha, < for past one, > for future one, number for type commit number you want, \"complete\" to go back to a commit and update commits until up to newest and newest feature \"100commit\"")
    iterate = 0
    iterate100 = 0
    iteratevalue = 0
    while stay:
        if iterate == 0 and iterate100 == 0:
            userinput = input("input: ")
        if userinput == "quit":
            stay = False
        elif userinput == "current":
            print(repo.head.commit)
            print(originalrepo.committed_date)
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
                print("you tried to go out of range, max range is: " + str(len(commits)))
                continue
        elif userinput == "complete" or iterate == 1:
            if iterate == 0:
                firstcommitnumber = int(input("How far back would you like to go in commits? Input: "))
                if firstcommitnumber > len(commits):
                    print("sorry, you have gone out of the scope of the project. There are " + str(len(commits)) + " total commits")
                else:
                    start_time = time.time()
                    current_original_commit = firstcommitnumber - 1
                    iterate = 1
            if iterate == 1:
                if current_original_commit > 0:
                    current_original_commit -=1
                else:
                    time_elapsed = time.time() - start_time
                    print("You have reached the final newest commit (shown below) in " + str(time_elapsed))
                    iterate = 0
        elif userinput == "100commit" or iterate100 == 1:
            if iterate100 == 0:
                firstcommitnumber = int(input("How far back would you like to go in commits? Input: "))
                if firstcommitnumber > len(commits):
                    print("sorry, you have gone out of the scope of the project. There are " + str(len(commits)) + " total commits")
                else:
                    start_time = time.time()
                    current_original_commit = firstcommitnumber - 1
                    iterate100 = 1
            if iterate100 == 1:
                if current_original_commit > 0:
                    if iteratevalue < 100:
                        current_original_commit -=1
                        iteratevalue+=1
                    else:
                        confirmation = input("type \"confirm\" to run the next 50 commits: ")
                        if confirmation == "confirm":
                            iteratevalue = 0
                            current_original_commit -=1
                else:
                    time_elapsed = time.time() - start_time
                    print("You have reached the final newest commit (shown below) in " + str(time_elapsed))
                    iterate100 = 0
            
        else:
            print("sorry, not recognised try again")
            continue
        originalrepo.checkout(commits[current_original_commit])

        

        
        

        dcmp = dircmp(localdirectory, gitdirectory) 
        #print("files and folders added:")
        add_diff_files(dcmp)
        #print("files and folders removed:")
        delete_diff_files(dcmp)
        #print("files and folders replaced:")
        merge_diff_files(dcmp)
        #print("DIFFERENCES" + str(dcmp.left_only) + str(dcmp.right_only) +str(dcmp.diff_files))
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




