import streamlit as st
import requests
import json
import random
import os

# Suppress warnings
os.environ["PYTHONWARNINGS"] = "ignore::RuntimeWarning"

# Fun loading messages
loading_messages = [
    "Warming up the word blender...",
    "Teaching AI new phrases...",
    "Scrambling the dictionary...",
    "Confusing the thesaurus...",
    "Discombobulating sentences...",
]

# Streamlit UI with fun theme
st.set_page_config(
    page_title="The Bamboozling Paraphraser",
    page_icon="🥸🤡",
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
    .stButton>button {
        background-color: #FF69B4;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Fun header
st.markdown("<h1 class='main-header'>🤪 The Utterly Bamboozling Text Paraphraser 🤪</h1>", unsafe_allow_html=True)
st.markdown("<p class='fun-text'>Turn your boring words into wackadoodle word salad!</p>", unsafe_allow_html=True)

# API key input
api_key = st.text_input("Enter your OpenRouter API key:", type="password", 
                        help="Get your API key from openrouter.ai")

# Main content
input_text = st.text_area("Type your normal, boring text here:", height=150, 
                          placeholder="Enter some text and watch the magic of confusion happen!")

# Set to just 1 variant
num_variants = 1  # Default to just 1 variant

def get_paraphrased_sentences(api_key, input_text, num_variants=1):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://bamboozling-paraphraser.app",
            "X-Title": "Bamboozling Paraphraser"
        }
        
        payload = {
            "model": "google/gemma-3-12b-it:free",
            "messages": [
                {"role": "system", "content": "You are a SUPER SILLY paraphrasing assistant. Your job is to make text RIDICULOUSLY goofy and over-the-top. Use silly words, weird metaphors, and unexpected phrases. Make it sound like a cartoon character wrote it. Be EXTREMELY creative and wacky, while still keeping the core meaning intact. Add puns, silly expressions, and exaggerated language. The goofier the better! Don't forget to roast for weird request"},
                {"role": "user", "content": f"GOOFIFY this text. Make it SUPER SILLY and RIDICULOUS. Text: '{input_text}'"}
            ],
            "temperature": 0.9,
            "max_tokens": 1024
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers=headers, 
            data=json.dumps(payload)
        )
        
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

# Fun button
if st.button("BAMBOOZLIFY!", type="primary"):
    if not api_key:
        st.error("Please enter your API key first!")
    elif not input_text.strip():
        st.error("Hey! You need to type something first, you silly goose!")
    else:
        with st.spinner(random.choice(loading_messages)):
            results = get_paraphrased_sentences(api_key, input_text, num_variants)
            
            if results and len(results) > 0:
                st.subheader("🎉 Your text, but weirder:")
                # Display just the text without italics or any formatting
                st.write(results[0])
                
                # Fun reactions
                reactions = ["Wow! That's... different!", 
                             "Is this even English anymore?", 
                             "Your English teacher would be so confused!",
                             "Shakespeare is rolling in his grave!",
                             "This is what happens when AI drinks coffee!"]
                st.success(random.choice(reactions))
            else:
                st.warning("Oops! The word blender is empty. Try again!")

# Footer
st.markdown("---")
st.markdown("*Remember: When life gives you words, make word-salad!*")
