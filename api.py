import requests
import json
from datamodels import Identification, Result, PromptResponse, Response, Citation, Metadata, LlmCall
from utilities import check_for_keys, get_if_available
from constants import Constants as Cn

class MerlApi:
    ROOT_URL: str = "https://xsva.support.xboxlive.com/"

    def __make_full_url(endpoint: str) -> str:
        return f"{MerlApi.ROOT_URL}/{endpoint}"
    
    def __make_call(method: str, endpoint: str, headers: dict, data: str) -> Result:
        url: str = MerlApi.__make_full_url(endpoint)
        response: requests.Response = requests.post(url, headers = headers, data = data)
        response.raise_for_status()

        response_dict: dict = response.json()
        result: Result = Result(response.status_code, response_dict)

        return result
    
    def __post(endpoint: str, headers: dict, data: str) -> Result:
        METHOD: str = "POST"
        return MerlApi.__make_call(METHOD, endpoint, headers, data)
    
    def __get(endpoint: str, headers: dict, data: str) -> Result:
        METHOD: str = "GET"
        return MerlApi.__make_call(METHOD, endpoint, headers, data)

    def initialize_conversation(greeting = "") -> Identification:
        ENDPOINT: str = "initialize_conversation"

        payload: str = json.dumps({
            "clientId": "MINECRAFT_HELP",
            "conversationId": None,
            "forceReset": False,
            "greeting": greeting,
            "locale": "en-US",
            "country": "US"
        })
        headers: dict[str, str] = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://help.minecraft.net/',
            'activeusertreatments': '',
            'clientrequestid': '251ea13e-7462-4870-8f0c-26d24399d33d',
            'content-type': 'application/json',
            'expose_rag_context': 'false',
            'gstoken': '',
            'traceparent': '00-120203ff265d4c9ea425459336093000-981fcaa76c26418d-00',
            'xbltoken': '',
            'Origin': 'https://help.minecraft.net',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=4',
            'TE': 'trailers'
        }

        result: Result = MerlApi.__post(ENDPOINT, headers = headers, data = payload)
        response_dict: dict[str, str] = result.data

        return MerlApi.create_identification(response_dict)
    
    def prompt(identification: Identification, question_text: str) -> PromptResponse:
        ENDPOINT: str = "chat"

        payload: str = json.dumps({
            "conversationId": identification.convo_id,
            "eTag": identification.etag,
            "text": question_text,
            "customizationSelections": {
                "personaId": identification.personal_id
            }
        })
        headers: dict[str, str] = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://help.minecraft.net/',
            'activeusertreatments': '',
            'clientrequestid': '1648bedc-78f7-4859-82e1-3a36b1b9cf60',
            'content-type': 'application/json',
            'expose_rag_context': 'false',
            'gstoken': '',
            'traceparent': '00-120203ff265d4c9ea425459336093000-1eb15355647b498b-00',
            'xbltoken': '',
            'Origin': 'https://help.minecraft.net',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=4',
            'TE': 'trailers'
        }
        
        result: Result = MerlApi.__post(endpoint = ENDPOINT, headers = headers, data = payload)
        result_dict: dict = result.data

        return MerlApi.create_prompt_response(result_dict)
    
    def create_identification(result_dict: dict) -> Identification:
        #we make sure that the correct items are in the dictionary
        REQUIRED_KEYS: list[str] = [Cn.CONVERSATION_ID_KEY, Cn.ETAG_KEY, Cn.CUSTOM_SELECTIONS_KEY]

        check_for_keys(result_dict, REQUIRED_KEYS)
        check_for_keys(result_dict[Cn.CUSTOM_SELECTIONS_KEY], Cn.PERSONAL_ID_KEY)
        
        convo_id: str = result_dict[Cn.CONVERSATION_ID_KEY]
        etag: str = result_dict[Cn.ETAG_KEY]
        personal_id: str = result_dict[Cn.CUSTOM_SELECTIONS_KEY][Cn.PERSONAL_ID_KEY]

        return Identification(convo_id, etag, personal_id)
    
    def create_prompt_response(result_dict: dict) -> PromptResponse:
        REQUIRED_KEYS: list[str] = [Cn.ETAG_KEY, Cn.TURN_ID_KEY, Cn.RESPONSE_KEY, Cn.METADATA_KEY]
        check_for_keys(result_dict, REQUIRED_KEYS)

        etag: str = result_dict[Cn.ETAG_KEY]
        turn_id: str = result_dict[Cn.TURN_ID_KEY]

        citations: list[Citation] = []
        citation_dicts: list[dict] = []
        if Cn.CITATIONS_KEY in result_dict: 
            citation_dicts = result_dict[Cn.CITATIONS_KEY]
        #if there are no citations, this for loop wont run, since the list is empty
        #but if there are, then it will
        for citation_dict in citation_dicts:
            check_for_keys(citation_dict, [Cn.CITATIONS_TITLE_KEY, Cn.CITATIONS_URL_KEY])
            title: str = citation_dict[Cn.CITATIONS_TITLE_KEY]
            url: str = citation_dict[Cn.CITATIONS_URL_KEY]
            citation_obj: Citation = Citation(title, url)
            citations.append(citation_obj)
        
        metadata_dict: dict = result_dict[Cn.METADATA_KEY]
        intent: str | None = get_if_available(metadata_dict, Cn.METADATA_INTENT_KEY)
        overall_issue: str | None = get_if_available(metadata_dict, Cn.METADATA_OVERALL_ISSUE_KEY)
        intent_llm_call_dict: dict | None = get_if_available(metadata_dict, Cn.METADATA_INTENT_LLM_KEY)
        chat_llm_call_dict: dict | None = get_if_available(metadata_dict, Cn.METADATA_CHAT_LLM_KEY)
        intent_llm_call: LlmCall | None = MerlApi.create_llm_obj(intent_llm_call_dict)
        chat_llm_call: LlmCall | None = MerlApi.create_llm_obj(chat_llm_call_dict)
        
        metadata: Metadata = Metadata(intent = intent, overall_issue = overall_issue, intent_llm_call = intent_llm_call, 
                                      chat_llm_call = chat_llm_call)
        
        
        responses: list[Response] = []
        texts: list[str | list[str]] = []
        for response_dict in result_dict[Cn.RESPONSE_KEY]:
            voice: str | None = response_dict[Cn.RESPONSE_VOICE_KEY]
            animation: str | None = response_dict[Cn.RESPONSE_ANIMATION_KEY]
            response_type: str | None = response_dict[Cn.RESPONSE_TYPE_KEY]

            text: str | list[str]
            if Cn.RESPONSE_TEXT_KEY in response_dict:
                text = response_dict[Cn.RESPONSE_TEXT_KEY]
            elif Cn.RESPONSE_LIST_KEY in response_dict:
                text = [text_dict[Cn.RESPONSE_TEXT_KEY] for text_dict in response_dict[Cn.RESPONSE_LIST_KEY]]

            response_obj: Response = Response(text = text, voice = voice, animation = animation, response_type = response_type)
            responses.append(response_obj)
            texts.append(text)

        prompt_response: PromptResponse = PromptResponse(result_dict, etag, turn_id, citations, 
                                                        metadata, responses, texts)

        return prompt_response

    def create_llm_obj(llm_dict: dict | None) -> LlmCall | None:
        if not isinstance(llm_dict, dict):
            return None
        
        call_id: str | None = get_if_available(llm_dict, Cn.LLM_CALL_ID_KEY)
        finish_reason: str | None = get_if_available(llm_dict, Cn.LLM_FINISH_REASON_KEY)
        prompt_tokens: int | None = get_if_available(llm_dict, Cn.LLM_PROMPT_TOKENS_KEY)
        completion_tokens: int | None = get_if_available(llm_dict, Cn.LLM_COMPLETION_TOKENS_KEY)
        total_tokens: int | None = get_if_available(llm_dict, Cn.LLM_TOTAL_TOKENS_KEY)
        max_tokens: int | None = get_if_available(llm_dict, Cn.LLM_MAX_TOKENS_KEY)
        status_code: int | None = get_if_available(llm_dict, Cn.LLM_STATUS_CODE_KEY)

        llm_call: LlmCall = LlmCall(call_id = call_id, finish_reason = finish_reason, prompt_tokens = prompt_tokens, completion_tokens = completion_tokens,
                                    total_tokens = total_tokens, max_tokens = max_tokens, status_code = status_code)
        
        return llm_call 
