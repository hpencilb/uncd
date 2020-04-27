# uncd

This is a CLI tool to find some information about a Unicode or a Block of Unicode.

## Usage

- `uncd f [OPTIONS] <ARGS>` returns the detail of a Unicode of a letter

  `[OPTIONS]`:

  `-c` or `--code` default option, accepts 0 to 0xFFFFF

  `-l` or `--letter` accepts any Unicode letter

- `uncd b <ARGS>` returns a whole block of Unicode only when the block name is found(use `uncd f` first to get the block name)

