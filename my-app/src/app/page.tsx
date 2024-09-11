"use client";
import {
  CopilotKit,
  useCoAgent,
  useCoAgentAction,
} from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <div>
        <Joke />
      </div>
      <div>
        <Email />
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
