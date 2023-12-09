
zsh_llm_suggestions_spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

zsh_llm_suggestions_run_query() {
  local llm="$1"
  local query="$2"
  local completion_file="$3"
  echo -n "$query" | eval $llm > $completion_file
}

zsh_llm_completion() {
  local llm="$1"
  local query=${BUFFER}

  # Empty prompt, nothing to do
  if [[ "$query" == "" ]]; then
    return
  fi

  # If the prompt is the last suggestions, just get another suggestion for the same query
  if [[ "$query" == "$ZSH_LLM_SUGGESTIONS_LAST_RESULT" ]]; then
    query=$ZSH_LLM_SUGGESTIONS_LAST_QUERY
  else
    ZSH_LLM_SUGGESTIONS_LAST_QUERY="$query"
  fi

  # Temporary file to store the result of the background process
  local completion_file="/tmp/llm-completion"
  # Run the actual query in the background (since it's long-running, and so that we can show a spinner)
  read < <( zsh_llm_suggestions_run_query $llm $query $completion_file & echo $! )
  # Get the PID of the background process
  local pid=$REPLY
  # Call the spinner function and pass the PID
  zsh_llm_suggestions_spinner $pid
  
  # Replace the current buffer with the result
  ZSH_LLM_SUGGESTIONS_LAST_RESULT=$(cat $completion_file)
  BUFFER="${ZSH_LLM_SUGGESTIONS_LAST_RESULT}"
  CURSOR=${#ZSH_LLM_SUGGESTIONS_LAST_RESULT}
}

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

zsh_llm_suggestions_openai() {
  zsh_llm_completion "$SCRIPT_DIR/zsh-llm-suggestions-openai.py"
}

zsh_llm_suggestions_github_copilot() {
  zsh_llm_completion "$SCRIPT_DIR/zsh-llm-suggestions-github-copilot.py"
}

zle -N zsh_llm_suggestions_openai
zle -N zsh_llm_suggestions_github_copilot
