## terminal-gpt

`terminal-gpt` is an interactive command-line tool that leverages GPT-based language models to provide intelligent, conversational assistance directly within your terminal. It enables on-the-fly code generation, debugging help, technical explanations, and more—all without leaving the command-line environment.

Designed for developers and tech enthusiasts, **terminal-gpt** streamlines workflows by integrating AI assistance seamlessly into terminal sessions, making complex tasks easier and faster to accomplish via intuitive, context-aware command-line interactions.

---

## Prerequisites

- Python 3.7+
- Pip (Python package manager)
- An OpenAI API key (see next section)

---

## Setup and Configuration

1. **Install**:
   ```bash
   git clone https://github.com/<username>/terminal-gpt.git
   cd terminal-gpt
   pip install .
   ```

2. **Get your OpenAI API key**:
   - Sign up or log in at [https://platform.openai.com](https://platform.openai.com).
   - Navigate to **API Keys** and create a new key.
   - Copy the generated key.

3. **Configure** your environment variable:
   - **Linux/macOS (bash/zsh)**:
     ```bash
     echo 'export OPENAI_API_KEY="<your_api_key>"' >> ~/.bashrc
     source ~/.bashrc
     ```
   - **Windows (PowerShell)**:
     ```powershell
     [Environment]::SetEnvironmentVariable('OPENAI_API_KEY', '<your_api_key>', 'User')
     ```

---

## Usage

### Start the interactive session:
```bash
terminal-gpt
```

### Example commands

- **Search the web for current news:**
  ```
  > Find the latest headlines about OpenAI
  ```

- **Look up technical documentation:**
  ```
  > What is the syntax for Python's list comprehensions?
  ```

- **Fetch real-time data (e.g., stock price):**
  ```
  > What's the current stock price of AAPL?
  ```

- **Summarize a web article:**
  ```
  > Summarize the top result for "machine learning trends 2025"
  ```

---

## Customization

You can configure the default model or terminal spinner settings by editing the configuration file at `~/.terminal-gpt/config.json`. Example:
```json
{
  "model": "gpt-4o-mini",
  "spinner": true
}
```

---

## Troubleshooting

- **"OPENAI_API_KEY not set"**: Ensure you exported the variable correctly and restarted your shell.
- **Slow responses**: Check your internet connection or change to a faster model in the config.

---

## License

MIT © 2025 terminal-gpt contributors


