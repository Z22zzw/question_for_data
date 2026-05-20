const view = document.getElementById("view");
const progressLabel = document.getElementById("progressLabel");
const languageToggle = document.getElementById("languageToggle");
const resetHomeButton = document.getElementById("resetHome");
const networkStatus = document.getElementById("networkStatus");

const i18n = {
  en: {
    switchLabel: "中文",
    eyebrow: "Research Questionnaire",
    title: "AI Code Supervision Study",
    pretest: "Pretest",
    pretestTitle: "Pretest Information",
    pretestHint: "Please complete the shared pretest before entering the task section. Your participant ID will be assigned automatically.",
    consent: "Consent",
    select: "Select",
    agree: "I agree",
    disagree: "I do not agree",
    start: "Start Tasks",
    taskProgress: (id) => `Task ${id} / 6`,
    supervisionCard: "Supervision Card",
    submitTask: "Submit Task",
    submitAll: "Submit Questionnaire",
    posttestProgress: "Posttest",
    submitPosttest: "Submit Posttest",
    complete: "Complete",
    completeTitle: "Submission Complete",
    completeText: "Your responses have been recorded. Scores and answer keys are not shown to participants.",
    unavailable: "Task unavailable",
    offline: "Network is unavailable. Your current responses are cached locally.",
    pending: "A saved submission is waiting for the network to recover.",
    restored: "Local draft restored.",
    resetHome: "New Session",
    fields: {
      age: "Age",
      gender: "Gender",
      grade_year: "Grade Year",
      major: "Major",
      programming_experience_years: "Programming Experience",
      python_familiarity: "Python Proficiency",
      file_io_familiarity: "Academic Reading/Writing Ability",
      numpy_familiarity: "NumPy Proficiency",
      ai_tool_use_frequency: "AI Tool Use Frequency",
      ai_code_review_experience: "AI Code Review Experience",
    },
  },
  zh: {
    switchLabel: "English",
    eyebrow: "研究问卷",
    title: "AI 代码监督能力研究",
    pretest: "前测",
    pretestTitle: "前测信息",
    pretestHint: "请先完成 A/B 共用前测。参与者 ID 将由系统自动分配。",
    consent: "知情同意",
    select: "请选择",
    agree: "I agree",
    disagree: "I do not agree",
    start: "开始任务",
    taskProgress: (id) => `任务 ${id} / 6`,
    supervisionCard: "监督卡",
    submitTask: "提交本任务",
    submitAll: "提交问卷",
    posttestProgress: "后测",
    submitPosttest: "提交后测",
    complete: "完成",
    completeTitle: "提交完成",
    completeText: "你的作答已记录。系统不会向被试展示分数、答案或解析。",
    unavailable: "任务不可用",
    offline: "当前网络不可用。本页作答已缓存在本地。",
    pending: "有一份提交已保存在本地，网络恢复后会自动重试。",
    restored: "已恢复本地草稿。",
    resetHome: "回到首页",
    fields: {
      age: "年龄",
      gender: "性别",
      grade_year: "年级",
      major: "专业",
      programming_experience_years: "编程经验",
      python_familiarity: "Python 掌握程度",
      file_io_familiarity: "撰写/阅读文献能力",
      numpy_familiarity: "NumPy 掌握程度",
      ai_tool_use_frequency: "AI 工具使用频率",
      ai_code_review_experience: "AI 代码审查经验",
    },
  },
};

