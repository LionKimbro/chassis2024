# Infrastructure Index

Chassis 2024 ships with several infrastructure packages.

You are encouraged to write and publish your own infrastructure packages, but these are the infrastructure packages that ship by default with Chassis 2024, as of February 2024.

| Package Module | Title | Description |
| -------------- | ----- | ----------- |
| [chassis2024.basicrun](infra_basicrun.md) | Basic Runner | Provides a single entry point for executing your application, after all infrastructure has been loaded. |
| [chassis2024.argparse](infra_argparse.md) | Argument Parser | Instantiates an [argparse.ArgumentParser,](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser) and makes it available for argument parsing. |
| [chassis2024.basicjsonpersistence](infra_basicjsonpersistence.md) | Basic JSON Persistence | Reads from a JSON file when your program begins, and saves the data back out when the program ends. |

