from pathlib import Path

from fastapi.testclient import TestClient
from openpyxl import load_workbook

from app.main import SESSION_COOKIE_NAME, create_app


def make_client(tmp_path: Path) -> TestClient:
    db_path = tmp_path / "test.sqlite"
    app = create_app(db_path=db_path, admin_password="secret")
    return TestClient(app)


def make_two_clients(tmp_path: Path) -> tuple[TestClient, TestClient]:
    db_path = tmp_path / "test.sqlite"
    app = create_app(db_path=db_path, admin_password="secret")
    return TestClient(app), TestClient(app)


def pretest_payload() -> dict:
    return {
        "consent": "I agree",
        "age": 20,
        "gender": "Prefer not to say",
        "grade_year": "Year 3",
        "major": "Computer Science",
        "programming_experience_years": "3-4",
        "python_familiarity": "4",
        "file_io_familiarity": "3",
        "numpy_familiarity": "3",
        "ai_tool_use_frequency": "Often",
        "ai_code_review_experience": "Sometimes",
    }


def correct_answers(start: int, end: int) -> dict:
    key = {
        "Q1": "B",
        "Q2": "B",
        "Q3": "B",
        "Q4": "A",
        "Q5": "B",
        "Q6": "B",
        "Q7": "B",
        "Q8": "D",
        "Q9": "A",
        "Q10": "B",
        "Q11": "A",
        "Q12": "A",
        "Q13": "A",
        "Q14": "A",
        "Q15": "D",
        "Q16": "B",
        "Q17": "B",
        "Q18": "B",
        "Q19": "A",
        "Q20": "B",
        "Q21": "A",
        "Q22": "A",
        "Q23": "A",
        "Q24": "A",
        "Q25": "D",
        "Q26": "B",
        "Q27": "B",
        "Q28": "B",
        "Q29": "A",
        "Q30": "A",
    }
    return {qid: answer for qid, answer in key.items() if start <= int(qid[1:]) <= end}


def posttest_payload() -> dict:
    return {
        "post_attitude_useful": "Agree",
        "post_attitude_confident": "Agree",
        "post_attitude_learning_value": "Strongly agree",
        "post_attitude_cognitive_load": "Neutral",
        "post_attitude_future_use": "Agree",
        "post_strategy_requirements_first": "Strongly agree",
        "post_strategy_trace_code": "Agree",
        "post_strategy_predict_output": "Agree",
        "post_strategy_test_cases": "Strongly agree",
        "post_strategy_delivery_risk": "Agree",
        "post_trust_ai_correctness": "Neutral",
        "post_trust_ai_boundary_cases": "Disagree",
        "post_trust_ai_direct_submit": "Strongly disagree",
        "post_trust_ai_with_review": "Agree",
        "post_trust_ai_overall": "Neutral",
    }


