import streamlit as st
import random

st.markdown('''
<style>
@keyframes move {
  0% {top: 100vh;}
  100% {top: -50px;}
}

.emoji {
  position: absolute;
  font-size: 50px;
  animation: move 5s infinite ease-in-out;
}

''', unsafe_allow_html=True)

# Adding multiple emoji sprays
for i in range(15):
    # Randomize left position and delay for each emoji
    left_position = random.randint(0, 100)  # Left percentage
    animation_delay = random.uniform(0, 5)  # Delay in seconds
    emoji_choice = random.choice(['😊', '😢', '😐'])  # Choose between emojis
    
    st.markdown(f'''
    <style>
    .emoji-{i} {{
      left: {left_position}%;
      animation-delay: {animation_delay}s;
    }}
    </style>
    <div class="emoji emoji-{i}">{emoji_choice}</div>
    ''', unsafe_allow_html=True)
