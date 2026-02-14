#importando as bibliotecas necessárias para interação com o sistema operacional
import os

#importando a biblioteca streamlit para criação de interfaces web
import streamlit as st

#importando a biblioteca gorq para criação de agentes de inteligência artificial
from groq import Groq

st.set_page_config(
  page_title="Javs",
  page_icon="🤖",
  layout="wide",
  initial_sidebar_state="expanded")

