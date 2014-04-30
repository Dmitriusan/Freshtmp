#!/usr/bin/env python
import os, subprocess

work_dir = "/tmp"
backup_repo_dir = "/media/hotspot/backups/freshtmp_repo"
git_dir = os.path.join(backup_repo_dir, ".git")


#####

GIT_INIT_CMD = ["git", "init"]
GIT_CLEAN_CMD = ["git", "clean", "-df"]

git_env = os.environ.copy()
git_env["GIT_DIR"] = backup_repo_dir

#####


def prepare_repo_dir():
  if os.path.isfile(backup_repo_dir):
    # Stupid situation
    raise IOError("Repo dir {0} is a file?!!".format(backup_repo_dir))
  if not os.path.isdir(backup_repo_dir):
    print "Creating repo dir {0}...".format(backup_repo_dir)
    os.makedirs(backup_repo_dir)
  if not os.path.isdir(git_dir):
    print "Initialising new git repository at {0}".format(backup_repo_dir)
    subprocess.check_call(GIT_INIT_CMD, env=git_env)
  subprocess.check_call(GIT_CLEAN_CMD, env=git_env)


def main():
  os.chdir("/tmp/a1")
  prepare_repo_dir()

if __name__ == "__main__":
  main()