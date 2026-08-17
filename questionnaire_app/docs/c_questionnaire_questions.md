# C 语言版本题目文档

本文档从系统题库导出，用于研究者核对 C 语言版本的前台展示题目。

对应答案文档：`c_questionnaire_answer_key.md`。

## C 任务 1：按商品编号查价并计算订单总价

### 任务要求

- double calculate_total(int ids[], int qty[], int n, int price_ids[], double prices[], int m, int vip)
- 对 ids 中的每个商品编号，在 price_ids 中查找匹配编号。
- 如果任意商品编号不存在，返回 -1 表示 "Unknown item"。
- 如果 vip 为真，先对小计应用 10% 折扣。
- 折扣后小计大于 100 则免运费，否则运费为 8。
- 返回最终金额。

### 人工智能编程智能体(AI coding agent)给出的代码(code)

```c
double calculate_total(int ids[], int qty[], int n, int price_ids[], double prices[], int m, int vip) {
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
}
```

### B 组监督检查卡

#### T1_SC_problem_definition - 理解任务要求

- 题目：任务是否要求商品编号未知时返回 -1？
- 选项：
  - 是
  - 否
  - 不确定

#### T1_SC_code_understanding - 理解智能体(agent)生成的代码(code)

- 题目：把 price 初始化为 0，是否会让未知商品按 0 元计入小计？
- 选项：
  - 是
  - 否
  - 不确定

#### T1_SC_output_debugging - 核对智能体(agent)输出

- 题目：对于 ids={1,9}，编号 9 是否会被静默按 0 元处理？
- 选项：
  - 是
  - 否
  - 不确定

#### T1_SC_verification_testing - 验证与测试(testing)

- 题目：哪个输入最能暴露未知编号问题？
- 选项：
  - A. ids={1}
  - B. ids={9}
  - C. ids={1,1}

#### T1_SC_responsibility - 交付责任与监督

- 题目：如果未知编号被按 0 元收费，这份智能体(agent)输出是否可以直接交付？
- 选项：
  - 可以提交
  - 不可以提交
  - 不确定

### 正式题

#### Q1

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否完全满足任务要求？
- 选项：
  - A. 是
  - B. 否

#### Q2

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否可以直接交付？
- 选项：
  - A. 可以提交
  - B. 不可以提交

#### Q3

- 背景：给定 ids={1,9}, qty={2,1}, price_ids={1,2}, prices={10,50}, vip=0。
- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)实际会返回什么？
- 选项：
  - A. -1
  - B. 28
  - C. 20
  - D. 编译错误

#### Q4

- 题目：根据任务要求，上述输入的正确返回值应该是什么？
- 选项：
  - A. -1
  - B. 28
  - C. 20
  - D. 8

#### Q5

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)中，最需要发现的隐藏错误是什么？
- 选项：
  - A. VIP 折扣计算错误
  - B. 未知商品编号被按 0 元处理
  - C. 缺少运费阈值
  - D. 循环完全没有执行

## C 任务 2：文件行计数与输出

### 任务要求

- int count_nonempty_lines(const char *input_path, const char *output_path)
- 读取输入文件的所有行。
- 只包含换行符的空行应被跳过。
- 返回非空行数量。
- 把计数写入 output_path，并覆盖旧内容。

### 人工智能编程智能体(AI coding agent)给出的代码(code)

```c
int count_nonempty_lines(const char *input_path, const char *output_path) {
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
    fprintf(out, "%d\n", count);
    fclose(in);
    fclose(out);
    return count;
}
```

### B 组监督检查卡

#### T2_SC_problem_definition - 理解任务要求

- 题目：任务是否要求跳过只包含换行符的空行？
- 选项：
  - 是
  - 否
  - 不确定

#### T2_SC_code_understanding - 理解智能体(agent)生成的代码(code)

- 题目：strcmp(line, "") 能否跳过被读取为 "\n" 的空行？
- 选项：
  - 能
  - 不能
  - 不确定

