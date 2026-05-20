from __future__ import annotations

from .questionnaire import (
    ANSWER_KEY,
    DELIVERABILITY_QUESTIONS,
    ERROR_IDENTIFICATION_QUESTIONS,
    REASONING_QUESTIONS,
    SUPERVISION_KEY,
)

MIN_TOTAL_SECONDS = 5 * 60   # 5 minutes
MIN_TASK_SECONDS = 60        # 1 minute per task


def check_timing(task_durations: dict[int, int | None], total_seconds: int | None) -> list[str]:
    """Return list of timing violation reasons; empty means valid."""
    flags = []
    if total_seconds is not None and total_seconds < MIN_TOTAL_SECONDS:
        flags.append(f"total_time_too_short ({total_seconds}s < {MIN_TOTAL_SECONDS}s)")
    for task_id, duration in task_durations.items():
        if duration is not None and duration < MIN_TASK_SECONDS:
            flags.append(f"task_{task_id}_too_short ({duration}s < {MIN_TASK_SECONDS}s)")
    return flags


def check_response_pattern(answers: dict[str, str]) -> list[str]:
    """Return list of pattern violation reasons; empty means valid."""
    flags = []
    values = list(answers.values())
    if len(values) >= 10 and len(set(values)) == 1:
        flags.append(f"all_same_answer ({values[0]})")
    # Check per-task blocks of 5 questions (Q1-Q5, Q6-Q10, ...)
    task_qids = [
        [f"Q{i}" for i in range(start, start + 5)]
        for start in range(1, 31, 5)
    ]
    for block in task_qids:
        block_vals = [answers[q] for q in block if q in answers]
        if len(block_vals) == 5 and len(set(block_vals)) == 1:
            flags.append(f"task_block_all_same ({block[0]}-{block[-1]}: {block_vals[0]})")
    return flags


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
