<!--
SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>

SPDX-License-Identifier: GPL-3.0-only
-->

# Contributing to Tonuino Cards Manager

Thank you for your interest in this project. Contributions are welcome. Feel free to open an issue with questions or reporting ideas and bugs, or open pull requests to contribute code.

We are committed to fostering a welcoming, respectful, and harassment-free environment. Be kind!

## Development setup

Starting development is as easy as installing Python `uv` and running `uv sync` once.

In order to run the project in the new virtual environment, run `uv run tonuino-cards-manager`.

## Test locally

In the CI pipeline, we run a number of functional and syntactic checks to keep the project tidy and avoiding regressions. Of course, you can wait for the CI pipeline to finish and yield a result, but you may also run these checks locally, using the `Makefile`:

`make test-all`

Feel free to make that your [local pre-commit hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

Note: This as well requires `uv` to be installed, the rest should be taken care of automatically.


## Licensing

It is assumed that you contribute under the [main license](LICENSE) of the project and own all the rights to the content you submit.

## Commit Messages

This project follows the [**Conventional Commits**](https://www.conventionalcommits.org/) specification for commit messages. This is critical to support proper automation of the release process and changelog generation.

## Pull Requests

When contributing to this project, please open a pull request with a clear description of the changes you have made. The **title of your pull request** should follow the conventional commit format (e.g., `feat: add new feature`, `fix: correct a bug`, etc.).

Ensure to use the **Squash and merge** option when merging your pull request.

Both the PR title and merge method are required for a proper release process (see below).

## Release Process

This project uses [release-please](https://github.com/googleapis/release-please) and its respective GitHub Action to automate the release process. This automatically creates a pull request with the version bump and changelog updates whenever a commit is pushed to the default branch. The version bump is determined by the [conventional commit messages](https://www.conventionalcommits.org/) in the commit history since the last release. Once the release pull request is merged, a new release will be published on GitHub.

The relevant configuration for release-please can be found in the `.github/workflows/release-please.yaml` file and the `release-please-config.json` file. Ensure that the branch and project names are correctly set up in the workflow file and configuration file to match your repository's structure.