#### T2_SC_output_debugging - 核对智能体(agent)输出

- 题目：这段代码是否会追加到旧输出后，而不是覆盖旧内容？
- 选项：
  - 是
  - 否
  - 不确定

#### T2_SC_verification_testing - 验证与测试(testing)

- 题目：哪个输入最能测试空行处理？
- 选项：
  - A. "a\n"
  - B. "a\n\nb\n"
  - C. 空文件

#### T2_SC_responsibility - 交付责任与监督

- 题目：如果旧输出会保留在文件里，这份智能体(agent)输出是否可以直接交付？
- 选项：
  - 可以提交
  - 不可以提交
  - 不确定

### 正式题

#### Q6

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否完全满足任务要求？
- 选项：
  - A. 是
  - B. 否

#### Q7

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否可以直接交付？
- 选项：
  - A. 可以提交
  - B. 不可以提交

#### Q8

- 背景：输入文件内容为 "a\n\nb\n"。
- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)最可能发生什么？
- 选项：
  - A. 2
  - B. 1
  - C. 0
  - D. 3

#### Q9

- 题目：根据任务要求，上述输入的正确返回结果应该是什么？
- 选项：
  - A. 2
  - B. 3
  - C. 1
  - D. 0

#### Q10

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)中，最需要发现的隐藏问题包括哪一组？
- 选项：
  - A. 只是缺少 fclose
  - B. 没有跳过只含换行符的空行，且使用追加模式
  - C. 完全无法读取文件
  - D. 没有问题

## C 任务 3：学生成绩报告

### 任务要求

- 根据学生 id，从成绩表中填充每个学生的成绩。
- 如果某个学生 id 在成绩表中缺失，成绩应为 0。
- 保持原始学生顺序。

### 人工智能编程智能体(AI coding agent)给出的代码(code)

```c
typedef struct { int id; char name[32]; int score; } Student;

void build_report(Student students[], int n, int scores[][2], int score_n) {
    for (int i = 0; i < n; i++) {
        students[i].score = 0;
        for (int j = 0; j < score_n; j++) {
            if (scores[j][0] == students[i].id) {
                students[i].score = scores[j][1];
            }
        }
    }
}
```

### 正式题

#### Q11

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否完全满足任务要求？
- 选项：
  - A. 是
  - B. 否

#### Q12

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否可以直接交付？
- 选项：
  - A. 可以提交
  - B. 不可以提交

#### Q13

- 背景：students 为 [{id:2,name:Bob},{id:1,name:Ana}]，scores={{1,90}}。
- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)会返回什么？
- 选项：
  - A. Bob 为 0，Ana 为 90，原顺序不变
  - B. Ana 被移动到 Bob 前面
  - C. 两人的成绩都变为 90
  - D. 编译错误

#### Q14

- 题目：根据任务要求，上述输入的正确结果应该是什么？
- 选项：
  - A. Bob 为 0，Ana 为 90
  - B. Bob 为 90，Ana 为 0
  - C. 两人的成绩都变为 0
  - D. 不应赋任何成绩

#### Q15

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)中，最需要发现的隐藏错误是什么？
- 选项：
  - A. 没有问题
  - B. 没有处理缺失成绩
  - C. 修改了姓名
  - D. 不能使用结构体

## C 任务 4：排除哨兵值的数组平均值

### 任务要求

- 忽略值为 -1 的元素。
- 以 double 返回有效值的平均数。
- 如果没有有效值，返回 0.0。

### 人工智能编程智能体(AI coding agent)给出的代码(code)

```c
double average_valid(int arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum / n;
}
```

### 正式题

#### Q16

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否完全满足任务要求？
- 选项：
  - A. 是
  - B. 否

#### Q17

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否可以直接交付？
- 选项：
  - A. 可以提交
  - B. 不可以提交

#### Q18

