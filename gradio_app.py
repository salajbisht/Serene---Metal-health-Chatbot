import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/chat"

CSS = """
:root {
    color-scheme: light;
    --body-background-fill: #f5fbf9;
    --body-text-color: #173532;
    --block-background-fill: #ffffff;
    --block-border-color: #d8e8e4;
    --input-background-fill: #ffffff;
    --button-primary-background-fill: #145c58;
    --button-primary-background-fill-hover: #0f4946;
}

body {
    background: #f5fbf9 !important;
    color: #173532 !important;
}

.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
    padding: 32px 18px !important;
    background: #f5fbf9 !important;
}

#serene-header {
    text-align: center;
    margin-bottom: 22px;
}

#serene-title {
    color: #145c58;
    font-size: 100px;
    font-weight: 800;
    line-height: 1;
    margin: 0;
    letter-spacing: 0;
}

#serene-tagline {
    color: #5f7673;
    font-size: 18px;
    font-style: italic;
    margin-top: 10px;
}

.chatbot {
    background: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid #d8e8e4 !important;
    box-shadow: 0 12px 36px rgba(20, 92, 88, 0.08) !important;
}

.chatbot .label-wrap,
.chatbot .message-buttons,
.chatbot button[title="Copy"],
.chatbot button[title="Share"],
.chatbot button[title="Delete"] {
    display: none !important;
}

.chatbot .message {
    border: 0 !important;
    box-shadow: none !important;
}

.chatbot .user .message {
    background: #145c58 !important;
    color: #ffffff !important;
    border-radius: 18px 18px 4px 18px !important;
}

.chatbot .bot .message {
    background: #edf7f4 !important;
    color: #173532 !important;
    border-radius: 18px 18px 18px 4px !important;
}

#message-row {
    margin-top: 14px;
}

#message-row textarea {
    background: #ffffff !important;
    color: #173532 !important;
    border: 1px solid #d8e8e4 !important;
}

#message-row button {
    background: #145c58 !important;
    border: 0 !important;
    color: #ffffff !important;
}

#footer {
    text-align: center;
    color: #6b7f7c;
    padding: 18px;
    font-size: 13px;
}

footer {
    display: none !important;
}
"""


def chat(message, history):

    history = history or []

    try:
        response = requests.post(
            API_URL,
            json={"message": message},
            timeout=120
        )

        bot_reply = response.json()["response"]

    except Exception as e:
        bot_reply = str(e)

    history.append(
        {"role":"user","content":message}
    )

    history.append(
        {"role":"assistant","content":bot_reply}
    )

    return "", history


theme = gr.themes.Soft(primary_hue="teal", neutral_hue="slate")


with gr.Blocks(fill_height=True) as demo:

    gr.HTML("""
        <div id="serene-header">
            <h1 id="serene-title">SERENE</h1>
            <div id="serene-tagline">every feelings deserved to be heard</div>
        </div>
    """)

    chatbot = gr.Chatbot(
        height=620,
        elem_classes=["chatbot"],
        show_label=False,
        buttons=[],
        feedback_options=None,
        layout="bubble"
    )

    with gr.Row(elem_id="message-row"):

        msg = gr.Textbox(
            placeholder="Share what's on your mind...",
                scale=9,
                container=False,
                lines=1
        )

        send = gr.Button(
            "Send",
            variant="primary",
            scale=1
        )

    send.click(
        chat,
        [msg, chatbot],
        [msg, chatbot]
    )

    msg.submit(
        chat,
        [msg, chatbot],
        [msg, chatbot]
    )

    gr.HTML(
        """
        <div id="footer">
            © 2026 Serene. Made by Salaj Bisht. All Rights Reserved.
        </div>
        """
    )

demo.launch(css=CSS, theme=theme)
