#!/usr/bin/env python
import os, subprocess
import shutil
import time

work_dir = "/tmp"
backup_repo_dir = "/media/hotspot/backups/freshtmp_repo"
patch_extensions = [".patch", ".diff"]
# How many minutes since last file modification should pass
# before it is considered stale
stale_minutes = 120
minute = 60 # seconds

#####

GIT_INIT_CMD = ["git", "init"]
GIT_CLEAN_CMD = ["git", "clean", "-df"]
GIT_TAG_CMD = ["git", "tag", "initial"]
GIT_RESET_CMD = ["git", "reset", "--hard", "initial"]
GIT_ADD_CMD = ["git", "add", "."]
GIT_COMMIT_CMD = ["git", "commit", "-a"]
git_dir = os.path.join(backup_repo_dir, ".git")

#####


def prepare_repo_dir():
  if os.path.isfile(backup_repo_dir):
    # Stupid situation
    raise IOError("Repo dir {0} is a file?!!".format(backup_repo_dir))
  if not os.path.isdir(backup_repo_dir):
    print "Creating repo dir {0}".format(backup_repo_dir)
    os.makedirs(backup_repo_dir)
  os.chdir(backup_repo_dir)
  if not os.path.isdir(git_dir):
    print "Initializing new git repository at {0}".format(backup_repo_dir)
    subprocess.check_call(GIT_INIT_CMD)
    subprocess.check_call(GIT_TAG_CMD)
  subprocess.check_call(GIT_RESET_CMD)
  subprocess.check_call(GIT_CLEAN_CMD)

def move_files():
  print "Working..."
  for directory, dirnames, filenames in os.walk(work_dir):
    for f in filenames:
      abs_path = os.path.join(directory, f)
      if  is_applicable(abs_path):
        try:
          move(abs_path)
        except Exception, e:
          print "Can not move file {0} : {1}".format(abs_path, e.message)
    # try to remove directory if it is empty
    try:
      os.rmdir(directory)
    except OSError:
      # ignore
      pass

def is_applicable(file_path):
  '''
  Checks whether file is applicable for removal
  '''
  ext = os.path.splitext(file_path)
  now = time.time()
  mod_time = os.stat(file_path).st_mtime
  return ext[1] in patch_extensions and mod_time < now - stale_minutes * minute

def move(file_path):
  # Extracts subpath from the working dir to a given path
  subpath = os.path.relpath(os.path.dirname(file_path), os.path.abspath(work_dir))
  # new file location
  new_dir = os.path.join(backup_repo_dir, subpath)
  print "Moving {0} to {1}".format(file_path, new_dir)
  if not os.path.exists(new_dir):
    os.makedirs(new_dir)
  shutil.move(file_path, new_dir)

def commit():
  print "Committing..."
  subprocess.check_call(GIT_ADD_CMD)
  # Adding commit message
  message =time.strftime("Automatic commit on %d/%m/%Y %H:%M:%S")
  cmd = GIT_COMMIT_CMD + ["-m", message]
  subprocess.call(cmd)


def main():
  prepare_repo_dir()
  move_files()
  commit()

if __name__ == "__main__":
  main()