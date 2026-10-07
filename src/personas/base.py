from typing import Generator


def build_messages(system_prompt: str, history: list, user_message: str) -> list:
    """
    Build the OpenAI messages array.
    Gradio history is a list of [user_msg, assistant_msg] pairs.
    """
    messages = [{"role": "system", "content": system_prompt}]

    for human_msg, ai_msg in history:
        messages.append({"role": "user", "content": human_msg})
        messages.append({"role": "assistant", "content": ai_msg})

    messages.append({"role": "user", "content": user_message})
    return messages


def stream_response(system_prompt: str, message: str, history: list, client, config) -> Generator:
    """
    Yield partial response strings for Gradio's ChatInterface.
    Each yield re-renders the UI live (word-by-word streaming).
    """
    messages = build_messages(system_prompt, history, message)

    stream = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=messages,
        temperature=config.TEMPERATURE,
        stream=True,
    )

    partial = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            partial += delta
            yield partial

