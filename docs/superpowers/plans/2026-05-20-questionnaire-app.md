# Questionnaire App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a responsive A/B questionnaire website with FastAPI, SQLite persistence, scoring, timing, and Excel export.

**Architecture:** The app is an isolated `questionnaire_app/` project. FastAPI serves JSON APIs and static HTML/CSS/JS. SQLite stores sessions, participant metadata, task responses, timestamps, scores, and supervision-card answers.

**Tech Stack:** FastAPI, SQLite, pytest, openpyxl, vanilla HTML/CSS/JS.

---

### Task 1: Backend Tests

**Files:**
- Create: `questionnaire_app/tests/test_backend.py`
- Create: `questionnaire_app/requirements.txt`

- [ ] Write tests for session creation, task submission, locked progress, scoring, and export.
- [ ] Run `pytest questionnaire_app/tests -q` and verify tests fail because app code does not exist yet.

### Task 2: Backend Implementation

**Files:**
- Create: `questionnaire_app/app/questionnaire.py`
- Create: `questionnaire_app/app/scoring.py`
- Create: `questionnaire_app/app/database.py`
- Create: `questionnaire_app/app/export.py`
- Create: `questionnaire_app/app/main.py`

- [ ] Implement questionnaire content, answer key, and score categories.
- [ ] Implement SQLite schema and data access helpers.
- [ ] Implement session lifecycle and progress locking.
- [ ] Implement scoring and Excel export.
- [ ] Run `pytest questionnaire_app/tests -q` and verify tests pass.

### Task 3: Frontend

**Files:**
- Create: `questionnaire_app/static/index.html`
- Create: `questionnaire_app/static/styles.css`
- Create: `questionnaire_app/static/app.js`
- Create: `questionnaire_app/static/admin.html`
- Create: `questionnaire_app/README.md`

- [ ] Build responsive pretest and task UI.
- [ ] Hide group label from participants.
- [ ] Render B-group supervision cards only when returned by backend.
- [ ] Prevent browser back navigation from changing completed answers by relying on backend state.
- [ ] Add admin export page using `ADMIN_PASSWORD`.

### Task 4: Verification

**Files:**
- Modify as needed.

- [ ] Run backend tests.
- [ ] Start FastAPI dev server.
- [ ] Verify landing page returns HTTP 200.
- [ ] Provide local URL and admin export URL.
