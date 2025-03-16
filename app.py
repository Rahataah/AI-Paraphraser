import streamlit as st
import os
import warnings
import random
import requests
import json

# Suppress all warnings
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore::RuntimeWarning"

# Fun loading messages
loading_messages = [
    "Warming up the word blender...",
    "Teaching AI new phrases...",
    "Scrambling the dictionary...",
    "Confusing the thesaurus...",
    "Discombobulating sentences...",
]

# OpenRouter API configuration for DeepSeek
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_paraphrased_sentences(input_text, num_variants=1):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://bamboozling-paraphraser.app",  # Required by OpenRouter
            "X-Title": "Bamboozling Paraphraser"  # Required by OpenRouter
        }
        
        payload = {
            "model": "deepseek/deepseek-r1-zero:free",  # Correct model name for DeepSeek R1 Zero
            "messages": [
                {"role": "system", "content": "You are a creative paraphrasing assistant. Your task is to rewrite the given text in different ways while preserving the core meaning. Be creative, use different vocabulary, and vary sentence structures. Make it sound natural but different from the original."},
                {"role": "user", "content": f"Please paraphrase this text in {num_variants} different ways. Number each version. Text: '{input_text}'"}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, data=json.dumps(payload))
        
        if response.status_code != 200:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return []
            
        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Parse the response to extract variants
        variants = []
        lines = content.split("\n")
        current_variant = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line starts with a number followed by period or colon
            if (line[0].isdigit() and line[1:].startswith(". ")) or (line[0].isdigit() and line[1:].startswith(": ")):
                if current_variant:
                    variants.append(current_variant)
                current_variant = line[line.find(" ")+1:].strip()
            else:
                current_variant += " " + line
                
        # Add the last variant if exists
        if current_variant and current_variant not in variants:
            variants.append(current_variant)
            
        # If parsing failed, just split by lines
        if not variants:
            variants = [line.strip() for line in content.split("\n") if line.strip()]
            
        return variants[:num_variants]
        
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
