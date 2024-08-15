from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
import tensorflow as tf
import sys
import json

# Load model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = TFGPT2LMHeadModel.from_pretrained('gpt2')

def generate_text(prompt):
    # Encode input text
    inputs = tokenizer(prompt, return_tensors='tf') 
    # Generate output with adjusted parameters
    outputs = model.generate(
        inputs['input_ids'], 
        max_length=150,            # Allow more space for detailed responses
        num_return_sequences=1, 
        temperature=0.5,           # Lower temperature for more focused output
        top_k=30,                  # Top-K sampling for reduced randomness
        top_p=0.85,                # Nucleus sampling
        repetition_penalty=1.2     # Reduces repetitive text
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No prompt provided")
        sys.exit(1)

    prompt = sys.argv[1]
    generated_text = generate_text(prompt)
    print(json.dumps({"generated_text": generated_text}))
