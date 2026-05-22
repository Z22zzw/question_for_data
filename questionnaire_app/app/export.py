from __future__ import annotations

from io import BytesIO

from openpyxl import Workbook

from .database import decode_json, seconds_between, seconds_to_hms
from .questionnaire import ANSWER_KEY, POSTTEST_FIELDS, PRETEST_FIELDS, SUPERVISION_KEY
from .scoring import score_answers, score_supervision


def pretest_fields_for_export(version: str) -> list[str]:
    return [
        field
        for field in PRETEST_FIELDS
        if version == "python" or field != "numpy_familiarity"
    ]


def build_export_workbook(rows: list[dict], version: str = "python") -> bytes:
    pretest_fields = pretest_fields_for_export(version)
    headers = [
        "session_id",
        "participant_id",
        "group",
    ]
    for task_id in range(1, 7):
        headers.append(f"task{task_id}_duration_hms")
    headers.append("total_duration_hms")
    headers.extend(pretest_fields)
    headers.extend(POSTTEST_FIELDS)
    headers.extend(ANSWER_KEY.keys())
    headers.extend(f"{qid}_score" for qid in ANSWER_KEY)
    headers.extend(
        [
            "total_score",
            "deliverability_score",
            "reasoning_score",
            "error_identification_score",
        ]
    )
    headers.extend(SUPERVISION_KEY.keys())
    headers.extend(["t1_supervision_card_score", "t2_supervision_card_score", "supervision_card_score"])

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "responses"
    sheet.append(headers)

    for row in rows:
        session = row["session"]
        pretest = decode_json(session["pretest_json"])
        posttest = decode_json(session["posttest_json"])
        answers: dict[str, str] = {}
        supervision: dict[str, str] = {}
        submit_times: dict[int, str] = {}
        for response in row["responses"]:
            answers.update(decode_json(response["answers_json"]))
            supervision.update(decode_json(response["supervision_json"]))
            submit_times[response["task_id"]] = response["submitted_at"]
        formal_scores = score_answers(answers)
        supervision_scores = score_supervision(supervision)

        values = [
            session["id"],
            session["participant_id"],
            session["group_name"],
        ]
        for task_id in range(1, 7):
            start = row["starts"].get(task_id)
            start_time = start["started_at"] if start else None
            submit_time = submit_times.get(task_id)
            values.append(seconds_to_hms(seconds_between(start_time, submit_time)))
        values.append(seconds_to_hms(seconds_between(session["created_at"], session["completed_at"])))
        values.extend(pretest.get(field) for field in pretest_fields)
        values.extend(posttest.get(field) for field in POSTTEST_FIELDS)
        values.extend(answers.get(qid) for qid in ANSWER_KEY)
        values.extend(formal_scores["per_question"].get(qid, 0) for qid in ANSWER_KEY)
        values.extend(
            [
                formal_scores["total_score"],
                formal_scores["deliverability_score"],
                formal_scores["reasoning_score"],
                formal_scores["error_identification_score"],
            ]
        )
        values.extend(supervision.get(key) for key in SUPERVISION_KEY)
        values.extend(
            [
                supervision_scores["t1_supervision_card_score"],
                supervision_scores["t2_supervision_card_score"],
                supervision_scores["supervision_card_score"],
            ]
        )
        sheet.append(values)

    stream = BytesIO()
    workbook.save(stream)
    return stream.getvalue()