const optionLabels = {
  gender: {
    en: ["Female", "Male", "Non-binary", "Prefer not to say"],
    zh: ["女性", "男性", "非二元", "不愿透露"],
    values: ["Female", "Male", "Non-binary", "Prefer not to say"],
  },
  grade_year: {
    en: ["Year 1", "Year 2", "Year 3", "Year 4", "Master", "PhD", "Other"],
    zh: ["大一", "大二", "大三", "大四", "硕士", "博士", "其他"],
    values: ["Year 1", "Year 2", "Year 3", "Year 4", "Master", "PhD", "Other"],
  },
  programming_experience_years: {
    en: ["Less than 1", "1-2", "3-4", "5 or more"],
    zh: ["少于 1 年", "1-2 年", "3-4 年", "5 年及以上"],
    values: ["Less than 1", "1-2", "3-4", "5 or more"],
  },
  python_familiarity: {
    en: ["No experience", "Basic understanding", "Comfortable", "Proficient", "Expert"],
    zh: ["完全不熟悉", "了解基础", "能独立使用", "熟练掌握", "非常精通"],
    values: ["1", "2", "3", "4", "5"],
  },
  file_io_familiarity: {
    en: ["Never read/written academic papers", "Occasionally read papers or reports", "Comfortable reading and summarizing literature", "Proficient in literature review and academic writing", "Expert in academic research writing and synthesis"],
    zh: ["从未阅读或撰写过学术文献", "偶尔阅读论文或报告", "能阅读并归纳文献内容", "熟练进行文献综述与学术写作", "精通学术研究写作与文献整合"],
    values: ["1", "2", "3", "4", "5"],
  },
  numpy_familiarity: {
    en: ["Never used NumPy", "Used a few basic functions", "Comfortable with arrays and indexing", "Proficient with NumPy operations", "Expert in NumPy and numerical computing"],
    zh: ["从未使用过 NumPy", "用过少量基础函数", "能使用数组与索引操作", "熟练使用 NumPy 运算", "精通 NumPy 与数值计算"],
    values: ["1", "2", "3", "4", "5"],
  },
  ai_tool_use_frequency: {
    en: ["Never", "Rarely", "Sometimes", "Often", "Very often"],
    zh: ["从不", "很少", "有时", "经常", "非常频繁"],
    values: ["Never", "Rarely", "Sometimes", "Often", "Very often"],
  },
  ai_code_review_experience: {
    en: ["Never", "Rarely", "Sometimes", "Often", "Very often"],
    zh: ["从不", "很少", "有时", "经常", "非常频繁"],
    values: ["Never", "Rarely", "Sometimes", "Often", "Very often"],
  },
};

const state = {
  status: "loading",
  nextStage: null,
  nextTask: null,
  lang: localStorage.getItem("questionnaire_lang") || "en",
};

const pretestFields = [
  ["age", "number"],
  ["gender", "select"],
  ["grade_year", "select"],
  ["major", "text"],
  ["programming_experience_years", "select"],
  ["python_familiarity", "select"],
  ["file_io_familiarity", "select"],
  ["numpy_familiarity", "select"],
  ["ai_tool_use_frequency", "select"],
  ["ai_code_review_experience", "select"],
];

