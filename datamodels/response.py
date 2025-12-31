from dataclasses import dataclass

@dataclass
class Response:
    text: str | list[str]
    voice: str | None = None
    animation: str | None = None
    response_type: str | None = None

    def __post_init__(self) -> None:
        pass