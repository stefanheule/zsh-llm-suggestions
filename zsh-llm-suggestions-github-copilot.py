#!/usr/bin/env python3

import sys
import os
import subprocess
import re

MISSING_PREREQUISITES = "zsh-llm-suggestions missing prerequisites:"

def main():

  mode = sys.argv[1]
  if mode != 'generate' and mode != 'explain':
    print("ERROR: something went wrong in zsh-llm-suggestions, please report a bug. Got unknown mode: " + mode)
    return

  try:
    subprocess.run(['gh', 'version'], text=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
  except:
    print(f'echo "{MISSING_PREREQUISITES} Install GitHub CLI first by following https://github.com/cli/cli#installation"')
    return
  
  buffer = sys.stdin.read()
  env = None
  if mode == 'explain':
    env = os.environ.copy()
    env["CLICOLOR_FORCE"] = "1"
    command = ['gh', 'copilot', 'explain', buffer]
  else:
    command = ['gh', 'copilot', 'suggest', '-t', 'shell', buffer]
  process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
  
  output, error = process.communicate()

  if "Error: No valid OAuth token detected" in error:
    print(f"echo '{MISSING_PREREQUISITES} Authenticate with github first:' && \gh auth login --web -h github.com")
    return

  if 'unknown command "copilot" for "gh"' in error:
    if "You are not logged into any GitHub hosts" in subprocess.run(['gh', 'auth', 'status'], text=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL).stderr:
      print(f"echo '{MISSING_PREREQUISITES} Authenticate with github first:' && \gh auth login --web -h github.com")
      return
    print(f"echo '{MISSING_PREREQUISITES} Install github copilot extension first:' && \gh extension install github/gh-copilot")
    return

  if "Suggestion not readily available. Please revise for better results." in output:
    print("No answer from GitHub CoPilot.")
    return

  # Strip unnecessary output
  if mode == 'generate':
    needle = '# Suggestion:'
    idx = output.find(needle)
    if idx != -1:
      output = output[idx + len(needle):]
    idx = output.find("\x0a\x0a\x1b\x37\x1b\x5b\x3f")
    if idx != -1:
      output = output[:idx]
  
  if mode == 'explain':
    needle = "\x45\x78\x70\x6c\x61\x6e\x61\x74\x69\x6f\x6e\x1b\x5b\x30\x6d\x1b\x5b\x31\x6d\x3a"
    idx = output.find(needle)
    if idx != -1:
      output = output[idx + len(needle):]
    output = re.sub(r"^\x1b\x5b\x30\x6d( +\n)*", "\x1b\x5b\x30\x6d", output)
  
  output = output.strip()

  # Something went wrong
  if output == "" and error != "":
    print("ERROR: " + error)
    return

  print(output)
  # hex_output = ' '.join(hex(ord(c)) for c in output)
  # print(hex_output)

  return

if __name__ == '__main__':
  main()
