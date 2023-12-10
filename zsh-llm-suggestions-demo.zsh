
# To record a demo, it's helpful to not have the LLMs give random answers, so I
# saved some real answers in the demo folder. This function will cycle through
# them for a demo.

# To record:
# - ZSH_LLM_SUGGESTIONS_DEMO_NR=0
# - ctrl+l
# - start recording
# - type: who contributed the most to this git repository?
# - ctrl+o
# - ctrl+o
# - enter
# - ctrl+l
# - type: tell me a joke
# - ctrl+o
# - ctrl+u
# - type: delete the git submodule called modules/zsh-async
# - ctrl+o
# - ctrl+o
# - ctrl+u

# I use ScreenToGif to record and add subtitles.

# Subtitles:
# - Press ctrl+p to ask an LLM for a suggestion
# - The LLM result is shown directly in the prompt
# - Great, but what exactly does this command do? Press ctrl+shift+o to ask the LLM to explain.
# - Explanation appears above the prompt. Hit enter to run the command if it looks good.
# - Several LLMs are supported, e.g. ctrl+o for OpenAI's GPT4, ctrl+p for GitHub Copilot.
# - Sometimes, LLMs give bad suggestions. Press ctrl+p again to get a new suggestion for the same query. Or press ctrl+o to switch to a different LLM.

zsh_llm_suggestions_spinner() {
    local delay=0.1
    local spinstr='|/-\'
    
    for ((i=0; i<20; i++)); do
        local temp=${spinstr#?}
        printf " [%c]" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

SCRIPT_DIR=$( cd -- "$( dirname -- "$0" )" &> /dev/null && pwd )

zsh_llm_suggestions_demo() {
  ZSH_LLM_SUGGESTIONS_DEMO_NR=$((ZSH_LLM_SUGGESTIONS_DEMO_NR+1))
  if [[ $ZSH_LLM_SUGGESTIONS_DEMO_NR -gt 5 ]]; then
    ZSH_LLM_SUGGESTIONS_DEMO_NR=1
  fi

  suggestion=$(cat $SCRIPT_DIR/demo/git-commits-explain)
    
  if [[ $ZSH_LLM_SUGGESTIONS_DEMO_NR -eq 1 ]]; then
    suggestion=$(cat $SCRIPT_DIR/demo/git-commits)
  fi
  if [[ $ZSH_LLM_SUGGESTIONS_DEMO_NR -eq 2 ]]; then
    suggestion=$(cat $SCRIPT_DIR/demo/git-commits-explain)
    zsh_llm_suggestions_spinner
    echo ""
    eval "echo -e \"$suggestion\""
    echo ""
    zle reset-prompt
    return
  fi
  if [[ $ZSH_LLM_SUGGESTIONS_DEMO_NR -eq 3 ]]; then
    suggestion=$(cat $SCRIPT_DIR/demo/joke)
  fi
  if [[ $ZSH_LLM_SUGGESTIONS_DEMO_NR -eq 4 ]]; then
    suggestion=$(cat $SCRIPT_DIR/demo/git-delete-submodule)
  fi
  if [[ $ZSH_LLM_SUGGESTIONS_DEMO_NR -eq 5 ]]; then
    suggestion=$(cat $SCRIPT_DIR/demo/git-delete-submodule-2)
  fi

  zsh_llm_suggestions_spinner
  BUFFER="$suggestion"
  CURSOR=${#BUFFER}
}

zle -N zsh_llm_suggestions_demo
