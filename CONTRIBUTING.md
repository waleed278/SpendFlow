# Contributing to SpendFlow

## Development workflow

1. Start from an issue with a clear problem statement.
2. Create a focused branch from `main`.
3. Keep commits small and descriptive.
4. Add or update tests when behavior changes.
5. Update documentation for user-facing or architectural changes.
6. Open a pull request with verification notes.

## Branch naming

- `feat/<topic>`
- `fix/<topic>`
- `docs/<topic>`
- `test/<topic>`
- `chore/<topic>`

## Commit messages

Prefer concise conventional-style messages, for example:

- `feat: add manager approval endpoint`
- `fix: reject invalid expense transition`
- `docs: document local configuration`
- `test: cover authentication failure`

## Security

Never commit JWT secrets, database credentials, storage keys, access tokens, or `.env` files.
