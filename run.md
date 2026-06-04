# How to Run Serene

Run these commands from a terminal.

## 1. Go to the project folder

```bash
cd /Users/Salaj/Desktop/serene
```

## 2. Create a virtual environment

If `.venv` does not already exist:

```bash
python3.11 -m venv .venv
```

If `python3.11` is not available, try:

```bash
python3 -m venv .venv
```

## 3. Install requirements

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## 4. Run the FastAPI backend

```bash
.venv/bin/python -m uvicorn main:app
```

When it starts successfully, you should see:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000
```

The chat endpoint is:

```text
http://127.0.0.1:8000/chat
```

## If port 8000 is already in use

Run the backend on another port:

```bash
.venv/bin/python -m uvicorn main:app --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

## 5. Run the Gradio chat UI

The Gradio app is the chat screen for Serene.

First, keep the FastAPI backend running in one terminal:

```bash
cd /Users/Salaj/Desktop/serene
.venv/bin/python -m uvicorn main:app
```

Then open a second terminal and run:

```bash
cd /Users/Salaj/Desktop/serene
.venv/bin/python gradio_app.py
```

Gradio will print a local URL, usually:

```text
http://127.0.0.1:7860
```

Open that URL in your browser.

## If the Gradio port is already in use

Stop the old Gradio process by pressing `CTRL+C` in the terminal where it is running.

Or run Gradio on another port:

```bash
GRADIO_SERVER_PORT=7861 .venv/bin/python gradio_app.py
```

Then open:

```text
http://127.0.0.1:7861
```

## Stop the server

Press:

```text
CTRL+C
```
