import streamlit as st
import os
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Force CPU execution
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
device = torch.device("cpu")

# Load Pegasus model with manual class specification
@st.cache_resource
def load_model():
    model_name = "tuner007/pegasus_paraphrase"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    return model, tokenizer

model, tokenizer = load_model()

def paraphrase_text(text):
    # Encode input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="longest").to(device)
    # Generate paraphrased output
    output = model.generate(**inputs, max_length=150, min_length=30, do_sample=True, num_return_sequences=1)
    # Decode output
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Streamlit UI
st.title("AI-Powered Text Paraphraser (CPU Optimized)")
st.write("Enter a passage and get a paraphrased version using the Pegasus model.")

input_text = st.text_area("Enter your text here:")
if st.button("Paraphrase"):
    if input_text.strip():
        with st.spinner("Generating paraphrased text..."):
            paraphrased_text = paraphrase_text(input_text)
        st.subheader("Paraphrased Text:")
        st.write(paraphrased_text)
    else:
        st.warning("Please enter some text to paraphrase.")

# Footer
st.markdown("---")
st.markdown("Powered by [Hugging Face Transformers](https://huggingface.co/).")