- 背景：arr={2,4,-1}, n=3。-1 表示无效值，应被忽略。
- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)最可能返回什么？
- 选项：
  - A. 3.0
  - B. 1.0
  - C. 2.5
  - D. Error

#### Q19

- 题目：根据任务要求，上述输入的正确返回值应该是什么？
- 选项：
  - A. 3.0
  - B. 1.0
  - C. -1.0
  - D. 0.0

#### Q20

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)中，最需要发现的隐藏错误是什么？
- 选项：
  - A. 使用了循环
  - B. 把哨兵值 -1 计入平均值，且执行了整数除法
  - C. 返回 double
  - D. 没有问题

## C 任务 5：分类销售额汇总

### 任务要求

- 销售额计算为 price * quantity。
- 按分类下标汇总销售额。
- 累计前应设置每个分类的初始总额。

### 人工智能编程智能体(AI coding agent)给出的代码(code)

```c
void category_revenue(double prices[], int qty[], int cat[], int n, double totals[], int cat_count) {
    for (int i = 0; i < cat_count; i++) totals[i] = 0;
    for (int i = 0; i < n; i++) {
        totals[cat[i]] += prices[i] * qty[i];
    }
}
```

### 正式题

#### Q21

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否完全满足任务要求？
- 选项：
  - A. 是
  - B. 否

#### Q22

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否可以直接交付？
- 选项：
  - A. 可以提交
  - B. 不可以提交

#### Q23

- 背景：prices={10,20,5}, qty={2,1,4}, cat={0,1,0}, cat_count=2。
- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)会返回什么？
- 选项：
  - A. totals[0]=40，totals[1]=20
  - B. totals[0]=15，totals[1]=20
  - C. totals[0]=20，totals[1]=20
  - D. 编译错误

#### Q24

- 题目：根据任务要求，上述输入的正确结果应该是什么？
- 选项：
  - A. totals[0]=40，totals[1]=20
  - B. totals[0]=15，totals[1]=20
  - C. totals[0]=20，totals[1]=20
  - D. 所有 totals 都应为 0

#### Q25

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)中，最需要发现的隐藏错误是什么？
- 选项：
  - A. 没有问题
  - B. 没有计算 price * quantity
  - C. 没有初始化 totals
  - D. 使用了数组

## C 任务 6：CSV 商品汇总

### 任务要求

- 每行格式为 product_id,units,price。
- 如果商品编号未知，或 units/price 为负数，返回 0。
- 计算 units * price。
- 按分类汇总 totals，成功时返回 1。

### 人工智能编程智能体(AI coding agent)给出的代码(code)

```c
int summarize(FILE *fp, int ids[], int cats[], int product_n, double totals[], int cat_count) {
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
}
```

### 正式题

#### Q26

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否完全满足任务要求？
- 选项：
  - A. 是
  - B. 否

#### Q27

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)是否可以直接交付？
- 选项：
  - A. 可以提交
  - B. 不可以提交

#### Q28

- 背景：输入行是 1,2,10 和 2,3,5。ids={1,2}, cats={0,1}。
- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)会返回什么？
- 选项：
  - A. totals[0]=20，totals[1]=15
  - B. totals[0]=12，totals[1]=8
  - C. totals[0]=10，totals[1]=5
  - D. 返回 0

#### Q29

- 题目：根据任务要求，上述输入的正确结果应该是什么？
- 选项：
  - A. totals[0]=20，totals[1]=15
  - B. totals[0]=12，totals[1]=8
  - C. totals[0]=10，totals[1]=5
  - D. 返回 0

#### Q30

- 题目：这份人工智能编程智能体(AI coding agent)给出的代码(code)中，最需要发现的隐藏问题包括哪一组？
- 选项：
  - A. 销售额使用加法而不是乘法，且未知或负数数据不会失败
  - B. 只有循环条件错误
  - C. 只是 totals 没有初始化
  - D. 没有问题
