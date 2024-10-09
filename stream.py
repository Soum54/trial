import streamlit as st
st.markdown('''
<style>
@keyframes move {
  0% {top: 100vh;}
  100% {top: -50px;}
}
.emoji {
  position: absolute;
  left: 50%;
  animation: move 5s infinite;
  font-size: 50px;
}
.emoji.negative { left: 40%; }
.emoji.neutral { left: 60%; }
</style>
<div class="emoji positive">😊</div>
<div class="emoji negative">😢</div>
<div class="emoji neutral">😐</div>
''', unsafe_allow_html=True)
