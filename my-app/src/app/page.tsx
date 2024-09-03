import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <div>
        <h1>Hello World</h1>
      </div>
      <CopilotSidebar />
    </CopilotKit>
  );
}
