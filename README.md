# Serene

Serene is a mental health support chatbot built with FastAPI, Gradio, and a local fine-tuned language model.

The assistant is designed to provide compassionate emotional support for topics like stress, anxiety, loneliness, relationships, self-esteem, grief, and crisis prevention. It also includes a scope guard so unrelated requests, such as coding or general knowledge questions, are refused.

## Features

- FastAPI backend for chat responses
- Gradio chat interface
- Local Qwen-based model with a LoRA adapter
- Mental-health-only scope restriction
- Crisis-aware response guidance
- Simple setup with `requirements.txt`

## Project Structure

```text
serene/
├── main.py                 # FastAPI backend
├── gradio_app.py           # Gradio chat UI
├── app.py                  # Local model test script
├── test.py                 # Extra test script
├── requirements.txt        # Python dependencies
├── run.md                  # Step-by-step run instructions
├── mental_health_model/    # LoRA adapter and tokenizer files
└── README.md
```

## Requirements

- Python 3.11 recommended
- macOS/Linux terminal
- Enough memory to load the local model

## Setup

Go to the project folder:

```bash
cd /Users/Salaj/Desktop/serene
```

Create a virtual environment:

```bash
python3.11 -m venv .venv
```

If `python3.11` is not available:

```bash
python3 -m venv .venv
```

Install dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## Run the FastAPI Backend

```bash
.venv/bin/python -m uvicorn main:app
```

Open:

```text
http://127.0.0.1:8000
```

The chat endpoint is:

```text
http://127.0.0.1:8000/chat
```

## Run the Gradio Chat UI

Keep the FastAPI backend running. Then open a second terminal:

```bash
cd /Users/Salaj/Desktop/serene
.venv/bin/python gradio_app.py
```

Open the Gradio URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

## If a Port Is Already in Use

Run FastAPI on another port:

```bash
.venv/bin/python -m uvicorn main:app --port 8001
```

Run Gradio on another port:

```bash
GRADIO_SERVER_PORT=7861 .venv/bin/python gradio_app.py
```

## Important Note

Serene is not a replacement for a licensed mental health professional. For urgent safety concerns or crisis situations, users should contact emergency services, a trusted person, or a crisis helpline immediately.
