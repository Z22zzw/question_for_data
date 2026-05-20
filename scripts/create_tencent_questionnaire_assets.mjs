import fs from "node:fs";

const env = Object.fromEntries(
  fs
    .readFileSync(".env", "utf8")
    .split(/\r?\n/)
    .filter((line) => line.includes("="))
    .map((line) => {
      const i = line.indexOf("=");
      return [line.slice(0, i), line.slice(i + 1)];
    })
);

const token = env.QQDOC_ACCESS_TOKEN;
if (!token) {
  throw new Error("Missing QQDOC_ACCESS_TOKEN in .env");
}

let id = 1;
async function mcpCall(method, params = {}) {
  const res = await fetch("https://docs.qq.com/openapi/mcp", {
    method: "POST",
    headers: {
      Authorization: token,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: id++,
      method,
      params,
    }),
  });
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(`Non-JSON response ${res.status}: ${text.slice(0, 500)}`);
  }
  if (!res.ok || data.error) {
    throw new Error(JSON.stringify(data.error ?? data));
  }
  return data.result;
}

async function tool(name, args) {
  return mcpCall("tools/call", { name, arguments: args });
}

const questionnaireMarkdown = `# AI Supervision A/B Test Questionnaire Build Spec

## Implementation Summary

This document is the build specification for the Tencent Docs questionnaire. Use one public entry link. All participants complete the same pretest first, then the system assigns them to Group A or Group B with a hidden 50/50 random split.

Group A and Group B receive the same 6 tasks and the same 30 formal single-choice questions. Group B additionally sees a supervision card above Task 1 and Task 2. Group A does not see any supervision card. The supervision card is a process measure and intervention; it is scored separately and is not included in the main 30-point score.

Participants must not see the group label, standard answers, score, other participants' responses, or any page that has already been completed. Each task is one page. Participants can scroll within the current task page, but after submitting a task page they cannot return, redo, or edit it.

## Flow

1. Pretest page, shared by A and B.
2. Hidden random assignment after pretest: Group A or Group B.
3. Task 1 page: Group A sees task and Q1-Q5; Group B sees supervision card, task, and Q1-Q5.
4. Task 2 page: Group A sees task and Q6-Q10; Group B sees supervision card, task, and Q6-Q10.
5. Task 3 page: both groups see task and Q11-Q15.
6. Task 4 page: both groups see task and Q16-Q20.
7. Task 5 page: both groups see task and Q21-Q25.
8. Task 6 page: both groups see task and Q26-Q30.
9. Final submit page. Do not show score or answer key.

## Pretest Fields

Use English export field names:

| Field name | Type | Options / Notes |
|---|---|---|
| participant_id | text | Required |
| consent | single choice | I agree / I do not agree |
| age | number | Required |
| gender | single choice | Female / Male / Non-binary / Prefer not to say |
| grade_year | single choice | Year 1 / Year 2 / Year 3 / Year 4 / Master / PhD / Other |
| major | text | Required |
| programming_experience_years | single choice | Less than 1 / 1-2 / 3-4 / 5 or more |
| python_familiarity | single choice | 1 / 2 / 3 / 4 / 5 |
| file_io_familiarity | single choice | 1 / 2 / 3 / 4 / 5 |
| numpy_familiarity | single choice | 1 / 2 / 3 / 4 / 5 |
| ai_tool_use_frequency | single choice | Never / Rarely / Sometimes / Often / Very often |
| ai_code_review_experience | single choice | Never / Rarely / Sometimes / Often / Very often |

## Hidden / Export Fields

| Field name | Notes |
|---|---|
| group | Hidden value: A or B |
| start_time | Questionnaire start timestamp |
| pretest_submit_time | Pretest page submit timestamp |
| task1_start_time | Task 1 page open timestamp |
| task1_submit_time | Task 1 page submit timestamp |
| task2_start_time | Task 2 page open timestamp |
| task2_submit_time | Task 2 page submit timestamp |
| task3_start_time | Task 3 page open timestamp |
| task3_submit_time | Task 3 page submit timestamp |
| task4_start_time | Task 4 page open timestamp |
| task4_submit_time | Task 4 page submit timestamp |
| task5_start_time | Task 5 page open timestamp |
| task5_submit_time | Task 5 page submit timestamp |
| task6_start_time | Task 6 page open timestamp |
| task6_submit_time | Task 6 page submit timestamp |
| end_time | Final submit timestamp |
| total_duration_seconds | end_time - start_time |
| task1_duration_seconds | task1_submit_time - task1_start_time |
| task2_duration_seconds | task2_submit_time - task2_start_time |
| task3_duration_seconds | task3_submit_time - task3_start_time |
| task4_duration_seconds | task4_submit_time - task4_start_time |
| task5_duration_seconds | task5_submit_time - task5_start_time |
| task6_duration_seconds | task6_submit_time - task6_start_time |

If Tencent Forms cannot record per-page timing, record at least start_time, end_time, and total_duration_seconds.

## Task 1: Dictionary Price Lookup and Order Total

### Task Requirements

\`\`\`python
calculate_order_total(items, price_table, vip=False)
\`\`\`

1. items is a dictionary in the format {product_id: quantity}.
2. price_table is a dictionary in the format {product_id: unit_price}.
3. If items contains a product ID that does not exist in price_table, return "Unknown item".
4. First calculate item subtotal: unit price multiplied by quantity.
5. If vip=True, apply a 10% discount to the subtotal.
6. If the discounted subtotal is greater than 100, shipping is free; otherwise shipping is 8.
7. Return the final amount rounded to two decimal places.

### AI-Generated Answer

\`\`\`python
def calculate_order_total(items, price_table, vip=False):
    subtotal = 0
    for pid, qty in items.items():
        subtotal += price_table.get(pid, 0) * qty
    if vip:
        subtotal *= 0.9
    if subtotal > 100:
        shipping = 0
    else:
        shipping = 8
    return round(subtotal + shipping, 2)
\`\`\`

### Group B Supervision Card for Task 1

| Dimension | Supervision check item | Options | Export field |
|---|---|---|---|
| Problem Definition | Does the task require returning "Unknown item" for an unknown product ID? | Yes / No / Not sure | T1_SC_problem_definition |
| AI Code Understanding | Does price_table.get(pid, 0) treat an unknown product as price 0? | Yes / No / Not sure | T1_SC_code_understanding |
| AI Output Debugging | For items={"A":2,"X":1}, will the unknown product X be silently ignored by the AI code? | Yes / No / Not sure | T1_SC_output_debugging |
| Verification and Testing | Which input best reveals the unknown-product problem? | A. {"A":2} / B. {"X":1} / C. {"A":20} | T1_SC_verification_testing |
| Responsibility and Supervision | If an unknown product is treated as 0 yuan, can this code be submitted directly? | Can submit / Cannot submit / Not sure | T1_SC_responsibility |

### Formal Questions

Q1. Does this AI-generated answer fully satisfy the task requirements?
A. Yes
B. No

Q2. Can this AI-generated answer be submitted directly?
A. Can submit
B. Cannot submit

Given:
\`\`\`python
price_table = {"A": 10, "B": 50}
items = {"A": 2, "X": 1}
calculate_order_total(items, price_table, vip=False)
\`\`\`

Q3. What will the AI code return?
A. "Unknown item"
B. 28.0
C. 20.0
D. Error

Q4. According to the task requirements, what should the correct return value be?
A. "Unknown item"
B. 28.0
C. 20.0
D. 8.0

Q5. What is the main problem with this AI-generated answer?
A. The VIP discount is calculated incorrectly
B. Unknown product IDs are treated as price 0
C. It does not round to two decimal places
D. The shipping rule is completely reversed

## Task 2: File I/O and Tag Counting

### Task Requirements

\`\`\`python
count_tags(input_path, output_path)
\`\`\`

1. Each line in the input file has the format: user,tag.
2. Empty lines should be skipped.
3. Spaces before and after tag should be stripped.
4. Count the occurrences of each tag and return a dictionary.
5. Write the result to output_path.
6. Each output line should have the format: tag,count.
7. Output lines should be sorted alphabetically by tag.
8. The output file should be overwritten, not appended.

### AI-Generated Answer

\`\`\`python
def count_tags(input_path, output_path):
    counts = {}
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            if line == "":
                continue
            user, tag = line.split(",")
            tag = tag.strip()
            counts[tag] = counts.get(tag, 0) + 1
    with open(output_path, "a", encoding="utf-8") as f:
        for tag, c in counts.items():
            f.write(f"{tag},{c}\\n")
    return counts
\`\`\`

### Group B Supervision Card for Task 2

| Dimension | Supervision check item | Options | Export field |
|---|---|---|---|
| Problem Definition | Does the task require empty lines to be skipped? | Yes / No / Not sure | T2_SC_problem_definition |
| AI Code Understanding | Can if line == "" skip an empty line represented as "\\n" in a file? | Can / Cannot / Not sure | T2_SC_code_understanding |
| AI Output Debugging | When an empty line is encountered, can user, tag = line.split(",") raise an error? | Yes / No / Not sure | T2_SC_output_debugging |
| Verification and Testing | Which input best tests empty-line handling? | A. "u1,python\\n" / B. "u1,python\\n\\nu2,ai\\n" / C. Empty file | T2_SC_verification_testing |
| Responsibility and Supervision | If the code may keep old output in the file, can it be submitted directly? | Can submit / Cannot submit / Not sure | T2_SC_responsibility |

### Formal Questions

Q6. Does this AI-generated answer fully satisfy the task requirements?
A. Yes
B. No

Q7. Can this AI-generated answer be submitted directly?
A. Can submit
B. Cannot submit

If the input file content is:
\`\`\`text
u1,python

u2,ai
\`\`\`

Q8. What is the AI code most likely to do?
A. Return {"python": 1, "ai": 1}
B. Return {"python": 1, "": 1, "ai": 1}
C. Return {"python": 1}
D. Raise an error

Q9. According to the task requirements, what should the correct returned dictionary be?
A. {"python": 1, "ai": 1}
B. {"python": 1, "": 1, "ai": 1}
C. {"ai": 2}
D. 0

Q10. Which group of problems does this AI-generated answer have?
A. Only missing encoding
B. It does not correctly skip empty lines, uses append mode, and does not sort output
C. It does not use a dictionary
D. It has no problem

## Task 3: Student Profile and Score Report

### Task Requirements

\`\`\`python
build_score_report(profile_path, scores)
\`\`\`

1. profile_path points to a student profile file.
2. Each line has the format: student_id,name.
3. Empty lines should be skipped.
4. scores is a dictionary in the format {student_id: score}.
5. If a student has no score, the score should be 0.
6. Return a list of dictionaries: {"id": student_id, "name": name, "score": score}.
7. The returned list should be sorted by student_id in ascending order.

### AI-Generated Answer

\`\`\`python
def build_score_report(profile_path, scores):
    result = []
    with open(profile_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid, name = line.split(",")
            result.append({
                "id": sid,
                "name": name,
                "score": scores.get(sid, 0)
            })
    return sorted(result, key=lambda x: x["id"])
\`\`\`

### Formal Questions

Q11. Does this AI-generated answer fully satisfy the task requirements?
A. Yes
B. No

Q12. Can this AI-generated answer be submitted directly?
A. Can submit
B. Cannot submit

If the profile file content is:
\`\`\`text
s2,Bob
s1,Ana
\`\`\`
and scores = {"s1": 90}

Q13. What will the AI code return?
A. [{"id": "s1", "name": "Ana", "score": 90}, {"id": "s2", "name": "Bob", "score": 0}]
B. [{"id": "s2", "name": "Bob", "score": 0}, {"id": "s1", "name": "Ana", "score": 90}]
C. Error
D. {"s1": 90, "s2": 0}

Q14. According to the task requirements, what should the correct return value be?
A. [{"id": "s1", "name": "Ana", "score": 90}, {"id": "s2", "name": "Bob", "score": 0}]
B. [{"id": "s2", "name": "Bob", "score": 0}, {"id": "s1", "name": "Ana", "score": 90}]
C. Error
D. None

Q15. What is the main problem with this AI-generated answer?
A. It does not handle empty lines
B. It does not handle missing scores
C. It does not sort
D. It has no problem

## Task 4: NumPy Array Standardization

### Task Requirements

\`\`\`python
standardize_scores(arr)
\`\`\`

1. arr is a NumPy array.
2. The array may contain np.nan.
3. np.nan should be ignored when calculating mean and standard deviation.
4. If the standard deviation after ignoring np.nan is 0, valid positions should return 0, while original np.nan positions should remain np.nan.
5. Otherwise return the standardized result: (arr - mean) / std.
6. Return the result rounded to two decimal places.

### AI-Generated Answer

\`\`\`python
import numpy as np

def standardize_scores(arr):
    mean = np.mean(arr)
    std = np.std(arr)
    return np.round((arr - mean) / std, 2)
\`\`\`

### Formal Questions

Q16. Does this AI-generated answer fully satisfy the task requirements?
A. Yes
B. No

Q17. Can this AI-generated answer be submitted directly?
A. Can submit
B. Cannot submit

Given:
\`\`\`python
arr = np.array([1.0, 2.0, np.nan])
standardize_scores(arr)
\`\`\`

Q18. What will the AI code most likely return?
A. array([-1.0, 1.0, nan])
B. array([nan, nan, nan])
C. array([0.0, 0.0, nan])
D. Error

Q19. According to the task requirements, what should the correct return value be?
A. array([-1.0, 1.0, nan])
B. array([nan, nan, nan])
C. array([0.0, 0.0, nan])
D. array([1.0, 2.0, nan])

Q20. What is the main problem with this AI-generated answer?
A. It does not use NumPy
B. It does not ignore np.nan and does not handle the zero-standard-deviation case
C. The standardization formula is reversed
D. It has no problem

## Task 5: NumPy and Dictionary Category Revenue

### Task Requirements

\`\`\`python
category_revenue(prices, quantities, categories)
\`\`\`

1. prices is a one-dimensional NumPy array of product prices.
2. quantities is a one-dimensional NumPy array of product sales quantities.
3. categories is a dictionary in the format {product_index: category_name}.
4. Each product's revenue is price multiplied by quantity.
5. Return a dictionary that summarizes total revenue for each category.
6. Each category amount should be rounded to two decimal places.

### AI-Generated Answer

\`\`\`python
def category_revenue(prices, quantities, categories):
    revenue = prices * quantities
    totals = {}
    for i, r in enumerate(revenue):
        cat = categories[i]
        totals[cat] = totals.get(cat, 0) + r
    return {k: round(float(v), 2) for k, v in totals.items()}
\`\`\`

### Formal Questions

Q21. Does this AI-generated answer fully satisfy the task requirements?
A. Yes
B. No

Q22. Can this AI-generated answer be submitted directly?
A. Can submit
B. Cannot submit

Given:
\`\`\`python
prices = np.array([10, 20, 5])
quantities = np.array([2, 1, 4])
categories = {0: "A", 1: "B", 2: "A"}
\`\`\`

Q23. What will the AI code return?
A. {"A": 40.0, "B": 20.0}
B. {"A": 15.0, "B": 20.0}
C. {"A": 20.0, "B": 20.0}
D. Error

Q24. According to the task requirements, what should the correct return value be?
A. {"A": 40.0, "B": 20.0}
B. {"A": 15.0, "B": 20.0}
C. {"A": 20.0, "B": 20.0}
D. None

Q25. What is the main problem with this AI-generated answer?
A. It does not perform element-wise multiplication
B. It does not accumulate by category
C. It does not round to two decimal places
D. It has no problem

## Task 6: File, Dictionary, and NumPy Integrated Summary

### Task Requirements

\`\`\`python
monthly_product_summary(csv_path, category_map)
\`\`\`

1. The input file has no header.
2. Each line has the format: month,product_id,units,price.
3. Empty lines should be skipped.
4. category_map is a dictionary in the format {product_id: category}.
5. If product_id is not in category_map, return "Invalid data" immediately.
6. If units or price is negative, return "Invalid data" immediately.
7. Use NumPy to calculate revenue for each row: units multiplied by price.
8. Return a dictionary that summarizes total revenue for each category.
9. Amounts should be rounded to two decimal places.

### AI-Generated Answer

\`\`\`python
import numpy as np

def monthly_product_summary(csv_path, category_map):
    categories = []
    units = []
    prices = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            month, pid, u, p = line.strip().split(",")
            categories.append(category_map.get(pid, "Unknown"))
            units.append(int(u))
            prices.append(float(p))
    revenue = np.array(units) + np.array(prices)
    result = {}
    for cat, r in zip(categories, revenue):
        result[cat] = result.get(cat, 0) + r
    return {k: round(v, 2) for k, v in result.items()}
\`\`\`

### Formal Questions

Q26. Does this AI-generated answer fully satisfy the task requirements?
A. Yes
B. No

Q27. Can this AI-generated answer be submitted directly?
A. Can submit
B. Cannot submit

If the input file content is:
\`\`\`text
2024-01,P1,2,10
2024-01,P2,3,5
\`\`\`
and category_map = {"P1": "book", "P2": "food"}

Q28. What will the AI code return?
A. {"book": 20.0, "food": 15.0}
B. {"book": 12.0, "food": 8.0}
C. {"book": 10.0, "food": 5.0}
D. "Invalid data"

Q29. According to the task requirements, what should the correct return value be?
A. {"book": 20.0, "food": 15.0}
B. {"book": 12.0, "food": 8.0}
C. {"book": 10.0, "food": 5.0}
D. "Invalid data"

Q30. Which group of problems does this AI-generated answer have?
A. Revenue uses addition instead of multiplication; unknown products and negative values also do not return "Invalid data" as required
B. It only should not use NumPy
C. It only does not skip empty lines
D. It has no problem

## Answer Key

Do not show this section to participants.

| Question | Answer |
|---|---|
| Q1 | B |
| Q2 | B |
| Q3 | B |
| Q4 | A |
| Q5 | B |
| Q6 | B |
| Q7 | B |
| Q8 | D |
| Q9 | A |
| Q10 | B |
| Q11 | A |
| Q12 | A |
| Q13 | A |
| Q14 | A |
| Q15 | D |
| Q16 | B |
| Q17 | B |
| Q18 | B |
| Q19 | A |
| Q20 | B |
| Q21 | A |
| Q22 | A |
| Q23 | A |
| Q24 | A |
| Q25 | D |
| Q26 | B |
| Q27 | B |
| Q28 | B |
| Q29 | A |
| Q30 | A |

## Scoring Rules

| Score field | Questions | Max score |
|---|---|---|
| total_score | Q1-Q30 | 30 |
| deliverability_score | Q1, Q2, Q6, Q7, Q11, Q12, Q16, Q17, Q21, Q22, Q26, Q27 | 12 |
| reasoning_score | Q3, Q4, Q8, Q9, Q13, Q14, Q18, Q19, Q23, Q24, Q28, Q29 | 12 |
| error_identification_score | Q5, Q10, Q15, Q20, Q25, Q30 | 6 |
| t1_supervision_card_score | T1 supervision card items | 5 |
| t2_supervision_card_score | T2 supervision card items | 5 |
| supervision_card_score | Task 1 and Task 2 supervision cards | 10 |

## Recommended Export Columns

\`\`\`text
participant_id
group
start_time
pretest_submit_time
task1_start_time
task1_submit_time
task2_start_time
task2_submit_time
task3_start_time
task3_submit_time
task4_start_time
task4_submit_time
task5_start_time
task5_submit_time
task6_start_time
task6_submit_time
end_time
total_duration_seconds
task1_duration_seconds
task2_duration_seconds
task3_duration_seconds
task4_duration_seconds
task5_duration_seconds
task6_duration_seconds
Q1
Q2
Q3
Q4
Q5
Q6
Q7
Q8
Q9
Q10
Q11
Q12
Q13
Q14
Q15
Q16
Q17
Q18
Q19
Q20
Q21
Q22
Q23
Q24
Q25
Q26
Q27
Q28
Q29
Q30
Q1_score
Q2_score
Q3_score
Q4_score
Q5_score
Q6_score
Q7_score
Q8_score
Q9_score
Q10_score
Q11_score
Q12_score
Q13_score
Q14_score
Q15_score
Q16_score
Q17_score
Q18_score
Q19_score
Q20_score
Q21_score
Q22_score
Q23_score
Q24_score
Q25_score
Q26_score
Q27_score
Q28_score
Q29_score
Q30_score
total_score
deliverability_score
reasoning_score
error_identification_score
T1_SC_problem_definition
T1_SC_code_understanding
T1_SC_output_debugging
T1_SC_verification_testing
T1_SC_responsibility
T2_SC_problem_definition
T2_SC_code_understanding
T2_SC_output_debugging
T2_SC_verification_testing
T2_SC_responsibility
t1_supervision_card_score
t2_supervision_card_score
supervision_card_score
\`\`\`
`;

