#!/usr/bin/env python3

import sys
import os
import subprocess
import re

MISSING_PREREQUISITES = "zsh-llm-suggestions missing prerequisites:"

def main():

  if subprocess.run(['gh', 'version'], text=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL).returncode != 0:
    print(f'echo "{MISSING_PREREQUISITES} Install GitHub CLI first by following https://github.com/cli/cli#installation"')
    return 0
  
  buffer = sys.stdin.read()
  process = subprocess.Popen(['gh', 'copilot', 'suggest', '-t', 'shell', buffer], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  
  output, error = process.communicate()

  # Remove escape sequences
  ansi_escape = re.compile(r'''
      \x1B  # ESC
      (?:   # 7-bit C1 Fe (except CSI)
          [@-Z\\-_]
      |     # or [ for CSI, followed by a control sequence
          \[
          [0-?]*  # Parameter bytes
          [ -/]*  # Intermediate bytes
          [@-~]   # Final byte
      )
  ''', re.VERBOSE)
  output = ansi_escape.sub('', output)

  if "Error: No valid OAuth token detected" in error:
    print(f"echo '{MISSING_PREREQUISITES} Authenticate with github first:' && \gh auth login --web -h github.com")
    return 0

  if 'unknown command "copilot" for "gh"' in error:
    if "You are not logged into any GitHub hosts" in subprocess.run(['gh', 'auth', 'status'], text=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL).stderr:
      print(f"echo '{MISSING_PREREQUISITES} Authenticate with github first:' && \gh auth login --web -h github.com")
      return 0
    print(f"echo '{MISSING_PREREQUISITES} Install github copilot extension first:' && \gh extension install github/gh-copilot")
    return 0

  if "Suggestion not readily available. Please revise for better results." in output:
    print("No answer from GitHub CoPilot.")
    return 0

  # Strip unnecessary output
  idx = output.find('# Suggestion:')
  if idx != -1:
    output = output[idx + len('# Suggestion:'):]
  idx = output.find("\x0a\x0a\x1b\x37\x1b\x38\x0a\x3f")
  if idx != -1:
    output = output[:idx]
  
  output = output.strip()
  
  # Something went wrong
  if output == "" and error != "":
    print("ERROR: " + error)
    return 0

  print(output)

  return 0


if __name__ == '__main__':
  sys.exit(main())
