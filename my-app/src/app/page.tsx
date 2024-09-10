"use client";
import { CopilotKit, useCoAgent } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <div>
        <Joke />
      </div>
      <CopilotSidebar defaultOpen={true} clickOutsideToClose={false} />
    </CopilotKit>
  );
}

function Joke() {
  const { state } = useCoAgent({ name: "joke_agent" });

  return <div>{state.joke}</div>;
}
