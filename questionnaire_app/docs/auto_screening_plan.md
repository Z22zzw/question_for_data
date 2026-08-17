# Automatic Screening Plan

This plan describes recommended automatic filters for the exported Excel workbook. The goal is to mark suspicious responses for exclusion or sensitivity analysis without deleting raw data.

## Recommended Output Columns

Add these derived columns in the analysis workbook or downstream script:

| Column | Type | Rule |
|---|---|---|
| screening_status | text | keep / review / exclude |
| screening_flags | text | Semicolon-separated flags |
| completed | boolean | total_score is not blank and all Q1-Q30 are answered |
| total_duration_seconds | number | Convert total_duration_hms to seconds |
| task1_duration_seconds ... task6_duration_seconds | number | Convert each task duration to seconds |

## Exclusion Rules

Use `screening_status = exclude` when any rule is true:

1. `consent != "I agree"`.
2. Any formal question Q1-Q30 is blank.
3. `total_duration_seconds <= 300`.
4. The same participant row has duplicated submission data caused by manual database import or accidental copy.

## Review Rules

Use `screening_status = review` when any rule is true but no exclusion rule is true:

1. `total_duration_seconds > 7200`.
2. Formal `total_score <= 5`, which may indicate non-engaged responding or severe misunderstanding.
3. B-group supervision-card score is 0 while total completion time is unusually short.

Repeated use of the same option letter is no longer a response-quality flag by itself.

## Keep Rules

Use `screening_status = keep` when:

1. No exclusion rule is true.
2. No review rule is true.
3. Q1-Q30 are complete.

## Suggested Excel Formula Pattern

After converting duration strings to seconds, use a helper formula style like:

```text
=TEXTJOIN("; ", TRUE,
IF(consent<>"I agree","no_consent",""),
IF(COUNTA(Q1:Q30)<30,"incomplete_formal_answers",""),
IF(total_duration_seconds<=300,"too_fast_total",""),
IF(total_duration_seconds>7200,"too_slow_total",""),
IF(total_score<=5,"very_low_score","")
)
```

Then:

```text
=IF(OR(ISNUMBER(SEARCH("no_consent",screening_flags)),ISNUMBER(SEARCH("incomplete",screening_flags)),ISNUMBER(SEARCH("too_fast_total",screening_flags))),"exclude",IF(screening_flags<>"","review","keep"))
```

## Recommended Analysis Practice

Run the primary analysis on `screening_status = keep`. Then run a sensitivity analysis on `keep + review` to verify whether the treatment effect changes materially. Keep excluded rows in the raw workbook, but do not include them in the primary analysis dataset.
