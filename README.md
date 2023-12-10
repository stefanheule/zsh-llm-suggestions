# LLM-based command suggestions for zsh

`zsh` commands can be difficult to remember, but LLMs are great at turning
human descriptions of what to do into a command. Enter `zsh-llm-suggestions`:
You describe what you would like to do directly in your prompt, you hit a
keyboard shortcut of your choosing, and the LLM replaces your request with
the command.

## Installation

Clone the repository:

```
git clone git@github.com:stefanheule/zsh-llm-suggestions.git ~/zsh/zsh-llm-suggestions
```

Source the script and configure the hotkey in `.zshrc`:

```
source ~/zsh/zsh-llm-suggestions/zsh-llm-suggestions.zsh
bindkey '^o' zsh_llm_suggestions_openai
bindkey '^p' zsh_llm_suggestions_github_copilot
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

## Supported LLMs

Right now, two LLMs are supported:
1. GitHub Copilot (via GitHub CLI). Requires a GitHub Copilot subscription.
2. OpenAI. Requires an OpenAI API key. Currently uses `gpt-4-1106-preview`.

## Prompt ideas

Small source of inspiration:
- who contributed the most to this git repository?
- tell me a joke
- delete the git submodule called modules/foo
