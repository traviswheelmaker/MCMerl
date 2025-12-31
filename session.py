from api import MerlApi
from datamodels import Identification, PromptResponse
from datamodels.identification import Identification
from datamodels.prompt_response import PromptResponse

class Session:
    def __init__(self) -> None:
        self.__id: Identification = self.__start_session()
        self.__session_history: list[dict] = []

    def __start_session(self) -> Identification:
        return MerlApi.initialize_conversation()

    def get_id(self) -> Identification:
        return self.__id

    def get_convo_id(self) -> str:
        return self.__id.convo_id
    
    def get_etag(self) -> str:
        return self.__id.etag
    
    def get_personal_id(self) -> str:
        return self.__id.personal_id
    
    def get_session_history(self) -> list[PromptResponse]:
        return self.__session_history

    def prompt(self, text: str) -> PromptResponse:
        merls_response: PromptResponse = MerlApi.prompt(identification = self.__id, question_text = text)

        """
        every time a response is given, a new etag is returned.
        this new etag must be used in the following response, or it will 412
        we will therefore need to update the etag after prompting merl
        """
        new_etag: str = merls_response.etag
        self.__id.update_etag(new_etag)

        self.__session_history.append(merls_response)

        return merls_response
    
    def restart_session(self) -> None:
        self.__id = self.__start_session()
        self.__session_history = []