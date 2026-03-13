# Contributing to URN Randomization Flask

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## How to Report Bugs

If you find a bug, please open a GitHub issue and include:

- A clear and descriptive title.
- Steps to reproduce the problem.
- Expected behavior vs. actual behavior.
- Your environment details (OS, Python version, browser if applicable).
- Any relevant logs or screenshots.

## How to Submit Changes

1. **Fork** the repository.
2. Create a **feature branch** from `master`:
   ```bash
   git checkout -b feature/my-change
   ```
3. Make your changes and commit them with a clear message.
4. Push your branch to your fork:
   ```bash
   git push origin feature/my-change
   ```
5. Open a **Pull Request** against `master` and describe your changes.

## Code Style

This project uses the following tools to enforce consistent code style:

- **[black](https://github.com/psf/black)** for code formatting.
- **[isort](https://pycqa.github.io/isort/)** for import sorting.
- **[flake8](https://flake8.pycqa.org/)** for linting.

Please run these tools before submitting a pull request:

```bash
black urand/ urand_gui/ plugins/ tests/
isort urand/ urand_gui/ plugins/ tests/
flake8 urand/ urand_gui/ plugins/ tests/
```

## Running Tests

Run the test suite with pytest:

```bash
pytest tests/
```