const answerKeyCsv = [
  ["question_id", "correct_answer", "score_category"],
  ["Q1", "B", "deliverability_score"],
  ["Q2", "B", "deliverability_score"],
  ["Q3", "B", "reasoning_score"],
  ["Q4", "A", "reasoning_score"],
  ["Q5", "B", "error_identification_score"],
  ["Q6", "B", "deliverability_score"],
  ["Q7", "B", "deliverability_score"],
  ["Q8", "D", "reasoning_score"],
  ["Q9", "A", "reasoning_score"],
  ["Q10", "B", "error_identification_score"],
  ["Q11", "A", "deliverability_score"],
  ["Q12", "A", "deliverability_score"],
  ["Q13", "A", "reasoning_score"],
  ["Q14", "A", "reasoning_score"],
  ["Q15", "D", "error_identification_score"],
  ["Q16", "B", "deliverability_score"],
  ["Q17", "B", "deliverability_score"],
  ["Q18", "B", "reasoning_score"],
  ["Q19", "A", "reasoning_score"],
  ["Q20", "B", "error_identification_score"],
  ["Q21", "A", "deliverability_score"],
  ["Q22", "A", "deliverability_score"],
  ["Q23", "A", "reasoning_score"],
  ["Q24", "A", "reasoning_score"],
  ["Q25", "D", "error_identification_score"],
  ["Q26", "B", "deliverability_score"],
  ["Q27", "B", "deliverability_score"],
  ["Q28", "B", "reasoning_score"],
  ["Q29", "A", "reasoning_score"],
  ["Q30", "A", "error_identification_score"],
];

