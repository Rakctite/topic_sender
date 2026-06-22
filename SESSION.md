# Session Notes

## Current Context
- Project path: `C:\Users\mingyu.shin\docker\0_services\topic_sender`.
- Integrated workspace root: `C:\Users\mingyu.shin\docker`.
- This service responds to MQTT topic/sensor-code requests using PostgreSQL mapping data.
- When starting Codex here, also read the root `C:\Users\mingyu.shin\docker\SESSION.md` for integrated service context.

## Repositories
- Git remote: `https://github.com/Rakctite/topic_sender.git`.
- Main branch: `main`.
- Latest pushed commit: `1c34a2a Release topic sender 2.0.1`.

## Session Discipline
- When Codex changes files in this project, update this `SESSION.md` in the same work session.
- Record the purpose of the change, key files touched, verification result, commit hash, and any remaining TODO.
- If work is done from another terminal, branch, or worktree, sync this file after the commit is merged or pushed to `main`.
- If the change affects integrated deployment behavior, also update the root `C:\Users\mingyu.shin\docker\SESSION.md`.

## Docker Image
- Last recorded integrated image: `203.228.107.184:5000/btx/ctm_topic_sender:2.0.1`.
- Compose default tag: `TOPIC_SENDER_IMAGE_TAG:-2.0.1`.

## Latest State
- 2026-06-18: Repository was initialized locally and pushed to GitHub.
- 2026-06-18: Working tree was clean and tracking `origin/main`.
- 2026-06-18: Service uses image name `btx/ctm_topic_sender` in compose contexts.

## Open TODO
- Decide whether to keep both `Dockerfile_1.0.0` and `Dockerfile_2.0.0`.
- Consider fixing garbled Korean comments/log messages if source encoding can be confirmed safely.
- Confirm whether credentials currently present as defaults in `app.py` and compose files should be moved to environment-only values.

## Work Log

### 2026-06-22
- Changed request-topic responses from a trailing empty seventh segment to an eighth topic level using `sensor_type` from `core.v_topic_mapping`.
- Touched `app.py`, `docker-compose.yml`, `Dockerfile_2.0.0`, and added unit tests under `tests/`.
- Verified locally with `python -m unittest discover` and `python -m compileall app.py`.
- Built and pushed `203.228.107.184:5000/btx/ctm_topic_sender:2.0.1`; registry digest `sha256:8079435ed24eefd3444fcfd1e501cea769386bc840bfee7895fa87a72e7528d3`.
- Deployed local container `ctm_topic_sender` with image `203.228.107.184:5000/btx/ctm_topic_sender:2.0.1` on network `edge-hmi-test_default`.
- Verified runtime logs show `Topic Sender Ver 2.0.1`, DB mapping load of 11 devices, and MQTT broker subscription.
- Verified MQTT request/response with MAC `OPC:PH01`; response topic payload was `3120/PH/CTM/LO001/PH01/-/OPC:PLC`.
- Note: `docker compose up -d --no-deps ctm_topic_sender` failed because local `.env` is missing; deployment was performed with `docker run` using the existing container environment values.
- Commit hash: `1c34a2a`.

### 2026-06-18
- Initialized Git repository on branch `main`.
- Added remote `https://github.com/Rakctite/topic_sender.git`.
- Added `.gitignore` for Python caches and local env folders/files.
- Verified syntax with `python -m compileall app.py`.
- Committed and pushed `7bab7cc Initial topic sender service`.
- Recorded Docker image version from compose.
