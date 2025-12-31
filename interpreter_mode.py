from session import Session
from datamodels import PromptResponse, Citation

def format_response_text(prompt_response: PromptResponse) -> str:
        texts: list[str | list[str]] = prompt_response.texts
        citations: list[Citation] = prompt_response.citations

        text_segments: list[str] = []
        for text_portion in texts:
            if isinstance(text_portion, str):
                text_segments.append(text_portion)
                continue
            elif not isinstance(text_portion, list):
                incorrect_type: any = type(text_portion)
                raise TypeError(f"'texts' can only include 'str' or 'list[str]'")
        
            text_segment: str = "\n".join([
                f"• {bullet_point}" for bullet_point in text_portion
            ])
            text_segments.append(text_segment)
        
        for citation in citations:
            citation_segment: str = f"{citation.title}: {citation.url}"
            text_segments.append(citation_segment)
        
        return "\n\n".join(text_segments)

def create_session() -> None:
    opening_text: str = "\n".join([
        "MerlApi",
        "Chatbot created by Microsoft",
        "Wrapper created by Travis Wheeler",
        "Feel free to ask any question. To stop, enter 'STOP'"
    ])
    print(opening_text)

    session: Session = Session()
    while True:
        question: str = input("\nUser Input: ")

        if question.upper() in {"STOP", "EXIT", "QUIT"}:
            print("Exiting...")
            break
        else:
            print("Generating...\n")

        try:
            prompt_response: PromptResponse = session.prompt(question)
            text_to_print: str = format_response_text(prompt_response)
            print(text_to_print)
        except:
            print("Request failed. Please try again...")
            session.restart_session()

if __name__ == "__main__":
    create_session()