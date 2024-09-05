import streamlit as st
from fpdf import FPDF
import requests

# Função para gerar PDF do orçamento personalizado
def generate_pdf(name, phone, budget, service_choice):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Orçamento Personalizado - Efetividade Tecnologia", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Nome: {name}", ln=True)
    pdf.cell(200, 10, f"Telefone: {phone}", ln=True)
    pdf.cell(200, 10, f"Serviço Escolhido: {service_choice}", ln=True)
    pdf.cell(200, 10, f"Orçamento Estimado: R$ {budget}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, "Obrigado por solicitar um orçamento. Entraremos em contato em breve!", ln=True)

    return pdf.output(dest='S').encode('latin1')  # Gera o PDF em formato binário

# Função para exibir um formulário em etapas
def form_slides():
    st.subheader("Solicite seu Orçamento Personalizado")

    # Slide 1 - Coleta do nome
    if "step" not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        st.session_state.name = st.text_input("Digite seu nome:")
        if st.session_state.name:
            if st.button("Próximo"):
                st.session_state.step = 2

    # Slide 2 - Coleta do telefone
    elif st.session_state.step == 2:
        st.session_state.phone = st.text_input("Digite seu telefone:")
        if st.session_state.phone:
            if st.button("Próximo"):
                st.session_state.step = 3

    # Slide 3 - Orçamento e Serviço
    elif st.session_state.step == 3:
        st.session_state.budget = st.slider('Selecione seu orçamento estimado (em R$)', 1000, 100000)
        st.session_state.service_choice = st.selectbox(
            "Escolha o serviço que deseja:",
            ["Consultoria", "Instalação Residencial", "Instalação Comercial", "Manutenção", "Energia por Assinatura"]
        )
        if st.button("Gerar Orçamento"):
            st.session_state.step = 4

    # Slide final - Gerar PDF
    if st.session_state.step == 4:
        st.success("Orçamento gerado com sucesso! Clique abaixo para baixar seu orçamento em PDF.")
        pdf = generate_pdf(st.session_state.name, st.session_state.phone, st.session_state.budget, st.session_state.service_choice)
        st.download_button(
            "Baixar PDF",
            data=pdf,
            file_name="orçamento_personalizado.pdf",
            mime="application/octet-stream"
        )

# Função para chamar o chatbot simulando a API de Gemini AI (Google)
def get_chatbot_response(message):
    api_key = "SUA_CHAVE_DE_API"  # Substitua pela chave de API do Google ou outro chatbot como Gemini AI
    endpoint = f"https://api.example.com/chatbot?message={message}&key={api_key}"
    
    # Aqui estamos simulando uma resposta, mas no caso real você usaria requests.get() com a API correta.
    # response = requests.get(endpoint)
    # if response.status_code == 200:
    #     return response.json()["response"]
    # else:
    #     return "Desculpe, o chatbot está indisponível no momento."
    
    # Resposta simulada para fins de exemplo
    return "Obrigado por entrar em contato! Ligue para (82)993022941 para solicitar seu orçamento."

# Chatbot no Streamlit
def chatbot():
    st.subheader("Chatbot Inteligente")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Digite sua mensagem")
    
    if user_input:
        # Adiciona a mensagem do usuário na sessão
        st.session_state.messages.append({"message": user_input, "is_user": True})
        
        # Obtém a resposta do chatbot
        bot_response = get_chatbot_response(user_input)
        st.session_state.messages.append({"message": bot_response, "is_user": False})
    
    # Exibe as mensagens na tela
    for message in st.session_state.messages:
        if message["is_user"]:
            st.write(f"Você: {message['message']}")
        else:
            st.write(f"Chatbot: {message['message']}")

# Função para exibir ícones e layout dinâmico
def display_icons():
    st.markdown("""
    <style>
    .icon {
        font-size: 50px;
        color: #ff4b4b;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center;">
        <span class="icon">💡</span><span class="icon">🔧</span><span class="icon">📊</span><span class="icon">⚡</span>
    </div>
    """, unsafe_allow_html=True)

    st.write("### Nossos Serviços:")
    st.write("- 💡 **Consultoria**: Avaliação de viabilidade e projetos personalizados.")
    st.write("- 🔧 **Instalação**: Sistemas residenciais e comerciais de energia solar.")
    st.write("- 📊 **Monitoramento**: Manutenção e monitoramento remoto para eficiência.")
    st.write("- ⚡ **Energia por Assinatura**: Alternativa para quem deseja economia sem instalação própria.")

# Função principal do site
def main():
    st.title("Efetividade Tecnologia - Energia Solar")
    st.write("### Soluções completas em Energia Solar Fotovoltaica e TI.")

    # Exibe ícones e layout dinâmico
    display_icons()

    # Seletor de opções (widget selectbox) para navegação
    option = st.sidebar.selectbox(
        "Navegue pelo site",
        ["Home", "Serviços", "Orçamento Personalizado", "Chatbot", "Contato"]
    )

    if option == "Home":
        st.write("Bem-vindo ao nosso site! Explore nossos serviços e solicite seu orçamento.")
    elif option == "Serviços":
        st.write("Aqui estão os nossos serviços completos para energia solar.")
        display_icons()
    elif option == "Orçamento Personalizado":
        form_slides()
    elif option == "Chatbot":
        chatbot()
    elif option == "Contato":
        st.write("Entre em contato conosco pelo telefone (82)993022941 ou pelo e-mail contato@efetividade.com.br.")

# Executa a aplicação
if __name__ == "__main__":
    main()
