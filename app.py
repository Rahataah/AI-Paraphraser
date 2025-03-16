import streamlit as st
from parrot import Parrot
import os

# Suppress warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load model once
@st.cache_resource(show_spinner=False)
def load_parrot_model():
    return Parrot(
        model_tag="prithivida/parrot_paraphraser_on_T5",
        use_gpu=False
    )

parrot = load_parrot_model()

def get_paraphrased_sentences(input_text, num_return_sequences=1):
    try:
        phrases = parrot.augment(
            input_phrase=input_text,
            diversity_ranker="levenshtein",
            max_return_phrases=num_return_sequences,
            adequacy_threshold=0.80,
            fluency_threshold=0.80,
            max_length=128,
            top_k=50,
            top_p=0.95
        )
        return [phrase[0] for phrase in phrases] if phrases else []
    except Exception as e:
        st.error(f"Paraphrasing error: {str(e)}")
        return []

# Streamlit UI
st.set_page_config(page_title="Paraphraser")
st.title("Text Paraphraser")
st.write("Enter text to get paraphrased versions")

input_text = st.text_area("Input Text:", height=150)
num_variants = st.slider("Variants", 1, 5, 1)

if st.button("Paraphrase", type="primary"):
    if input_text.strip():
        with st.spinner("Generating..."):
            results = get_paraphrased_sentences(input_text, num_variants)
            
            if results:
                st.subheader("Output:")
                for i, text in enumerate(results):
                    st.markdown(f"{i+1}. {text}")
            else:
                st.warning("No paraphrases generated")
    else:
        st.error("Please input text first")
