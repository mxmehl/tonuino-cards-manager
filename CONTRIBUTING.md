<!--
SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>

SPDX-License-Identifier: GPL-3.0-only
-->

# Contributing to Tonuino Cards Manager

Thank you for your interest in this project. Contributions are welcome. Feel free to open an issue with questions or reporting ideas and bugs, or open pull requests to contribute code.

We are committed to fostering a welcoming, respectful, and harassment-free environment. Be kind!

## Development setup

Starting development is as easy as installing Python `poetry` and running `poetry install` once.

In order to run the project in the new virtual environment, run `poetry run tonuino-cards-manager`.

## Test locally

In the CI pipeline, we run a number of functional and syntactic checks to keep the project tidy and avoiding regressions. Of course, you can wait for the CI pipeline to finish and yield a result, but you may also run these checks locally, using the `Makefile`:

`make test-all`

Feel free to make that your [local pre-commit hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

Note: This as well requires `poetry` to be installed, the rest should be taken care of automatically.


## Contribution workflow

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-or-fix-name`
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository: `git push origin feature-or-fix-name`
5. Open a Pull Request on the main repository.

It is assumed that you contribute under the [main license](LICENSE) of the project and own all the rights to the content you submit.
