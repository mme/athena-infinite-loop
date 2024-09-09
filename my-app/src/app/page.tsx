import { CopilotKit } from "@copilotkit-alt/react-core";
import { CopilotSidebar } from "@copilotkit-alt/react-ui";
import "@copilotkit-alt/react-ui/styles.css";

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
