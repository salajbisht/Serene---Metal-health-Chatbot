# Serene

**Because Every Feeling Deserves to Be Heard**

Serene is an AI-powered mental health support chatbot designed to provide empathetic, supportive, and safe conversations for individuals experiencing emotional challenges. Built using FastAPI, Gradio, and a fine-tuned Qwen language model, Serene offers a private and accessible space where users can discuss topics such as stress, anxiety, loneliness, self-esteem, relationships, grief, and emotional wellbeing.

The system incorporates mental-health-specific fine-tuning, **RAG** over bundled guide PDFs, scope restriction, and crisis-aware response handling to ensure conversations remain supportive, focused, and responsible.

---

## ✨ Key Features

### 🧠 Fine-Tuned Mental Health Assistant

* Built on Qwen2.5-3B-Instruct
* Fine-tuned using LoRA (PEFT)
* Optimized for empathetic and supportive conversations

### 📚 RAG (Retrieval-Augmented Generation)

* Indexes ~41 mental health guide PDFs locally
* Retrieves top relevant excerpts per user message
* Injects grounded context into the system prompt before generation
* Uses ChromaDB + sentence-transformers (no external API for retrieval)

### 💬 Interactive Chat Interface

* User-friendly Gradio web interface
* Real-time conversational experience
* Local deployment for enhanced privacy

### ⚡ FastAPI Backend

* REST API endpoint for chat interactions
* Lightweight and scalable architecture
* Easy integration with external applications

### 🛡️ Scope Restriction System

Serene is designed exclusively for mental health and emotional wellbeing discussions.

The assistant supports topics such as:

* Stress and burnout
* Anxiety and worry
* Loneliness and isolation
* Self-esteem and confidence
* Relationship challenges
* Grief and loss
* Emotional wellbeing

Requests outside the intended scope (e.g., programming help, mathematics, general knowledge, or unrelated tasks) are politely declined.

### 🚨 Crisis-Aware Guidance

The chatbot is designed to recognize potentially high-risk situations and encourage users to seek immediate support from trusted individuals, emergency services, or professional crisis resources when appropriate.

---

## How RAG Works

1. **Ingest** — `build_index.py` loads PDFs from the guides folder, splits text into chunks, and embeds them with `sentence-transformers/all-MiniLM-L6-v2`.
2. **Store** — Embeddings are saved in a local **Chroma** database at `data/chroma_db/` (gitignored).
3. **Retrieve** — On each in-scope `/chat` request, the top **4** chunks most similar to the user message are fetched.
4. **Generate** — Those excerpts are appended to the system prompt; the fine-tuned Qwen model responds with empathy while prioritizing crisis and safety rules.

The API still runs without an index; it logs a reminder and skips retrieval until you run `build_index.py`.

---

# 🏗️ Project Architecture

```text
User
 │
 ▼
Gradio Frontend
 │
 ▼
FastAPI Backend
 │
 ├──► ChromaDB (RAG retrieval)
 │
 ▼
Qwen2.5-3B-Instruct
 + LoRA Adapter
 │
 ▼
Mental Health Response
```

---

# 📂 Project Structure

```text
serene/
├── main.py                          # FastAPI backend, model + RAG integration
├── gradio_app.py                    # Gradio user interface
├── build_index.py                   # Build / rebuild the vector index
├── rag/
│   ├── config.py                    # Paths, chunk size, embedding model
│   ├── ingest.py                    # PDF load, chunk, embed, persist
│   └── retriever.py                 # Load index and retrieve context
├── Mental Health Chatbot guides/    # Source PDFs for RAG
├── data/chroma_db/                  # Generated index (gitignored)
├── mental_health_model/             # Fine-tuned LoRA adapter files
├── app.py                           # Local model testing script
├── test.py                          # Additional testing utilities
├── requirements.txt                 # Project dependencies
├── run.md                           # Detailed execution guide
└── README.md
```

---

# 🛠️ Technology Stack

| Component     | Technology                |
| ------------- | ------------------------- |
| Base Model    | Qwen2.5-3B-Instruct       |
| Fine-Tuning   | LoRA (PEFT)               |
| Backend       | FastAPI                   |
| Frontend      | Gradio                    |
| RAG           | ChromaDB, LangChain, sentence-transformers, pypdf |
| Deep Learning | PyTorch                   |
| Transformers  | Hugging Face Transformers |

---

# 📋 Requirements

* Python 3.11 or newer
* macOS, Linux, or Windows
* Sufficient RAM to load the model locally
* Internet connection for initial dependency and model download

---

# 🚀 Installation

## Clone the Repository

```bash
git clone https://github.com/salajbisht/Serene---Metal-health-Chatbot.git
cd Serene---Metal-health-Chatbot
```

## Create a Virtual Environment

```bash
python3.11 -m venv .venv
```

If Python 3.11 is unavailable:

```bash
python3 -m venv .venv
```

## Activate the Environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Build the RAG Index

Required for grounded answers. First run downloads the embedding model (~90 MB) from Hugging Face.

```bash
python build_index.py
```

Re-run whenever you add or replace PDFs in the guides folder.

If the build fails with a Chroma database error:

```bash
rm -rf data/chroma_db
python build_index.py
```

---

# ⚡ Running the Application

## Start the FastAPI Backend

```bash
uvicorn main:app
```

Default URL:

```text
http://127.0.0.1:8000
```

Chat API Endpoint:

```text
http://127.0.0.1:8000/chat
```

On startup, confirm the log shows **`RAG index loaded successfully.`** if you built the index.

---

## Launch the Gradio Interface

Open a new terminal:

```bash
python gradio_app.py
```

Default URL:

```text
http://127.0.0.1:7860
```

---

# 🔧 Custom Ports

### FastAPI

```bash
uvicorn main:app --port 8001
```

### Gradio

```bash
GRADIO_SERVER_PORT=7861 python gradio_app.py
```

---

# 🔍 Troubleshooting

| Problem | What to do |
|--------|------------|
| `RAG index not found` on API start | Run `python build_index.py` |
| Chroma error during index build | `rm -rf data/chroma_db` then run `build_index.py` again |
| Guides folder not found | Ensure PDFs are in a folder whose name contains `mental health chatbot guides` |
| Slow replies | Normal for a local 3B model; see `run.md` for details |

For step-by-step commands, see **[run.md](run.md)**.

---

# 🎯 Intended Use

Serene is intended for:

* Emotional support conversations
* Mental wellness applications
* Educational and research projects
* Demonstrations of domain-specific LLM fine-tuning
* AI-assisted wellbeing tools

---

# ⚠️ Limitations

Serene is **not**:

* A licensed therapist
* A medical professional
* A diagnostic tool
* A crisis intervention service
* A replacement for professional mental health care

The chatbot may generate inaccurate or incomplete responses and should be used as a supportive tool rather than a source of professional advice.

---

# 🆘 Safety Notice

If you or someone else may be in immediate danger, experiencing thoughts of self-harm, or facing a mental health emergency:

* Contact local emergency services immediately.
* Reach out to a trusted friend, family member, or guardian.
* Contact a qualified mental health professional or crisis helpline.

Professional support should always take priority during emergencies.

---

# 📜 License

This project is intended for educational, research, and demonstration purposes. Please ensure compliance with the licensing terms of all third-party dependencies and the base model used in this project.

---

# 👨‍💻 Author

**Salaj Bisht**

Final Year B.Tech Computer Science Student

*Building AI systems that are empathetic, safe, and accessible.*
