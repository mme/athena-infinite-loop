"use client";
import {
  CopilotKit,
  useCoAgent,
  useCoAgentAction,
  useCopilotAction,
} from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import Head from "next/head";
import { useState } from "react";

export default function Home() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <Head>
        <title>CopilotKit Sandbox - Athena | AJ</title>
      </Head>
      <div>
        <Joke />
      </div>
      <div>
        <Email />
      </div>
      <div>
        <TestNavigation />
      </div>
      <div>
        <Research />
      </div>
      <CopilotSidebar defaultOpen={true} clickOutsideToClose={false} />
    </CopilotKit>
  );
}

function Joke() {
  const { state } = useCoAgent({ name: "joke_agent" });

  useCoAgentAction({
    name: "joke_agent",
    nodeName: "joke_node",
    render: ({ state, nodeName }) => {
      return <div>Generating joke: {state.joke}</div>;
    },
  });

  return <div>Joke:{state.joke}</div>;
}

function Email() {
  const { state } = useCoAgent({ name: "email_agent" });

  useCoAgentAction({
    name: "email_agent",
    nodeName: "email_node",
    render: ({ state, nodeName }) => {
      return <div>Generating email: {state.email}</div>;
    },
  });

  return <div>Email:{state.email}</div>;
}

function Research() {
  const { state } = useCoAgent({ name: "search_agent" });
  console.log("ai_researcher_state: ",  state)

  return <div>
    <h1 style={{marginTop: "20px"}}>Research</h1>
    <div>
      <h2>Steps</h2>
      {state?.steps?.map((step: any, index: any) => (
        <div key={index}>
          <span>{step.description}</span>
          <span style={{color: step.status === "complete" ? "green" : "red"}}>Status: {step.status}</span>
        </div>
      ))}
    </div>
  </div>;
}

function TestNavigation() {
  const [path, setPath] = useState<string>("");
  useCopilotAction({
    name: "navigate",
    description: "Navigate to a path",
    parameters: [{ name: "path", type: "string" }],
    handler: async ({ path }) => {
      setPath(path);
    },
  });
  if (path === "") {
    return <div>Test Navigation (no path)</div>;
  } else {
    return <Path path={path} />;
  }
}

function Path({ path }: { path: string }) {
  useCopilotAction({
    name: "alertPath",
    description: "Show the current path to the user by alerting it.",
    handler: () => {
      alert(path);
    },
  });

  return <div>Path: {path}</div>;
}
