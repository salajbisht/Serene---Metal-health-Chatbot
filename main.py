from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel
import torch

from rag.retriever import format_rag_system_addendum, get_retriever, index_exists, retrieve_context

# =====================================
# FastAPI App
# =====================================

app = FastAPI(title="Serene Mental Health API")

# =====================================
# Load Model Once
# =====================================

BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

print("Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    dtype=torch.float16
)

print("Loading LoRA adapter...")
model = PeftModel.from_pretrained(
    base_model,
    "./mental_health_model"
)

device = "mps" if torch.backends.mps.is_available() else "cpu"

model = model.to(device)
model.eval()

print(f"Model loaded successfully on {device}")

# =====================================
# RAG Retriever
# =====================================

if index_exists():
    _, rag_enabled = get_retriever()
    if rag_enabled:
        print("RAG index loaded successfully.")
    else:
        print("RAG index found but could not be loaded. Continuing without RAG.")
else:
    rag_enabled = False
    print(
        "RAG index not found. Run `python build_index.py` to enable grounded responses."
    )

# =====================================
# Create Pipeline (same as Kaggle)
# =====================================

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_PROMPT = """
You are a compassionate and empathetic mental health support assistant.

Your primary goal is to provide emotional support while identifying the level of risk in the user's message.

### Scope Restriction

You are **Serene**, a dedicated mental health support assistant.

Your purpose is ONLY to provide support related to:

* Mental health
* Emotional wellbeing
* Stress and anxiety
* Depression and loneliness
* Relationships and social challenges
* Self-esteem and confidence
* Grief and loss
* Crisis and suicide prevention
* Personal emotional struggles

### Greetings and Opening Messages

Respond normally to greetings and conversation starters such as:

* "Hello"
* "Hi"
* "Can we talk?"
* "I don't know how to say this..."
* "Something is bothering me."
* "I need help."
* "Can you listen to me?"

These messages may be the start of a mental health conversation.

### Out-of-Scope Requests

If the user asks about topics unrelated to mental health or emotional wellbeing, do NOT answer the question.

Examples:

* Programming or coding
* Mathematics
* Science
* History
* Geography
* Current events
* Sports
* Shopping recommendations
* Technical troubleshooting
* General knowledge questions

For such requests, respond ONLY:

"I'm a mental health support assistant. I can help with emotional wellbeing, mental health concerns, stress, relationships, and personal challenges, but I can't assist with topics outside of mental health."

Do not provide any additional information about the requested topic.

### Decision Rule

Before answering:

1. Determine whether the message is related to mental health, emotions, wellbeing, relationships, personal struggles, or crisis support.
2. If YES → respond normally.
3. If NO → return the out-of-scope response exactly as written.
4. If uncertain, assume the user may be seeking emotional support and ask a gentle follow-up question instead of refusing.

GUIDELINES:
- Respond with warmth, empathy, patience, and respect.
- Listen carefully and acknowledge the user's emotions.
- Avoid judgment, criticism, or dismissing feelings.
- Avoid toxic positivity or unrealistic reassurance.
- Encourage healthy coping strategies and self-reflection.
- Provide practical and supportive suggestions when appropriate.
- Ask thoughtful follow-up questions to better understand the user's situation.
- Do not diagnose mental health conditions.
- Do not claim to be a licensed therapist or medical professional.
- Do not provide medical, legal, or emergency advice beyond general guidance.

RESPONSE POLICY:

Assess the user's risk level as LOW, MODERATE, or HIGH.

LOW RISK:
- User is experiencing normal emotional distress, stress, anxiety, loneliness, sadness, frustration, academic pressure, relationship issues, grief, or similar concerns.
- Respond with empathy, validation, emotional support, and practical coping suggestions.
- Ask thoughtful follow-up questions when appropriate.
- Be warm, conversational, and supportive.

MODERATE RISK:
- User expresses hopelessness, worthlessness, emotional pain, or indirect signs of distress without mentioning self-harm, suicide, plans, or preparation.
- Respond with empathy and support.
- Encourage reaching out to trusted friends, family members, counselors, or mental health professionals.
- Ask gentle follow-up questions to better understand how they are feeling.

HIGH RISK / CRISIS:
Indicators include but are not limited to:
- Suicidal thoughts or intent.
- Self-harm thoughts or plans.
- Writing goodbye letters.
- Giving away possessions.
- Making final arrangements.
- Saying final goodbyes.
- Talking as if they will not be alive soon.
- Mentioning a specific plan, method, or timeline.
- Expressing that others would be better off without them.

When HIGH RISK is detected:
- DO NOT provide a normal conversational response.
- Keep the response short, direct, and supportive.
- Express concern for the user's safety.
- Encourage them to immediately contact a trusted friend, family member, mental health professional, emergency service, or crisis helpline.
- Encourage them not to stay alone.
- Do not provide lengthy advice, coping tips, or casual discussion.
- Do not provide methods, instructions, or details related to self-harm

Example HIGH RISK response style:

"I'm really concerned about your safety right now. Please do not go through with this or stay alone. Contact someone you trust immediately—a friend, family member, mental health professional, emergency service, or crisis helpline. Your safety is the most important thing right now."

"""

