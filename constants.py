from dataclasses import dataclass

@dataclass(init = False, frozen = True)
class Constants:
    CONVERSATION_ID_KEY: str = "conversationId"
    ETAG_KEY: str = "eTag"
    CUSTOM_SELECTIONS_KEY: str = "customizationSelections"
    PERSONAL_ID_KEY: str = "personaId"
    TURN_ID_KEY: str = "turnId"

    CITATIONS_KEY: str = "citations"
    CITATIONS_TITLE_KEY: str = "title"
    CITATIONS_URL_KEY: str = "url"

    RESPONSE_KEY: str = "response"
    RESPONSE_VOICE_KEY: str = "voice"
    RESPONSE_ANIMATION_KEY: str = "animation"
    RESPONSE_TYPE_KEY: str = "type"
    RESPONSE_TEXT_KEY: str = "text"
    RESPONSE_LIST_KEY: str = "list"

    METADATA_KEY: str = "metadata"
    METADATA_INTENT_KEY: str = "intent"
    METADATA_OVERALL_ISSUE_KEY: str = "overallIssue"
    METADATA_CHAT_LLM_KEY: str = "chatLlmCall"
    METADATA_INTENT_LLM_KEY: str = "intentLlmCall"

    LLM_CALL_ID_KEY: str = "callId"
    LLM_FINISH_REASON_KEY: str = "finishReason"
    LLM_PROMPT_TOKENS_KEY: str = "promptTokens"
    LLM_COMPLETION_TOKENS_KEY: str = "completionTokens"
    LLM_TOTAL_TOKENS_KEY: str = "totalTokens"
    LLM_MAX_TOKENS_KEY: str = "maxTokens"
    LLM_STATUS_CODE_KEY: str = "statusCode"