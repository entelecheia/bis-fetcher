# Review instructions

Read by the required pre-merge reviewer (Claude Code, Codex, or Kimi Code) and human reviewers.

## Passes

- Bugs: logic errors, broken edge cases, regressions in link discovery, PDF download, text extraction, or the jsonl helpers.
- Security: requests built from untrusted input, unsafe file paths, secrets in code or logs, dependency changes without a matching `pyproject.toml` change.
- Compliance: the change matches its issue and keeps the scope it states.

## Repo focus

- The jsonl helpers (`src/bis_fetcher/jsonl.py`) keep HyFI 1.x behavior: UTF-8, `ensure_ascii=False`, one record per line, dedupe keeps the first match. `tests/bis_fetcher/test_jsonl.py` pins it; a behavior change needs a test and a stated reason.
- Fetched output is the contract: `tests/bis_fetcher/fetcher/test_bis_offline.py` compares against golden files. Changing them needs a stated reason in the PR.
- Live-site tests run only with `BIS_LIVE_TESTS=1`; do not make CI depend on the BIS site.

## What Important means here

Findings that change fetched or saved output without a test, lose records, add an undeclared dependency, or leak data. Style is a nit.

## Cap the nits

At most 5 nits per review; summarize the rest as a count.

## Do not report

- Generated paths: `uv.lock` (style only), `CHANGELOG.md`, `src/bis_fetcher/_version.py`.
- What CI already enforces: `uv lock --locked`, ruff check and format, pytest.