def test_pretest_assigns_hidden_balanced_groups(tmp_path: Path):
    client = make_client(tmp_path)

    for idx in range(4):
        response = client.post("/api/pretest", json=pretest_payload())
        assert response.status_code == 200
        data = response.json()
        assert data["next_task"] == 1
        assert data["next_stage"] == "task"
        assert data["participant_id"] == idx + 1
        assert set(data.keys()) == {"participant_id", "next_task", "next_stage"}
        assert SESSION_COOKIE_NAME in response.cookies
        assert "httponly" in response.headers["set-cookie"].lower()

    export_response = client.get("/api/admin/export?password=secret")
    export_path = tmp_path / "groups.xlsx"
    export_path.write_bytes(export_response.content)
    workbook = load_workbook(export_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    groups = [dict(zip(headers, [cell.value for cell in row]))["group"] for row in sheet.iter_rows(min_row=2)]
    assert groups.count("A") == 2
    assert groups.count("B") == 2


def test_group_b_gets_supervision_cards_only_for_first_two_tasks(tmp_path: Path):
    client_a, client_b = make_two_clients(tmp_path)
    client_a.post("/api/pretest", json=pretest_payload())
    client_b.post("/api/pretest", json=pretest_payload())

    task1_a = client_a.get("/api/task/1").json()
    task1_b = client_b.get("/api/task/1").json()

    assert task1_a["supervision_card"] is None
    assert task1_b["supervision_card"] is not None

    client_b.post(
        "/api/task/1",
        json={"answers": correct_answers(1, 5), "supervision_answers": {"T1_SC_problem_definition": "Yes"}},
    )
    task2 = client_b.get("/api/task/2").json()
    assert task2["supervision_card"] is not None

    client_b.post(
        "/api/task/2",
        json={"answers": correct_answers(6, 10), "supervision_answers": {"T2_SC_problem_definition": "Yes"}},
    )
    task3 = client_b.get("/api/task/3").json()
    assert task3["supervision_card"] is None


def test_completed_task_cannot_be_read_or_modified(tmp_path: Path):
    client = make_client(tmp_path)
    client.post("/api/pretest", json=pretest_payload())

    response = client.post(
        "/api/task/1",
        json={"answers": correct_answers(1, 5), "supervision_answers": {}},
    )
    assert response.status_code == 200

    back_read = client.get("/api/task/1")
    assert back_read.status_code == 409

    rewrite = client.post(
        "/api/task/1",
        json={"answers": {"Q1": "A"}, "supervision_answers": {}},
    )
    assert rewrite.status_code == 409


def test_scoring_and_excel_export(tmp_path: Path):
    client = make_client(tmp_path)
    pretest = client.post("/api/pretest", json=pretest_payload()).json()

    for task_id, start in enumerate([1, 6, 11, 16, 21, 26], start=1):
        response = client.post(
            f"/api/task/{task_id}",
            json={"answers": correct_answers(start, start + 4), "supervision_answers": {}},
        )
        assert response.status_code == 200

    summary_before_posttest = client.get("/api/session/current").json()
    assert summary_before_posttest["status"] == "posttest"
    assert summary_before_posttest["next_stage"] == "posttest"

    posttest_schema = client.get("/api/posttest?lang=en").json()
    assert posttest_schema["title"] == "Post-task Questionnaire"
    assert len(posttest_schema["questions"]) == 15
    assert posttest_schema["questions"][0]["id"] == "post_attitude_useful"

    posttest_response = client.post("/api/posttest", json=posttest_payload())
    assert posttest_response.status_code == 200

    summary = client.get("/api/session/current").json()
    assert summary["status"] == "complete"
    assert summary["scores"]["total_score"] == 30
    assert summary["scores"]["deliverability_score"] == 12
    assert summary["scores"]["reasoning_score"] == 12
    assert summary["scores"]["error_identification_score"] == 6

    export_response = client.get("/api/admin/export?password=secret")
    assert export_response.status_code == 200
    export_path = tmp_path / "export.xlsx"
    export_path.write_bytes(export_response.content)
    workbook = load_workbook(export_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    row = [cell.value for cell in sheet[2]]
    data = dict(zip(headers, row))
    assert data["participant_id"] == pretest["participant_id"]
    assert data["total_score"] == 30
    assert data["post_attitude_useful"] == "Agree"
    assert data["post_trust_ai_direct_submit"] == "Strongly disagree"
    assert "total_duration_hms" in headers
    assert "task1_duration_hms" in headers
    assert "start_time" not in headers
    assert "pretest_submit_time" not in headers
    assert "end_time" not in headers


def test_task_can_be_localized_to_chinese(tmp_path: Path):
    client = make_client(tmp_path)
    client.post("/api/pretest", json=pretest_payload())

    task = client.get("/api/task/1?lang=zh").json()

    assert task["title"].startswith("任务 1")
    assert "这份 AI 答案" in task["questions"][0]["prompt"]


def test_posttest_is_same_for_a_and_b_and_available_after_tasks(tmp_path: Path):
    clients = make_two_clients(tmp_path)
    for client in clients:
        client.post("/api/pretest", json=pretest_payload())

    posttest_titles = []
    for client in clients:
        for task_id, start in enumerate([1, 6, 11, 16, 21, 26], start=1):
            response = client.post(
                f"/api/task/{task_id}",
                json={"answers": correct_answers(start, start + 4), "supervision_answers": {}},
            )
            assert response.status_code == 200
        schema = client.get("/api/posttest?lang=zh").json()
        posttest_titles.append(schema["title"])
        assert "态度" in schema["sections"][0]["title"]
        assert len(schema["questions"]) == 15

    assert posttest_titles[0] == posttest_titles[1]


def test_session_current_and_reset_use_cookie_not_local_storage_ids(tmp_path: Path):
    client = make_client(tmp_path)

    assert client.get("/api/session/current").json()["status"] == "none"

    pretest_response = client.post("/api/pretest", json=pretest_payload())
    assert SESSION_COOKIE_NAME in pretest_response.cookies

    current = client.get("/api/session/current").json()
    assert current["status"] == "in_progress"
    assert current["next_task"] == 1
    assert "group" not in current
    assert "session_id" not in current

    reset_response = client.post("/api/session/reset")
    assert reset_response.status_code == 200
    assert client.get("/api/session/current").json()["status"] == "none"
