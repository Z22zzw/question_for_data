from __future__ import annotations

from copy import deepcopy

ANSWER_KEY = {
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

DELIVERABILITY_QUESTIONS = {
    "Q1",
    "Q2",
    "Q6",
    "Q7",
    "Q11",
    "Q12",
    "Q16",
    "Q17",
    "Q21",
    "Q22",
    "Q26",
    "Q27",
}
REASONING_QUESTIONS = {
    "Q3",
    "Q4",
    "Q8",
    "Q9",
    "Q13",
    "Q14",
    "Q18",
    "Q19",
    "Q23",
    "Q24",
    "Q28",
    "Q29",
}
ERROR_IDENTIFICATION_QUESTIONS = {"Q5", "Q10", "Q15", "Q20", "Q25", "Q30"}

SUPERVISION_KEY = {
    "T1_SC_problem_definition": "Yes",
    "T1_SC_code_understanding": "Yes",
    "T1_SC_output_debugging": "Yes",
    "T1_SC_verification_testing": "B",
    "T1_SC_responsibility": "Cannot submit",
    "T2_SC_problem_definition": "Yes",
    "T2_SC_code_understanding": "Cannot",
    "T2_SC_output_debugging": "Yes",
    "T2_SC_verification_testing": "B",
    "T2_SC_responsibility": "Cannot submit",
}

LIKERT_VALUES = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
LIKERT_LABELS_ZH = ["非常不同意", "不同意", "一般", "同意", "非常同意"]

POSTTEST_SECTIONS = [
    {
        "id": "attitude",
        "title": {"en": "Attitudes toward AI Code Supervision", "zh": "对 AI 代码监督的态度"},
        "question_ids": [
            "post_attitude_useful",
            "post_attitude_confident",
            "post_attitude_learning_value",
            "post_attitude_cognitive_load",
            "post_attitude_future_use",
        ],
    },
    {
        "id": "strategy",
        "title": {"en": "Supervision Strategies", "zh": "监督策略"},
        "question_ids": [
            "post_strategy_requirements_first",
            "post_strategy_trace_code",
            "post_strategy_predict_output",
            "post_strategy_test_cases",
            "post_strategy_delivery_risk",
        ],
    },
    {
        "id": "trust",
        "title": {"en": "Trust in AI-generated Code", "zh": "对 AI 代码的信任程度"},
        "question_ids": [
            "post_trust_ai_correctness",
            "post_trust_ai_boundary_cases",
            "post_trust_ai_direct_submit",
            "post_trust_ai_with_review",
            "post_trust_ai_overall",
        ],
    },
]

POSTTEST_QUESTIONS = [
    {
        "id": "post_attitude_useful",
        "section": "attitude",
        "prompt": {
            "en": "Reviewing AI-generated code is a useful skill for programming work.",
            "zh": "审查 AI 生成代码是一项有用的编程能力。",
        },
    },
    {
        "id": "post_attitude_confident",
        "section": "attitude",
        "prompt": {
            "en": "After this questionnaire, I feel more confident evaluating AI-generated code.",
            "zh": "完成本问卷后，我更有信心评估 AI 生成代码。",
        },
    },
    {
        "id": "post_attitude_learning_value",
        "section": "attitude",
        "prompt": {
            "en": "This task format helped me understand what code review requires.",
            "zh": "这种任务形式帮助我理解代码审查需要关注什么。",
        },
    },
    {
        "id": "post_attitude_cognitive_load",
        "section": "attitude",
        "prompt": {
            "en": "The tasks required a high level of mental effort.",
            "zh": "这些任务需要较高的认知投入。",
        },
    },
    {
        "id": "post_attitude_future_use",
        "section": "attitude",
        "prompt": {
            "en": "I would like to use similar checklists when reviewing AI-generated code in the future.",
            "zh": "未来审查 AI 代码时，我愿意使用类似检查清单。",
        },
    },
    {
        "id": "post_strategy_requirements_first",
        "section": "strategy",
        "prompt": {
            "en": "When reviewing AI code, I first compare it against the task requirements.",
            "zh": "审查 AI 代码时，我会先对照任务要求。",
        },
    },
    {
        "id": "post_strategy_trace_code",
        "section": "strategy",
        "prompt": {
            "en": "I trace the actual code logic instead of only reading the surface structure.",
            "zh": "我会追踪代码的实际逻辑，而不只是看表面结构。",
        },
    },
    {
        "id": "post_strategy_predict_output",
        "section": "strategy",
        "prompt": {
            "en": "I predict outputs for concrete inputs to check AI-generated code.",
            "zh": "我会用具体输入预测输出来检查 AI 代码。",
        },
    },
    {
        "id": "post_strategy_test_cases",
        "section": "strategy",
        "prompt": {
            "en": "I design edge cases or counterexamples to test AI-generated code.",
            "zh": "我会设计边界用例或反例来测试 AI 代码。",
        },
    },
    {
        "id": "post_strategy_delivery_risk",
        "section": "strategy",
        "prompt": {
            "en": "Before submitting AI-generated code, I consider delivery risk and responsibility.",
            "zh": "提交 AI 代码前，我会考虑交付风险和责任。",
        },
    },
    {
        "id": "post_trust_ai_correctness",
        "section": "trust",
        "prompt": {
            "en": "I generally trust AI-generated code to be correct for ordinary programming tasks.",
            "zh": "对于普通编程任务，我总体信任 AI 生成代码的正确性。",
        },
    },
    {
        "id": "post_trust_ai_boundary_cases",
        "section": "trust",
        "prompt": {
            "en": "I trust AI-generated code to handle boundary cases well.",
            "zh": "我信任 AI 生成代码能较好处理边界情况。",
        },
    },
    {
        "id": "post_trust_ai_direct_submit",
        "section": "trust",
        "prompt": {
            "en": "If AI-generated code looks reasonable, I would submit it without detailed review.",
            "zh": "如果 AI 生成代码看起来合理，我会不经详细审查直接提交。",
        },
    },
    {
        "id": "post_trust_ai_with_review",
        "section": "trust",
        "prompt": {
            "en": "With careful human review, AI-generated code can be reliable.",
            "zh": "经过认真人工审查后，AI 生成代码可以是可靠的。",
        },
    },
    {
        "id": "post_trust_ai_overall",
        "section": "trust",
        "prompt": {
            "en": "Overall, I trust AI tools as programming assistants.",
            "zh": "总体而言，我信任 AI 工具作为编程助手。",
        },
    },
]

POSTTEST_FIELDS = [question["id"] for question in POSTTEST_QUESTIONS]

PRETEST_FIELDS = [
    "consent",
    "questionnaire_version",
    "grade_year",
    "major",
    "programming_experience_years",
    "python_familiarity",
    "file_io_familiarity",
    "numpy_familiarity",
    "ai_tool_use_frequency",
    "ai_code_review_experience",
]


def choice(label: str, text: str) -> dict:
    return {"label": label, "text": text}


TASKS = [
    {
        "id": 1,
        "title": "Task 1: Dictionary Price Lookup and Order Total",
        "requirements": [
            "calculate_order_total(items, price_table, vip=False)",
            "items is a dictionary in the format {product_id: quantity}.",
            "price_table is a dictionary in the format {product_id: unit_price}.",
            'If items contains a product ID not in price_table, return "Unknown item".',
            "Apply a 10% VIP discount before shipping.",
            "If discounted subtotal is greater than 100, shipping is free; otherwise shipping is 8.",
            "Return the final amount rounded to two decimal places.",
        ],
        "code": """def calculate_order_total(items, price_table, vip=False):
    subtotal = 0
    for pid, qty in items.items():
        subtotal += price_table.get(pid, 0) * qty
    if vip:
        subtotal *= 0.9
    if subtotal > 100:
        shipping = 0
    else:
        shipping = 8
    return round(subtotal + shipping, 2)""",
        "supervision_card": [
            {
                "id": "T1_SC_problem_definition",
                "dimension": "Problem Definition",
                "prompt": 'Does the task require returning "Unknown item" for an unknown product ID?',
                "options": ["Yes", "No", "Not sure"],
            },
            {
                "id": "T1_SC_code_understanding",
                "dimension": "AI Code Understanding",
                "prompt": "Does price_table.get(pid, 0) treat an unknown product as price 0?",
                "options": ["Yes", "No", "Not sure"],
            },
            {
                "id": "T1_SC_output_debugging",
                "dimension": "AI Output Debugging",
                "prompt": 'For items={"A":2,"X":1}, will X be silently ignored by the AI code?',
                "options": ["Yes", "No", "Not sure"],
            },
            {
                "id": "T1_SC_verification_testing",
                "dimension": "Verification and Testing",
                "prompt": "Which input best reveals the unknown-product problem?",
                "options": ['A. {"A":2}', 'B. {"X":1}', 'C. {"A":20}'],
                "values": ["A", "B", "C"],
            },
            {
                "id": "T1_SC_responsibility",
                "dimension": "Responsibility and Supervision",
                "prompt": "If an unknown product is treated as 0 yuan, can this code be submitted directly?",
                "options": ["Can submit", "Cannot submit", "Not sure"],
            },
        ],
        "questions": [
            {
                "id": "Q1",
                "prompt": "Does this AI-generated answer fully satisfy the task requirements?",
                "options": [choice("A", "Yes"), choice("B", "No")],
            },
            {
                "id": "Q2",
                "prompt": "Can this AI-generated answer be submitted directly?",
                "options": [choice("A", "Can submit"), choice("B", "Cannot submit")],
            },
            {
                "id": "Q3",
                "context": 'Given price_table={"A":10,"B":50}, items={"A":2,"X":1}, vip=False.',
                "prompt": "What will the AI code return?",
                "options": [choice("A", '"Unknown item"'), choice("B", "28.0"), choice("C", "20.0"), choice("D", "Error")],
            },
            {
                "id": "Q4",
                "prompt": "According to the task requirements, what should the correct return value be?",
                "options": [choice("A", '"Unknown item"'), choice("B", "28.0"), choice("C", "20.0"), choice("D", "8.0")],
            },
            {
                "id": "Q5",
                "prompt": "What is the main problem with this AI-generated answer?",
                "options": [
                    choice("A", "The VIP discount is calculated incorrectly"),
                    choice("B", "Unknown product IDs are treated as price 0"),
                    choice("C", "It does not round to two decimal places"),
                    choice("D", "The shipping rule is completely reversed"),
                ],
            },
        ],
    },
    {
        "id": 2,
        "title": "Task 2: File I/O and Tag Counting",
        "requirements": [
            "count_tags(input_path, output_path)",
            "Each input line has the format user,tag.",
            "Empty lines should be skipped.",
            "Spaces before and after tag should be stripped.",
            "Return a dictionary of tag counts.",
            "Write tag,count lines sorted alphabetically by tag.",
            "Overwrite the output file instead of appending.",
        ],
        "code": """def count_tags(input_path, output_path):
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
    return counts""",
        "supervision_card": [
            {
                "id": "T2_SC_problem_definition",
                "dimension": "Problem Definition",
                "prompt": "Does the task require empty lines to be skipped?",
                "options": ["Yes", "No", "Not sure"],
            },
            {
                "id": "T2_SC_code_understanding",
                "dimension": "AI Code Understanding",
                "prompt": 'Can if line == "" skip an empty line represented as "\\n" in a file?',
                "options": ["Can", "Cannot", "Not sure"],
            },
            {
                "id": "T2_SC_output_debugging",
                "dimension": "AI Output Debugging",
                "prompt": 'When an empty line is encountered, can user, tag = line.split(",") raise an error?',
                "options": ["Yes", "No", "Not sure"],
            },
            {
                "id": "T2_SC_verification_testing",
                "dimension": "Verification and Testing",
                "prompt": "Which input best tests empty-line handling?",
                "options": ['A. "u1,python\\n"', 'B. "u1,python\\n\\nu2,ai\\n"', "C. Empty file"],
                "values": ["A", "B", "C"],
            },
            {
                "id": "T2_SC_responsibility",
                "dimension": "Responsibility and Supervision",
                "prompt": "If the code may keep old output in the file, can it be submitted directly?",
                "options": ["Can submit", "Cannot submit", "Not sure"],
            },
        ],
        "questions": [
            {"id": "Q6", "prompt": "Does this AI-generated answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q7", "prompt": "Can this AI-generated answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {
                "id": "Q8",
                "context": "Input file content: u1,python then an empty line then u2,ai.",
                "prompt": "What is the AI code most likely to do?",
                "options": [
                    choice("A", 'Return {"python": 1, "ai": 1}'),
                    choice("B", 'Return {"python": 1, "": 1, "ai": 1}'),
                    choice("C", 'Return {"python": 1}'),
                    choice("D", "Raise an error"),
                ],
            },
            {
                "id": "Q9",
                "prompt": "According to the task requirements, what should the correct returned dictionary be?",
                "options": [choice("A", '{"python": 1, "ai": 1}'), choice("B", '{"python": 1, "": 1, "ai": 1}'), choice("C", '{"ai": 2}'), choice("D", "0")],
            },
            {
                "id": "Q10",
                "prompt": "Which group of problems does this AI-generated answer have?",
                "options": [
                    choice("A", "Only missing encoding"),
                    choice("B", "It does not correctly skip empty lines, uses append mode, and does not sort output"),
                    choice("C", "It does not use a dictionary"),
                    choice("D", "It has no problem"),
                ],
            },
        ],
    },
]


def short_task(task_id: int, title: str, code: str, questions: list[dict], requirements: list[str]) -> dict:
    return {"id": task_id, "title": title, "requirements": requirements, "code": code, "supervision_card": None, "questions": questions}


TASKS.extend(
    [
        short_task(
            3,
            "Task 3: Student Profile and Score Report",
            """def build_score_report(profile_path, scores):
    result = []
    with open(profile_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid, name = line.split(",")
            result.append({"id": sid, "name": name, "score": scores.get(sid, 0)})
    return sorted(result, key=lambda x: x["id"])""",
            [
                {"id": "Q11", "prompt": "Does this AI-generated answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
                {"id": "Q12", "prompt": "Can this AI-generated answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
                {"id": "Q13", "context": 'Profile file: s2,Bob then s1,Ana. scores={"s1":90}.', "prompt": "What will the AI code return?", "options": [choice("A", '[{"id":"s1","name":"Ana","score":90},{"id":"s2","name":"Bob","score":0}]'), choice("B", '[{"id":"s2","name":"Bob","score":0},{"id":"s1","name":"Ana","score":90}]'), choice("C", "Error"), choice("D", '{"s1":90,"s2":0}')]},
                {"id": "Q14", "prompt": "According to the task requirements, what should the correct return value be?", "options": [choice("A", '[{"id":"s1","name":"Ana","score":90},{"id":"s2","name":"Bob","score":0}]'), choice("B", '[{"id":"s2","name":"Bob","score":0},{"id":"s1","name":"Ana","score":90}]'), choice("C", "Error"), choice("D", "None")]},
                {"id": "Q15", "prompt": "What is the main problem with this AI-generated answer?", "options": [choice("A", "It does not handle empty lines"), choice("B", "It does not handle missing scores"), choice("C", "It does not sort"), choice("D", "It has no problem")]},
            ],
            [
                "Read student_id,name rows from a profile file.",
                "Skip empty lines.",
                "Use score 0 when a student is missing from scores.",
                "Return dictionaries sorted by student_id ascending.",
            ],
        ),
        short_task(
            4,
            "Task 4: NumPy Array Standardization",
            """import numpy as np

def standardize_scores(arr):
    mean = np.mean(arr)
    std = np.std(arr)
    return np.round((arr - mean) / std, 2)""",
            [
                {"id": "Q16", "prompt": "Does this AI-generated answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
                {"id": "Q17", "prompt": "Can this AI-generated answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
                {"id": "Q18", "context": "arr = np.array([1.0, 2.0, np.nan])", "prompt": "What will the AI code most likely return?", "options": [choice("A", "array([-1.0, 1.0, nan])"), choice("B", "array([nan, nan, nan])"), choice("C", "array([0.0, 0.0, nan])"), choice("D", "Error")]},
                {"id": "Q19", "prompt": "According to the task requirements, what should the correct return value be?", "options": [choice("A", "array([-1.0, 1.0, nan])"), choice("B", "array([nan, nan, nan])"), choice("C", "array([0.0, 0.0, nan])"), choice("D", "array([1.0, 2.0, nan])")]},
                {"id": "Q20", "prompt": "What is the main problem with this AI-generated answer?", "options": [choice("A", "It does not use NumPy"), choice("B", "It does not ignore np.nan and does not handle zero standard deviation"), choice("C", "The standardization formula is reversed"), choice("D", "It has no problem")]},
            ],
            ["Ignore np.nan for mean and standard deviation.", "Preserve original np.nan positions.", "Handle zero standard deviation by returning 0 for valid positions.", "Round to two decimal places."],
        ),
        short_task(
            5,
            "Task 5: NumPy and Dictionary Category Revenue",
            """def category_revenue(prices, quantities, categories):
    revenue = prices * quantities
    totals = {}
    for i, r in enumerate(revenue):
        cat = categories[i]
        totals[cat] = totals.get(cat, 0) + r
    return {k: round(float(v), 2) for k, v in totals.items()}""",
            [
                {"id": "Q21", "prompt": "Does this AI-generated answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
                {"id": "Q22", "prompt": "Can this AI-generated answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
                {"id": "Q23", "context": 'prices=[10,20,5], quantities=[2,1,4], categories={0:"A",1:"B",2:"A"}.', "prompt": "What will the AI code return?", "options": [choice("A", '{"A":40.0,"B":20.0}'), choice("B", '{"A":15.0,"B":20.0}'), choice("C", '{"A":20.0,"B":20.0}'), choice("D", "Error")]},
                {"id": "Q24", "prompt": "According to the task requirements, what should the correct return value be?", "options": [choice("A", '{"A":40.0,"B":20.0}'), choice("B", '{"A":15.0,"B":20.0}'), choice("C", '{"A":20.0,"B":20.0}'), choice("D", "None")]},
                {"id": "Q25", "prompt": "What is the main problem with this AI-generated answer?", "options": [choice("A", "It does not perform element-wise multiplication"), choice("B", "It does not accumulate by category"), choice("C", "It does not round to two decimal places"), choice("D", "It has no problem")]},
            ],
            ["Compute product revenue as price * quantity.", "Aggregate revenue by category.", "Round each category total to two decimal places."],
        ),
        short_task(
            6,
            "Task 6: File, Dictionary, and NumPy Integrated Summary",
            """import numpy as np

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
    return {k: round(v, 2) for k, v in result.items()}""",
            [
                {"id": "Q26", "prompt": "Does this AI-generated answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
                {"id": "Q27", "prompt": "Can this AI-generated answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
                {"id": "Q28", "context": 'Rows: 2024-01,P1,2,10 and 2024-01,P2,3,5. category_map={"P1":"book","P2":"food"}.', "prompt": "What will the AI code return?", "options": [choice("A", '{"book":20.0,"food":15.0}'), choice("B", '{"book":12.0,"food":8.0}'), choice("C", '{"book":10.0,"food":5.0}'), choice("D", '"Invalid data"')]},
                {"id": "Q29", "prompt": "According to the task requirements, what should the correct return value be?", "options": [choice("A", '{"book":20.0,"food":15.0}'), choice("B", '{"book":12.0,"food":8.0}'), choice("C", '{"book":10.0,"food":5.0}'), choice("D", '"Invalid data"')]},
                {"id": "Q30", "prompt": "Which group of problems does this AI-generated answer have?", "options": [choice("A", 'Revenue uses addition instead of multiplication; unknown products and negative values do not return "Invalid data"'), choice("B", "It only should not use NumPy"), choice("C", "It only does not skip empty lines"), choice("D", "It has no problem")]},
            ],
            ["Skip empty lines.", 'Return "Invalid data" for unknown product IDs or negative units/prices.', "Use NumPy to calculate units * price.", "Aggregate by category and round to two decimal places."],
        ),
    ]
)


C_TASKS = [
    {
        "id": 1,
        "title": "C Task 1: Product Price Lookup and Order Total",
        "requirements": [
            "double calculate_total(int ids[], int qty[], int n, int price_ids[], double prices[], int m, int vip)",
            "For each product id in ids, find the matching id in price_ids.",
            'If any product id is not found, return -1 to mean "Unknown item".',
            "Apply a 10% VIP discount before shipping.",
            "If the discounted subtotal is greater than 100, shipping is free; otherwise shipping is 8.",
            "Return the final amount.",
        ],
        "code": """double calculate_total(int ids[], int qty[], int n, int price_ids[], double prices[], int m, int vip) {
    double subtotal = 0;
    for (int i = 0; i < n; i++) {
        double price = 0;
        for (int j = 0; j < m; j++) {
            if (price_ids[j] == ids[i]) {
                price = prices[j];
            }
        }
        subtotal += price * qty[i];
    }
    if (vip) subtotal *= 0.9;
    if (subtotal > 100) return subtotal;
    return subtotal + 8;
}""",
        "supervision_card": [
            {
                "id": "T1_SC_problem_definition",
                "dimension": "Problem Definition",
                "prompt": 'Does the task require returning -1 when a product id is unknown?',
                "options": ["Yes", "No", "Not sure"],
            },
            {
                "id": "T1_SC_code_understanding",
                "dimension": "AI Code Understanding",
                "prompt": "Does initializing price to 0 make an unknown product contribute 0 to subtotal?",
                "options": ["Yes", "No", "Not sure"],
            },
            {
                "id": "T1_SC_output_debugging",
                "dimension": "AI Output Debugging",
                "prompt": "For ids={1,9}, will id 9 be silently priced as 0?",
                "options": ["Yes", "No", "Not sure"],
            },
            {
                "id": "T1_SC_verification_testing",
                "dimension": "Verification and Testing",
                "prompt": "Which input best reveals the unknown-id problem?",
                "options": ["A. ids={1}", "B. ids={9}", "C. ids={1,1}"],
                "values": ["A", "B", "C"],
            },
            {
                "id": "T1_SC_responsibility",
                "dimension": "Responsibility and Supervision",
                "prompt": "If unknown ids are charged as 0, can this code be submitted directly?",
                "options": ["Can submit", "Cannot submit", "Not sure"],
            },
        ],
        "questions": [
            {"id": "Q1", "prompt": "Does this AI-generated C answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q2", "prompt": "Can this AI-generated C answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {
                "id": "Q3",
                "context": "Given ids={1,9}, qty={2,1}, price_ids={1,2}, prices={10,50}, vip=0.",
                "prompt": "What will the AI code return?",
                "options": [choice("A", "-1"), choice("B", "28"), choice("C", "20"), choice("D", "Compilation error")],
            },
            {"id": "Q4", "prompt": "According to the requirements, what should the correct return value be?", "options": [choice("A", "-1"), choice("B", "28"), choice("C", "20"), choice("D", "8")]},
            {"id": "Q5", "prompt": "What is the main problem with this AI-generated answer?", "options": [choice("A", "VIP discount is calculated incorrectly"), choice("B", "Unknown product ids are treated as price 0"), choice("C", "The shipping threshold is missing"), choice("D", "The loop never runs")]},
        ],
    },
    {
        "id": 2,
        "title": "C Task 2: File Line Counting and Output",
        "requirements": [
            "int count_nonempty_lines(const char *input_path, const char *output_path)",
            "Read all lines from the input file.",
            "Blank lines containing only a newline should be skipped.",
            "Return the number of non-empty lines.",
            "Write the count to output_path and overwrite any old content.",
        ],
        "code": """int count_nonempty_lines(const char *input_path, const char *output_path) {
    FILE *in = fopen(input_path, "r");
    char line[256];
    int count = 0;
    while (fgets(line, sizeof(line), in) != NULL) {
        if (strcmp(line, "") == 0) {
            continue;
        }
        count++;
    }
    FILE *out = fopen(output_path, "a");
    fprintf(out, "%d\\n", count);
    fclose(in);
    fclose(out);
    return count;
}""",
        "supervision_card": [
            {"id": "T2_SC_problem_definition", "dimension": "Problem Definition", "prompt": "Does the task require blank newline-only lines to be skipped?", "options": ["Yes", "No", "Not sure"]},
            {"id": "T2_SC_code_understanding", "dimension": "AI Code Understanding", "prompt": 'Can strcmp(line, "") skip a blank line read as "\\n"?', "options": ["Can", "Cannot", "Not sure"]},
            {"id": "T2_SC_output_debugging", "dimension": "AI Output Debugging", "prompt": "Will the code append to old output instead of overwriting it?", "options": ["Yes", "No", "Not sure"]},
            {"id": "T2_SC_verification_testing", "dimension": "Verification and Testing", "prompt": "Which input best tests blank-line handling?", "options": ['A. "a\\n"', 'B. "a\\n\\nb\\n"', "C. Empty file"], "values": ["A", "B", "C"]},
            {"id": "T2_SC_responsibility", "dimension": "Responsibility and Supervision", "prompt": "If old output is kept in the file, can this code be submitted directly?", "options": ["Can submit", "Cannot submit", "Not sure"]},
        ],
        "questions": [
            {"id": "Q6", "prompt": "Does this AI-generated C answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q7", "prompt": "Can this AI-generated C answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {"id": "Q8", "context": 'Input file content is "a\\n\\nb\\n".', "prompt": "What will the AI code return?", "options": [choice("A", "2"), choice("B", "1"), choice("C", "0"), choice("D", "3")]},
            {"id": "Q9", "prompt": "According to the requirements, what should the correct return value be?", "options": [choice("A", "2"), choice("B", "3"), choice("C", "1"), choice("D", "0")]},
            {"id": "Q10", "prompt": "Which group of problems does this answer have?", "options": [choice("A", "Only missing fclose"), choice("B", "It does not skip newline-only blank lines and uses append mode"), choice("C", "It cannot read files at all"), choice("D", "It has no problem")]},
        ],
    },
    short_task(
        3,
        "C Task 3: Student Score Report",
        """typedef struct { int id; char name[32]; int score; } Student;

void build_report(Student students[], int n, int scores[][2], int score_n) {
    for (int i = 0; i < n; i++) {
        students[i].score = 0;
        for (int j = 0; j < score_n; j++) {
            if (scores[j][0] == students[i].id) {
                students[i].score = scores[j][1];
            }
        }
    }
}""",
        [
            {"id": "Q11", "prompt": "Does this AI-generated C answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q12", "prompt": "Can this AI-generated C answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {"id": "Q13", "context": "students are [{id:2,name:Bob},{id:1,name:Ana}], scores={{1,90}}.", "prompt": "What will the AI code produce?", "options": [choice("A", "Bob has 0 and Ana has 90, original order unchanged"), choice("B", "Ana is moved before Bob"), choice("C", "Both scores become 90"), choice("D", "Compilation error")]},
            {"id": "Q14", "prompt": "According to the task requirements, what should the score values be?", "options": [choice("A", "Bob has 0 and Ana has 90"), choice("B", "Bob has 90 and Ana has 0"), choice("C", "Both scores become 0"), choice("D", "No scores should be assigned")]},
            {"id": "Q15", "prompt": "What is the main problem with this answer?", "options": [choice("A", "It has no problem"), choice("B", "It does not handle missing scores"), choice("C", "It changes names"), choice("D", "It cannot use structs")]},
        ],
        [
            "Fill each student's score from the scores table by id.",
            "Use score 0 when a student id is missing from scores.",
            "Keep the original student order.",
        ],
    ),
    short_task(
        4,
        "C Task 4: Array Average Excluding Sentinel Values",
        """double average_valid(int arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum / n;
}""",
        [
            {"id": "Q16", "prompt": "Does this AI-generated C answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q17", "prompt": "Can this AI-generated C answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {"id": "Q18", "context": "arr={2,4,-1}, n=3. -1 means invalid and should be ignored.", "prompt": "What will the AI code return in normal integer-division C behavior?", "options": [choice("A", "3.0"), choice("B", "1.0"), choice("C", "2.5"), choice("D", "Error")]},
            {"id": "Q19", "prompt": "According to the requirements, what should the correct return value be?", "options": [choice("A", "3.0"), choice("B", "1.0"), choice("C", "-1.0"), choice("D", "0.0")]},
            {"id": "Q20", "prompt": "What is the main problem with this answer?", "options": [choice("A", "It uses a loop"), choice("B", "It includes sentinel -1 and performs integer division"), choice("C", "It returns double"), choice("D", "It has no problem")]},
        ],
        ["Ignore values equal to -1.", "Return the average of valid values as double.", "If there are no valid values, return 0.0."],
    ),
    short_task(
        5,
        "C Task 5: Category Revenue Aggregation",
        """void category_revenue(double prices[], int qty[], int cat[], int n, double totals[], int cat_count) {
    for (int i = 0; i < cat_count; i++) totals[i] = 0;
    for (int i = 0; i < n; i++) {
        totals[cat[i]] += prices[i] * qty[i];
    }
}""",
        [
            {"id": "Q21", "prompt": "Does this AI-generated C answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q22", "prompt": "Can this AI-generated C answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {"id": "Q23", "context": "prices={10,20,5}, qty={2,1,4}, cat={0,1,0}, cat_count=2.", "prompt": "What totals will the AI code produce?", "options": [choice("A", "totals[0]=40, totals[1]=20"), choice("B", "totals[0]=15, totals[1]=20"), choice("C", "totals[0]=20, totals[1]=20"), choice("D", "Compilation error")]},
            {"id": "Q24", "prompt": "According to the requirements, what should the correct totals be?", "options": [choice("A", "totals[0]=40, totals[1]=20"), choice("B", "totals[0]=15, totals[1]=20"), choice("C", "totals[0]=20, totals[1]=20"), choice("D", "All totals should be 0")]},
            {"id": "Q25", "prompt": "What is the main problem with this answer?", "options": [choice("A", "It has no problem"), choice("B", "It does not multiply price and quantity"), choice("C", "It does not initialize totals"), choice("D", "It uses arrays")]},
        ],
        ["Compute revenue as price * quantity.", "Aggregate revenue by category index.", "Set every category total before accumulation."],
    ),
    short_task(
        6,
        "C Task 6: CSV Product Summary",
        """int summarize(FILE *fp, int ids[], int cats[], int product_n, double totals[], int cat_count) {
    int id, units;
    double price;
    for (int i = 0; i < cat_count; i++) totals[i] = 0;
    while (fscanf(fp, "%d,%d,%lf", &id, &units, &price) == 3) {
        int cat = -1;
        for (int i = 0; i < product_n; i++) {
            if (ids[i] == id) cat = cats[i];
        }
        if (cat >= 0) {
            totals[cat] += units + price;
        }
    }
    return 1;
}""",
        [
            {"id": "Q26", "prompt": "Does this AI-generated C answer fully satisfy the task requirements?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q27", "prompt": "Can this AI-generated C answer be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {"id": "Q28", "context": "Rows are 1,2,10 and 2,3,5. ids={1,2}, cats={0,1}.", "prompt": "What totals will the AI code produce?", "options": [choice("A", "totals[0]=20, totals[1]=15"), choice("B", "totals[0]=12, totals[1]=8"), choice("C", "totals[0]=10, totals[1]=5"), choice("D", "return 0")]},
            {"id": "Q29", "prompt": "According to the requirements, what should the correct totals be?", "options": [choice("A", "totals[0]=20, totals[1]=15"), choice("B", "totals[0]=12, totals[1]=8"), choice("C", "totals[0]=10, totals[1]=5"), choice("D", "return 0")]},
            {"id": "Q30", "prompt": "Which group of problems does this answer have?", "options": [choice("A", "Revenue uses addition instead of multiplication and unknown/negative data does not fail"), choice("B", "Only the loop condition is wrong"), choice("C", "Only totals are not initialized"), choice("D", "It has no problem")]},
        ],
        ["Each row has product_id,units,price.", "Return 0 if product id is unknown or units/price is negative.", "Compute units * price.", "Aggregate totals by category and return 1 on success."],
    ),
]

TASKS_BY_VERSION = {
    "python": TASKS,
    "c": C_TASKS,
}


def normalize_questionnaire_version(version: str | None) -> str:
    return "c" if version == "c" else "python"


def get_task(task_id: int, version: str = "python") -> dict:
    return TASKS_BY_VERSION[normalize_questionnaire_version(version)][task_id - 1]


def task_question_ids(task_id: int, version: str = "python") -> list[str]:
    return [question["id"] for question in get_task(task_id, version)["questions"]]


ZH_TASK_TEXT = {
    1: {
        "title": "任务 1：字典查价与订单总价",
        "requirements": [
            "calculate_order_total(items, price_table, vip=False)",
            "items 是字典，格式为 {商品ID: 数量}。",
            "price_table 是字典，格式为 {商品ID: 单价}。",
            '如果 items 中出现 price_table 不存在的商品 ID，应返回 "Unknown item"。',
            "如果 vip=True，小计享受 10% 折扣。",
            "折扣后小计如果大于 100，免运费；否则运费为 8。",
            "返回最终金额，保留两位小数。",
        ],
        "questions": {
            "Q1": "这份 AI 答案是否完全满足任务要求？",
            "Q2": "这份 AI 答案是否可以直接提交？",
            "Q3": "AI 代码会返回什么？",
            "Q4": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q5": "这份 AI 答案最主要的问题是什么？",
        },
        "contexts": {"Q3": '给定 price_table={"A":10,"B":50}, items={"A":2,"X":1}, vip=False。'},
        "supervision": {
            "T1_SC_problem_definition": '任务是否要求未知商品 ID 返回 "Unknown item"？',
            "T1_SC_code_understanding": "price_table.get(pid, 0) 是否会把未知商品价格当作 0？",
            "T1_SC_output_debugging": '对 items={"A":2,"X":1}，未知商品 X 是否会被 AI 代码静默忽略？',
            "T1_SC_verification_testing": "哪个输入最能暴露未知商品问题？",
            "T1_SC_responsibility": "如果未知商品被当作 0 元处理，这份代码是否可直接提交？",
        },
    },
    2: {
        "title": "任务 2：文件读写与标签计数",
        "requirements": [
            "count_tags(input_path, output_path)",
            "输入文件中每一行格式为：user,tag。",
            "空行应被跳过。",
            "tag 前后的空格应被去掉。",
            "统计每个 tag 出现次数，并返回字典。",
            "将结果写入 output_path，格式为 tag,count。",
            "输出文件应按 tag 字母顺序排序，并覆盖旧内容。",
        ],
        "questions": {
            "Q6": "这份 AI 答案是否完全满足任务要求？",
            "Q7": "这份 AI 答案是否可以直接提交？",
            "Q8": "AI 代码最可能发生什么？",
            "Q9": "根据任务要求，上述输入的正确返回字典应该是什么？",
            "Q10": "这份 AI 答案的问题包括哪一组？",
        },
        "contexts": {"Q8": "输入文件内容为：u1,python，然后一个空行，然后 u2,ai。"},
        "supervision": {
            "T2_SC_problem_definition": "任务是否要求空行应被跳过？",
            "T2_SC_code_understanding": 'if line == "" 能否跳过文件中的空行 "\\n"？',
            "T2_SC_output_debugging": '遇到空行时，user, tag = line.split(",") 是否可能报错？',
            "T2_SC_verification_testing": "哪个输入最能测试空行处理？",
            "T2_SC_responsibility": "如果代码可能把旧输出保留在文件中，这份代码是否可直接提交？",
        },
    },
    3: {
        "title": "任务 3：学生档案与成绩合并",
        "requirements": [
            "读取 student_id,name 格式的学生档案文件。",
            "空行应被跳过。",
            "scores 中缺失的学生成绩记为 0。",
            "返回按 student_id 升序排列的字典列表。",
        ],
        "questions": {
            "Q11": "这份 AI 答案是否完全满足任务要求？",
            "Q12": "这份 AI 答案是否可以直接提交？",
            "Q13": "AI 代码会返回什么？",
            "Q14": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q15": "这份 AI 答案最主要的问题是什么？",
        },
        "contexts": {"Q13": '档案文件：s2,Bob 然后 s1,Ana。scores={"s1":90}。'},
    },
    4: {
        "title": "任务 4：NumPy 数组标准化",
        "requirements": [
            "计算均值和标准差时应忽略 np.nan。",
            "原本为 np.nan 的位置仍保留 np.nan。",
            "如果忽略 np.nan 后标准差为 0，则有效位置返回 0。",
            "返回结果保留两位小数。",
        ],
        "questions": {
            "Q16": "这份 AI 答案是否完全满足任务要求？",
            "Q17": "这份 AI 答案是否可以直接提交？",
            "Q18": "AI 代码最可能返回什么？",
            "Q19": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q20": "这份 AI 答案最主要的问题是什么？",
        },
        "contexts": {"Q18": "arr = np.array([1.0, 2.0, np.nan])"},
    },
    5: {
        "title": "任务 5：NumPy 与字典分类汇总",
        "requirements": [
            "每个商品销售额为 price * quantity。",
            "按类别汇总销售额。",
            "每个类别金额保留两位小数。",
        ],
        "questions": {
            "Q21": "这份 AI 答案是否完全满足任务要求？",
            "Q22": "这份 AI 答案是否可以直接提交？",
            "Q23": "AI 代码会返回什么？",
            "Q24": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q25": "这份 AI 答案最主要的问题是什么？",
        },
        "contexts": {"Q23": 'prices=[10,20,5], quantities=[2,1,4], categories={0:"A",1:"B",2:"A"}。'},
    },
    6: {
        "title": "任务 6：文件、字典与 NumPy 综合汇总",
        "requirements": [
            "空行应被跳过。",
            '未知 product_id 或负数 units/price 应立即返回 "Invalid data"。',
            "使用 NumPy 计算每行销售额：units * price。",
            "按类别汇总销售额并保留两位小数。",
        ],
        "questions": {
            "Q26": "这份 AI 答案是否完全满足任务要求？",
            "Q27": "这份 AI 答案是否可以直接提交？",
            "Q28": "AI 代码会返回什么？",
            "Q29": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q30": "这份 AI 答案的问题包括哪一组？",
        },
        "contexts": {"Q28": '输入行：2024-01,P1,2,10 和 2024-01,P2,3,5。category_map={"P1":"book","P2":"food"}。'},
    },
}

C_ZH_TASK_TEXT = {
    1: {
        "title": "C 任务 1：商品价格查找与订单总价",
        "requirements": [
            "double calculate_total(int ids[], int qty[], int n, int price_ids[], double prices[], int m, int vip)",
            "对 ids 中的每个商品编号，在 price_ids 中查找匹配编号。",
            '如果任意商品编号不存在，返回 -1 表示 "Unknown item"。',
            "如果 vip 为真，先对小计应用 10% 折扣。",
            "折扣后小计大于 100 则免运费，否则运费为 8。",
            "返回最终金额。",
        ],
        "questions": {
            "Q1": "这份 AI 生成的 C 语言答案是否完全满足任务要求？",
            "Q2": "这份 AI 生成的 C 语言答案是否可以直接提交？",
            "Q3": "AI 代码会返回什么？",
            "Q4": "根据任务要求，正确返回值应该是什么？",
            "Q5": "这份 AI 生成答案的主要问题是什么？",
        },
        "contexts": {"Q3": "给定 ids={1,9}, qty={2,1}, price_ids={1,2}, prices={10,50}, vip=0。"},
        "supervision": {
            "T1_SC_problem_definition": "任务是否要求商品编号未知时返回 -1？",
            "T1_SC_code_understanding": "把 price 初始化为 0，是否会让未知商品按 0 元计入小计？",
            "T1_SC_output_debugging": "对于 ids={1,9}，编号 9 是否会被静默按 0 元处理？",
            "T1_SC_verification_testing": "哪个输入最能暴露未知编号问题？",
            "T1_SC_responsibility": "如果未知编号被按 0 元收费，这段代码是否可以直接提交？",
        },
    },
    2: {
        "title": "C 任务 2：文件行计数与输出",
        "requirements": [
            "int count_nonempty_lines(const char *input_path, const char *output_path)",
            "读取输入文件的所有行。",
            "只包含换行符的空行应被跳过。",
            "返回非空行数量。",
            "把计数写入 output_path，并覆盖旧内容。",
        ],
        "questions": {
            "Q6": "这份 AI 生成的 C 语言答案是否完全满足任务要求？",
            "Q7": "这份 AI 生成的 C 语言答案是否可以直接提交？",
            "Q8": "AI 代码会返回什么？",
            "Q9": "根据任务要求，正确返回值应该是什么？",
            "Q10": "这份答案的问题包括哪一组？",
        },
        "contexts": {"Q8": '输入文件内容为 "a\\n\\nb\\n"。'},
        "supervision": {
            "T2_SC_problem_definition": "任务是否要求跳过只包含换行符的空行？",
            "T2_SC_code_understanding": 'strcmp(line, "") 能否跳过被读取为 "\\n" 的空行？',
            "T2_SC_output_debugging": "这段代码是否会追加到旧输出后，而不是覆盖旧内容？",
            "T2_SC_verification_testing": "哪个输入最能测试空行处理？",
            "T2_SC_responsibility": "如果旧输出会保留在文件里，这段代码是否可以直接提交？",
        },
    },
    3: {
        "title": "C 任务 3：学生成绩报告",
        "requirements": ["根据学生 id，从成绩表中填充每个学生的成绩。", "如果某个学生 id 在成绩表中缺失，成绩应为 0。", "保持原始学生顺序。"],
        "questions": {
            "Q11": "这份 AI 生成的 C 语言答案是否完全满足任务要求？",
            "Q12": "这份 AI 生成的 C 语言答案是否可以直接提交？",
            "Q13": "AI 代码会生成什么结果？",
            "Q14": "根据任务要求，正确的成绩值应该是什么？",
            "Q15": "这份答案的主要问题是什么？",
        },
        "contexts": {"Q13": "students 为 [{id:2,name:Bob},{id:1,name:Ana}]，scores={{1,90}}。"},
    },
    4: {
        "title": "C 任务 4：排除哨兵值的数组平均值",
        "requirements": ["忽略值为 -1 的元素。", "以 double 返回有效值的平均数。", "如果没有有效值，返回 0.0。"],
        "questions": {
            "Q16": "这份 AI 生成的 C 语言答案是否完全满足任务要求？",
            "Q17": "这份 AI 生成的 C 语言答案是否可以直接提交？",
            "Q18": "在普通 C 整数除法行为下，AI 代码会返回什么？",
            "Q19": "根据任务要求，正确返回值应该是什么？",
            "Q20": "这份答案的主要问题是什么？",
        },
        "contexts": {"Q18": "arr={2,4,-1}, n=3。-1 表示无效值，应被忽略。"},
    },
    5: {
        "title": "C 任务 5：分类销售额汇总",
        "requirements": ["销售额计算为 price * quantity。", "按分类下标汇总销售额。", "累计前应设置每个分类的初始总额。"],
        "questions": {
            "Q21": "这份 AI 生成的 C 语言答案是否完全满足任务要求？",
            "Q22": "这份 AI 生成的 C 语言答案是否可以直接提交？",
            "Q23": "AI 代码会生成哪些 totals？",
            "Q24": "根据任务要求，正确的 totals 应该是什么？",
            "Q25": "这份答案的主要问题是什么？",
        },
        "contexts": {"Q23": "prices={10,20,5}, qty={2,1,4}, cat={0,1,0}, cat_count=2。"},
    },
    6: {
        "title": "C 任务 6：CSV 商品汇总",
        "requirements": ["每行格式为 product_id,units,price。", "如果商品编号未知，或 units/price 为负数，返回 0。", "计算 units * price。", "按分类汇总 totals，成功时返回 1。"],
        "questions": {
            "Q26": "这份 AI 生成的 C 语言答案是否完全满足任务要求？",
            "Q27": "这份 AI 生成的 C 语言答案是否可以直接提交？",
            "Q28": "AI 代码会生成哪些 totals？",
            "Q29": "根据任务要求，正确的 totals 应该是什么？",
            "Q30": "这份答案的问题包括哪一组？",
        },
        "contexts": {"Q28": "输入行是 1,2,10 和 2,3,5。ids={1,2}, cats={0,1}。"},
    },
}

C_OPTION_TEXT_ZH = {
    "Yes": "是",
    "No": "否",
    "Not sure": "不确定",
    "Can submit": "可以提交",
    "Cannot submit": "不可以提交",
    "Can": "能",
    "Cannot": "不能",
    "Compilation error": "编译错误",
    "VIP discount is calculated incorrectly": "VIP 折扣计算错误",
    "Unknown product ids are treated as price 0": "未知商品编号被按 0 元处理",
    "The shipping threshold is missing": "缺少运费阈值",
    "The loop never runs": "循环完全没有执行",
    "Only missing fclose": "只是缺少 fclose",
    "It does not skip newline-only blank lines and uses append mode": "没有跳过只含换行符的空行，且使用追加模式",
    "It cannot read files at all": "完全无法读取文件",
    "It has no problem": "没有问题",
    "Bob has 0 and Ana has 90, original order unchanged": "Bob 为 0，Ana 为 90，原顺序不变",
    "Ana is moved before Bob": "Ana 被移动到 Bob 前面",
    "Both scores become 90": "两人的成绩都变为 90",
    "Bob has 0 and Ana has 90": "Bob 为 0，Ana 为 90",
    "Bob has 90 and Ana has 0": "Bob 为 90，Ana 为 0",
    "Both scores become 0": "两人的成绩都变为 0",
    "No scores should be assigned": "不应赋任何成绩",
    "It does not handle missing scores": "没有处理缺失成绩",
    "It changes names": "修改了姓名",
    "It cannot use structs": "不能使用结构体",
    "It uses a loop": "使用了循环",
    "It includes sentinel -1 and performs integer division": "把哨兵值 -1 计入平均值，且执行了整数除法",
    "It returns double": "返回 double",
    "totals[0]=40, totals[1]=20": "totals[0]=40，totals[1]=20",
    "totals[0]=15, totals[1]=20": "totals[0]=15，totals[1]=20",
    "totals[0]=20, totals[1]=20": "totals[0]=20，totals[1]=20",
    "All totals should be 0": "所有 totals 都应为 0",
    "It does not multiply price and quantity": "没有计算 price * quantity",
    "It does not initialize totals": "没有初始化 totals",
    "It uses arrays": "使用了数组",
    "totals[0]=20, totals[1]=15": "totals[0]=20，totals[1]=15",
    "totals[0]=12, totals[1]=8": "totals[0]=12，totals[1]=8",
    "totals[0]=10, totals[1]=5": "totals[0]=10，totals[1]=5",
    "return 0": "返回 0",
    "Revenue uses addition instead of multiplication and unknown/negative data does not fail": "销售额使用加法而不是乘法，且未知或负数数据不会失败",
    "Only the loop condition is wrong": "只有循环条件错误",
    "Only totals are not initialized": "只是 totals 没有初始化",
    "C. Empty file": "C. 空文件",
}

COMMON_OPTION_TEXT_ZH = {
    "Yes": "是",
    "No": "否",
    "Not sure": "不确定",
    "Can submit": "可以提交",
    "Cannot submit": "不可以提交",
    "Can": "能",
    "Cannot": "不能",
    "Error": "报错",
    "Raise an error": "报错",
    "It has no problem": "没有问题",
    "The VIP discount is calculated incorrectly": "VIP 折扣计算错误",
    "Unknown product IDs are treated as price 0": "未知商品 ID 被当作价格 0 处理",
    "It does not round to two decimal places": "没有保留两位小数",
    "The shipping rule is completely reversed": "运费规则完全反了",
    "Only missing encoding": "只是缺少 encoding",
    "It does not correctly skip empty lines, uses append mode, and does not sort output": "没有正确跳过空行，使用追加模式，且输出没有排序",
    "It does not use a dictionary": "没有使用字典",
    "It does not handle empty lines": "没有处理空行",
    "It does not handle missing scores": "没有处理缺失成绩",
    "It does not sort": "没有排序",
    "It does not use NumPy": "没有使用 NumPy",
    "It does not ignore np.nan and does not handle zero standard deviation": "没有忽略 np.nan，且没有处理标准差为 0 的情况",
    "The standardization formula is reversed": "标准化公式反了",
    "It does not perform element-wise multiplication": "没有进行逐元素乘法",
    "It does not accumulate by category": "没有按类别累加",
    "Revenue uses addition instead of multiplication; unknown products and negative values do not return \"Invalid data\"": "销售额用了加法而不是乘法；未知商品和负数没有返回 \"Invalid data\"",
    "It only should not use NumPy": "只是本不应使用 NumPy",
    "It only does not skip empty lines": "只是没有跳过空行",
}


def localized_task(task_id: int, lang: str = "en", version: str = "python") -> dict:
    normalized_version = normalize_questionnaire_version(version)
    task = deepcopy(get_task(task_id, normalized_version))
    if lang != "zh":
        return task
    if normalized_version == "c":
        zh = C_ZH_TASK_TEXT.get(task_id, {})
        task["title"] = zh.get("title", task["title"])
        task["requirements"] = zh.get("requirements", task["requirements"])
        for question in task["questions"]:
            qid = question["id"]
            question["prompt"] = zh.get("questions", {}).get(qid, question["prompt"])
            if qid in zh.get("contexts", {}):
                question["context"] = zh["contexts"][qid]
            for option in question["options"]:
                option["text"] = C_OPTION_TEXT_ZH.get(option["text"], option["text"])
        if task.get("supervision_card"):
            for item in task["supervision_card"]:
                item["prompt"] = zh.get("supervision", {}).get(item["id"], item["prompt"])
                item["dimension"] = {
                    "Problem Definition": "问题定义能力",
                    "AI Code Understanding": "AI 代码理解能力",
                    "AI Output Debugging": "AI 输出调试能力",
                    "Verification and Testing": "验证与测试能力",
                    "Responsibility and Supervision": "责任与监督能力",
                }.get(item["dimension"], item["dimension"])
                item["options"] = [C_OPTION_TEXT_ZH.get(option, option) for option in item["options"]]
        return task

    zh = ZH_TASK_TEXT.get(task_id, {})
    task["title"] = zh.get("title", task["title"])
    task["requirements"] = zh.get("requirements", task["requirements"])
    for question in task["questions"]:
        qid = question["id"]
        question["prompt"] = zh.get("questions", {}).get(qid, question["prompt"])
        if qid in zh.get("contexts", {}):
            question["context"] = zh["contexts"][qid]
        for option in question["options"]:
            option["text"] = COMMON_OPTION_TEXT_ZH.get(option["text"], option["text"])
    if task.get("supervision_card"):
        for item in task["supervision_card"]:
            item["prompt"] = zh.get("supervision", {}).get(item["id"], item["prompt"])
            item["dimension"] = {
                "Problem Definition": "问题定义能力",
                "AI Code Understanding": "AI 代码理解能力",
                "AI Output Debugging": "AI 输出调试能力",
                "Verification and Testing": "验证与测试能力",
                "Responsibility and Supervision": "责任与监督能力",
            }.get(item["dimension"], item["dimension"])
            item["options"] = [COMMON_OPTION_TEXT_ZH.get(option, option) for option in item["options"]]
    return task


def posttest_schema(lang: str = "en") -> dict:
    language = "zh" if lang == "zh" else "en"
    labels = LIKERT_LABELS_ZH if language == "zh" else LIKERT_VALUES
    return {
        "title": "后测问卷" if language == "zh" else "Post-task Questionnaire",
        "intro": (
            "请根据完成全部任务后的真实感受作答。A/B 两组使用同一份后测。"
            if language == "zh"
            else "Please answer based on your experience after completing all tasks. This posttest is identical for Groups A and B."
        ),
        "sections": [
            {"id": section["id"], "title": section["title"][language], "question_ids": section["question_ids"]}
            for section in POSTTEST_SECTIONS
        ],
        "questions": [
            {
                "id": question["id"],
                "section": question["section"],
                "prompt": question["prompt"][language],
                "options": [{"value": value, "label": labels[index]} for index, value in enumerate(LIKERT_VALUES)],
            }
            for question in POSTTEST_QUESTIONS
        ],
    }
