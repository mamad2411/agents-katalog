import type { AgentOutput } from "@/types/hrms";
import type { AgentPersona } from "@/server/agents/prompts";

export const aiReasonTool = {
  name: "ai-reason",
  description:
    "Generate smart HR responses using Ollama (local) with OpenAI fallback",
  execute: async (
    input: string,
    context: string,
    persona?: AgentPersona,
  ): Promise<AgentOutput> => {
    try {
      const res = await fetch("/api/ai/reason", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input, context, persona }),
      });
      if (!res.ok) throw new Error("AI reason endpoint failed");

      const data = await res.json();
      return {
        type: "AI_REASON",
        message: data.answer ?? "No answer",
        source: data.provider ?? "llm",
      };
    } catch (error) {
      console.error("aiReasonTool error", error);
      return {
        type: "AI_REASON",
        message: "AI reasoning unavailable",
        source: "llm",
      };
    }
  },
};