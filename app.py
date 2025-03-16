import streamlit as st
from parrot import Parrot
import os
import warnings
import random

# Suppress all warnings
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

# Simpler approach to handle torch path errors
os.environ["PYTHONWARNINGS"] = "ignore::RuntimeWarning"

# Fun loading messages
loading_messages = [
    "Warming up the word blender...",
    "Teaching parrots new phrases...",
    "Scrambling the dictionary...",
    "Confusing the thesaurus...",
    "Discombobulating sentences...",
]

# Load model once with simplified configuration
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
            fluency_threshold=0.80
        )
        return [phrase[0] for phrase in phrases] if phrases else []
    except Exception as e:
        st.error(f"Oopsie woopsie! Paraphrasing boo-boo: {str(e)}")
        return []

# Streamlit UI with fun theme
st.set_page_config(
    page_title="The Bamboozling Paraphraser",
    page_icon="🦜",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-family: 'Comic Sans MS', cursive;
        color: #FF69B4;
    }
    .fun-text {
        font-family: 'Arial', sans-serif;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# Fun header
st.markdown("<h1 class='main-header'>🤪 The Utterly Bamboozling Text Paraphraser 🤪</h1>", unsafe_allow_html=True)
st.markdown("<p class='fun-text'>Turn your boring words into wackadoodle word salad!</p>", unsafe_allow_html=True)

input_text = st.text_area("Type your normal, boring text here:", height=150, 
                          placeholder="Enter some text and watch the magic of confusion happen!")

# Fun slider labels
num_variants = st.slider(
    "Flummoxification Level (how many variants?)",
    min_value=1,
    max_value=5,
    value=1,
    help="More variants = more nonsense!"
)

# Fun button
if st.button("BAMBOOZLIFY!", type="primary"):
    if input_text.strip():
        with st.spinner(random.choice(loading_messages)):
            results = get_paraphrased_sentences(input_text, num_variants)
            
            if results:
                st.subheader("🎉 Your text, but weirder:")
                for i, text in enumerate(results):
                    st.markdown(f"**Version {i+1}**: _{text}_")
                
                # Fun reactions
                reactions = ["Wow! That's... different!", 
                             "Is this even English anymore?", 
                             "Your English teacher would be so confused!",
                             "Shakespeare is rolling in his grave!",
                             "This is what happens when AI drinks coffee!"]
                st.success(random.choice(reactions))
            else:
                st.warning("Oops! The word blender is empty. Try again!")
    else:
        st.error("Hey! You need to type something first, you silly goose!")

# Footer
st.markdown("---")
st.markdown("*Remember: When life gives you words, make word-salad!*")
