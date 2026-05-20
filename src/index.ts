import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";

const accessToken = process.env.QQDOC_ACCESS_TOKEN;
const apiBase = process.env.QQDOC_API_BASE_URL || "https://docs.qq.com/openapi";

const client = axios.create({
  baseURL: apiBase,
  headers: {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  },
});

const tools: Tool[] = [
  {
    name: "create_document",
    description: "Create a new QQ document",
    inputSchema: {
      type: "object",
      properties: {
        title: { type: "string", description: "Document title" },
        content: { type: "string", description: "Document content" },
        type: {
          type: "string",
          enum: ["doc", "sheet", "slide"],
          description: "Document type",
        },
      },
      required: ["title", "type"],
    },
  },
  {
    name: "get_document",
    description: "Get document content",
    inputSchema: {
      type: "object",
      properties: {
        docId: { type: "string", description: "Document ID" },
      },
      required: ["docId"],
    },
  },
  {
    name: "update_document",
    description: "Update document content",
    inputSchema: {
      type: "object",
      properties: {
        docId: { type: "string", description: "Document ID" },
        content: { type: "string", description: "New content" },
      },
      required: ["docId", "content"],
    },
  },
  {
    name: "delete_document",
    description: "Delete a document",
    inputSchema: {
      type: "object",
      properties: {
        docId: { type: "string", description: "Document ID" },
      },
      required: ["docId"],
    },
  },
  {
    name: "list_documents",
    description: "List documents",
    inputSchema: {
      type: "object",
      properties: {
        limit: { type: "number", description: "Result limit", default: 10 },
        offset: { type: "number", description: "Offset", default: 0 },
      },
    },
  },
];

async function handleToolCall(
  name: string,
  args: Record<string, unknown>
): Promise<string> {
  try {
    switch (name) {
      case "create_document":
        return JSON.stringify(
          await client.post("/document/create", {
            title: args.title,
            content: args.content || "",
            type: args.type,
          })
        );
      case "get_document":
        return JSON.stringify(
          await client.get(`/document/${args.docId}`)
        );
      case "update_document":
        return JSON.stringify(
          await client.put(`/document/${args.docId}`, {
            content: args.content,
          })
        );
      case "delete_document":
        return JSON.stringify(
          await client.delete(`/document/${args.docId}`)
        );
      case "list_documents":
        return JSON.stringify(
          await client.get("/documents", {
            params: {
              limit: args.limit || 10,
              offset: args.offset || 0,
            },
          })
        );
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return JSON.stringify({ error: String(error) });
  }
}

const server = new Server(
  {
    name: "qq-doc-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => ({
  content: [
    {
      type: "text",
      text: await handleToolCall(
        request.params.name,
        request.params.arguments as Record<string, unknown>
      ),
    },
  ],
}));

const transport = new StdioServerTransport();
await server.connect(transport);
