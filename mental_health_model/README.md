---

base_model: Qwen/Qwen2.5-3B-Instruct
library_name: peft
------------------

# Model Card for Mental Health Chatbot Model

## Model Details

### Model Description

This model is a parameter-efficient fine-tuned (PEFT) version of Qwen2.5-3B-Instruct, designed to act as a mental health support chatbot. The model provides empathetic, supportive, and safety-aware responses related to emotional wellbeing, stress, anxiety, loneliness, self-esteem, and interpersonal challenges.

* **Developed by:** Salaj Bisht
* **Model type:** Causal Language Model (LLM)
* **Language(s):** English
* **License:** Apache 2.0 (inherits base model license where applicable)
* **Finetuned from model:** Qwen/Qwen2.5-3B-Instruct

### Model Sources

* **Base Model Repository:** https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
* **Framework:** PEFT (Parameter-Efficient Fine-Tuning)

## Uses

### Direct Use

This model is intended for:

* Mental health support conversations
* Emotional wellbeing assistance
* Stress and anxiety management discussions
* Self-reflection and coping strategies
* General emotional support

### Downstream Use

The model can be integrated into:

* Mental health chatbots
* Wellness applications
* Educational mental health tools
* Supportive conversational AI systems

### Out-of-Scope Use

This model should not be used for:

* Clinical diagnosis
* Medical advice
* Emergency crisis intervention
* Legal or financial advice
* Replacing licensed mental health professionals

## Bias, Risks, and Limitations

* The model may generate incorrect or misleading responses.
* It is not a licensed therapist or medical professional.
* Responses should not be considered professional mental health advice.
* The model may reflect biases present in training data.
* Users experiencing severe distress should seek professional help.

### Recommendations

Users should:

* Verify important information with qualified professionals.
* Avoid relying solely on the model for mental health treatment.
* Use the model as a supplementary support tool.

## How to Get Started with the Model

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model = "Qwen/Qwen2.5-3B-Instruct"
adapter_path = "./mental_health_lora"

tokenizer = AutoTokenizer.from_pretrained(base_model)

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    device_map="auto"
)

model = PeftModel.from_pretrained(model, adapter_path)

prompt = "I have been feeling anxious lately."

inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_new_tokens=200
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Training Details

### Training Data

The model was fine-tuned on a custom mental health conversational dataset containing supportive dialogues focused on:

* Anxiety
* Stress
* Depression-related discussions
* Emotional wellbeing
* Self-esteem
* Relationship concerns

### Training Procedure

#### Preprocessing

* Conversation formatting applied
* Instruction-response pairs created
* Text cleaned and standardized
* Duplicate samples removed where applicable

#### Training Hyperparameters

* **Training regime:** FP16 Mixed Precision
* **Fine-tuning method:** LoRA
* **Framework:** PEFT

#### Speeds, Sizes, Times

* **Base Model Size:** 3 Billion Parameters
* **Adapter Method:** LoRA
* **Framework Version:** PEFT 0.15.2

## Evaluation

### Testing Data, Factors & Metrics

#### Testing Data

Held-out validation conversations from the mental health support dataset.

#### Factors

Evaluation focused on:

* Empathy
* Helpfulness
* Safety
* Relevance
* Instruction following

#### Metrics

* Validation Loss
* Qualitative Human Evaluation
* Response Safety Assessment

### Results

The model demonstrates strong empathetic conversational abilities and maintains topic relevance in mental health support scenarios.

#### Summary

The fine-tuned model successfully adapts Qwen2.5-3B-Instruct for supportive mental health conversations while retaining general language understanding capabilities.

## Environmental Impact

* **Hardware Type:** GPU
* **Hours Used:** [Fill in]
* **Cloud Provider:** Kaggle
* **Compute Region:** [Fill in]
* **Carbon Emitted:** Not measured

## Technical Specifications

### Model Architecture and Objective

* Architecture: Transformer Decoder
* Base Model: Qwen2.5-3B-Instruct
* Objective: Next Token Prediction
* Fine-Tuning Method: LoRA (PEFT)

### Compute Infrastructure

#### Hardware

* NVIDIA GPU (Kaggle Environment)

#### Software

* Transformers
* PEFT 0.15.2
* PyTorch
* Accelerate

## Citation

### BibTeX

```bibtex
@misc{mentalhealthqwen2026,
  author = {Salaj Bisht},
  title = {Mental Health Chatbot Fine-Tuned on Qwen2.5-3B-Instruct},
  year = {2026},
  publisher = {Hugging Face}
}
```

### APA

Bisht, S. (2026). Mental Health Chatbot Fine-Tuned on Qwen2.5-3B-Instruct. Hugging Face.

## More Information

This model was created as an educational and research project focused on developing empathetic conversational AI for mental health support applications.

## Model Card Authors

Salaj Bisht

## Model Card Contact

For questions or feedback, contact the model author through the Hugging Face repository.

### Framework Versions

* PEFT 0.15.2
* Transformers 4.x
* PyTorch 2.x
