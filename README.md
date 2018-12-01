# Freshtmp

## Stale files

Clean up stale patch/diff files from /tmp. 

In a process of development, I create/download/apply a lot of patch files. Having too lot of them at a single dir
is error-prone.
I usually hold this temporary staff in /tmp folder. This simple script removes old patch files making
my /tmp folder to shine like new. Patch files older than 2 hours (by default) 
are moved to backup dir and committed to git repo before
removal, so I'm sure I don't lose anything.

This script is meant to be fetched and executed by a Jenkins job running in a docker container on my working machine.

## *.dropme directories 

Sometimes I need a temporary workspace (e.g. to download screenshots, logs and other staff
related to jira). I don't need that stuff anymore after that, but it hangs around in my tmp folder.
Decided to add also convention to remove *.dropme directories that are older than 2 hours (by default). 
