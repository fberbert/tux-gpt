#!/usr/bin/env python3
import os
import sys
import time
import threading
import itertools
import json
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Paths for configuration
CONFIG_DIR = os.path.expanduser('~/.terminal-gpt')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')


def spinner_task(stop_event):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\r{c}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 20 + '\r')
    sys.stdout.flush()


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


def main():
    console = Console()

    welcome_message = """\

                     Welcome to the terminal-gpt!
          This is a terminal-based interactive tool using GPT.
      Please, visit us at https://github.com/fberbert/terminal-gpt
                        Type 'exit' to quit.
    """

    console.print(f"[bold blue]{welcome_message}[/bold blue]", justify="left")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set your OPENAI_API_KEY environment variable.")
        exit(1)

    config = load_config()
    model = config.get("model", "gpt-4.1-mini")

    client = OpenAI(api_key=api_key)
    console = Console()

    # System prompt: allow Markdown output
    history = [
        {
            "role": "system",
            "content": (
                "You are a virtual assistant that can search the web. "
                "Always search the web when user asks for something data related. "
                "For example: 'What is the weather today?' or 'Which date is today?'. "
                "You are running in a Linux terminal. "
                "Return responses formatted in Markdown so they can be rendered in the terminal using rich."
            )
        }
    ]

    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            console.print("\nExiting.")
            break

        history.append({"role": "user", "content": user_input})

        # start spinner
        stop_event = threading.Event()
        spinner = threading.Thread(target=spinner_task, args=(stop_event,), daemon=True)
        spinner.start()

        # call to Responses API with web_search tool
        resp = client.responses.create(
            model=model,
            input=history,
            tools=[{"type": "web_search_preview"}]
        )

        # stop spinner
        stop_event.set()
        spinner.join()

        # get and render Markdown answer
        answer = resp.output_text.strip()
        console.print()
        console.print(Markdown(answer))
        console.print()

        history.append({"role": "assistant", "content": answer})
        if len(history) > 20:
            history = history[-20:]


if __name__ == "__main__":
    main()

