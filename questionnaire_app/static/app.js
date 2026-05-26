const view = document.getElementById("view");
const progressLabel = document.getElementById("progressLabel");
const overallProgressLabel = document.getElementById("overallProgressLabel");
const timerLabel = document.getElementById("timerLabel");
const languageToggle = document.getElementById("languageToggle");
const resetHomeButton = document.getElementById("resetHome");
const networkStatus = document.getElementById("networkStatus");
const topbar = document.querySelector(".topbar");

const i18n = {
  en: {
    switchLabel: "中文",
    eyebrow: "Research Questionnaire",
    title: "AI Coding Agent Supervision Study",
    pretest: "Pretest",
    pretestTitle: "Pretest Information",
    pretestHint: "Please complete the shared pretest before entering the task section. Your participant ID will be assigned automatically.",
    introTitle: "Welcome to the AI Coding Agent Supervision Study",
    introPurpose: "In this study, an AI coding agent generates code for a task. You act as the human supervisor and judge whether the agent's output meets the requirements, contains hidden errors, needs more testing, and can be delivered.",
    introSections: [
      {
        title: "What will you do?",
        body: "You will first answer background questions, then review six AI coding agent outputs, and finally complete a short post-task questionnaire.",
      },
      {
        title: "How should you answer?",
        body: "Read the task requirements, inspect the agent's output, reason through the given inputs, and choose the option that best matches your own supervision judgment.",
      },
    ],
    introContinue: "Continue to Pretest",
    introNotInterested: "I do not want to participate",
    notInterestedText: "No other action is required. You may close this page now.",
    consent: "Consent",
    noticeTitle: "Research Notice and Rules",
    noticeIntro: "Please read the following rules carefully before starting.",
    noticeSections: [
      {
        title: "Research Purpose",
        body: "This questionnaire studies AI coding agent supervision ability: understanding requirements, checking the agent's output, identifying hidden errors, deciding whether more testing is needed, and judging delivery risk.",
      },
      {
        title: "What will happen if you participate?",
        body: "You will complete a pretest, six formal tasks, and a posttest. The formal response stage is limited to 40 minutes.",
      },
      {
        title: "Data and Rules",
        body: "The study records responses, progress, group assignment, submission time, and response duration for academic research and statistical analysis only. Please answer independently without AI coding agent tools, search engines, coding assistants, or help from others.",
      },
      {
        title: "If you are no longer interested",
        body: "Participation is voluntary. If you do not want to continue, choose Cancel or close this page.",
      },
    ],
    noticeRules: [
      "This questionnaire includes a pretest, formal tasks, and a posttest. The total formal response time is limited to 40 minutes. Timing starts after you click “Agree and Start”; page refreshes, closing the page, disconnections, and re-entry all count toward the total time.",
      "Please complete the questionnaire independently. Do not use AI coding agent tools, search engines, coding assistants, or help from others to gain answer-related assistance.",
      "This questionnaire collects response data, progress, group assignment, submission time, and response duration. The data is used only for academic research and statistical analysis, and will not be used for commercial purposes or personal identification.",
      "If the response time exceeds 40 minutes, the system will automatically stop this attempt. The data from this attempt will not be included as a valid sample. You may return to the home page and restart.",
    ],
    noticeAgreement: "I have read and agree to the research notice and questionnaire rules",
    noticeStart: "Agree and Start",
    noticeCancel: "Cancel",
    notStarted: "Not started",
    overallPretest: "Overall progress: Pretest · 1 / 8",
    overallTask: (id) => `Overall progress: Task ${id} / 6 · ${id + 1} / 8`,
    overallPosttest: "Overall progress: Posttest · 8 / 8",
    overallComplete: "Overall progress: Complete · 8 / 8",
    remaining: (time) => `Remaining ${time}`,
    timeoutTitle: "Time limit reached. Please restart.",
    timeoutText: "This questionnaire is limited to 40 minutes. Because the current attempt exceeded the time limit, this response will not be included as a valid sample. Please return to the home page and restart.",
    restart: "Restart",
    select: "Select",
    agree: "我同意",
    disagree: "我不同意",
    start: "Start Tasks",
    taskProgress: (id) => `Task ${id} / 6`,
    taskGuideTitle: "How to Answer",
    taskGuideSteps: [
      "Read the task requirements first: they define what the AI coding agent was asked to deliver.",
      "Then inspect the agent's output and reason about what it actually does.",
      "For behavior questions, answer according to the code or execution trace. For correctness questions, answer according to the original task requirements.",
      "Judge whether the agent output satisfies the task, whether hidden errors remain, whether more testing is needed, and whether it can be delivered.",
    ],
    answerBackgroundTitle: "Answering Background",
    answerBackgroundCode: "An AI coding agent generated the following code according to the task requirements. You are the human supervisor. Decide whether the agent's output meets the requirements, contains hidden errors, needs further testing, and can be delivered.",
    answerBackgroundTrace: "An AI coding agent completed the following work according to the task requirements. You are the human supervisor. Decide whether the agent's actions, evidence, and final output meet the requirements, contain hidden errors, need further testing, and can be delivered.",
    taskSectionLabels: {
      requirements: "Task Requirements",
      aiCode: "Code Generated by the AI Coding Agent",
      agentTrace: "AI Coding Agent Work Log",
      questions: "Formal Questions",
      givenInput: "Given Input",
    },
    supervisionCard: "Supervision Card",
    supervisionIntro: "This card helps you review the AI coding agent's output step by step. Answer it based on your own judgment; it is not an answer key.",
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
    requiredQuestionWarning: "Please answer this question before submitting.",
    resetHome: "New Session",
    fields: {
      questionnaire_version: "Questionnaire Version",
      grade_year: "Grade Year",
      major: "Major",
      programming_experience_years: "Programming Experience",
      python_familiarity: "Python Proficiency",
      file_io_familiarity: "Academic Reading/Writing Ability",
      numpy_familiarity: "NumPy Proficiency",
      ai_tool_use_frequency: "AI Coding Agent Tool Use Frequency",
      ai_code_review_experience: "AI Coding Agent Output Review Experience",
    },
  },
  zh: {
    switchLabel: "English",
    eyebrow: "研究问卷",
    title: "人工智能编程智能体(AI coding agent)交付监督研究",
    pretest: "前测",
    pretestTitle: "开始前的小问卷",
    pretestHint: "请先填写基本信息。系统会自动生成参与者 ID，你不需要手动填写。",
    introTitle: "欢迎参加人工智能编程智能体(AI coding agent)监督研究",
    introPurpose: "本研究的场景是：一个人工智能编程智能体(AI coding agent)根据任务要求生成了代码(code)。你作为人工监督者(human supervisor)，需要判断它的输出是否满足需求、是否存在隐藏错误、是否需要进一步测试，以及是否可以交付。",
    introSections: [
      {
        title: "你需要做什么？",
        body: "你会先填写基本信息，然后查看 6 份人工智能编程智能体(AI coding agent)的交付结果，最后完成一份很短的感受问卷。",
      },
      {
        title: "怎么判断？",
        body: "先看任务要求，再看智能体(agent)生成的代码(code)或运行记录。请站在人工监督者(human supervisor)的角度，选择最符合你判断的答案。",
      },
    ],
    introContinue: "进入前测",
    introNotInterested: "我不想参加",
    notInterestedText: "无需进行其他操作。你可以直接关闭本页面。",
    consent: "知情同意",
    noticeTitle: "研究说明与作答规则",
    noticeIntro: "开始前请先确认以下规则：",
    noticeSections: [
      {
        title: "这项研究在看什么？",
        body: "本问卷关注你能否监督人工智能编程智能体(AI coding agent)的交付结果：看懂任务、核对输出、发现隐藏错误、判断是否还要测试，以及判断是否能交付。",
      },
      {
        title: "你会经历哪些步骤？",
        body: "你会完成开始前的小问卷、6 个正式任务和结束后的小问卷。正式任务限时 40 分钟。",
      },
      {
        title: "数据与规则",
        body: "系统会记录你的答案、进度、分组、提交时间和用时，仅用于学术研究和统计分析。请独立完成，不使用人工智能编程智能体(AI coding agent)工具、搜索引擎、代码助手或他人帮助。",
      },
      {
        title: "如果你不想继续参加",
        body: "参与完全自愿。如果你不想继续，可以点击取消或关闭本页面。",
      },
    ],
    noticeRules: [
      "本问卷包含开始前的小问卷、正式任务和结束后的小问卷。正式任务总时长为 40 分钟。点击“同意并开始作答”后开始计时，刷新、关闭页面、断网或重新进入都会继续计入时间。",
      "请独立完成作答。不要使用人工智能编程智能体(AI coding agent)工具、搜索引擎、代码助手或他人帮助来寻找答案。",
      "系统会收集你的答案、进度、分组、提交时间和作答用时。这些数据只用于学术研究和统计分析，不用于商业用途，也不会用来识别你的个人身份。",
      "如果正式任务超过 40 分钟，系统会自动结束本次作答，本次数据不会作为有效样本。你可以回到首页重新开始。",
    ],
    noticeAgreement: "我已阅读并同意研究说明与作答规则",
    noticeStart: "同意并开始作答",
    noticeCancel: "取消",
    notStarted: "未开始",
    overallPretest: "总进度：前测 · 1 / 8",
    overallTask: (id) => `总进度：任务 ${id} / 6 · ${id + 1} / 8`,
    overallPosttest: "总进度：后测 · 8 / 8",
    overallComplete: "总进度：完成 · 8 / 8",
    remaining: (time) => `剩余 ${time}`,
    timeoutTitle: "已超过 40 分钟，请重新开始",
    timeoutText: "本次正式任务限时 40 分钟。由于当前作答已经超时，这次回答不会作为有效样本。请返回首页重新开始。",
    restart: "重新作答",
    select: "请选择",
    agree: "I agree",
    disagree: "I do not agree",
    start: "开始任务",
    taskProgress: (id) => `任务 ${id} / 6`,
    taskGuideTitle: "作答时请这样看",
    taskGuideSteps: [
      "先看任务要求：它说明人工智能编程智能体(AI coding agent)原本应该交付什么。",
      "再看智能体(agent)生成的代码(code)或运行记录，判断它实际做了什么。",
      "遇到行为类问题时，按代码(code)或运行记录的实际结果回答；遇到正确性问题时，按任务要求回答。",
      "最后判断该智能体(agent)的输出是否满足需求、是否存在隐藏错误、是否需要进一步测试，以及是否可以交付。",
    ],
    answerBackgroundTitle: "回答背景",
    answerBackgroundCode: "一个人工智能编程智能体(AI coding agent)根据任务要求生成了以下代码(code)。你作为人工监督者(human supervisor)，需要判断该智能体(agent)的输出是否满足需求、是否存在隐藏错误、是否需要进一步测试，以及是否可以交付。",
    answerBackgroundTrace: "一个人工智能编程智能体(AI coding agent)根据任务要求完成了以下工作。你作为人工监督者(human supervisor)，需要判断该智能体(agent)的操作、证据和最终输出是否满足需求、是否存在隐藏错误、是否需要进一步测试，以及是否可以交付。",
    taskSectionLabels: {
      requirements: "任务要求",
      aiCode: "人工智能编程智能体(AI coding agent)给出的代码(code)",
      agentTrace: "人工智能编程智能体(AI coding agent)工作记录",
      questions: "正式问题",
      givenInput: "给定输入",
    },
    supervisionCard: "监督检查卡",
    supervisionIntro: "这张卡帮助你一步步检查人工智能编程智能体(AI coding agent)的交付结果。请按自己的判断填写，它不是答案提示。",
    submitTask: "提交本任务",
    submitAll: "提交问卷",
    posttestProgress: "结束后小问卷",
    submitPosttest: "提交结束后小问卷",
    complete: "完成",
    completeTitle: "提交完成",
    completeText: "你的作答已记录。系统不会向参与者展示分数、答案或解析。",
    unavailable: "任务不可用",
    offline: "当前网络不可用。本页作答已缓存在本地。",
    pending: "有一份提交已保存在本地，网络恢复后会自动重试。",
    restored: "已恢复本地草稿。",
    requiredQuestionWarning: "请先回答这个问题。",
    resetHome: "回到首页",
    fields: {
      questionnaire_version: "任务版本",
      grade_year: "年级",
      major: "专业",
      programming_experience_years: "编程经验",
      python_familiarity: "Python 掌握程度",
      file_io_familiarity: "阅读和写作学术资料的经验",
      numpy_familiarity: "NumPy 掌握程度",
      ai_tool_use_frequency: "人工智能编程智能体(AI coding agent)工具使用频率",
      ai_code_review_experience: "人工智能编程智能体(AI coding agent)输出审查经验",
    },
  },
};