function t(key) {
  return i18n[state.lang][key];
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function setLanguage(lang) {
  state.lang = lang;
  localStorage.setItem("questionnaire_lang", lang);
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  languageToggle.textContent = t("switchLabel");
  resetHomeButton.textContent = t("resetHome");
  if (state.status === "in_progress" && state.nextTask >= 1 && state.nextTask <= 6) {
    loadTask(state.nextTask);
  } else if (state.status === "posttest") {
    loadPosttest();
  } else if (state.status === "complete") {
    renderComplete();
  } else if (state.status !== "loading") {
    renderPretest();
  } else {
    progressLabel.textContent = t("pretest");
  }
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = response.headers.get("content-type")?.includes("application/json") ? await response.json() : null;
  if (!response.ok) throw new Error(data?.detail || "Request failed");
  return data;
}

function draftKey(name) {
  return `questionnaire_draft_${name}`;
}

function readForm(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  if (data.age) data.age = Number(data.age);
  return data;
}

function restoreForm(form, key) {
  const raw = localStorage.getItem(draftKey(key));
  if (!raw) return;
  const data = JSON.parse(raw);
  for (const [name, value] of Object.entries(data)) {
    const field = form.elements[name];
    if (!field) continue;
    if (field instanceof RadioNodeList) {
      const radio = Array.from(field).find((item) => item.value === value);
      if (radio) radio.checked = true;
    } else {
      field.value = value;
    }
  }
  networkStatus.textContent = t("restored");
}

function bindDraft(form, key) {
  restoreForm(form, key);
  form.addEventListener("input", () => {
    localStorage.setItem(draftKey(key), JSON.stringify(readForm(form)));
  });
}

function savePending(payload) {
  localStorage.setItem("questionnaire_pending_submit", JSON.stringify(payload));
  networkStatus.textContent = navigator.onLine ? t("pending") : t("offline");
}

async function retryPending() {
  const raw = localStorage.getItem("questionnaire_pending_submit");
  if (!raw || !navigator.onLine) return;
  const pending = JSON.parse(raw);
  try {
    const result = await api(pending.path, { method: pending.method, body: JSON.stringify(pending.body) });
    localStorage.removeItem("questionnaire_pending_submit");
    if (pending.kind === "pretest") {
      state.status = "in_progress";
      state.nextStage = result.next_stage;
      state.nextTask = result.next_task;
      localStorage.removeItem(draftKey("pretest"));
      await loadTask(state.nextTask);
    } else if (pending.kind === "task") {
      state.status = result.posttest_required ? "posttest" : "in_progress";
      state.nextStage = result.posttest_required ? "posttest" : "task";
      state.nextTask = result.next_task;
      localStorage.removeItem(draftKey(`task_${pending.taskId}`));
      if (result.posttest_required) await loadPosttest();
      else if (result.complete) renderComplete();
      else await loadTask(result.next_task);
    } else if (pending.kind === "posttest") {
      localStorage.removeItem("questionnaire_pending_submit");
      localStorage.removeItem(draftKey("posttest"));
      renderComplete();
    }
  } catch {
    networkStatus.textContent = t("pending");
  }
}

function renderPretest() {
  progressLabel.textContent = t("pretest");
  const fields = pretestFields
    .map(([name, type]) => {
      const label = i18n[state.lang].fields[name];
      if (type === "select") {
        const config = optionLabels[name];
        return `<label class="field"><span>${label}</span><select name="${name}" required><option value="">${t("select")}</option>${config.values
          .map((value, index) => `<option value="${escapeHtml(value)}">${escapeHtml(config[state.lang][index])}</option>`)
          .join("")}</select></label>`;
      }
      return `<label class="field"><span>${label}</span><input name="${name}" type="${type}" required /></label>`;
    })
    .join("");

  view.innerHTML = `
    <form id="pretestForm">
      <h2>${t("pretestTitle")}</h2>
      <p class="status">${t("pretestHint")}</p>
      <div class="grid">
        <label class="field">
          <span>${t("consent")}</span>
          <select name="consent" required>
            <option value="">${t("select")}</option>
            <option value="I agree">${t("agree")}</option>
            <option value="I do not agree">${t("disagree")}</option>
          </select>
        </label>
        ${fields}
      </div>
      <div class="actions">
        <button class="primary" type="submit">${t("start")}</button>
      </div>
      <p class="status error" id="error"></p>
    </form>
  `;

  const form = document.getElementById("pretestForm");
  bindDraft(form, "pretest");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = readForm(form);
    const pending = { kind: "pretest", path: "/api/pretest", method: "POST", body: payload };
    try {
      const result = await api(pending.path, { method: pending.method, body: JSON.stringify(payload) });
      localStorage.removeItem(draftKey("pretest"));
      state.status = "in_progress";
      state.nextStage = result.next_stage;
      state.nextTask = result.next_task;
      await loadTask(state.nextTask);
    } catch (error) {
      savePending(pending);
      document.getElementById("error").textContent = error.message;
    }
  });
}

function renderOptions(fieldName, options, values) {
  return options
    .map((option, index) => {
      const value = values?.[index] || option.label || option;
      const text = option.text ? `${option.label}. ${option.text}` : option;
      return `
        <label class="option">
          <input type="radio" name="${fieldName}" value="${escapeHtml(value)}" required />
          <span>${escapeHtml(text)}</span>
        </label>
      `;
    })
    .join("");
}