const docResult = await tool("manage.create_file", {
  title: "AI监督AB问卷搭建稿",
  file_type: "doc",
});
const docPayload = docResult.content?.[0]?.text
  ? JSON.parse(docResult.content[0].text)
  : docResult;
const docFileId = docPayload.file_id;
if (!docFileId) {
  throw new Error(`Doc creation returned no file_id: ${JSON.stringify(docResult)}`);
}

await tool("doc.insert_markdown", {
  file_id: docFileId,
  index: 0,
  base64_markdown: Buffer.from(questionnaireMarkdown, "utf8").toString("base64"),
});

const formResult = await tool("manage.create_file", {
  title: "AI监督AB问卷",
  file_type: "form",
});
const formPayload = formResult.content?.[0]?.text
  ? JSON.parse(formResult.content[0].text)
  : formResult;

const sheetResult = await tool("manage.create_file", {
  title: "AI监督AB评分表",
  file_type: "sheet",
});
const sheetPayload = sheetResult.content?.[0]?.text
  ? JSON.parse(sheetResult.content[0].text)
  : sheetResult;

fs.mkdirSync("tmp", { recursive: true });
fs.writeFileSync(
  "tmp/tencent-questionnaire-assets.json",
  JSON.stringify(
    {
      doc: docPayload,
      form: formPayload,
      sheet: sheetPayload,
      answer_key_rows: answerKeyCsv.length,
    },
    null,
    2
  )
);

console.log(
  JSON.stringify(
    {
      doc: {
        title: docPayload.title,
        file_id: docPayload.file_id,
        url: docPayload.url,
        error: docPayload.error,
      },
      form: {
        title: formPayload.title,
        file_id: formPayload.file_id,
        url: formPayload.url,
        error: formPayload.error,
      },
      sheet: {
        title: sheetPayload.title,
        file_id: sheetPayload.file_id,
        url: sheetPayload.url,
        error: sheetPayload.error,
      },
    },
    null,
    2
  )
);
