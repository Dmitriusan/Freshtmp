# Freshtmp
Clean up stale patch/diff files from /tmp . 

In a process of development, I create/download/apply a lot of patch files. Having to lot of them 
is error-prone.
I usually hold this temporary staff in /tmp folder. This simple script removes old patch files making
my /tmp folder to shine like new.

This script is meant to be fetched and executed by a jenkins job running in a docker container on my working machine.
