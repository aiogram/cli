# aiogram-cli (PoC)

Command line interface for developers

Works only with [aiogram](https://github.com/aiogram/aiogram) 3.0+

Here is only bootstrap for CLI interface with extensions based on [pkg_resources](https://setuptools.readthedocs.io/en/latest/pkg_resources.html)

## Installation

### From PyPi
`pip install aiogram-cli` or `pip install aiogram[cli]`

## Usage

Just run in terminal `aiogram` and see what you can do with it.

## Example

[![asciicast](https://asciinema.org/a/5tg0CV7ogvuqQz8ZmHP9CBPjl.svg)](https://asciinema.org/a/5tg0CV7ogvuqQz8ZmHP9CBPjl)

## Writing extensions

Any **aiogram-cli** extension package should provide an entry point like this:
```
[aiogram_cli.plugins]
my_extension = my_package.module:my_command
```

Or with poetry like this:
```toml
[tool.poetry.plugins."aiogram_cli.plugins"]
"builtin-about" = "aiogram_cli.about:command_about"
"builtin-plugins" = "aiogram_cli.plugins:command_plugins"
```
