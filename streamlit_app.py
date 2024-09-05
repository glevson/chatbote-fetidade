import streamlit as st
import pandas as pd
import numpy as np
import requests

# Função para cache
@st.cache
def expensive_calculation(x):
    # Exemplo de uma função com cálculo pesado
    return x ** 2

# Função para enviar mensagem ao chatbot (simulação de API)
def get_chatbot_response(message):
    # Simulando uma resposta do chatbot
    api_key = "SUA_CHAVE_DE_API"  # Substitua pela chave de API correta, se disponível
    # endpoint = f"https://api.example.com/chatbot?message={message}&key={api_key}"
    
    # Aqui estamos simulando uma resposta, mas no caso real você usaria requests.get()
    # response = requests.get(endpoint)
    # if response.status_code == 200:
    #     return response.json()["response"]
    # else:
    #     return "Desculpe, o chatbot está indisponível no momento."
    
    # Resposta simulada para fins de exemplo
    return "Para mais informações, entre em contato conosco pelo telefone (82)993022941."

# Chatbot no Streamlit
def chatbot():
    st.subheader("Chatbot Inteligente")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    user_input = st.text_input("Digite sua mensagem")
    
    if user_input:
        # Adiciona a mensagem do usuário na sessão
        st.session_state.messages.append({"message": user_input, "is_user": True})
        
        # Obtém a resposta do chatbot usando a função que chama a API simulada
        bot_response = get_chatbot_response(user_input)
        st.session_state.messages.append({"message": bot_response, "is_user": False})
    
    # Exibe as mensagens na tela
    for message in st.session_state.messages:
        if message["is_user"]:
            st.write(f"Você: {message['message']}")
        else:
            st.write(f"Chatbot: {message['message']}")

# Função para exibir o mapa interativo
def mapa_interativo():
    st.subheader("Mapa Interativo de Instalações")
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],  # Simulação de coordenadas
        columns=['lat', 'lon'])
    st.map(df)

# Função principal do site
def main():
    st.title("Efetividade Tecnologia - Energia Solar")
    st.write("Soluções em Energia Solar Fotovoltaica e TI.")
    
    # Seletor de opções (widget selectbox)
    option = st.selectbox(
        "Escolha um serviço para saber mais:",
        ["Orçamento", "Instalação", "Manutenção", "Energia por Assinatura"]
    )
    
    st.write(f"Você escolheu: {option}")
    
    # Slider (widget slider) para orçamento estimado
    budget = st.slider('Selecione seu orçamento estimado (em R$)', 1000, 100000)
    st.write(f"Orçamento escolhido: R$ {budget}")
    
    # Função com cache
    st.write(f"Resultado de um cálculo pesado (cache): {expensive_calculation(10)}")
    
    # Adiciona o chatbot à página
    chatbot()
    
    # Exibe um mapa interativo
    mapa_interativo()

# Executa a aplicação
if __name__ == "__main__":
    main()
