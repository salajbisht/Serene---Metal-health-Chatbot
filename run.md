# How to Run Serene

Run these commands from a terminal. Replace the project path with your own clone location if different.

## 1. Go to the project folder

```bash
cd /Users/Salaj/Desktop/serene
```

## 2. Create a virtual environment

If `.venv` does not already exist:

```bash
python3.11 -m venv .venv
```

If `python3.11` is not available:

```bash
python3 -m venv .venv
```

## 3. Install requirements

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## 4. Build the RAG index (first time)

Index the mental health guide PDFs so chat responses can use retrieved excerpts:

```bash
.venv/bin/python build_index.py
```

What this does:

- Finds the guides folder (name contains `mental health chatbot guides`; may have a leading space)
- Loads all `*.pdf` files (~41 guides)
- Splits text into chunks and embeds with `all-MiniLM-L6-v2`
- Saves the vector store to `data/chroma_db/`

Re-run this command whenever you add or replace PDFs.

If the build fails with a Chroma database error:

```bash
rm -rf data/chroma_db
.venv/bin/python build_index.py
```

## 5. Run the FastAPI backend

```bash
.venv/bin/python -m uvicorn main:app
```

When it starts successfully:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8000
```

Check the logs:

- **`RAG index loaded successfully.`** — RAG is active for `/chat`
- **`RAG index not found. Run python build_index.py`** — complete step 4 first

Open:

```text
http://127.0.0.1:8000
```

Chat endpoint:

```text
http://127.0.0.1:8000/chat
```

The first API start may take several minutes while Qwen2.5-3B and the LoRA adapter load.

## 6. Run the Gradio chat UI

Keep the FastAPI backend running in one terminal.

In a second terminal:

```bash
cd /Users/Salaj/Desktop/serene
.venv/bin/python gradio_app.py
```

Open the URL printed in the terminal, usually:

```text
http://127.0.0.1:7860
```

## If port 8000 is already in use

```bash
.venv/bin/python -m uvicorn main:app --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

Update `API_URL` in `gradio_app.py` if you use a non-default port.

## If the Gradio port is already in use

Stop the old Gradio process with `CTRL+C`, or:

```bash
GRADIO_SERVER_PORT=7861 .venv/bin/python gradio_app.py
```

Then open:

```text
http://127.0.0.1:7861
```

## Stop the servers

Press `CTRL+C` in each terminal running uvicorn or Gradio.

## Quick reference

| Step | Command |
|------|---------|
| Install deps | `.venv/bin/python -m pip install -r requirements.txt` |
| Build RAG index | `.venv/bin/python build_index.py` |
| Start API | `.venv/bin/python -m uvicorn main:app` |
| Start UI | `.venv/bin/python gradio_app.py` |
| Reset index | `rm -rf data/chroma_db && .venv/bin/python build_index.py` |
