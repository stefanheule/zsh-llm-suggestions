# LLM-based command suggestions for zsh

![Demo of zsh-llm-suggestions](https://github.com/stefanheule/zsh-llm-suggestions/blob/master/zsh-llm-suggestions.gif?raw=true)

`zsh` commands can be difficult to remember, but LLMs are great at turning
human descriptions of what to do into a command. Enter `zsh-llm-suggestions`:
You describe what you would like to do directly in your prompt, you hit a
keyboard shortcut of your choosing, and the LLM replaces your request with
the command.

Similarly, if you have a command that you don't understand, `zsh-llm-suggestions`
can query an LLM for you to explain that command. You can combine these, by
first generating a command from a human description, and then asking the LLM
to explain the command.

## Installation

Clone the repository:

```
git clone git@github.com:stefanheule/zsh-llm-suggestions.git ~/zsh/zsh-llm-suggestions
```

Source the script and configure the hotkey in `.zshrc`:

```
source ~/zsh/zsh-llm-suggestions/zsh-llm-suggestions.zsh
bindkey '^o' zsh_llm_suggestions_openai # Ctrl + O to have OpenAI suggest a command given a English description
bindkey '^[^o' zsh_llm_suggestions_openai_explain # Ctrl + alt + O to have OpenAI explain a command
bindkey '^p' zsh_llm_suggestions_github_copilot # Ctrl + P to have GitHub Copilot suggest a command given a English description
bindkey '^[^p' zsh_llm_suggestions_github_copilot_explain # Ctrl + alt + P to have GitHub Copilot explain a command
```

Make sure `python3` is installed.

Both LLMs require a bit of configuration. Either follow the rest of the instructions
here, or just enter something on the prompt (because an empty prompt won't run the
LLM) and hit your configured keyboard shortcut. Instead of answering the prompt, it will
tell you how to finish the setup.

For `zsh_llm_suggestions_openai` (OpenAI-based suggestions):
- Set the `OPENAI_API_KEY` environment variable to your API key. You can get it
  from [https://platform.openai.com/api-keys](platform.openai.com/api-keys). Note
  that every suggestion costs a small amount of money, you are solely responsible for
  these charges.
  ```
  export OPENAI_API_KEY="..."
  ```
- Install the Python 3 package `openai`:
  ```
  pip3 install openai
  ```
- Optional, if you want syntax highlighting for the command explanation, install pygments
  ```
  pip3 install pygments
  ```

For `zsh_llm_suggestions_github_copilot` (GitHub Copilot suggestions):
- Install GitHub CLI: Follow [https://github.com/cli/cli#installation](github.com/cli/cli#installation).
- Authenticate with GitHub:
  ```
  /usr/bin/gh auth login --web -h github.com
  ```
- Install GitHub Copilot extension:
  ```
  /usr/bin/gh extension install github/gh-copilot
  ```

## Usage

### LLM suggested commands

Type out what you'd like to do in English, then hit ctrl+P or ctrl+O (or whatever hotkey)
you configured. `zsh-llm-suggestions` will then query OpenAI or GitHub Copilot, and replace
the query with the command suggested.

If you don't like the suggestion and think the LLM can do better, just hit ctrl+P/O again,
and a new suggestion will be fetched.

### Explain commands using LLM

If you typed a command (or maybe the LLM generated one) that you don't understand, hit
ctrl+alt+O to have OpenAI explain the command in English, or hit ctrl+alt+P to have
GitHub Copilot explain it.

## Warning

There are some risks using `zsh-llm-suggestions`:
1. LLMs can suggest bad commands, it is up to you to make sure you
   are okay executing the commands.
2. The supported LLMs are not free, so you might incur a cost when using `zsh-llm-suggestions`.

## Supported LLMs

Right now, two LLMs are supported:
1. GitHub Copilot (via GitHub CLI). Requires a GitHub Copilot subscription.
2. OpenAI. Requires an OpenAI API key. Currently uses `gpt-4-1106-preview`.

## Prompt ideas

Small source of inspiration:
- who contributed the most to this git repository?
- tell me a joke
- delete the git submodule called modules/zsh-async
