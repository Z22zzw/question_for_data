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
    assert '["class_name", "text"]' in pretest_fields
    assert '["student_name", "text"]' in pretest_fields
    assert '["student_id", "text"]' in pretest_fields
    assert '["questionnaire_version", "select"]' in pretest_fields
    assert '["major", "select"]' in pretest_fields
    assert "function pretestFieldsForVersion" in app_js
    assert 'name !== "numpy_familiarity"' in app_js
    assert "delete data.numpy_familiarity" in app_js
    assert '"Agent Version"' in app_js
    assert '"agent"' in app_js
    assert "Agent 监督版本" in app_js
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
    assert "test_group" in app_js
    assert "测试问卷" in app_js
    assert "本次作答不会计入正式样本、统计或导出" in app_js
    assert "state.isTest" in app_js
    assert "state.status = \"notice\";" in app_js
    assert "renderResearchNotice();" in app_js
    assert "我已阅读并同意研究说明与作答规则" in app_js
    assert "核心总题量：Python 版本 47 道；C 语言/Agent 版本 46 道" in app_js
    assert "6 个正式任务和后测必须在 40 分钟内提交" in app_js
    assert "连续选择同一个选项本身不会再计入质量异常" in app_js
    assert "function updateTimer" in app_js
    assert "function renderTimeoutNotice" in app_js
    assert "已超过 40 分钟，请重新开始" in app_js
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
    assert "agentTrace" in app_js
    assert "人工智能编程智能体(AI coding agent)工作记录" in app_js
    assert 'task.questionnaire_version === "agent"' in app_js
    assert "正式问题" in app_js
    assert "人工智能编程智能体(AI coding agent)给出的代码(code)" in app_js
    assert "回答背景" in app_js
    assert "人工监督者(human supervisor)" in app_js


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


def test_mobile_modal_scrolls_inside_viewport():
    styles = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert "height: 100dvh" in styles
    assert "max-height: calc(100dvh - 20px)" in styles
    assert "-webkit-overflow-scrolling: touch" in styles
    assert "touch-action: pan-y" in styles
    assert 'window.matchMedia("(max-width: 760px)").matches' in app_js


def test_topbar_reveals_only_on_upward_scroll_after_leaving_view():
    app_js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    styles = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")

    assert "function updateTopbarVisibility" in app_js
    assert 'window.addEventListener("scroll", updateTopbarVisibility' in app_js
    assert ".topbar.is-floating" in styles
    assert ".topbar.is-hidden" in styles
    assert "position: sticky" not in styles


def test_admin_page_has_completion_and_incomplete_reason_filters():
    admin_html = (ROOT / "static" / "admin.html").read_text(encoding="utf-8")

    assert 'id="versionFilter"' in admin_html
    assert 'value="agent"' in admin_html
    assert 'id="completionFilter"' in admin_html
    assert 'id="incompleteReasonFilter"' in admin_html
    assert 'id="bulkDeleteSelectedBtn"' in admin_html
    assert 'id="bulkDeleteFilteredBtn"' in admin_html
    assert 'id="statsPageBtn"' in admin_html
    assert "/stats.html" in admin_html
    assert "/api/admin/sessions/bulk-delete" in admin_html
    assert 'value="normal_completed"' in admin_html
    assert 'value="pending_posttest"' in admin_html
    assert 'value="quality_failed"' in admin_html
    assert 'value="timeout"' in admin_html
    assert "总耗时" in admin_html
    assert "前台开放" in admin_html
    assert 'data-version-toggle="agent"' in admin_html
    assert "/api/admin/questionnaire-settings" in admin_html
    assert "post_agent_supervision_score" in admin_html
    assert 'id="editCompletionOverride"' in admin_html
    assert 'id="editCompletionOverrideNote"' in admin_html
    assert "function saveCompletionOverride" in admin_html
    assert "completion_override" in admin_html
    assert "is_test" in admin_html
    assert "测试不计入" in admin_html
    assert "正式正常完成" in admin_html
    assert "automatic_completion" in admin_html
    assert "人工复核" in admin_html
    assert "班级" in admin_html
    assert "姓名" in admin_html
    assert "学号" in admin_html
    assert "class_name" in admin_html
    assert "student_name" in admin_html
    assert "student_id" in admin_html
    assert "function filteredSessions" in admin_html
    assert "function shouldIncludeAbandoned" in admin_html
    assert "questionnaire_${version}_normal_completed_export.xlsx" in admin_html


def test_admin_stats_page_exists_and_reads_stats_endpoint():
    stats_html = (ROOT / "static" / "stats.html").read_text(encoding="utf-8")

    assert "问卷统计看板" in stats_html
    assert "各问卷版本平均分" in stats_html
    assert "A/B 组平均分" in stats_html
    assert "正常完成样本明细" in stats_html
    assert "sampleBody" in stats_html
    assert "class_name" in stats_html
    assert "student_name" in stats_html
    assert "student_id" in stats_html
    assert "/api/admin/stats" in stats_html
    assert "questionnaire_admin_password" in stats_html
    assert "average_total_score" in stats_html
