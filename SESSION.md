# Session Notes

## Current Context
- Project path: `C:\Users\mingyu.shin\docker\0_services\topic_sender`.
- Integrated workspace root: `C:\Users\mingyu.shin\docker`.
- This service responds to MQTT topic/sensor-code requests using PostgreSQL mapping data.
- When starting Codex here, also read the root `C:\Users\mingyu.shin\docker\SESSION.md` for integrated service context.

## Repositories
- Git remote: `https://github.com/Rakctite/topic_sender.git`.
- Main branch: `main`.
- Latest pushed commit: `7bab7cc Initial topic sender service`.

## Session Discipline
- When Codex changes files in this project, update this `SESSION.md` in the same work session.
- Record the purpose of the change, key files touched, verification result, commit hash, and any remaining TODO.
- If work is done from another terminal, branch, or worktree, sync this file after the commit is merged or pushed to `main`.
- If the change affects integrated deployment behavior, also update the root `C:\Users\mingyu.shin\docker\SESSION.md`.

## Docker Image
- Last recorded integrated image: `203.228.107.184:5000/btx/ctm_topic_sender:2.0.0`.
- Compose default tag: `TOPIC_SENDER_IMAGE_TAG:-2.0.0`.

## Latest State
- 2026-06-18: Repository was initialized locally and pushed to GitHub.
- 2026-06-18: Working tree was clean and tracking `origin/main`.
- 2026-06-18: Service uses image name `btx/ctm_topic_sender` in compose contexts.

## Open TODO
- Decide whether to keep both `Dockerfile_1.0.0` and `Dockerfile_2.0.0`.
- Consider fixing garbled Korean comments/log messages if source encoding can be confirmed safely.
- Confirm whether credentials currently present as defaults in `app.py` and compose files should be moved to environment-only values.

## Work Log

### 2026-06-18
- Initialized Git repository on branch `main`.
- Added remote `https://github.com/Rakctite/topic_sender.git`.
- Added `.gitignore` for Python caches and local env folders/files.
- Verified syntax with `python -m compileall app.py`.
- Committed and pushed `7bab7cc Initial topic sender service`.
- Recorded Docker image version from compose.
