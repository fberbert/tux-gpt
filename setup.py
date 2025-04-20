from setuptools import setup, find_packages

setup(
    name="terminal-gpt",
    version="0.1.0",
    description="An interactive terminal tool using GPT",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
)
entry_points={
    'console_scripts': [
        'terminal-gpt=terminal_gpt.terminal_gpt:main'
    ],
},
