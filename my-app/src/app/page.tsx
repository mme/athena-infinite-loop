"use client";
import {
  CopilotKit,
  useCoAgent,
  useCoAgentAction,
  useCopilotAction,
} from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { useState } from "react";

export default function Home() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <div>
        <Joke />
      </div>
      <div>
        <Email />
      </div>
      <div>
        <TestNavigation />
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
