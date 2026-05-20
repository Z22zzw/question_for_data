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
const assets = JSON.parse(fs.readFileSync("tmp/tencent-questionnaire-assets.json", "utf8"));

let id = 100;
async function mcpCall(method, params = {}) {
  const res = await fetch("https://docs.qq.com/openapi/mcp", {
    method: "POST",
    headers: {
      Authorization: token,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ jsonrpc: "2.0", id: id++, method, params }),
  });
  const data = await res.json();
  if (!res.ok || data.error) {
    throw new Error(JSON.stringify(data.error ?? data));
  }
  return data.result;
}

async function tool(name, args) {
  const result = await mcpCall("tools/call", { name, arguments: args });
  if (result.content?.[0]?.text) {
    return JSON.parse(result.content[0].text);
  }
  return result;
}

const answerRows = [
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

const sheetInfo = await tool("sheet.get_sheet_info", { file_id: assets.sheet.file_id });
const sheetId = sheetInfo.sheets?.[0]?.sheet_id;
if (!sheetId) {
  throw new Error(`No sheet_id found: ${JSON.stringify(sheetInfo)}`);
}

const values = answerRows.flatMap((row, r) =>
  row.map((cell, c) => ({
    row: r,
    col: c,
    value_type: "STRING",
    string_value: cell,
  }))
);
const sheetWrite = await tool("sheet.set_range_value", {
  file_id: assets.sheet.file_id,
  sheet_id: sheetId,
  values,
});

const content = await tool("get_content", { file_id: assets.doc.file_id });
const docInfo = await tool("manage.query_file_info", { file_id: assets.doc.file_id });
const formInfo = await tool("manage.query_file_info", { file_id: assets.form.file_id });
const sheetFileInfo = await tool("manage.query_file_info", { file_id: assets.sheet.file_id });

console.log(
  JSON.stringify(
    {
      doc_title: docInfo.title,
      doc_type: docInfo.type,
      doc_content_chars: content.content?.length ?? 0,
      doc_contains_q30: Boolean(content.content?.includes("Q30")),
      form_title: formInfo.title,
      form_type: formInfo.type,
      sheet_title: sheetFileInfo.title,
      sheet_type: sheetFileInfo.type,
      sheet_id: sheetId,
      answer_key_rows_written: answerRows.length,
      sheet_write_error: sheetWrite.error ?? "",
    },
    null,
    2
  )
);
