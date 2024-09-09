import { NextRequest } from "next/server";
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit-alt/runtime";
import OpenAI from "openai";

const openai = new OpenAI();
const serviceAdapter = new OpenAIAdapter({ openai });

// const BASE_URL = process.env.REMOTE_ACTION_URL || "http://127.0.0.1:8000";

const runtime = new CopilotRuntime({
  remoteActions: [
    {
      url: `http://localhost:8000/copilotkit`,
    },
  ],
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
