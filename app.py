import streamlit as st
from parrot import Parrot

# Load model once
@st.cache_resource
def load_parrot_model():
    return Parrot(
        model_tag="prithivida/parrot_paraphraser_on_T5",
        use_gpu=False
    )  # Only these 2 parameters are valid

parrot = load_parrot_model()

def get_paraphrased_sentences(input_text, num_return_sequences=1):
    try:
        phrases = parrot.augment(
            input_phrase=input_text,
            diversity_ranker="levenshtein",
            do_diverse=False,
            max_return_phrases=num_return_sequences,
            adequacy_threshold=0.80,
            fluency_threshold=0.80,
            max_length=128,  # Generation parameters stay here
            do_sample=True,
            top_k=50,
            top_p=0.95
        )
        return [phrase[0] for phrase in phrases] if phrases else ["No paraphrases generated"]
    except Exception as e:
        st.error(f"Error in paraphrasing: {str(e)}")
        return ["Error in paraphrasing"]

# Streamlit UI
st.title("Text Paraphraser")
st.write("Enter a passage and get a paraphrased version.")

input_text = st.text_area("Enter your text here:")
num_variants = st.slider("Number of paraphrased variants", min_value=1, max_value=5, value=1)

if st.button("Paraphrase"):
    if input_text.strip():
        with st.spinner("Generating paraphrases..."):
            paraphrased_texts = get_paraphrased_sentences(input_text, num_return_sequences=num_variants)
            
            st.subheader("Paraphrased Text:")
            for i, text in enumerate(paraphrased_texts):
                st.markdown(f"- {text}")
    else:
        st.warning("Please enter some text to paraphrase.")
