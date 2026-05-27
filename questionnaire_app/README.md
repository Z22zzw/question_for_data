# AI Supervision A/B Questionnaire

FastAPI + SQLite + static HTML/CSS/JS implementation for the AI supervision A/B questionnaire.

## Run

```powershell
cd questionnaire_app
pip install -r requirements.txt
$env:ADMIN_PASSWORD='admin123'
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Participant URL:

```text
http://127.0.0.1:8000/
```

Admin export URL:

```text
http://127.0.0.1:8000/admin.html
```

## Docker

The Docker service is intended to sit behind the `ask_cn_ai` nginx container on
the shared `ask_cn_ai_default` Docker network.

```bash
cd /data/question_for_data
./start.sh up
```

Public URLs through nginx:

```text
http://xiaozhenxing.top/question/
http://xiaozhenxing.top/question/admin
```

## Behavior

- Pretest is shared by both groups.
- The backend assigns A/B groups after pretest with balanced 50/50 allocation.
- Participants never see their group label in the UI.
- Participant IDs are assigned automatically as incremental integers.
- The participant UI supports English and Chinese switching; Excel export remains English-only.
- Sessions are server-managed with an HttpOnly SameSite cookie. The browser no longer stores or passes `session_id` in localStorage or URLs.
- On page load, the app asks `/api/session/current` for the authoritative progress state and resumes the correct task or posttest.
- The New Session / 回到首页 button calls `/api/session/reset`, clears the cookie, abandons any incomplete server session, and removes local drafts.
- Form drafts are cached in localStorage only as drafts. If the network disconnects, the current draft or pending submission is kept locally and retried after reconnect.
- Group B sees supervision cards only on Task 1 and Task 2.
- Each task is locked after submission; completed tasks cannot be read again or modified.
- After Task 6, both groups complete the same post-task questionnaire covering attitudes, supervision strategies, and trust in AI.
- Excel export includes pretest fields, group, duration-only timing fields in `HH:MM:SS`, answers, per-question scores, summary scores, and supervision-card scores.

## Screening

See `docs/auto_screening_plan.md` for recommended automatic filtering rules for exported Excel data.
