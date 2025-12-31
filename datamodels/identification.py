from dataclasses import dataclass

@dataclass
class Identification:
    convo_id: str
    etag: str
    personal_id: str

    def update_etag(self, new_etag: str) -> None:
        self.etag = new_etag