from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_task_page_renders_supervision_card_between_description_and_questions():
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    form_template_start = app_js.index('view.innerHTML = `\n    <form id="taskForm"')
    form_template_end = app_js.index('const form = document.getElementById("taskForm");')
    task_template = app_js[form_template_start:form_template_end]

    description_index = task_template.index('<ol class="requirements">${task.requirements')
    supervision_index = task_template.index("${supervision}")
    questions_index = task_template.index("${questions}")

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


def test_pretest_omits_age_and_gender_and_uses_major_dropdown():
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    fields_start = app_js.index("const pretestFields = [")
    fields_end = app_js.index("];", fields_start)
    pretest_fields = app_js[fields_start:fields_end]

    assert '["age",' not in pretest_fields
    assert '["gender",' not in pretest_fields
    assert '["questionnaire_version", "select"]' in pretest_fields
    assert '["major", "select"]' in pretest_fields
    assert "function pretestFieldsForVersion" in app_js
    assert 'name !== "numpy_familiarity"' in app_js
    assert "delete data.numpy_familiarity" in app_js
    assert "majorOptionsByVersion" in app_js
    assert "familiarityLabelsByVersion" in app_js
    assert '"C Language Proficiency"' in app_js
    assert '"C 语言掌握程度"' in app_js
    assert '"计算机类"' in app_js
    assert '"计算机科学与技术"' in app_js
    assert '"网络空间安全"' in app_js
    assert '"数字媒体技术"' in app_js
    assert '"物联网工程"' in app_js
    assert '"智能科技与技术"' in app_js
    assert '"软件工程"' in app_js


def test_c_answer_key_markdown_exists():
    answer_key = (ROOT / "docs" / "c_questionnaire_answer_key.md").read_text(encoding="utf-8")

    assert "# C 语言版本标准答案与评分标准" in answer_key
    assert "| Q30 | A |" in answer_key
    assert "T1_SC_problem_definition" in answer_key
    assert "监督卡总分 10 分" in answer_key


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


def test_frontend_has_two_stage_guidance_modals_and_modal_language_switch():
    index_html = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert 'rel="icon"' in index_html
    assert "function renderIntroModal" in app_js
    assert "function renderModalLanguageButton" in app_js
    assert "introPurpose" in app_js
    assert "introNotInterested" in app_js
    assert "notInterestedText" in app_js
    assert "noticeSections" in app_js
    assert "modal-language" in app_js


def test_frontend_task_page_explains_how_to_answer_and_supervision_card_role():
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert "taskGuideTitle" in app_js
    assert "taskGuideSteps" in app_js
    assert "taskSectionLabels" in app_js
    assert "supervisionIntro" in app_js
    assert "正式问题" in app_js
    assert "AI 生成的代码" in app_js


def test_frontend_scrolls_to_first_unanswered_required_group():
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    styles = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")

    assert "function validateRequiredRadioGroups" in app_js
    assert "scrollIntoView" in app_js
    assert "unanswered" in app_js
    assert "requiredQuestionWarning" in app_js
    assert ".question.unanswered" in styles


def test_mobile_layout_prevents_page_level_horizontal_overflow():
    styles = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")

    assert "overflow-x: hidden" in styles
    assert ".task-block" in styles
    assert "min-width: 0" in styles
    assert "overflow-wrap: anywhere" in styles
    assert "max-width: 100%" in styles


def test_admin_page_has_completion_and_incomplete_reason_filters():
    admin_html = (ROOT / "static" / "admin.html").read_text(encoding="utf-8")

    assert 'id="versionFilter"' in admin_html
    assert 'id="completionFilter"' in admin_html
    assert 'id="incompleteReasonFilter"' in admin_html
    assert 'id="bulkDeleteSelectedBtn"' in admin_html
    assert 'id="bulkDeleteFilteredBtn"' in admin_html
    assert "/api/admin/sessions/bulk-delete" in admin_html
    assert 'value="normal_completed"' in admin_html
    assert 'value="pending_posttest"' in admin_html
    assert 'value="quality_failed"' in admin_html
    assert 'value="timeout"' in admin_html
    assert "总耗时" in admin_html
    assert "function filteredSessions" in admin_html
    assert "function shouldIncludeAbandoned" in admin_html
    assert "questionnaire_${version}_normal_completed_export.xlsx" in admin_html
