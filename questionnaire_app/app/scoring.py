from __future__ import annotations

from .questionnaire import (
    ANSWER_KEY,
    DELIVERABILITY_QUESTIONS,
    ERROR_IDENTIFICATION_QUESTIONS,
    REASONING_QUESTIONS,
    SUPERVISION_KEY,
)


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
