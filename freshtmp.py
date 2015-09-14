#!/usr/bin/env python
import os
import subprocess
import shutil
import time
import argparse

target_dir = "/tmp"
backup_repo_dir = "/media/backups/freshtmp_repo"
patch_extensions = [".patch", ".diff", ".patch~", ".diff~"]
# How many minutes since last file modification should pass
# before it is considered stale
stale_minutes = 120
minute = 60  # seconds

# How many file movements have been performed during run
total_movements = 0

#####

GIT_INIT_CMD = ["git", "init"]
GIT_CLEAN_CMD = ["git", "clean", "-df"]
TOUCH = ["touch", "placeholder"]
GIT_TAG_CMD = ["git", "tag", "initial"]
GIT_RESET_CMD = ["git", "reset", "--hard", "initial"]
GIT_ADD_CMD = ["git", "add", "."]
GIT_COMMIT_CMD = ["git", "commit", "-a"]
#####


def prepare_repo_dir():
  if os.path.isfile(backup_repo_dir):
    # Stupid situation
    raise IOError("Repo dir {0} is a file?!!".format(backup_repo_dir))
  if not os.path.isdir(backup_repo_dir):
    print "Creating repo dir {0}".format(backup_repo_dir)
    os.makedirs(backup_repo_dir)
  os.chdir(backup_repo_dir)
  git_dir = os.path.join(backup_repo_dir, ".git")
  if not os.path.isdir(git_dir):
    print "Initializing new git repository at {0}".format(git_dir)
    subprocess.check_call(GIT_INIT_CMD)
    subprocess.check_call(TOUCH)
    subprocess.check_call(GIT_ADD_CMD)
    cmd = GIT_COMMIT_CMD + ["-m", "Initial commit"]
    subprocess.check_call(cmd)
    subprocess.check_call(GIT_TAG_CMD)
  subprocess.check_call(GIT_RESET_CMD)
  subprocess.check_call(GIT_CLEAN_CMD)


def move_files():
  print "Working..."
  for directory, dirnames, filenames in os.walk(target_dir):
    for f in filenames:
      abs_path = os.path.join(directory, f)
      try:
        ext = os.path.splitext(abs_path)
        filename = os.path.basename(abs_path)
        applicable = os.path.isfile(abs_path) and (ext[1] in patch_extensions or
                                                   '.patch.' in filename)
        if applicable and is_stale(abs_path):
          move(abs_path)
      except Exception, e:
        print "Can not move file {0} : {1}".format(abs_path, e.message)
    # try to remove directory if it is empty
    try:
      os.rmdir(directory)
    except OSError:
      # ignore
      pass


def is_stale(file_path):
  """
  Checks whether file is older then threshold
  """
  now = time.time()
  mod_time = os.stat(file_path).st_mtime
  result = mod_time < now - stale_minutes * minute
  return result


def move(file_path):
  # Extracts subpath from the working dir to a given path
  subpath = os.path.relpath(os.path.dirname(file_path),
                            os.path.abspath(target_dir))
  # new file location
  new_dir = os.path.join(backup_repo_dir, subpath)
  print "Moving {0} to {1}".format(file_path, new_dir)
  if not os.path.exists(new_dir):
    os.makedirs(new_dir)
  shutil.move(file_path, new_dir)
  global total_movements
  total_movements += 1


def commit():
  print "Committing..."
  subprocess.check_call(GIT_ADD_CMD)
  # Adding commit message
  message = time.strftime("Automatic commit on %d/%m/%Y %H:%M:%S")
  cmd = GIT_COMMIT_CMD + ["-m", message]
  subprocess.call(cmd)


def remove_dropme_directories():
  print "Removing *.dropme directories if any..."
  for current_dir, dirnames, filenames in os.walk(target_dir):
    if current_dir.endswith(".dropme") and is_stale(current_dir) and\
            check_latest_files_in_dropme_dir(current_dir):
      try:
        print("Decided to remove dir " + current_dir)
        shutil.rmtree(current_dir)
      except OSError:
        # ignore
        pass
  pass


def check_latest_files_in_dropme_dir(dropme_dir):
  """
  Iterate over files in dropme dir
  :param dropme_dir:
  :return:  True if even latest files in dir are stale
  """
  for subdir, subsubdirs, subfiles in os.walk(dropme_dir):
    for subfile in subfiles:
      abs_path = os.path.join(subdir, subfile)
      try:
        if not is_stale(abs_path):
          return False
      except Exception, e:
        print "Can not stat file {0}: {1}".format(abs_path, e.message)
  return True


def main():
  parser = argparse.ArgumentParser(
    description='This script cleans up patch files from a given dir',
    epilog='Use at your own risk'
  )
  parser.add_argument('-d', '--target-directory', metavar='D', type=str,
                      action='store', help='Target directory for cleanup')
  parser.add_argument('-b', '--backup-directory', metavar='B', type=str,
                      action='store', help='Backup directory')
  parser.add_argument('-t', '--stale-minutes', metavar='T', type=int,
                      action='store', help='How many minutes since last file '
                                           'modification should pass before it '
                                           'is considered stale')
  args = parser.parse_args()

  if args.target_directory:
    global target_dir
    target_dir = args.target_directory

  if args.backup_directory:
    global backup_repo_dir
    backup_repo_dir = args.backup_directory

  if args.stale_minutes:
    global stale_minutes
    stale_minutes = args.stale_minutes

  prepare_repo_dir()
  move_files()
  commit()
  remove_dropme_directories()
  global total_movements
  print "Totals: {0} file(s) moved".format(total_movements)


if __name__ == "__main__":
  main()
