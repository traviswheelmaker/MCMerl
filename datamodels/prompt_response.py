from dataclasses import dataclass
from datamodels.response import Response
from datamodels.citation import Citation
from datamodels.metadata import Metadata

@dataclass
class PromptResponse:
    result_data: dict
    #conversation_id: str
    etag: str
    turn_id: str
    citations: list[Citation]
    metadata: Metadata
    responses: list[Response]
    texts: list[str | list[str]]
        


