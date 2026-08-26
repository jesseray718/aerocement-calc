# Contributing to aerocement-calc

## Principles

- Keep the tool offline-first and zero-dependency for core functions.
- Every change must leave the calculator runnable on Termux with stock Python.
- Prefer small, tested patches.
- Document limitations honestly.

## Process

1. Fork and clone.
2. Create a branch: `git checkout -b feature/short-description`
3. Make the change + add or update a test.
4. Run: `python3 tests/test_calc.py`
5. Commit with a clear message.
6. Open a pull request against main.

## Code style

- Pure Python 3.8+ syntax.
- Type hints encouraged.
- No new required runtime dependencies without strong η justification.
