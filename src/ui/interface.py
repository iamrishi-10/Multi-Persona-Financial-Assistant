import gradio as gr
from src.personas import PERSONAS
from src.llm.streamer import stream_persona_response
from src.storage.conversation_logger import log_exchange, read_log, clear_log


def _make_chat_fn(persona_key: str):
    system_prompt = PERSONAS[persona_key]

    def chat_fn(message: str, history: list):
        full_response = ""
        for partial in stream_persona_response(system_prompt, message, history):
            full_response = partial
            yield partial

        log_exchange(
            persona=persona_key,
            user_message=message,
            ai_response=full_response,
        )

    return chat_fn


def _build_log_table() -> list:
    log = read_log()
    if not log:
        return []
    return [
        [
            entry["timestamp"][:19].replace("T", " "),
            entry["persona"].capitalize(),
            entry["user_message"],
            entry["ai_response"],
        ]
        for entry in reversed(log)
    ]


def _build_summary() -> str:
    log = read_log()
    if not log:
        return "_No conversations logged yet. Start chatting in any tab._"
    counts: dict = {}
    for entry in log:
        counts[entry["persona"]] = counts.get(entry["persona"], 0) + 1
    lines = [f"**Total conversations: {len(log)}**"]
    for persona, count in counts.items():
        lines.append(f"- {persona.capitalize()}: {count}")
    return "\n".join(lines)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Multi-Persona Financial Assistant") as app:

        with gr.Row():
            gr.Markdown(
                "# Multi-Persona Financial Assistant\n"
                "**Same question. Three expert perspectives. Pick the tab that matches your situation.**"
            )
            dark_toggle = gr.Button("Toggle Dark Mode", size="sm", scale=0)

        dark_toggle.click(
            fn=None,
            js="() => { document.documentElement.classList.toggle('dark') }",
        )

        with gr.Tabs():

            with gr.Tab("🌱 Beginner Investor"):
                gr.Markdown(
                    "**Who this is for:** Ages 22-28, first-time investors, earning Rs 25,000-50,000/month. "
                    "Simple language, small amounts, one action at a time."
                )
                gr.ChatInterface(
                    fn=_make_chat_fn("beginner"),
                    examples=[
                        "How do I start investing with Rs 1,000/month?",
                        "What is a mutual fund and is it safe?",
                        "Is FD better than SIP?",
                        "How much should I save before I start investing?",
                    ],
                    cache_examples=False,
                )

            with gr.Tab("📈 Experienced Trader"):
                gr.Markdown(
                    "**Who this is for:** Rs 10L+ invested, reads financial news daily, understands valuations. "
                    "Technical analysis, macro context, opinionated views."
                )
                gr.ChatInterface(
                    fn=_make_chat_fn("trader"),
                    examples=[
                        "What is your view on IT sector valuations right now?",
                        "How should I think about portfolio rebalancing?",
                        "Explain the current FII vs DII flow dynamic",
                        "Is mid-cap the right place to be given current Nifty levels?",
                    ],
                    cache_examples=False,
                )

            with gr.Tab("🛡️ Insurance Advisor"):
                gr.Markdown(
                    "**Who this is for:** Anyone with dependents or liabilities wanting protection-first advice. "
                    "Risk coverage, not returns. Honest about what to avoid."
                )
                gr.ChatInterface(
                    fn=_make_chat_fn("insurance"),
                    examples=[
                        "Do I need term insurance if I have no dependents?",
                        "What is the difference between ULIP and a mutual fund?",
                        "How much health insurance cover do I actually need?",
                        "My agent is recommending an endowment plan — should I buy it?",
                    ],
                    cache_examples=False,
                )

            with gr.Tab("📊 Conversation Logs"):
                gr.Markdown("### All saved conversations")

                with gr.Row():
                    log_refresh_btn = gr.Button("Refresh", variant="primary")
                    log_clear_btn   = gr.Button("Clear All Logs", variant="stop")

                log_summary = gr.Markdown(value=_build_summary())
                log_table   = gr.Dataframe(
                    value=_build_log_table(),
                    headers=["Timestamp", "Persona", "User Message", "AI Response"],
                    datatype=["str", "str", "str", "str"],
                    wrap=True,
                    interactive=False,
                )

                def refresh_logs():
                    return _build_summary(), _build_log_table()

                def clear_logs():
                    clear_log()
                    return _build_summary(), _build_log_table()

                log_refresh_btn.click(fn=refresh_logs, outputs=[log_summary, log_table])
                log_clear_btn.click(fn=clear_logs, outputs=[log_summary, log_table])

    return app
