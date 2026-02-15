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

#Definindo o prompt para o agente de inteligência artificial
CUSTOM_PROMPT = """
Você é o "Javs", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.
REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com código.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas."""

#craiando a barra lateral no streamlit
with st.sidebar:
  #Definindo o título da barra lateral
  st.title("Javs - Assistente de IA para Programação")
  #Adicionando uma descrição do assistente de IA
  st.markdown(""" **Javs** é um assistente de inteligência artificial especializado em programação, com foco principal em Python.
  """)

  #campo para inserção do token de acesso à API da Groq
  groq_api_key = st.text_input("Insira seu token de acesso à API da Groq",
  type="password",
  help="Obtenha seu token em https://console.groq.com/keys"
  )

#Adiciona linhas divisorias e explicaoes na barra lateral
  st.markdown("---")
  st.markdown("""Desenvolvido para ajudar desenvolvedores iniciantes, **Javs** responde a dúvidas de programação de forma clara, precisa e útil, seguindo regras específicas para garantir respostas de alta qualidade.""")

#Titulo principal da aplicação
st.title("Javs - IA para Programação")
st.caption("Digite sua pergunta sobre programação e obtenha respostas detalhadas, exemplos de código e referências úteis.")

#inicializa o historico de mensagens na sessão, caso ainda nao exista
if "messages" not in st.session_state:
  st.session_state.messages = []

#Exibe todas as mensagens do histórico
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

#inicializa a variavel de entrada do usuário
Client = None

#Verifica se o token de acesso à API da Groq foi inserido
if groq_api_key:
  try:
    #cria cliente Groq com o token de acesso
    Client = Groq(api_key=groq_api_key)
  except Exception as e:
    st.error(f"Erro ao criar cliente Groq: {e}")
    st.stop()

#Caso não tenha chave de acesso, mas já existam mensagens no histórico, exibe um aviso para o usuário
elif st.session_state.messages:
  st.warning("Por favor, insira seu token de acesso à API da Groq para continuar a conversa.")

#Campo de entrada para a pergunta do usuário
if prompt := st.chat_input("Digite sua pergunta sobre programação..."):
  #se não tiver um clinte valido, exibe um aviso para o usuário e para a execução do código
  if not Client:
    st.warning("Por favor, insira seu token de acesso à API da Groq para enviar sua pergunta.")
    st.stop()

#armazena a mensagem do usuário no histórico
st.session_state.messages.append({"role": "user", "content": prompt})

#exibe a mensagem do usuário na interface
with st.chat_message("user"):
  st.markdown(prompt)

#Preparando a mensagem para enviar a API, icluindo o prompt
messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
for msg in st.session_state:
  messages_for_api.append(msg)

#cria a resposta do agente de IA usando a API da Groq
with st.chat_message("assistant"):
  with st.spinner("Javs está pensando..."):
    try:
      #chama a API da Groq para obter a resposta do agente de IA
      chat_completion = Client.chat.completions.create(
        messages=messages_for_api,
        model="openai/gpt-oss-20b",
        temperature=0.7,
        max_tokens=2048,
      )
      #Extraindo a resposta do agente de IA da resposta da API
      javs_response = chat_completion.choices[0].message.content
      #Exibindo a resposta do agente de IA na interface
      st.markdown(javs_response)
      #Armazenando a resposta do agente de IA no histórico de mensagens
      st.session_state.messages.append({"role": "assistant", "content": javs_response})
    except Exception as e:
      st.error(f"Erro ao obter resposta do Javs: {e}")
      #st.stop()
st.markdown(
  """
  <div style="text-align: center; color: gray;">
    <hr>
    <p>Desenvolvido por [Francisco Bowe] - 2026</p>
  </div>
  """,
  unsafe_allow_html=True
)

#comando para executar a aplicação streamlit
#streamlit run 002_ex_agentIA_py.py

