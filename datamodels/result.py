from dataclasses import dataclass

@dataclass
class Result:
    status_code: int
    data: any