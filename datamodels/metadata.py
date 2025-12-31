from dataclasses import dataclass
from datamodels.llm_call import LlmCall

@dataclass 
class Metadata:
    intent: str | None = None
    overall_issue: str | None = None
    intent_llm_call: LlmCall | None = None
    chat_llm_call: LlmCall | None = None