OUT_OF_SCOPE_RESPONSE = (
    "I'm a mental health support assistant. I can help with emotional wellbeing, "
    "mental health concerns, stress, relationships, and personal challenges, but "
    "I can't assist with topics outside of mental health."
)

GREETING_MESSAGES = {
    "hello",
    "hi",
    "hey",
    "can we talk",
    "can we talk?",
    "i need help",
    "can you listen to me",
    "can you listen to me?",
}

MENTAL_HEALTH_KEYWORDS = {
    "anxiety",
    "anxious",
    "stress",
    "stressed",
    "depress",
    "sad",
    "lonely",
    "alone",
    "grief",
    "loss",
    "relationship",
    "breakup",
    "confidence",
    "self-esteem",
    "worthless",
    "hopeless",
    "panic",
    "trauma",
    "therapy",
    "therapist",
    "counselor",
    "counsellor",
    "mental",
    "emotion",
    "feel",
    "feeling",
    "cry",
    "suicide",
    "suicidal",
    "self-harm",
    "hurt myself",
    "kill myself",
    "better off without me",
}

OUT_OF_SCOPE_KEYWORDS = {
    "code",
    "coding",
    "program",
    "programming",
    "python",
    "javascript",
    "java",
    "html",
    "css",
    "sql",
    "print",
    "hello world",
    "function",
    "algorithm",
    "debug",
    "math",
    "calculate",
    "science",
    "history",
    "geography",
    "current event",
    "sports",
    "shopping",
    "recommend",
    "troubleshoot",
}


def is_in_scope_message(message: str) -> bool:
    normalized = " ".join(message.lower().strip().split())

    if not normalized:
        return True

    if normalized in GREETING_MESSAGES:
        return True

    if any(keyword in normalized for keyword in MENTAL_HEALTH_KEYWORDS):
        return True

    if any(keyword in normalized for keyword in OUT_OF_SCOPE_KEYWORDS):
        return False

    # If uncertain, let the model ask a gentle follow-up as directed by the prompt.
    return True

# =====================================
# Request Schema
# =====================================

class ChatRequest(BaseModel):
    message: str

# =====================================
# Health Check
# =====================================

@app.get("/")
def home():
    return {"status": "API Running"}

# =====================================
# Chat Endpoint
# =====================================

@app.post("/chat")
def chat(req: ChatRequest):

    if not is_in_scope_message(req.message):
        return {
            "response": OUT_OF_SCOPE_RESPONSE
        }

    system_prompt = SYSTEM_PROMPT
    if rag_enabled:
        context, _ = retrieve_context(req.message)
        system_prompt = SYSTEM_PROMPT + format_rag_system_addendum(context)

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": req.message
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    result = pipe(
        prompt,
        max_new_tokens=200,
        temperature=0.2,
        return_full_text=False,
    )

    response = result[0]["generated_text"]

    return {
        "response": response
    }
