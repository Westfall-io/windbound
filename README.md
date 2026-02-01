# Windbound — Git README

This document explains how the code in this repository prepares and uploads input artifacts for Windbound using Git-based templates.

## Overview

- The primary orchestration runs in `src/main.py` and performs an input-build flow for a given `action` (template).
- Configuration values are provided by `src/env.py` and are read from environment variables with reasonable defaults.
- The flow interacts with external services: Windstorm API (for execution status and OAuth), MinIO (object storage), Git repositories (templates), and Keycloak (auth).

## High-level flow (what `src/main.py` does)

1. Create a MinIO client for object storage access.
2. Authenticate to Windstorm API to obtain an OAuth token.
3. Update thread execution status to indicate start.
4. Check for dependency on a previous thread; if present, download the dependent output from object storage.
5. Clone the template repository for the specified action.
6. Render / build template artifacts (via the template renderer).
7. Package and upload an input archive to MinIO.
8. Initialize a local repository in the attached volume for runner consumption.
9. Update thread execution status at checkpoints so orchestrators can observe progress.

## Important files

- [src/main.py](src/main.py) — main CLI entrypoint and orchestration.
- [src/env.py](src/env.py) — environment configuration constants used by the application.
- `requirements.txt` — Python dependencies (install with `pip install -r requirements.txt`).

## Configuration (env variables used in `src/env.py`)

- `VOLUME` — Path to the attached volume (defaults to `/mnt/vol`).
- `WINDRUNNERHOST` — Windrunner webhook/endpoint.
- `WINDSTORMAPIHOST` — Windstorm API base URL.
- `WINDSTORMAPICLIENT` / `WINDSTORMAPISECRET` — OAuth client credentials for Windstorm.
- `MINIOHOST` / `MINIOUSER` / `MINIOTOKEN` — MinIO endpoint and credentials.
- `MINIORETENTIONDAYS` — Default retention days for stored objects.
- `GITHOST` / `GITUSER` / `GITPASS` — Git host and credentials.
- `KEYCLOAKHOST` / `KEYCLOAKREALM` — Keycloak identity provider settings.

Set these environment variables before running the CLI or provide production values via your orchestration layer.

## Running locally

- Install dependencies:

```
python -m pip install -r requirements.txt
```

- Ensure a `VOLUME` path exists and is accessible. On Windows PowerShell example:

```
$env:VOLUME = 'C:\path\to\volume'
python -m src.main
```

Or on Linux/macOS (bash):

```
export VOLUME=/path/to/volume
python -m src.main
```

Notes:
- `src/main.py` creates a `tmp` directory and requires the configured `VOLUME` to exist; otherwise it raises an error.
- Many flows depend on external services (MinIO, Windstorm, Keycloak); running the full flow locally typically requires access to those services or suitable test doubles.

## Developer notes

- The project currently uses Fire to expose `main` as a CLI.
- Additions to documentation or docstrings should follow the module-level patterns used in `src/env.py` and `src/main.py`.
- Consider adding unit tests and a lightweight integration test harness that can stub Windstorm and MinIO.

## Next steps

- Document other modules under `src/windbinder` as they are added/implemented.
- Run linters (`flake8`/`ruff`) and type checks if desired.



