from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_task_page_renders_supervision_card_between_description_and_questions():
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    form_template_start = app_js.index('view.innerHTML = `\n    <form id="taskForm"')
    form_template_end = app_js.index('const form = document.getElementById("taskForm");')
    task_template = app_js[form_template_start:form_template_end]

    description_index = task_template.index('<ol class="requirements">${task.requirements')
    supervision_index = task_template.index("${supervision}")
    questions_index = task_template.index('<section class="task-block">${questions}</section>')

    assert description_index < supervision_index < questions_index


def test_home_reset_entry_clears_session_and_cached_submission():
    index_html = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert 'id="resetHome"' in index_html
    assert "function resetToHome" in app_js
    assert 'api("/api/session/reset", { method: "POST" })' in app_js
    assert 'localStorage.removeItem("questionnaire_pending_submit")' in app_js
    assert "questionnaire_session_id" not in app_js


def test_frontend_resumes_from_server_current_session_endpoint():
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert "async function bootstrapSession" in app_js
    assert 'api("/api/session/current")' in app_js


def test_frontend_shows_research_notice_after_pretest_and_tracks_time():
    index_html = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert 'id="overallProgressLabel"' in index_html
    assert 'id="timerLabel"' in index_html
    assert 'path: "/api/pretest"' in app_js
    assert "function renderResearchNotice" in app_js
    assert 'api("/api/session/start", { method: "POST"' in app_js
    assert "state.status = \"notice\";" in app_js
    assert "renderResearchNotice();" in app_js
    assert "我已阅读并同意研究告知书与作答规则" in app_js
    assert "function updateTimer" in app_js
    assert "function renderTimeoutNotice" in app_js
    assert "作答已超时，请重新作答" in app_js
    assert "function clearQuestionnaireLocalState" in app_js
    assert "function setOverallProgress" in app_js


def test_frontend_scrolls_to_first_unanswered_required_group():
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    styles = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")

    assert "function validateRequiredRadioGroups" in app_js
    assert "scrollIntoView" in app_js
    assert "unanswered" in app_js
    assert ".question.unanswered" in styles


def test_admin_page_has_completion_and_incomplete_reason_filters():
    admin_html = (ROOT / "static" / "admin.html").read_text(encoding="utf-8")

    assert 'id="completionFilter"' in admin_html
    assert 'id="incompleteReasonFilter"' in admin_html
    assert 'value="normal_completed"' in admin_html
    assert 'value="pending_posttest"' in admin_html
    assert 'value="quality_failed"' in admin_html
    assert 'value="timeout"' in admin_html
    assert "总耗时" in admin_html
    assert "function filteredSessions" in admin_html
    assert "function shouldIncludeAbandoned" in admin_html
    assert "questionnaire_normal_completed_export.xlsx" in admin_html
