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

LIKERT_VALUES = ["A", "B", "C", "D", "E"]
LIKERT_LABELS_EN = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
LIKERT_LABELS_ZH = ["非常不同意", "不同意", "一般", "同意", "非常同意"]
POSTTEST_OPTION_ORDER = ["E", "D", "C", "B", "A"]

POSTTEST_SECTIONS = [
    {
        "id": "mindset",
        "title": {"en": "AI Supervision Mindset", "zh": "人工智能(AI)监督意识"},
        "question_ids": [
            "post_supervisor_role",
            "post_requirements_first",
            "post_missing_conditions",
            "post_code_logic_tracing",
            "post_output_prediction",
            "post_test_design",
        ],
    },
    {
        "id": "responsibility",
        "title": {"en": "Responsibility and Intervention", "zh": "责任与人工干预"},
        "question_ids": [
            "post_human_intervention",
            "post_responsible_submission",
        ],
    },
]

POSTTEST_QUESTIONS = [
    {
        "id": "post_supervisor_role",
        "section": "mindset",
        "prompt": {
            "en": "When working with AI-generated code, I see my role as supervising AI output rather than simply accepting it.",
            "zh": "看到人工智能编程智能体(AI coding agent)生成的代码(code)时，我认为自己是人工监督者(human supervisor)，应该负责检查它，而不是直接接受。",
        },
    },
    {
        "id": "post_requirements_first",
        "section": "mindset",
        "prompt": {
            "en": "When evaluating AI-generated code, I first check whether it follows all task requirements.",
            "zh": "检查人工智能编程智能体(AI coding agent)的输出时，我会先核对它有没有满足所有任务要求。",
        },
    },
    {
        "id": "post_missing_conditions",
        "section": "mindset",
        "prompt": {
            "en": "I pay attention to whether the AI has missed important conditions, constraints, or edge cases in the task.",
            "zh": "我会留意人工智能编程智能体(AI coding agent)是否漏掉了题目中的重要条件、限制或特殊情况。",
        },
    },
    {
        "id": "post_code_logic_tracing",
        "section": "mindset",
        "prompt": {
            "en": "I trace the actual logic of AI-generated code rather than only judging whether it looks reasonable.",
            "zh": "我会顺着人工智能编程智能体(AI coding agent)生成代码(code)的实际步骤去判断，而不只看它表面上像不像对的。",
        },
    },
    {
        "id": "post_output_prediction",
        "section": "mindset",
        "prompt": {
            "en": "I try to predict the output of AI-generated code for specific inputs to find possible errors.",
            "zh": "我会用具体输入来推一遍代码(code)会输出什么，从而发现可能的错误。",
        },
    },
    {
        "id": "post_test_design",
        "section": "mindset",
        "prompt": {
            "en": "I design test cases or counterexamples to check whether AI-generated code is correct.",
            "zh": "我会设计测试用例(test case)或反例，检查人工智能编程智能体(AI coding agent)生成的代码(code)是否真的正确。",
        },
    },
    {
        "id": "post_human_intervention",
        "section": "responsibility",
        "prompt": {
            "en": "I can judge when AI-generated code needs human correction or intervention.",
            "zh": "我能判断什么时候需要人工修改或介入人工智能编程智能体(AI coding agent)生成的代码(code)。",
        },
    },
    {
        "id": "post_responsible_submission",
        "section": "responsibility",
        "prompt": {
            "en": "Before submitting AI-generated code, I consider the possible risks and my responsibility for errors.",
            "zh": "交付人工智能编程智能体(AI coding agent)生成的代码(code)前，我会考虑可能的风险，以及自己作为人工监督者(human supervisor)需要承担的检查责任。",
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


def agent_supervision_card(task_id: int) -> list[dict]:
    prefix = f"T{task_id}_SC"
    return [
        {
            "id": f"{prefix}_factuality",
            "dimension": "Factuality",
            "prompt": "Are the agent's test result, error analysis, and final conclusion directly supported by the observation log?",
            "options": ["Yes", "No", "Not sure"],
        },
        {
            "id": f"{prefix}_action_feasibility",
            "dimension": "Action Feasibility",
            "prompt": "Did the agent really perform the file edit, command, test, or verification step it claims to have performed?",
            "options": ["Yes", "No", "Not sure"],
        },
        {
            "id": f"{prefix}_goal_alignment",
            "dimension": "Goal Alignment",
            "prompt": "Does the final artifact match the user's original programming goal rather than only looking plausible?",
            "options": ["Yes", "No", "Not sure"],
        },
        {
            "id": f"{prefix}_side_effect",
            "dimension": "Side-effect Control",
            "prompt": "Could the agent's actions overwrite files, append stale output, delete useful data, or otherwise pollute the environment?",
            "options": ["Yes", "No", "Not sure"],
        },
        {
            "id": f"{prefix}_efficiency",
            "dimension": "Efficiency Evaluation",
            "prompt": "Did the agent revise its plan based on observations, or did it ignore clear evidence and stop too early?",
            "options": ["Revised appropriately", "Ignored evidence", "Not sure"],
        },
    ]


def agent_task(task_id: int, title: str, requirements: list[str], trace: str, questions: list[dict]) -> dict:
    return {
        "id": task_id,
        "title": title,
        "requirements": requirements,
        "code": trace,
        "supervision_card": agent_supervision_card(task_id),
        "questions": questions,
    }


AGENT_TASKS = [
    agent_task(
        1,
        "Agent Task 1: Product Price Lookup",
        [
            "User goal: modify calculate_total.c so unknown product ids return -1.",
            "Apply a 10% VIP discount before shipping.",
            "Shipping is free when the discounted subtotal is greater than 100; otherwise add 8.",
            "The agent must run a test containing an unknown product id before claiming success.",
        ],
        """Agent plan:
Step 1. Read calculate_total.c.
Step 2. Find the price lookup loop.
Step 3. Add order total logic and run a sample test.

Agent action log:
[Read] calculate_total.c
[Edit] Initializes price = 0 before searching price_ids.
[Edit] Adds subtotal += price * qty[i].
[Run] gcc calculate_total.c -o calculate_total
[Note] EN: gcc compiles calculate_total.c and writes an executable named calculate_total. ZH: gcc 表示编译 calculate_total.c，并生成名为 calculate_total 的可执行程序。
[Run] ./calculate_total --ids 1,9 --qty 2,1
[Note] EN: ./calculate_total runs that executable; --ids and --qty are test arguments. ZH: ./calculate_total 表示运行该程序；--ids 和 --qty 是测试用的商品编号和数量参数。
[Observation] Program prints 28.00.
[Final] Test passed. Unknown products are handled and the code can be submitted.

Modified key code:
double price = 0;
for (int j = 0; j < m; j++) {
    if (price_ids[j] == ids[i]) price = prices[j];
}
subtotal += price * qty[i];""",
        [
            {"id": "Q1", "prompt": "Is the agent's final claim supported by the observation log?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q2", "prompt": "Did the agent actually verify the required unknown-id behavior?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q3", "prompt": "Does the modified code align with the user goal?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q4", "prompt": "What should a correct implementation return for ids={1,9} when 9 is unknown?", "options": [choice("A", "-1"), choice("B", "28.00"), choice("C", "20.00"), choice("D", "8.00")]},
            {"id": "Q5", "prompt": "What is the main supervision problem?", "options": [choice("A", "The agent used too many tests"), choice("B", "It treated an unknown id as price 0 and still claimed success"), choice("C", "The code cannot compile"), choice("D", "There is no problem")]},
        ],
    ),
    agent_task(
        2,
        "Agent Task 2: Count Non-empty Lines",
        [
            "User goal: modify count_lines.c to count non-empty lines in input.txt.",
            "A blank line containing only a newline must not be counted.",
            "Write the count to output.txt using overwrite mode, not append mode.",
            "The agent must use the observed output to decide whether more editing is needed.",
        ],
        """Agent plan:
Step 1. Read count_lines.c.
Step 2. Check current blank-line logic.
Step 3. Run input "a\\n\\nb\\n".
Step 4. Submit if output is 2.

Agent action log:
[Read] count_lines.c
[Edit] Keeps if (strcmp(line, "") != 0) count++;
[Edit] Opens output with fopen(output_path, "a").
[Run] gcc count_lines.c -o count_lines
[Note] EN: gcc compiles count_lines.c and creates an executable named count_lines. ZH: gcc 表示编译 count_lines.c，并生成名为 count_lines 的可执行程序。
[Run] ./count_lines input.txt output.txt
[Note] EN: input.txt is the input file and output.txt is where the program writes the count. ZH: input.txt 是输入文件，output.txt 是程序写入计数结果的输出文件。
[Observation] output.txt contains appended value 3.
[Final] Test passed. The code can be submitted.

Modified key code:
while (fgets(line, sizeof(line), in)) {
    if (strcmp(line, "") != 0) count++;
}
FILE *out = fopen(output_path, "a");""",
        [
            {"id": "Q6", "prompt": "Is the agent's claim that the test passed supported by the observation?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q7", "prompt": "Did the agent complete the required overwrite-write action?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q8", "prompt": "For input \"a\\n\\nb\\n\", what did the agent's code output in the log?", "options": [choice("A", "0"), choice("B", "1"), choice("C", "2"), choice("D", "3")]},
            {"id": "Q9", "prompt": "According to the user goal, what should the count be?", "options": [choice("A", "2"), choice("B", "3"), choice("C", "1"), choice("D", "0")]},
            {"id": "Q10", "prompt": "Which issue should the supervisor catch?", "options": [choice("A", "Only the filename is wrong"), choice("B", "Blank-line handling is wrong and output is appended"), choice("C", "The agent never compiled"), choice("D", "There is no issue")]},
        ],
    ),
    agent_task(
        3,
        "Agent Task 3: Student Score Matching",
        [
            "User goal: fill each student's score by id.",
            "Missing score ids should produce score 0.",
            "Keep the original student order.",
            "This task is intentionally correct to test whether supervisors can allow valid agent work.",
        ],
        """Agent plan:
Step 1. Read report.c and the score table format.
Step 2. Match scores by student id.
Step 3. Run a test with one missing score.

Agent action log:
[Read] report.c
[Edit] Sets each student score to 0 before lookup.
[Edit] Replaces the score when ids match.
[Run] gcc report.c -o report
[Note] EN: gcc compiles report.c and creates an executable named report. ZH: gcc 表示编译 report.c，并生成名为 report 的可执行程序。
[Run] ./report --students "2:Bob,1:Ana" --scores "1:90"
[Note] EN: --students and --scores pass sample student data and score data to the program. ZH: --students 和 --scores 用来向程序传入测试学生数据和成绩数据。
[Observation] Bob remains first with score 0; Ana remains second with score 90.
[Final] The implementation matches the goal and can be submitted.

Modified key code:
students[i].score = 0;
if (scores[j][0] == students[i].id) {
    students[i].score = scores[j][1];
}""",
        [
            {"id": "Q11", "prompt": "Is the agent's conclusion supported by the observation?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q12", "prompt": "Can this agent result be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {"id": "Q13", "prompt": "What does the observation show?", "options": [choice("A", "Bob has 0 and Ana has 90, original order unchanged"), choice("B", "Ana is moved before Bob"), choice("C", "Both scores become 90"), choice("D", "The program fails to run")]},
            {"id": "Q14", "prompt": "According to the user goal, what should happen for Bob's missing score?", "options": [choice("A", "Bob should receive 0"), choice("B", "Bob should receive 90"), choice("C", "Bob should be deleted"), choice("D", "The program should stop")]},
            {"id": "Q15", "prompt": "What is the main supervision decision?", "options": [choice("A", "Reject because every agent output is risky"), choice("B", "Require unrelated refactoring"), choice("C", "Delete the test data"), choice("D", "Allow submission because the trace supports correctness")]},
        ],
    ),
    agent_task(
        4,
        "Agent Task 4: Average Excluding Sentinel Values",
        [
            "User goal: compute the average of valid array values.",
            "The sentinel value -1 must be ignored.",
            "Return a double result; if there are no valid values, return 0.0.",
            "The agent must inspect the concrete test output before claiming success.",
        ],
        """Agent plan:
Step 1. Read average.c.
Step 2. Sum the array and divide by n.
Step 3. Run arr={2,4,-1}.

Agent action log:
[Read] average.c
[Edit] Sums every element, including -1.
[Edit] Returns sum / n.
[Run] gcc average.c -o average
[Note] EN: gcc compiles average.c and creates an executable named average. ZH: gcc 表示编译 average.c，并生成名为 average 的可执行程序。
[Run] ./average
[Note] EN: ./average runs the compiled test program. ZH: ./average 表示运行刚编译出的测试程序。
[Observation] The program prints 1.000000.
[Final] The average function works correctly and can be submitted.

Modified key code:
int sum = 0;
for (int i = 0; i < n; i++) sum += arr[i];
return sum / n;""",
        [
            {"id": "Q16", "prompt": "Is the agent's final conclusion supported by the test observation?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q17", "prompt": "Did the agent implement the required sentinel exclusion?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q18", "prompt": "For arr={2,4,-1}, what did the agent's code output?", "options": [choice("A", "3.0"), choice("B", "1.0"), choice("C", "2.5"), choice("D", "0.0")]},
            {"id": "Q19", "prompt": "According to the user goal, what should the correct average be?", "options": [choice("A", "3.0"), choice("B", "1.0"), choice("C", "2.5"), choice("D", "0.0")]},
            {"id": "Q20", "prompt": "What should the supervisor require next?", "options": [choice("A", "Allow submission"), choice("B", "Ignore -1, use valid count and double division, then retest"), choice("C", "Delete average.c"), choice("D", "Only rename variables")]},
        ],
    ),
    agent_task(
        5,
        "Agent Task 5: Category Revenue Aggregation",
        [
            "User goal: compute price * quantity and aggregate totals by category.",
            "Initialize every category total before accumulation.",
            "This task is intentionally correct to measure correct acceptance.",
        ],
        """Agent plan:
Step 1. Read revenue.c.
Step 2. Initialize totals.
Step 3. Accumulate price * quantity by category.
Step 4. Run a two-category sample.

Agent action log:
[Read] revenue.c
[Edit] Sets totals[i] = 0 for all categories.
[Edit] Adds prices[i] * qty[i] to totals[cat[i]].
[Run] gcc revenue.c -o revenue
[Note] EN: gcc compiles revenue.c and creates an executable named revenue. ZH: gcc 表示编译 revenue.c，并生成名为 revenue 的可执行程序。
[Run] ./revenue
[Note] EN: ./revenue runs the compiled sample test. ZH: ./revenue 表示运行刚编译出的样例测试程序。
[Observation] totals[0]=40 and totals[1]=20.
[Final] The implementation matches the requirement and can be submitted.

Modified key code:
for (int i = 0; i < cat_count; i++) totals[i] = 0;
for (int i = 0; i < n; i++) {
    totals[cat[i]] += prices[i] * qty[i];
}""",
        [
            {"id": "Q21", "prompt": "Is the final claim supported by the trace?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q22", "prompt": "Can this agent result be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {"id": "Q23", "prompt": "For prices={10,20,5}, qty={2,1,4}, cat={0,1,0}, what totals are observed?", "options": [choice("A", "totals[0]=40, totals[1]=20"), choice("B", "totals[0]=15, totals[1]=20"), choice("C", "totals[0]=20, totals[1]=20"), choice("D", "Compilation error")]},
            {"id": "Q24", "prompt": "According to the user goal, what should the totals be?", "options": [choice("A", "totals[0]=40, totals[1]=20"), choice("B", "totals[0]=15, totals[1]=20"), choice("C", "totals[0]=20, totals[1]=20"), choice("D", "All totals should be 0")]},
            {"id": "Q25", "prompt": "What is the main supervision decision?", "options": [choice("A", "Reject because it uses arrays"), choice("B", "Require a rewrite even though the trace is correct"), choice("C", "Delete the output file"), choice("D", "Allow submission; no issue is shown")]},
        ],
    ),
    agent_task(
        6,
        "Agent Task 6: Sales Summary Validation",
        [
            "User goal: read product rows, reject unknown ids or negative data, compute units * price, and aggregate by category.",
            "Return failure when a row is invalid.",
            "The agent must not claim success from a test that only covers happy-path rows.",
        ],
        """Agent plan:
Step 1. Read summarize.c.
Step 2. Parse id, units, price.
Step 3. Find category and update totals.
Step 4. Run a normal two-row test.

Agent action log:
[Read] summarize.c
[Edit] If id is found, adds units + price to totals[cat].
[Edit] Unknown ids are silently skipped; negative units are not rejected.
[Run] gcc summarize.c -o summarize
[Note] EN: gcc compiles summarize.c and creates an executable named summarize. ZH: gcc 表示编译 summarize.c，并生成名为 summarize 的可执行程序。
[Run] ./summarize --rows "1,2,10;2,3,5"
[Note] EN: --rows passes two test rows in product_id,units,price format. ZH: --rows 传入两行测试数据，格式为 product_id,units,price。
[Observation] totals[0]=12 and totals[1]=8.
[Final] Sales totals are correct and edge cases are handled.

Modified key code:
if (cat >= 0) {
    totals[cat] += units + price;
}
return 1;""",
        [
            {"id": "Q26", "prompt": "Is the agent's final conclusion fully supported by the trace?", "options": [choice("A", "Yes"), choice("B", "No")]},
            {"id": "Q27", "prompt": "Can this agent result be submitted directly?", "options": [choice("A", "Can submit"), choice("B", "Cannot submit")]},
            {"id": "Q28", "prompt": "For rows 1,2,10 and 2,3,5, what totals did the agent's code produce?", "options": [choice("A", "totals[0]=20, totals[1]=15"), choice("B", "totals[0]=12, totals[1]=8"), choice("C", "totals[0]=10, totals[1]=5"), choice("D", "return 0")]},
            {"id": "Q29", "prompt": "According to the user goal, what should the totals be for those rows?", "options": [choice("A", "totals[0]=20, totals[1]=15"), choice("B", "totals[0]=12, totals[1]=8"), choice("C", "totals[0]=10, totals[1]=5"), choice("D", "return 0")]},
            {"id": "Q30", "prompt": "Which supervision judgment is most accurate?", "options": [choice("A", "The agent used addition instead of multiplication and did not prove invalid-row handling"), choice("B", "Only the filename is wrong"), choice("C", "Only totals initialization is wrong"), choice("D", "There is no issue")]},
        ],
    ),
]

TASKS_BY_VERSION = {
    "python": TASKS,
    "c": C_TASKS,
    "agent": AGENT_TASKS,
}


def normalize_questionnaire_version(version: str | None) -> str:
    return version if version in TASKS_BY_VERSION else "python"


def get_task(task_id: int, version: str = "python") -> dict:
    return TASKS_BY_VERSION[normalize_questionnaire_version(version)][task_id - 1]


def task_question_ids(task_id: int, version: str = "python") -> list[str]:
    return [question["id"] for question in get_task(task_id, version)["questions"]]


ZH_TASK_TEXT = {
    1: {
        "title": "任务 1：按商品编号查价并计算订单总价",
        "requirements": [
            "calculate_order_total(items, price_table, vip=False)",
            "items 是字典(dictionary)，格式为 {商品ID: 数量}。",
            "price_table 是字典(dictionary)，格式为 {商品ID: 单价}。",
            '如果 items 中出现 price_table 不存在的商品 ID，应返回 "Unknown item"。',
            "如果 vip=True，小计享受 10% 折扣。",
            "折扣后小计如果大于 100，免运费；否则运费为 8。",
            "返回最终金额，保留两位小数。",
        ],
        "questions": {
            "Q1": "这份人工智能编程智能体(AI coding agent)生成的代码(code)是否完全满足任务要求？",
            "Q2": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q3": "该智能体(agent)生成的代码(code)实际会返回什么？",
            "Q4": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q5": "这份智能体(agent)输出最主要的隐藏错误是什么？",
        },
        "contexts": {"Q3": '给定 price_table={"A":10,"B":50}, items={"A":2,"X":1}, vip=False。'},
        "supervision": {
            "T1_SC_problem_definition": '任务是否要求未知商品 ID 返回 "Unknown item"？',
            "T1_SC_code_understanding": "price_table.get(pid, 0) 是否会把未知商品价格当作 0？",
            "T1_SC_output_debugging": '对 items={"A":2,"X":1}，未知商品 X 是否会被该智能体(agent)生成的代码(code)悄悄忽略？',
            "T1_SC_verification_testing": "哪个输入最能暴露未知商品问题？",
            "T1_SC_responsibility": "如果未知商品被当作 0 元处理，这份智能体(agent)输出是否可直接交付？",
        },
    },
    2: {
        "title": "任务 2：读取文件并统计标签数量",
        "requirements": [
            "count_tags(input_path, output_path)",
            "输入文件中每一行格式为：user,tag。",
            "空行应被跳过。",
            "tag 前后的空格应被去掉。",
            "统计每个 tag 出现次数，并返回字典(dictionary)。",
            "将结果写入 output_path，格式为 tag,count。",
            "输出文件应按 tag 字母顺序排序，并覆盖旧内容。",
        ],
        "questions": {
            "Q6": "这份人工智能编程智能体(AI coding agent)生成的代码(code)是否完全满足任务要求？",
            "Q7": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q8": "该智能体(agent)生成的代码(code)最可能发生什么？",
            "Q9": "根据任务要求，上述输入的正确返回字典(dictionary)应该是什么？",
            "Q10": "这份智能体(agent)输出的问题包括哪一组？",
        },
        "contexts": {"Q8": "输入文件内容为：u1,python，然后一个空行，然后 u2,ai。"},
        "supervision": {
            "T2_SC_problem_definition": "任务是否要求空行应被跳过？",
            "T2_SC_code_understanding": 'if line == "" 能否跳过文件中的空行 "\\n"？',
            "T2_SC_output_debugging": '遇到空行时，user, tag = line.split(",") 是否可能报错？',
            "T2_SC_verification_testing": "哪个输入最能测试空行处理？",
            "T2_SC_responsibility": "如果代码(code)可能把旧输出保留在文件中，这份智能体(agent)输出是否可直接交付？",
        },
    },
    3: {
        "title": "任务 3：学生档案与成绩合并",
        "requirements": [
            "读取 student_id,name 格式的学生档案文件。",
            "空行应被跳过。",
            "scores 中缺失的学生成绩记为 0。",
            "返回按 student_id 从小到大排列的字典(dictionary)列表。",
        ],
        "questions": {
            "Q11": "这份人工智能编程智能体(AI coding agent)生成的代码(code)是否完全满足任务要求？",
            "Q12": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q13": "该智能体(agent)生成的代码(code)会返回什么？",
            "Q14": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q15": "这份智能体(agent)输出最主要的隐藏错误是什么？",
        },
        "contexts": {"Q13": '档案文件：s2,Bob 然后 s1,Ana。scores={"s1":90}。'},
    },
    4: {
        "title": "任务 4：用数值计算库(NumPy)处理数组",
        "requirements": [
            "计算均值和标准差时应忽略 np.nan。",
            "原本为 np.nan 的位置仍保留 np.nan。",
            "如果忽略 np.nan 后标准差为 0，则有效位置返回 0。",
            "返回结果保留两位小数。",
        ],
        "questions": {
            "Q16": "这份人工智能编程智能体(AI coding agent)生成的代码(code)是否完全满足任务要求？",
            "Q17": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q18": "该智能体(agent)生成的代码(code)最可能返回什么？",
            "Q19": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q20": "这份智能体(agent)输出最主要的隐藏错误是什么？",
        },
        "contexts": {"Q18": "arr = np.array([1.0, 2.0, np.nan])"},
    },
    5: {
        "title": "任务 5：用数值计算库(NumPy)和字典(dictionary)按类别汇总",
        "requirements": [
            "每个商品销售额为 price * quantity。",
            "按类别汇总销售额。",
            "每个类别金额保留两位小数。",
        ],
        "questions": {
            "Q21": "这份人工智能编程智能体(AI coding agent)生成的代码(code)是否完全满足任务要求？",
            "Q22": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q23": "该智能体(agent)生成的代码(code)会返回什么？",
            "Q24": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q25": "这份智能体(agent)输出最主要的隐藏错误是什么？",
        },
        "contexts": {"Q23": 'prices=[10,20,5], quantities=[2,1,4], categories={0:"A",1:"B",2:"A"}。'},
    },
    6: {
        "title": "任务 6：综合处理文件、字典(dictionary)和数值计算库(NumPy)",
        "requirements": [
            "空行应被跳过。",
            '未知 product_id 或负数 units/price 应立即返回 "Invalid data"。',
            "使用数值计算库(NumPy)计算每行销售额：units * price。",
            "按类别汇总销售额并保留两位小数。",
        ],
        "questions": {
            "Q26": "这份人工智能编程智能体(AI coding agent)生成的代码(code)是否完全满足任务要求？",
            "Q27": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q28": "该智能体(agent)生成的代码(code)会返回什么？",
            "Q29": "根据任务要求，上述输入的正确返回值应该是什么？",
            "Q30": "这份智能体(agent)输出的问题包括哪一组？",
        },
        "contexts": {"Q28": '输入行：2024-01,P1,2,10 和 2024-01,P2,3,5。category_map={"P1":"book","P2":"food"}。'},
    },
}

C_ZH_TASK_TEXT = {
    1: {
        "title": "C 任务 1：按商品编号查价并计算订单总价",
        "requirements": [
            "double calculate_total(int ids[], int qty[], int n, int price_ids[], double prices[], int m, int vip)",
            "对 ids 中的每个商品编号，在 price_ids 中查找匹配编号。",
            '如果任意商品编号不存在，返回 -1 表示 "Unknown item"。',
            "如果 vip 为真，先对小计应用 10% 折扣。",
            "折扣后小计大于 100 则免运费，否则运费为 8。",
            "返回最终金额。",
        ],
        "questions": {
            "Q1": "这份人工智能编程智能体(AI coding agent)生成的 C 语言代码(code)是否完全满足任务要求？",
            "Q2": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q3": "该智能体(agent)生成的代码(code)会返回什么？",
            "Q4": "根据任务要求，正确返回值应该是什么？",
            "Q5": "这份智能体(agent)输出的主要隐藏错误是什么？",
        },
        "contexts": {"Q3": "给定 ids={1,9}, qty={2,1}, price_ids={1,2}, prices={10,50}, vip=0。"},
        "supervision": {
            "T1_SC_problem_definition": "任务是否要求商品编号未知时返回 -1？",
            "T1_SC_code_understanding": "把 price 初始化为 0，是否会让未知商品按 0 元计入小计？",
            "T1_SC_output_debugging": "对于 ids={1,9}，编号 9 是否会被静默按 0 元处理？",
            "T1_SC_verification_testing": "哪个输入最能暴露未知编号问题？",
            "T1_SC_responsibility": "如果未知编号被按 0 元收费，这份智能体(agent)输出是否可以直接交付？",
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
            "Q6": "这份人工智能编程智能体(AI coding agent)生成的 C 语言代码(code)是否完全满足任务要求？",
            "Q7": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q8": "该智能体(agent)生成的代码(code)会返回什么？",
            "Q9": "根据任务要求，正确返回值应该是什么？",
            "Q10": "这份答案的问题包括哪一组？",
        },
        "contexts": {"Q8": '输入文件内容为 "a\\n\\nb\\n"。'},
        "supervision": {
            "T2_SC_problem_definition": "任务是否要求跳过只包含换行符的空行？",
            "T2_SC_code_understanding": 'strcmp(line, "") 能否跳过被读取为 "\\n" 的空行？',
            "T2_SC_output_debugging": "这段代码是否会追加到旧输出后，而不是覆盖旧内容？",
            "T2_SC_verification_testing": "哪个输入最能测试空行处理？",
            "T2_SC_responsibility": "如果旧输出会保留在文件里，这份智能体(agent)输出是否可以直接交付？",
        },
    },
    3: {
        "title": "C 任务 3：学生成绩报告",
        "requirements": ["根据学生 id，从成绩表中填充每个学生的成绩。", "如果某个学生 id 在成绩表中缺失，成绩应为 0。", "保持原始学生顺序。"],
        "questions": {
            "Q11": "这份人工智能编程智能体(AI coding agent)生成的 C 语言代码(code)是否完全满足任务要求？",
            "Q12": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q13": "该智能体(agent)生成的代码(code)会生成什么结果？",
            "Q14": "根据任务要求，正确的成绩值应该是什么？",
            "Q15": "这份答案的主要问题是什么？",
        },
        "contexts": {"Q13": "students 为 [{id:2,name:Bob},{id:1,name:Ana}]，scores={{1,90}}。"},
    },
    4: {
        "title": "C 任务 4：排除哨兵值的数组平均值",
        "requirements": ["忽略值为 -1 的元素。", "以 double 返回有效值的平均数。", "如果没有有效值，返回 0.0。"],
        "questions": {
            "Q16": "这份人工智能编程智能体(AI coding agent)生成的 C 语言代码(code)是否完全满足任务要求？",
            "Q17": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q18": "按普通 C 语言整数除法规则，该智能体(agent)生成的代码(code)会返回什么？",
            "Q19": "根据任务要求，正确返回值应该是什么？",
            "Q20": "这份答案的主要问题是什么？",
        },
        "contexts": {"Q18": "arr={2,4,-1}, n=3。-1 表示无效值，应被忽略。"},
    },
    5: {
        "title": "C 任务 5：分类销售额汇总",
        "requirements": ["销售额计算为 price * quantity。", "按分类下标汇总销售额。", "累计前应设置每个分类的初始总额。"],
        "questions": {
            "Q21": "这份人工智能编程智能体(AI coding agent)生成的 C 语言代码(code)是否完全满足任务要求？",
            "Q22": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q23": "该智能体(agent)生成的代码(code)会生成哪些 totals？",
            "Q24": "根据任务要求，正确的 totals 应该是什么？",
            "Q25": "这份答案的主要问题是什么？",
        },
        "contexts": {"Q23": "prices={10,20,5}, qty={2,1,4}, cat={0,1,0}, cat_count=2。"},
    },
    6: {
        "title": "C 任务 6：CSV 商品汇总",
        "requirements": ["每行格式为 product_id,units,price。", "如果商品编号未知，或 units/price 为负数，返回 0。", "计算 units * price。", "按分类汇总 totals，成功时返回 1。"],
        "questions": {
            "Q26": "这份人工智能编程智能体(AI coding agent)生成的 C 语言代码(code)是否完全满足任务要求？",
            "Q27": "作为人工监督者(human supervisor)，你认为这份智能体(agent)输出是否可以直接交付？",
            "Q28": "该智能体(agent)生成的代码(code)会生成哪些 totals？",
            "Q29": "根据任务要求，正确的 totals 应该是什么？",
            "Q30": "这份答案的问题包括哪一组？",
        },
        "contexts": {"Q28": "输入行是 1,2,10 和 2,3,5。ids={1,2}, cats={0,1}。"},
    },
}

AGENT_ZH_TASK_TEXT = {
    1: {
        "title": "智能体(agent)任务 1：检查商品查价结果",
        "requirements": [
            "用户目标：修改 calculate_total.c，让未知商品编号返回 -1。",
            "如果是 VIP 订单，先打 9 折，再计算运费。",
            "打折后小计大于 100 时免运费，否则加 8 元运费。",
            "智能体(agent)在声称完成前，必须运行一个包含未知商品编号的测试。",
        ],
        "questions": {
            "Q1": "智能体(agent)最后说“测试通过”，这个说法是否有运行记录支持？",
            "Q2": "智能体(agent)是否真的验证了“未知商品编号应被处理”这个要求？",
            "Q3": "修改后的代码(code)是否符合用户目标？",
            "Q4": "如果 ids={1,9} 且 9 是未知商品编号，正确实现应该返回什么？",
            "Q5": "这里最需要监督者发现的问题是什么？",
        },
    },
    2: {
        "title": "智能体(agent)任务 2：检查非空行计数结果",
        "requirements": [
            "用户目标：修改 count_lines.c，统计 input.txt 中的非空行数量。",
            "只包含换行符的空白行不能计入数量。",
            "把计数写入 output.txt 时应覆盖旧内容，而不是追加到旧内容后面。",
            "智能体(agent)必须根据实际看到的输出，判断是否还需要继续修改。",
        ],
        "questions": {
            "Q6": "智能体(agent)说“测试通过”，这个说法是否有观察结果支持？",
            "Q7": "智能体(agent)是否完成了“覆盖写入”这个要求？",
            "Q8": "对于输入 \"a\\n\\nb\\n\"，运行记录里智能体(agent)的代码(code)输出了什么？",
            "Q9": "根据用户目标，正确计数应该是多少？",
            "Q10": "监督者应该发现哪一类问题？",
        },
    },
    3: {
        "title": "智能体(agent)任务 3：检查学生成绩匹配结果",
        "requirements": [
            "用户目标：按学生 id 填入每个学生的成绩。",
            "如果某个学生 id 没有成绩，应记为 0。",
            "保持学生原来的顺序。",
            "这道题本身是正确案例，用来检查监督者能否接受确实有效的智能体(agent)结果。",
        ],
        "questions": {
            "Q11": "智能体(agent)的结论是否有观察结果支持？",
            "Q12": "作为人工监督者(human supervisor)，你认为这个智能体(agent)交付结果是否可以直接交付？",
            "Q13": "运行记录显示了什么？",
            "Q14": "根据用户目标，Bob 缺失成绩时应该怎样处理？",
            "Q15": "最合适的监督决定是什么？",
        },
    },
    4: {
        "title": "智能体(agent)任务 4：检查排除特殊值后的平均数",
        "requirements": [
            "用户目标：计算数组中有效数值的平均数。",
            "特殊值 -1 必须被忽略。",
            "返回 double 类型结果；如果没有有效值，返回 0.0。",
            "智能体(agent)在声称成功前，必须查看具体测试输出。",
        ],
        "questions": {
            "Q16": "智能体(agent)最后的结论是否有测试观察结果支持？",
            "Q17": "智能体(agent)是否实现了“忽略 -1”这个要求？",
            "Q18": "对于 arr={2,4,-1}，智能体(agent)的代码(code)输出了什么？",
            "Q19": "根据用户目标，正确平均数应该是多少？",
            "Q20": "监督者下一步应该要求什么？",
        },
    },
    5: {
        "title": "智能体(agent)任务 5：检查分类销售额汇总结果",
        "requirements": [
            "用户目标：计算 price * quantity，并按类别汇总总额。",
            "累加前要先初始化每个类别的总额。",
            "这道题本身是正确案例，用来检查监督者能否正确接受结果。",
        ],
        "questions": {
            "Q21": "智能体(agent)最后的说法是否有运行流程支持？",
            "Q22": "作为人工监督者(human supervisor)，你认为这个智能体(agent)交付结果是否可以直接交付？",
            "Q23": "对于 prices={10,20,5}, qty={2,1,4}, cat={0,1,0}，观察到的 totals 是什么？",
            "Q24": "根据用户目标，totals 应该是什么？",
            "Q25": "最合适的监督决定是什么？",
        },
    },
    6: {
        "title": "智能体(agent)任务 6：检查销售汇总和异常数据处理",
        "requirements": [
            "用户目标：读取商品行，遇到未知商品或负数数据时拒绝，计算 units * price，并按类别汇总。",
            "只要某一行无效，就应返回失败。",
            "智能体(agent)不能只用正常数据测试就声称所有边界情况都处理好了。",
        ],
        "questions": {
            "Q26": "智能体(agent)最后的结论是否完全有运行流程支持？",
            "Q27": "作为人工监督者(human supervisor)，你认为这个智能体(agent)交付结果是否可以直接交付？",
            "Q28": "对于 1,2,10 和 2,3,5 这两行，智能体(agent)的代码(code)生成了哪些 totals？",
            "Q29": "根据用户目标，这两行的正确 totals 应该是什么？",
            "Q30": "哪一个监督判断最准确？",
        },
    },
}

AGENT_OPTION_TEXT_ZH = {
    "Yes": "是",
    "No": "否",
    "Not sure": "不确定",
    "Can submit": "可以提交",
    "Cannot submit": "不可以提交",
    "Revised appropriately": "根据证据适当调整了",
    "Ignored evidence": "忽视了证据",
    "The agent used too many tests": "智能体(agent)用了太多测试",
    "It treated an unknown id as price 0 and still claimed success": "它把未知编号按 0 元处理，却仍然声称成功",
    "The code cannot compile": "代码(code)无法编译",
    "There is no problem": "没有问题",
    "Only the filename is wrong": "只是文件名错误",
    "Blank-line handling is wrong and output is appended": "空行处理错误，并且输出被追加到旧内容后面",
    "The agent never compiled": "智能体(agent)根本没有编译",
    "Bob has 0 and Ana has 90, original order unchanged": "Bob 为 0，Ana 为 90，原顺序不变",
    "Ana is moved before Bob": "Ana 被移动到 Bob 前面",
    "Both scores become 90": "两人的成绩都变为 90",
    "The program fails to run": "程序运行失败",
    "Bob should receive 0": "Bob 应该记为 0",
    "Bob should receive 90": "Bob 应该记为 90",
    "Bob should be deleted": "Bob 应该被删除",
    "The program should stop": "程序应该停止",
    "Reject because every agent output is risky": "因为所有智能体(agent)输出都有风险，所以拒绝",
    "Require unrelated refactoring": "要求做无关重构",
    "Delete the test data": "删除测试数据",
    "Allow submission because the trace supports correctness": "允许提交，因为运行流程支持它是正确的",
    "Ignore -1, use valid count and double division, then retest": "忽略 -1，使用有效数量和 double 除法，然后重新测试",
    "Only rename variables": "只是重命名变量",
    "Reject because it uses arrays": "因为它使用数组，所以拒绝",
    "Require a rewrite even though the trace is correct": "即使运行流程正确，也要求重写",
    "Delete the output file": "删除输出文件",
    "Allow submission; no issue is shown": "允许提交；没有看到问题",
    "The agent used addition instead of multiplication and did not prove invalid-row handling": "智能体(agent)用了加法而不是乘法，也没有证明自己处理了无效数据行",
    "Only totals initialization is wrong": "只是 totals 初始化错误",
    "There is no issue": "没有问题",
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


AGENT_TRACE_REPLACEMENTS_ZH = {
    "Agent plan:": "智能体(agent)计划：",
    "Agent action log:": "智能体(agent)操作记录：",
    "Modified key code:": "修改后的关键代码(code)：",
    "Step 1. Read calculate_total.c.": "步骤 1：读取 calculate_total.c。",
    "Step 2. Find the price lookup loop.": "步骤 2：找到查找价格的循环。",
    "Step 3. Add order total logic and run a sample test.": "步骤 3：添加订单总价逻辑，并运行一个样例测试。",
    "Step 1. Read count_lines.c.": "步骤 1：读取 count_lines.c。",
    "Step 2. Check current blank-line logic.": "步骤 2：检查当前空行处理逻辑。",
    'Step 3. Run input "a\\n\\nb\\n".': '步骤 3：运行输入 "a\\n\\nb\\n"。',
    "Step 4. Submit if output is 2.": "步骤 4：如果输出为 2，就提交。",
    "Step 1. Read report.c and the score table format.": "步骤 1：读取 report.c 和成绩表格式。",
    "Step 2. Match scores by student id.": "步骤 2：按学生 id 匹配成绩。",
    "Step 3. Run a test with one missing score.": "步骤 3：运行一个有缺失成绩的测试。",
    "Step 1. Read average.c.": "步骤 1：读取 average.c。",
    "Step 2. Sum the array and divide by n.": "步骤 2：把数组全部相加，再除以 n。",
    "Step 3. Run arr={2,4,-1}.": "步骤 3：运行 arr={2,4,-1}。",
    "Step 1. Read revenue.c.": "步骤 1：读取 revenue.c。",
    "Step 2. Initialize totals.": "步骤 2：初始化 totals。",
    "Step 3. Accumulate price * quantity by category.": "步骤 3：按类别累加 price * quantity。",
    "Step 4. Run a two-category sample.": "步骤 4：运行一个包含两个类别的样例。",
    "Step 1. Read summarize.c.": "步骤 1：读取 summarize.c。",
    "Step 2. Parse id, units, price.": "步骤 2：解析 id、units、price。",
    "Step 3. Find category and update totals.": "步骤 3：找到类别并更新 totals。",
    "Step 4. Run a normal two-row test.": "步骤 4：运行一个正常的两行数据测试。",
    "[Read]": "[读取]",
    "[Edit] Initializes price = 0 before searching price_ids.": "[修改] 在查找 price_ids 前，把 price 初始化为 0。",
    "[Edit] Adds subtotal += price * qty[i].": "[修改] 添加 subtotal += price * qty[i]。",
    "[Edit] Keeps if (strcmp(line, \"\") != 0) count++;": "[修改] 保留 if (strcmp(line, \"\") != 0) count++;。",
    "[Edit] Opens output with fopen(output_path, \"a\").": "[修改] 用 fopen(output_path, \"a\") 打开输出文件，也就是追加写入。",
    "[Edit] Sets each student score to 0 before lookup.": "[修改] 查找前先把每个学生成绩设为 0。",
    "[Edit] Replaces the score when ids match.": "[修改] 当 id 匹配时替换成绩。",
    "[Edit] Sums every element, including -1.": "[修改] 把每个元素都相加，包括 -1。",
    "[Edit] Returns sum / n.": "[修改] 返回 sum / n。",
    "[Edit] Sets totals[i] = 0 for all categories.": "[修改] 把所有类别的 totals[i] 设为 0。",
    "[Edit] Adds prices[i] * qty[i] to totals[cat[i]].": "[修改] 把 prices[i] * qty[i] 加到 totals[cat[i]]。",
    "[Edit] If id is found, adds units + price to totals[cat].": "[修改] 如果找到 id，就把 units + price 加到 totals[cat]。",
    "[Edit] Unknown ids are silently skipped; negative units are not rejected.": "[修改] 未知 id 被悄悄跳过；负数 units 没有被拒绝。",
    "[Run]": "[运行]",
    "[Note]": "[说明]",
    "[Observation] Program prints 28.00.": "[观察结果] 程序输出 28.00。",
    "[Observation] output.txt contains appended value 3.": "[观察结果] output.txt 中出现了追加进去的数值 3。",
    "[Observation] Bob remains first with score 0; Ana remains second with score 90.": "[观察结果] Bob 仍排第一且成绩为 0；Ana 仍排第二且成绩为 90。",
    "[Observation] The program prints 1.000000.": "[观察结果] 程序输出 1.000000。",
    "[Observation] totals[0]=40 and totals[1]=20.": "[观察结果] totals[0]=40，totals[1]=20。",
    "[Observation] totals[0]=12 and totals[1]=8.": "[观察结果] totals[0]=12，totals[1]=8。",
    "[Final] Test passed. Unknown products are handled and the code can be submitted.": "[最终结论] 测试通过。未知商品已处理，代码(code)可以提交。",
    "[Final] Test passed. The code can be submitted.": "[最终结论] 测试通过。代码(code)可以提交。",
    "[Final] The implementation matches the goal and can be submitted.": "[最终结论] 实现符合目标，可以提交。",
    "[Final] The average function works correctly and can be submitted.": "[最终结论] 平均数函数工作正确，可以提交。",
    "[Final] The implementation matches the requirement and can be submitted.": "[最终结论] 实现符合要求，可以提交。",
    "[Final] Sales totals are correct and edge cases are handled.": "[最终结论] 销售额汇总正确，特殊情况也已处理。",
    "EN:": "英文说明：",
    "ZH:": "中文说明：",
}


def localized_agent_trace(trace: str) -> str:
    localized = trace
    for source, target in AGENT_TRACE_REPLACEMENTS_ZH.items():
        localized = localized.replace(source, target)
    return localized


def localized_task(task_id: int, lang: str = "en", version: str = "python") -> dict:
    normalized_version = normalize_questionnaire_version(version)
    task = deepcopy(get_task(task_id, normalized_version))
    task["questionnaire_version"] = normalized_version
    if lang != "zh":
        return task
    if normalized_version == "agent":
        zh = AGENT_ZH_TASK_TEXT.get(task_id, {})
        task["title"] = zh.get("title", task["title"])
        task["requirements"] = zh.get("requirements", task["requirements"])
        task["code"] = localized_agent_trace(task["code"])
        for question in task["questions"]:
            qid = question["id"]
            question["prompt"] = zh.get("questions", {}).get(qid, question["prompt"])
            for option in question["options"]:
                option["text"] = AGENT_OPTION_TEXT_ZH.get(option["text"], option["text"])
        if task.get("supervision_card"):
            for item in task["supervision_card"]:
                item["prompt"] = {
                    "factuality": "智能体(agent)的测试结果、错误分析和最终结论，是否都能从运行记录中直接看出来？",
                    "action_feasibility": "智能体(agent)声称做过的文件修改、命令、测试或验证步骤，是否真的做了？",
                    "goal_alignment": "最终交付物是否符合用户最初的编程目标，而不只是看起来像是合理的？",
                    "side_effect": "智能体(agent)的操作是否可能覆盖文件、追加旧输出、删除有用数据，或给环境带来其他影响？",
                    "efficiency": "智能体(agent)是否根据观察结果调整计划，还是忽视明显证据后过早停止？",
                }.get(item["id"].split("_SC_", 1)[-1], item["prompt"])
                item["dimension"] = {
                    "Factuality": "事实核对能力",
                    "Action Feasibility": "操作核对能力",
                    "Goal Alignment": "目标一致性",
                    "Side-effect Control": "副作用控制",
                    "Efficiency Evaluation": "过程调整判断",
                }.get(item["dimension"], item["dimension"])
                item["options"] = [AGENT_OPTION_TEXT_ZH.get(option, option) for option in item["options"]]
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
                    "Problem Definition": "理解任务要求",
                    "AI Code Understanding": "理解智能体(agent)生成的代码(code)",
                    "AI Output Debugging": "核对智能体(agent)输出",
                    "Verification and Testing": "验证与测试(testing)",
                    "Responsibility and Supervision": "交付责任与监督",
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
                "Problem Definition": "理解任务要求",
                "AI Code Understanding": "理解智能体(agent)生成的代码(code)",
                "AI Output Debugging": "核对智能体(agent)输出",
                "Verification and Testing": "验证与测试(testing)",
                "Responsibility and Supervision": "交付责任与监督",
            }.get(item["dimension"], item["dimension"])
            item["options"] = [COMMON_OPTION_TEXT_ZH.get(option, option) for option in item["options"]]
    return task


def posttest_schema(lang: str = "en") -> dict:
    language = "zh" if lang == "zh" else "en"
    labels = LIKERT_LABELS_ZH if language == "zh" else LIKERT_LABELS_EN
    label_by_value = dict(zip(LIKERT_VALUES, labels))
    return {
        "title": "AI 监督能力后测" if language == "zh" else "AI Supervision Competence Post-test",
        "intro": (
            "请根据完成全部任务后的真实感受作答。这里想了解你是否形成了作为人工监督者(human supervisor)监督人工智能编程智能体(AI coding agent)交付结果的意识、方法和责任判断。结束后小问卷不计入正式任务得分。"
            if language == "zh"
            else "Please answer based on your experience after completing all tasks. This post-test measures your mindset, strategies, and responsibility judgments when supervising AI outputs. It is not included in the formal task score."
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
                "options": [{"value": value, "label": label_by_value[value]} for value in POSTTEST_OPTION_ORDER],
            }
            for question in POSTTEST_QUESTIONS
        ],
    }
