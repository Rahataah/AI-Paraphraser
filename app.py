import streamlit as st
from transformers import pipeline

# Load Pegasus model
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="tuner007/pegasus_paraphrase")

paraphrase_model = load_model()

def paraphrase_text(text):
    # Adjust parameters for paraphrasing with Pegasus
    paraphrased = paraphrase_model(text, max_length=150, min_length=30, do_sample=True, num_return_sequences=1)
    return paraphrased[0]['generated_text']

# Streamlit UI
st.title("Text Paraphraser (Pegasus Model)")
st.write("Enter a passage and get a paraphrased version.")

input_text = st.text_area("Enter your text here:")
if st.button("Paraphrase"):
    if input_text.strip():
        paraphrased_text = paraphrase_text(input_text)
        st.subheader("Paraphrased Text:")
        st.write(paraphrased_text)
    else:
        st.warning("Please enter some text to paraphrase.")
