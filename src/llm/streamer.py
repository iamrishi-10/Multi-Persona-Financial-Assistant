from typing import Generator
import config
from src.llm.client import get_client
from src.personas.base import build_messages


def stream_persona_response(
    system_prompt: str,
    message: str,
    history: list,
) -> Generator[str, None, None]:
    """
    Stream a persona response to Gradio word-by-word.

    Yields cumulative partial strings so Gradio re-renders on every chunk.
    The final yielded value is the complete response text.
    """
    client = get_client()
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


def calculate_cost(input_tokens: int, output_tokens: int) -> dict:
    """
    Return token counts and estimated cost in both USD and INR.

    Used by the conversation logger to record cost per exchange.
    """
    input_cost_usd = (input_tokens / 1000) * config.INPUT_COST_PER_1K
    output_cost_usd = (output_tokens / 1000) * config.OUTPUT_COST_PER_1K
    total_usd = input_cost_usd + output_cost_usd

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost_usd": round(total_usd, 6),
        "cost_inr": round(total_usd * config.USD_TO_INR, 4),
    }


def format_cost_label(input_tokens: int, output_tokens: int) -> str:
    """Return a short display string for the Gradio UI status line."""
    cost = calculate_cost(input_tokens, output_tokens)
    return (
        f"Tokens: {cost['total_tokens']:,} "
        f"(in: {cost['input_tokens']:,} / out: {cost['output_tokens']:,}) "
        f"| Cost: ₹{cost['cost_inr']:.4f}"
    )
