from transformers import pipeline


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device=-1,
)


messages = [
    {
        "role": "user",
        "content": "Explain the purpose of the NIST AI Risk Management Framework in simple terms.",
    }
]


result = generator(
    messages,
    max_new_tokens=200,
    do_sample=False,
)


print(result)