function validateRequiredRadioGroups(form) {
  form.querySelectorAll(".question.unanswered").forEach((node) => {
    node.classList.remove("unanswered");
    node.querySelector(".question-warning")?.remove();
  });
  const names = [...new Set([...form.querySelectorAll('input[type="radio"][required]')].map((input) => input.name))];
  for (const name of names) {
    const group = [...form.querySelectorAll(`input[type="radio"][name="${CSS.escape(name)}"]`)];
    if (!group.some((input) => input.checked)) {
      const question = group[0].closest(".question");
      question.classList.add("unanswered");
      const warning = document.createElement("p");
      warning.className = "question-warning";
      warning.textContent = state.lang === "zh" ? "请先回答这个问题。" : "Please answer this question before submitting.";
      question.appendChild(warning);
      question.scrollIntoView({ behavior: "smooth", block: "center" });
      group[0].focus({ preventScroll: true });
      return false;
    }
  }
  return true;
}

async function loadTask(taskId) {
  progressLabel.textContent = t("taskProgress")(taskId);
  try {
    const task = await api(`/api/task/${taskId}?lang=${state.lang}`);
    renderTask(task);
  } catch (error) {
    view.innerHTML = `<h2>${t("unavailable")}</h2><p class="status error">${escapeHtml(error.message)}</p>`;
  }
}

function renderTask(task) {
  const supervision = task.supervision_card
    ? `
      <section class="supervision">
        <h3>${t("supervisionCard")}</h3>
        ${task.supervision_card
          .map(
            (item) => `
              <div class="question">
                <strong>${escapeHtml(item.dimension)}</strong>
                <p>${escapeHtml(item.prompt)}</p>
                <div class="options">${renderOptions(item.id, item.options, item.values)}</div>
              </div>
            `
          )
          .join("")}
      </section>
    `
    : "";

  const questions = task.questions
    .map(
      (question) => `
        <div class="question">
          <h3>${escapeHtml(question.id)}</h3>
          ${question.context ? `<p class="context">${escapeHtml(question.context)}</p>` : ""}
          <p>${escapeHtml(question.prompt)}</p>
          <div class="options">${renderOptions(question.id, question.options)}</div>
        </div>
      `
    )
    .join("");

  view.innerHTML = `
    <form id="taskForm" class="task-layout">
      <section class="task-block">
        <h2>${escapeHtml(task.title)}</h2>
        <ol class="requirements">${task.requirements.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ol>
        <pre><code>${escapeHtml(task.code)}</code></pre>
      </section>
      ${supervision}
      <section class="task-block">${questions}</section>
      <div class="actions">
        <button class="primary" type="submit">${task.id === 6 ? t("submitAll") : t("submitTask")}</button>
      </div>
      <p class="status error" id="error"></p>
    </form>
  `;

  const form = document.getElementById("taskForm");
  bindDraft(form, `task_${task.id}`);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!validateRequiredRadioGroups(form)) return;
    const formData = new FormData(form);
    const answers = {};
    const supervision_answers = {};
    for (const [key, value] of formData.entries()) {
      if (key.startsWith("T")) supervision_answers[key] = value;
      if (key.startsWith("Q")) answers[key] = value;
    }
    const pending = {
      kind: "task",
      taskId: task.id,
      path: `/api/task/${task.id}`,
      method: "POST",
      body: { answers, supervision_answers },
    };
    try {
      const result = await api(pending.path, { method: pending.method, body: JSON.stringify(pending.body) });
      localStorage.removeItem(draftKey(`task_${task.id}`));
      state.status = result.posttest_required ? "posttest" : "in_progress";
      state.nextStage = result.posttest_required ? "posttest" : "task";
      state.nextTask = result.next_task;
      if (result.posttest_required) {
        window.scrollTo({ top: 0 });
        await loadPosttest();
      } else if (result.complete) renderComplete();
      else {
        window.scrollTo({ top: 0 });
        await loadTask(result.next_task);
      }
    } catch (error) {
      savePending(pending);
      document.getElementById("error").textContent = error.message;
    }
  });
}

