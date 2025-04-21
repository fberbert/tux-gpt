#!/usr/bin/env python3
import os
import sys
import json
import atexit
try:
    import readline
except ImportError:
    readline = None
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

 # Paths for configuration
CONFIG_DIR = os.path.expanduser('~/.terminal-gpt')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')
# Paths for chat history and input history
HISTORY_PATH = os.path.join(CONFIG_DIR, 'history.json')
INPUT_HISTORY_PATH = os.path.join(CONFIG_DIR, 'input_history')
# maximum number of messages to keep in memory and persist
MAX_HISTORY = 20



def write_default_config():
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    default_config = {"model": "gpt-4.1-mini"}
    with open(CONFIG_PATH, 'w') as f:
        json.dump(default_config, f, indent=2)


def load_config():
    if not os.path.exists(CONFIG_PATH):
        write_default_config()
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: failed to load config {CONFIG_PATH}: {e}")
        return {"model": "gpt-4.1-mini"}
    
def load_history():
    """Load persisted conversation history (last MAX_HISTORY messages)."""
    if not os.path.exists(HISTORY_PATH):
        return []
    try:
        with open(HISTORY_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: failed to load history {HISTORY_PATH}: {e}")
        return []

def save_history(history):
    """Persist conversation history, keeping only last MAX_HISTORY messages."""
    try:
        with open(HISTORY_PATH, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Warning: failed to save history {HISTORY_PATH}: {e}")


def main():
    console = Console()
    # ensure config directory exists
    os.makedirs(CONFIG_DIR, exist_ok=True)
    # setup input line history if available
    if readline:
        try:
            readline.read_history_file(INPUT_HISTORY_PATH)
        except Exception:
            pass
        atexit.register(lambda: readline.write_history_file(INPUT_HISTORY_PATH))

    welcome_message = """\

                     Welcome to the terminal-gpt!
          This is a terminal-based interactive tool using GPT.
      Please, visit us at https://github.com/fberbert/terminal-gpt
                        Type 'exit' to quit.
    """

    console.print(f"[bold blue]{welcome_message}[/bold blue]", justify="left")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]Please set your OPENAI_API_KEY environment variable.[/red]")
        sys.exit(1)

    config = load_config()
    model = config.get("model", "gpt-4.1-mini")

    client = OpenAI(api_key=api_key)
    console = Console()

    # System prompt: allow Markdown output
    system_msg = {
        "role": "system",
        "content": (
            "You are a virtual assistant that can search the web. "
            "Always search the web when user asks for something data related. "
            "For example: 'What is the weather today?' or 'Which date is today?'. "
            "You are running in a Linux terminal. "
            "Return responses formatted in Markdown so they can be rendered in the terminal using rich."
        )
    }
    # load persisted conversation (last MAX_HISTORY messages)
    persisted = load_history()

    # main REPL loop
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            console.print("\nExiting.")
            break
        # handle exit commands without sending to model
        if user_input.strip().lower() in ("exit", "quit"):
            console.print("Exiting.")
            break
        # build messages for API: system + last persisted + current user
        call_history = [system_msg] + persisted + [{"role": "user", "content": user_input}]
        # call API with rich spinner/status
        try:
            with console.status("[bold green]", spinner="dots"):
                resp = client.responses.create(
                    model=model,
                    input=call_history,
                    tools=[{"type": "web_search_preview"}]
                )
        except Exception as e:
            console.print(f"[red]Error calling OpenAI API: {e}[/red]")
            continue
        # render and persist response
        answer = resp.output_text.strip()
        console.print()
        console.print(Markdown(answer))
        console.print()
        # update persisted history and save
        persisted.append({"role": "user", "content": user_input})
        persisted.append({"role": "assistant", "content": answer})
        # keep only last MAX_HISTORY messages
        if len(persisted) > MAX_HISTORY:
            persisted = persisted[-MAX_HISTORY:]
        save_history(persisted)


if __name__ == "__main__":
    main()

