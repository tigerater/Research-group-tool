# Research-group-tool

Make sure you have the following installed:
Python (I used 3.7.6)
gitpython
git

Steps for use:
clone target repo and your blank repo to drive
open the file
replace the four vars at the top of the file according to needs:

localdirectory = blank repo
testinggiturl = blank repo url
gitdirectory = target repo
giturl = target repo url

run it

quit to quit, current to check current commit sha, "<" for past one, ">" for future one, number for type commit number you want

so if I wanted to iterate from the 60th oldest to newest commit I would type
60 (this sets the repo to the 60th oldest commit)
> (this moves it a commit newer)
> (this moves it a commit newer)

Newest commit is 0

dw about hitting limits, it wont crash