const optionLabels = {
  questionnaire_version: {
    en: ["Python Version", "C Version", "Agent Version"],
    zh: ["Python 版本", "C 语言版本", "智能体(agent)监督版本 / Agent 监督版本"],
    values: ["python", "c", "agent"],
  },
  grade_year: {
    en: ["Year 1", "Year 2", "Year 3", "Year 4", "Master", "PhD", "Other"],
    zh: ["大一", "大二", "大三", "大四", "硕士", "博士", "其他"],
    values: ["Year 1", "Year 2", "Year 3", "Year 4", "Master", "PhD", "Other"],
  },
  major: {
    en: ["计算机类", "电子信息类", "自动化类", "电气类", "机械类"],
    zh: ["计算机类", "电子信息类", "自动化类", "电气类", "机械类"],
    values: ["计算机类", "电子信息类", "自动化类", "电气类", "机械类"],
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

const majorOptionsByVersion = {
  python: {
    en: ["计算机类", "电子信息类", "自动化类", "电气类", "机械类"],
    zh: ["计算机类", "电子信息类", "自动化类", "电气类", "机械类"],
    values: ["计算机类", "电子信息类", "自动化类", "电气类", "机械类"],
  },
  c: {
    en: ["计算机科学与技术", "网络空间安全", "数字媒体技术", "物联网工程", "智能科技与技术", "软件工程"],
    zh: ["计算机科学与技术", "网络空间安全", "数字媒体技术", "物联网工程", "智能科技与技术", "软件工程"],
    values: ["计算机科学与技术", "网络空间安全", "数字媒体技术", "物联网工程", "智能科技与技术", "软件工程"],
  },
  agent: {
    en: ["Computer Science", "Data Science", "Mathematics", "Engineering", "Information Management"],
    zh: ["计算机类", "数据科学类", "数学类", "工程类", "信息管理类"],
    values: ["Computer Science", "Data Science", "Mathematics", "Engineering", "Information Management"],
  },
};

const familiarityLabelsByVersion = {
  python: {
    en: "Python Proficiency",
    zh: "Python 掌握程度",
  },
  c: {
    en: "C Language Proficiency",
    zh: "C 语言掌握程度",
  },
  agent: {
    en: "Programming Proficiency",
    zh: "编程基础掌握程度",
  },
};

const state = {
  status: "loading",
  nextStage: null,
  nextTask: null,
  lang: localStorage.getItem("questionnaire_lang") || "zh",
  expiresAt: null,
  timeLimitSeconds: 40 * 60,
  enabledVersions: new Set(["python", "c", "agent"]),
};

let timerInterval = null;
let activeModal = null;
let showNotInterestedMessage = false;
let lastScrollY = window.scrollY;

function updateTopbarVisibility() {
  if (!topbar) return;
  const currentY = Math.max(0, window.scrollY);
  const threshold = topbar.offsetHeight + 24;
  const scrollingDown = currentY > lastScrollY + 4;
  const scrollingUp = currentY < lastScrollY - 4;

  if (currentY <= threshold) {
    topbar.classList.remove("is-floating", "is-hidden");
  } else if (scrollingDown) {
    topbar.classList.add("is-floating", "is-hidden");
  } else if (scrollingUp) {
    topbar.classList.add("is-floating");
    topbar.classList.remove("is-hidden");
  }
  lastScrollY = currentY;
}

function ensureModalRoot() {
  let root = document.getElementById("modalRoot");
  if (!root) {
    root = document.createElement("div");
    root.id = "modalRoot";
    document.body.appendChild(root);
  }
  return root;
}

function closeModal() {
  const root = ensureModalRoot();
  root.innerHTML = "";
  activeModal = null;
  showNotInterestedMessage = false;
}

function renderModalLanguageButton() {
  return `<button class="ghost modal-language" id="modalLanguageToggle" type="button">${t("switchLabel")}</button>`;
}

function renderModal(html) {
  const root = ensureModalRoot();
  root.innerHTML = `
    <div class="modal-overlay" role="presentation">
      <section class="modal-dialog" role="dialog" aria-modal="true">
        ${html}
      </section>
    </div>
  `;
  document.getElementById("modalLanguageToggle")?.addEventListener("click", () => setLanguage(state.lang === "en" ? "zh" : "en"));
}

function maybeShowIntroModal() {
  if (sessionStorage.getItem("questionnaire_intro_seen") || activeModal) return;
  renderIntroModal();
}

function renderIntroModal() {
  activeModal = "intro";
  const sections = t("introSections")
    .map(
      (section) => `
        <section class="modal-section">
          <h3>${escapeHtml(section.title)}</h3>
          <p>${escapeHtml(section.body)}</p>
        </section>
      `
    )
    .join("");
  renderModal(`
    <div class="modal-header">
      <h2>${t("introTitle")}</h2>
      ${renderModalLanguageButton()}
    </div>
    <p class="modal-lead">${t("introPurpose")}</p>
    ${sections}
    ${showNotInterestedMessage ? `<p class="status error">${t("notInterestedText")}</p>` : ""}
    <div class="actions">
      <button class="ghost" type="button" id="introNotInterested">${t("introNotInterested")}</button>
      <button class="primary" type="button" id="introContinue">${t("introContinue")}</button>
    </div>
  `);
  document.getElementById("introContinue").onclick = () => {
    sessionStorage.setItem("questionnaire_intro_seen", "1");
    closeModal();
  };
  document.getElementById("introNotInterested").onclick = () => {
    showNotInterestedMessage = true;
    renderIntroModal();
  };
}

const pretestFields = [
  ["questionnaire_version", "select"],
  ["grade_year", "select"],
  ["major", "select"],
  ["programming_experience_years", "select"],
  ["python_familiarity", "select"],
  ["file_io_familiarity", "select"],
  ["numpy_familiarity", "select"],
  ["ai_tool_use_frequency", "select"],
  ["ai_code_review_experience", "select"],
];

function pretestFieldsForVersion(version) {
  return pretestFields.filter(([name]) => version === "python" || name !== "numpy_familiarity");
}

function enabledVersionValues() {
  return optionLabels.questionnaire_version.values.filter((value) => state.enabledVersions.has(value));
}

function configForField(name, version) {
  const config = name === "major" ? majorOptionsByVersion[version] : optionLabels[name];
  if (name !== "questionnaire_version") return config;
  const enabled = enabledVersionValues();
  const indexes = optionLabels.questionnaire_version.values
    .map((value, index) => ({ value, index }))
    .filter((item) => enabled.includes(item.value))
    .map((item) => item.index);
  return {
    values: enabled,
    en: indexes.map((index) => optionLabels.questionnaire_version.en[index]),
    zh: indexes.map((index) => optionLabels.questionnaire_version.zh[index]),
  };
}

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

function formatClock(totalSeconds) {
  const safe = Math.max(0, Number(totalSeconds) || 0);
  const minutes = Math.floor(safe / 60);
  const seconds = safe % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function setOverallProgress(stage, taskId = null) {
  if (stage === "pretest") overallProgressLabel.textContent = t("overallPretest");
  else if (stage === "task") overallProgressLabel.textContent = t("overallTask")(taskId);
  else if (stage === "posttest") overallProgressLabel.textContent = t("overallPosttest");
  else if (stage === "complete") overallProgressLabel.textContent = t("overallComplete");
  else overallProgressLabel.textContent = t("notStarted");
}

function setTimerFromSession(session) {
  state.timeLimitSeconds = session.time_limit_seconds || 40 * 60;
  if (typeof session.remaining_seconds === "number") {
    state.expiresAt = Date.now() + session.remaining_seconds * 1000;
  } else if (!state.expiresAt) {
    state.expiresAt = Date.now() + state.timeLimitSeconds * 1000;
  }
  startTimer();
}

function stopTimer() {
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = null;
}

function updateTimer() {
  if (!state.expiresAt || ["none", "loading", "complete", "timeout"].includes(state.status)) {
    timerLabel.textContent = formatClock(state.timeLimitSeconds);
    timerLabel.classList.remove("warning");
    return;
  }
  const remaining = Math.max(0, Math.ceil((state.expiresAt - Date.now()) / 1000));
  timerLabel.textContent = t("remaining")(formatClock(remaining));
  timerLabel.classList.toggle("warning", remaining <= 5 * 60);
  if (remaining <= 0) {
    stopTimer();
    handleTimeout();
  }
}

function startTimer() {
  stopTimer();
  updateTimer();
  timerInterval = setInterval(updateTimer, 1000);
}

function clearQuestionnaireLocalState() {
  localStorage.removeItem("questionnaire_pending_submit");
  for (const key of Object.keys(localStorage)) {
    if (key.startsWith("questionnaire_draft_")) {
      localStorage.removeItem(key);
    }
  }
}

async function handleTimeout() {
  try {
    await api("/api/session/current");
  } catch {
    // The timeout UI still needs to be shown even if the network is unavailable.
  }
  clearQuestionnaireLocalState();
  renderTimeoutNotice();
}

function setLanguage(lang) {
  const modalBeforeLanguageChange = activeModal;
  state.lang = lang;
  localStorage.setItem("questionnaire_lang", lang);
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  languageToggle.textContent = t("switchLabel");
  resetHomeButton.textContent = t("resetHome");
  if (state.status === "pretest") {
    renderPretest();
  } else if (state.status === "notice") {
    renderResearchNotice();
  } else if (state.status === "in_progress" && state.nextTask >= 1 && state.nextTask <= 6) {
    loadTask(state.nextTask);
  } else if (state.status === "posttest") {
    loadPosttest();
  } else if (state.status === "complete") {
    renderComplete();
  } else if (state.status !== "loading") {
    renderPretest();
  } else {
    progressLabel.textContent = t("pretest");
    setOverallProgress("none");
  }
  if (modalBeforeLanguageChange === "intro") {
    renderIntroModal();
  } else if (modalBeforeLanguageChange === "notice" && state.status === "notice") {
    renderResearchNotice();
  }
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = response.headers.get("content-type")?.includes("application/json") ? await response.json() : null;
  if (!response.ok) {
    const error = new Error(data?.detail || "Request failed");
    error.status = response.status;
    throw error;
  }
  return data;
}

function maybeRenderTimeout(error) {
  if (error.status === 410) {
    clearQuestionnaireLocalState();
    renderTimeoutNotice();
    return true;
  }
  return false;
}

function draftKey(name) {
  return `questionnaire_draft_${name}`;
}

function readForm(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  if (data.questionnaire_version !== "python") delete data.numpy_familiarity;
  return data;
}

async function loadQuestionnaireSettings() {
  const settings = await api("/api/questionnaire-settings");
  state.enabledVersions = new Set(
    (settings.versions || [])
      .filter((item) => item.enabled)
      .map((item) => item.version)
  );
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

function readDraftData(key) {
  try {
    return JSON.parse(localStorage.getItem(draftKey(key)) || "{}");
  } catch {
    return {};
  }
}

function updateMajorOptions(form) {
  const version = ["python", "c", "agent"].includes(form.elements.questionnaire_version?.value)
    ? form.elements.questionnaire_version.value
    : "python";
  const major = form.elements.major;
  if (!major) return;
  const previous = major.value;
  const config = majorOptionsByVersion[version];
  major.innerHTML = `<option value="">${t("select")}</option>${config.values
    .map((value, index) => `<option value="${escapeHtml(value)}">${escapeHtml(config[state.lang][index])}</option>`)
    .join("")}`;
  major.value = config.values.includes(previous) ? previous : "";
}

function pretestFieldLabel(name, version) {
  if (name === "python_familiarity") {
    return familiarityLabelsByVersion[version][state.lang];
  }
  return i18n[state.lang].fields[name];
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
      state.status = "notice";
      state.nextStage = result.next_stage;
      state.nextTask = result.next_task;
      localStorage.removeItem(draftKey("pretest"));
      renderResearchNotice();
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
  } catch (error) {
    if (maybeRenderTimeout(error)) return;
    networkStatus.textContent = t("pending");
  }
}

function renderResearchNotice() {
  stopTimer();
  state.status = "notice";
  state.nextStage = "notice";
  state.nextTask = null;
  state.expiresAt = null;
  activeModal = "notice";
  progressLabel.textContent = t("consent");
  setOverallProgress("pretest");
  timerLabel.textContent = formatClock(state.timeLimitSeconds);
  timerLabel.classList.remove("warning");
  view.innerHTML = `
    <section class="task-block">
      <h2>${t("noticeTitle")}</h2>
      <p class="status">${t("noticeIntro")}</p>
    </section>
  `;
  const sections = t("noticeSections")
    .map(
      (section) => `
        <section class="modal-section">
          <h3>${escapeHtml(section.title)}</h3>
          <p>${escapeHtml(section.body)}</p>
        </section>
      `
    )
    .join("");
  renderModal(`
    <form id="noticeForm" class="modal-form">
      <div class="modal-header">
        <h2>${t("noticeTitle")}</h2>
        ${renderModalLanguageButton()}
      </div>
      <p class="modal-lead">${t("noticeIntro")}</p>
      ${sections}
      <ol class="notice-list">
        ${t("noticeRules").map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ol>
      <label class="agreement">
        <input type="checkbox" name="agreement" value="I agree" required />
        <span>${t("noticeAgreement")}</span>
      </label>
      <div class="actions">
        <button class="ghost" type="button" id="noticeCancel">${t("noticeCancel")}</button>
        <button class="primary" type="submit">${t("noticeStart")}</button>
      </div>
      <p class="status error" id="error"></p>
    </form>
  `);

  document.getElementById("noticeCancel").onclick = resetToHome;
  document.getElementById("noticeForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const result = await api("/api/session/start", { method: "POST", body: JSON.stringify({ agreement: "I agree" }) });
      state.status = "in_progress";
      state.nextStage = result.next_stage;
      state.nextTask = result.next_task;
      closeModal();
      setTimerFromSession(result);
      await loadTask(state.nextTask);
    } catch (error) {
      document.getElementById("error").textContent = error.message;
    }
  });
}

function renderTimeoutNotice() {
  state.status = "timeout";
  state.nextStage = null;
  state.nextTask = null;
  state.expiresAt = null;
  progressLabel.textContent = t("unavailable");
  setOverallProgress("none");
  timerLabel.textContent = t("remaining")(formatClock(0));
  timerLabel.classList.add("warning");
  view.innerHTML = `
    <section class="task-block">
      <h2>${t("timeoutTitle")}</h2>
      <p class="status error">${t("timeoutText")}</p>
      <div class="actions">
        <button class="primary" id="restartBtn" type="button">${t("restart")}</button>
      </div>
    </section>
  `;
  document.getElementById("restartBtn").onclick = resetToHome;
}

function renderPretest() {
  stopTimer();
  state.status = "pretest";
  state.nextStage = "pretest";
  state.nextTask = null;
  state.expiresAt = null;
  setOverallProgress("pretest");
  progressLabel.textContent = t("pretest");
  timerLabel.textContent = formatClock(state.timeLimitSeconds);
  timerLabel.classList.remove("warning");
  const enabledVersions = enabledVersionValues();
  if (!enabledVersions.length) {
    view.innerHTML = `
      <section class="task-block">
        <h2>${t("unavailable")}</h2>
        <p class="status error">All questionnaire versions are currently closed.</p>
      </section>
    `;
    return;
  }
  const draftData = readDraftData("pretest");
  const selectedVersion = enabledVersions.includes(draftData.questionnaire_version)
    ? draftData.questionnaire_version
    : enabledVersions[0];
  const fields = pretestFieldsForVersion(selectedVersion)
    .map(([name, type]) => {
      const label = pretestFieldLabel(name, selectedVersion);
      if (type === "select") {
        const config = configForField(name, selectedVersion);
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
        <input name="consent" type="hidden" value="I agree" />
        ${fields}
      </div>
      <div class="actions">
        <button class="primary" type="submit">${t("start")}</button>
      </div>
      <p class="status error" id="error"></p>
    </form>
  `;

  const form = document.getElementById("pretestForm");
  form.elements.questionnaire_version.value = selectedVersion;
  bindDraft(form, "pretest");
  if (!enabledVersions.includes(form.elements.questionnaire_version.value)) {
    form.elements.questionnaire_version.value = selectedVersion;
  }
  form.elements.questionnaire_version?.addEventListener("change", () => {
    localStorage.setItem(draftKey("pretest"), JSON.stringify(readForm(form)));
    renderPretest();
  });
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = readForm(form);
    const pending = { kind: "pretest", path: "/api/pretest", method: "POST", body: payload };
    try {
      const result = await api(pending.path, { method: pending.method, body: JSON.stringify(payload) });
      localStorage.removeItem(draftKey("pretest"));
      state.status = "notice";
      state.nextStage = result.next_stage;
      state.nextTask = result.next_task;
      renderResearchNotice();
    } catch (error) {
      if (maybeRenderTimeout(error)) return;
      savePending(pending);
      document.getElementById("error").textContent = error.message;
    }
  });
  maybeShowIntroModal();
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
  const error = form.querySelector("#error");
  if (error) error.textContent = "";
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
      warning.textContent = t("requiredQuestionWarning");
      question.appendChild(warning);
      if (error) error.textContent = t("requiredQuestionWarning");
      question.scrollIntoView({ behavior: "smooth", block: "center" });
      group[0].focus({ preventScroll: true });
      return false;
    }
  }
  return true;
}

async function loadTask(taskId) {
  setOverallProgress("task", taskId);
  progressLabel.textContent = t("taskProgress")(taskId);
  try {
    const task = await api(`/api/task/${taskId}?lang=${state.lang}`);
    renderTask(task);
  } catch (error) {
    if (maybeRenderTimeout(error)) return;
    view.innerHTML = `<h2>${t("unavailable")}</h2><p class="status error">${escapeHtml(error.message)}</p>`;
  }
}

function renderTask(task) {
  const sectionLabels = t("taskSectionLabels");
  const codeSectionTitle = task.questionnaire_version === "agent" ? sectionLabels.agentTrace : sectionLabels.aiCode;
  const answerBackground = task.questionnaire_version === "agent" ? t("answerBackgroundTrace") : t("answerBackgroundCode");
  const taskGuide = `
    <section class="task-guide">
      <h2>${t("taskGuideTitle")}</h2>
      <ol>
        ${t("taskGuideSteps").map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ol>
    </section>
  `;
  const supervision = task.supervision_card
    ? `
      <section class="supervision">
        <h3>${t("supervisionCard")}</h3>
        <p class="status">${t("supervisionIntro")}</p>
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
          ${question.context ? `<p class="context-label">${sectionLabels.givenInput}</p><p class="context">${escapeHtml(question.context)}</p>` : ""}
          <p>${escapeHtml(question.prompt)}</p>
          <div class="options">${renderOptions(question.id, question.options)}</div>
        </div>
      `
    )
    .join("");

  view.innerHTML = `
    <form id="taskForm" class="task-layout" novalidate>
      ${taskGuide}
      <section class="scenario-card">
        <h2>${t("answerBackgroundTitle")}</h2>
        <p>${escapeHtml(answerBackground)}</p>
      </section>
      <section class="task-block">
        <h2>${escapeHtml(task.title)}</h2>
        <h3>${sectionLabels.requirements}</h3>
        <ol class="requirements">${task.requirements.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ol>
        <h3 class="section-subtitle">${codeSectionTitle}</h3>
        <pre><code>${escapeHtml(task.code)}</code></pre>
      </section>
      ${supervision}
      <section class="task-block">
        <h2>${sectionLabels.questions}</h2>
        ${questions}
      </section>
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
      if (maybeRenderTimeout(error)) return;
      savePending(pending);
      document.getElementById("error").textContent = error.message;
    }
  });
}

async function loadPosttest() {
  setOverallProgress("posttest");
  progressLabel.textContent = t("posttestProgress");
  try {
    const schema = await api(`/api/posttest?lang=${state.lang}`);
    renderPosttest(schema);
  } catch (error) {
    if (maybeRenderTimeout(error)) return;
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
    <form id="posttestForm" class="task-layout" novalidate>
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
      if (maybeRenderTimeout(error)) return;
      savePending(pending);
      document.getElementById("error").textContent = error.message;
    }
  });
}

function renderComplete() {
  stopTimer();
  state.expiresAt = null;
  setOverallProgress("complete");
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
  closeModal();
  clearQuestionnaireLocalState();
  state.status = "none";
  state.nextStage = null;
  state.nextTask = 0;
  state.expiresAt = null;
  networkStatus.textContent = "";
  renderPretest();
}

function applyCurrentSession(current) {
  state.status = current.status;
  state.nextStage = current.next_stage || null;
  state.nextTask = current.next_task || null;
  if (["in_progress", "posttest"].includes(current.status)) {
    setTimerFromSession(current);
  }
  if (current.status === "pretest") {
    renderPretest();
  } else if (current.status === "notice") {
    renderResearchNotice();
  } else if (current.status === "in_progress") {
    loadTask(current.next_task);
  } else if (current.status === "posttest") {
    loadPosttest();
  } else if (current.status === "complete") {
    renderComplete();
  } else if (current.status === "timeout") {
    clearQuestionnaireLocalState();
    renderTimeoutNotice();
  } else if (current.status === "closed") {
    stopTimer();
    clearQuestionnaireLocalState();
    setOverallProgress("none");
    progressLabel.textContent = t("unavailable");
    view.innerHTML = `
      <section class="task-block">
        <h2>${t("unavailable")}</h2>
        <p class="status error">This questionnaire version is currently closed.</p>
        <div class="actions">
          <button class="primary" id="restartBtn" type="button">${t("restart")}</button>
        </div>
      </section>
    `;
    document.getElementById("restartBtn").onclick = resetToHome;
  } else {
    renderPretest();
  }
}

async function bootstrapSession() {
  setLanguage(state.lang);
  try {
    await loadQuestionnaireSettings();
  } catch {
    state.enabledVersions = new Set(["python", "c", "agent"]);
  }
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
window.addEventListener("scroll", updateTopbarVisibility, { passive: true });
window.addEventListener("resize", updateTopbarVisibility);

bootstrapSession();
