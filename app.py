from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# =========================
# Load Model
# =========================

BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

print("Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    dtype=torch.float16,
)

print("Loading adapter...")
model = PeftModel.from_pretrained(
    base_model,
    "./mental_health_model"
)

# Apple Silicon GPU
device = "mps" if torch.backends.mps.is_available() else "cpu"
model = model.to(device)

print("Model loaded successfully!")
print(model)

# =========================
# Test Message
# =========================

messages = [
    {
        "role": "system",
        "content": """
You are a compassionate and empathetic mental health support assistant.

Your primary goal is to provide emotional support while identifying the level of risk in the user's message.

HIGH RISK INDICATORS INCLUDE:
- Suicidal thoughts or intent
- Self-harm plans
- Writing goodbye letters
- Giving away possessions
- Making final arrangements
- Saying final goodbyes
- Talking as if they won't be alive soon

When HIGH RISK is detected:
- Express concern
- Prioritize safety
- Encourage immediate support
- Keep responses direct and supportive
"""
    },
    {
        "role": "user",
        "content": "I gave away all my belongings today."
    }
]

# =========================
# Create Prompt
# =========================

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer(
    prompt,
    return_tensors="pt"
).to(device)

outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    temperature=0.2,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id,
    eos_token_id=tokenizer.eos_token_id,
)

response = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

assistant_response = response.split("assistant")[-1].strip()

print("\nAssistant:\n")
print(assistant_response)

print("\n========== RESPONSE ==========\n")
print(response)