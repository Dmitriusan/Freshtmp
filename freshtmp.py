#!/usr/bin/env python
import os, subprocess

work_dir = "/tmp"
backup_repo_dir = "/media/hotspot/backups/freshtmp_repo"
git_dir = os.path.join(backup_repo_dir, ".git")


#####

GIT_INIT_CMD = ["git", "init"]
GIT_CLEAN_CMD = ["git", "clean", "-df"]

#####


def prepare_repo_dir():
  os.chdir(backup_repo_dir)
  if os.path.isfile(backup_repo_dir):
    # Stupid situation
    raise IOError("Repo dir {0} is a file?!!".format(backup_repo_dir))
  if not os.path.isdir(backup_repo_dir):
    print "Creating repo dir {0}...".format(backup_repo_dir)
    os.makedirs(backup_repo_dir)
  if not os.path.isdir(git_dir):
    print "Initializing new git repository at {0}".format(backup_repo_dir)
    subprocess.check_call(GIT_INIT_CMD)
  subprocess.check_call(GIT_CLEAN_CMD)


def main():
  prepare_repo_dir()

if __name__ == "__main__":
  main()