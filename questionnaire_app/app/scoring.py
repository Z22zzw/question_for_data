from __future__ import annotations

from .questionnaire import (
    ANSWER_KEY,
    DELIVERABILITY_QUESTIONS,
    ERROR_IDENTIFICATION_QUESTIONS,
    POSTTEST_FIELDS,
    REASONING_QUESTIONS,
    SUPERVISION_KEY,
)

MIN_TOTAL_SECONDS = 5 * 60   # 5 minutes


def check_timing(_task_durations: dict[int, int | None], total_seconds: int | None) -> list[str]:
    """Return timing violation reasons; empty means valid."""
    flags = []
    if total_seconds is not None and total_seconds <= MIN_TOTAL_SECONDS:
        flags.append(f"total_time_too_short ({total_seconds}s <= {MIN_TOTAL_SECONDS}s)")
    return flags


def check_response_pattern(answers: dict[str, str]) -> list[str]:
    """Response-pattern monitoring is disabled by policy."""
    return []


def score_answers(answers: dict[str, str]) -> dict:
    per_question = {qid: int(answers.get(qid) == correct) for qid, correct in ANSWER_KEY.items()}
    return {
        "per_question": per_question,
        "total_score": sum(per_question.values()),
        "deliverability_score": sum(per_question[qid] for qid in DELIVERABILITY_QUESTIONS),
        "reasoning_score": sum(per_question[qid] for qid in REASONING_QUESTIONS),
        "error_identification_score": sum(per_question[qid] for qid in ERROR_IDENTIFICATION_QUESTIONS),
    }


def score_supervision(supervision_answers: dict[str, str]) -> dict:
    per_item = {
        key: int(supervision_answers.get(key) == correct)
        for key, correct in SUPERVISION_KEY.items()
        if key in supervision_answers
    }
    t1_score = sum(value for key, value in per_item.items() if key.startswith("T1_"))
    t2_score = sum(value for key, value in per_item.items() if key.startswith("T2_"))
    return {
        "per_item": per_item,
        "t1_supervision_card_score": t1_score,
        "t2_supervision_card_score": t2_score,
        "supervision_card_score": t1_score + t2_score,
    }


POSTTEST_SCORE_VALUES = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "Strongly disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly agree": 5,
}


def score_posttest(posttest: dict[str, str]) -> dict:
    values = [POSTTEST_SCORE_VALUES.get(posttest.get(field, "")) for field in POSTTEST_FIELDS]
    numeric_values = [value for value in values if value is not None]
    score = round(sum(numeric_values) / len(numeric_values), 2) if numeric_values else None
    return {"post_agent_supervision_score": score}