async function loadPosttest() {
  progressLabel.textContent = t("posttestProgress");
  try {
    const schema = await api(`/api/posttest?lang=${state.lang}`);
    renderPosttest(schema);
  } catch (error) {
    view.innerHTML = `<h2>${t("unavailable")}</h2><p class="status error">${escapeHtml(error.message)}</p>`;
  }
}

function renderPosttest(schema) {
  const questionsBySection = new Map();
  for (const question of schema.questions) {
    if (!questionsBySection.has(question.section)) questionsBySection.set(question.section, []);
    questionsBySection.get(question.section).push(question);
  }
  const sections = schema.sections
    .map((section) => {
      const questions = questionsBySection.get(section.id) || [];
      return `
        <section class="task-block">
          <h3>${escapeHtml(section.title)}</h3>
          ${questions
            .map(
              (question) => `
                <div class="question">
                  <p>${escapeHtml(question.prompt)}</p>
                  <div class="options">
                    ${question.options
                      .map(
                        (option) => `
                          <label class="option">
                            <input type="radio" name="${escapeHtml(question.id)}" value="${escapeHtml(option.value)}" required />
                            <span>${escapeHtml(option.label)}</span>
                          </label>
                        `
                      )
                      .join("")}
                  </div>
                </div>
              `
            )
            .join("")}
        </section>
      `;
    })
    .join("");

  view.innerHTML = `
    <form id="posttestForm" class="task-layout">
      <section class="task-block">
        <h2>${escapeHtml(schema.title)}</h2>
        <p class="status">${escapeHtml(schema.intro)}</p>
      </section>
      ${sections}
      <div class="actions">
        <button class="primary" type="submit">${t("submitPosttest")}</button>
      </div>
      <p class="status error" id="error"></p>
    </form>
  `;

  const form = document.getElementById("posttestForm");
  bindDraft(form, "posttest");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!validateRequiredRadioGroups(form)) return;
    const body = Object.fromEntries(new FormData(form).entries());
    const pending = {
      kind: "posttest",
      path: "/api/posttest",
      method: "POST",
      body,
    };
    try {
      const result = await api(pending.path, { method: pending.method, body: JSON.stringify(body) });
      if (result.complete) {
        state.status = "complete";
        state.nextStage = null;
        state.nextTask = null;
        localStorage.removeItem(draftKey("posttest"));
        renderComplete();
      }
    } catch (error) {
      savePending(pending);
      document.getElementById("error").textContent = error.message;
    }
  });
}

function renderComplete() {
  progressLabel.textContent = t("complete");
  view.innerHTML = `
    <h2>${t("completeTitle")}</h2>
    <p class="status">${t("completeText")}</p>
  `;
}

async function resetToHome() {
  try {
    await api("/api/session/reset", { method: "POST" });
  } catch {
    // If offline, still clear browser-side drafts so the user can restart locally.
  }
  localStorage.removeItem("questionnaire_pending_submit");
  for (const key of Object.keys(localStorage)) {
    if (key.startsWith("questionnaire_draft_")) {
      localStorage.removeItem(key);
    }
  }
  state.status = "none";
  state.nextStage = null;
  state.nextTask = 0;
  networkStatus.textContent = "";
  renderPretest();
}

function applyCurrentSession(current) {
  state.status = current.status;
  state.nextStage = current.next_stage || null;
  state.nextTask = current.next_task || null;
  if (current.status === "in_progress") {
    loadTask(current.next_task);
  } else if (current.status === "posttest") {
    loadPosttest();
  } else if (current.status === "complete") {
    renderComplete();
  } else {
    renderPretest();
  }
}

async function bootstrapSession() {
  setLanguage(state.lang);
  await retryPending();
  try {
    const current = await api("/api/session/current");
    applyCurrentSession(current);
  } catch {
    state.status = "none";
    renderPretest();
  }
}

languageToggle.addEventListener("click", () => setLanguage(state.lang === "en" ? "zh" : "en"));
resetHomeButton.addEventListener("click", resetToHome);
window.addEventListener("online", retryPending);
window.addEventListener("offline", () => {
  networkStatus.textContent = t("offline");
});

bootstrapSession();
