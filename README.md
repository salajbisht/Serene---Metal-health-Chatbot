# Serene

**Because Every Feeling Deserves to Be Heard**

Serene is an AI-powered mental health support chatbot designed to provide empathetic, supportive, and safe conversations for individuals experiencing emotional challenges. Built using FastAPI, Gradio, and a fine-tuned Qwen language model, Serene offers a private and accessible space where users can discuss topics such as stress, anxiety, loneliness, self-esteem, relationships, grief, and emotional wellbeing.

The system incorporates mental-health-specific fine-tuning, scope restriction, and crisis-aware response handling to ensure conversations remain supportive, focused, and responsible.

---

## ✨ Key Features

### 🧠 Fine-Tuned Mental Health Assistant

* Built on Qwen2.5-3B-Instruct
* Fine-tuned using LoRA (PEFT)
* Optimized for empathetic and supportive conversations

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
├── main.py                 # FastAPI backend server
├── gradio_app.py           # Gradio user interface
├── app.py                  # Local model testing script
├── test.py                 # Additional testing utilities
├── requirements.txt        # Project dependencies
├── run.md                  # Detailed execution guide
├── mental_health_model/    # Fine-tuned LoRA adapter files
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
| Deep Learning | PyTorch                   |
| Transformers  | Hugging Face Transformers |

---

# 📋 Requirements

* Python 3.11 or newer
* macOS, Linux, or Windows
* Sufficient RAM to load the model locally
* Internet connection for initial dependency installation

---

# 🚀 Installation

## Clone the Repository

```bash
git clone <repository-url>
cd serene
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
