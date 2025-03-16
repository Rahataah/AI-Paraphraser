import streamlit as st
import os
from transformers import pipeline

# Force CPU execution
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Load Pegasus model with PyTorch weights
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="tuner007/pegasus_paraphrase", device=-1, framework="pt", from_pt=True)

paraphrase_model = load_model()

def paraphrase_text(text):
    paraphrased = paraphrase_model(text, max_length=150, min_length=30, do_sample=True, num_return_sequences=1)
    return paraphrased[0]['generated_text']

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
