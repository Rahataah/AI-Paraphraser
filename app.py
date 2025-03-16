import streamlit as st
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Load model once
@st.cache_resource
def load_parrot_model():
    # Load Parrot model (Pegasus-based paraphraser)
    tokenizer = PegasusTokenizer.from_pretrained("tuner007/pegasus_paraphrase")
    model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
    return model, tokenizer

# Get paraphraser model and tokenizer
model, tokenizer = load_parrot_model()

def get_paraphrased_sentences(input_text, num_return_sequences=1, num_beams=10):
    # Tokenize the input text
    inputs = tokenizer([input_text], truncation=True, padding="longest", return_tensors="pt")
    
    # Generate paraphrased sentences
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            num_beams=num_beams,
            num_return_sequences=num_return_sequences,
            max_length=60,
            temperature=1.5
        )
    
    # Decode the generated outputs back to text
    paraphrased_texts = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    
    return paraphrased_texts

# Streamlit UI
st.title("Text Paraphraser")
st.write("Enter a passage and get a paraphrased version.")

input_text = st.text_area("Enter your text here:")
num_variants = st.slider("Number of paraphrased variants", min_value=1, max_value=5, value=1)

!pip install git+https://github.com/PrithivirajDamodaran/Parrot_Paraphraser.git
from parrot import Parrot
import torch

# Load model once
@st.cache_resource
def load_parrot_model():
    # Initialize Parrot paraphraser with proper settings
    parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", 
                   use_gpu=False, 
                   max_length=128,  # Increased max length for better paraphrasing
                   do_sample=True)
    return parrot

parrot = load_parrot_model()

def get_paraphrased_sentences(input_text, num_return_sequences=1):
    try:
        # Get paraphrases using Parrot's augment method
        phrases = parrot.augment(input_phrase=input_text,
                                diversity_ranker="levenshtein",
                                do_diverse=False, 
                                max_return_phrases=num_return_sequences,
                                adequacy_threshold=0.80,
                                fluency_threshold=0.80)
        return [phrase[0] for phrase in phrases] if phrases else ["No paraphrases generated"]
    except:
        return ["Error in paraphrasing"]

if st.button("Paraphrase"):
    if input_text.strip():
        with st.spinner("Generating paraphrases..."):
            paraphrased_texts = get_paraphrased_sentences(input_text, num_return_sequences=num_variants)
            
            st.subheader("Paraphrased Text:")
            for i, text in enumerate(paraphrased_texts):
                st.markdown(f"- {text}")  # Better formatting with bullet points
    else:
        st.warning("Please enter some text to paraphrase.")
