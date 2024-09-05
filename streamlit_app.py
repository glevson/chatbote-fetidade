import streamlit as st
from streamlit_chat import message as st_message

# Função para exibir a página inicial
def home():
    st.title("Bem-vindo à Efetividade Tecnologia")
    st.image("https://via.placeholder.com/1200x300.png", use_column_width=True)
    st.subheader("Especialistas em Energia Solar Fotovoltaica e Soluções de TI")
    st.write("Na Efetividade Tecnologia, oferecemos soluções sustentáveis em energia solar e serviços de TI personalizados para você.")
    st.button("Solicitar Orçamento", on_click=lambda: st.sidebar.selectbox("Menu", menu, index=5))
    st.button("Consulta Técnica Gratuita", on_click=lambda: st.sidebar.selectbox("Menu", menu, index=5))

# Função para exibir a página de serviços
def nossos_servicos():
    st.title("Nossos Serviços")
    st.subheader("Consultoria em Energia Solar")
    st.write("Oferecemos avaliação de viabilidade e projetos personalizados para sua instalação solar.")
    st.subheader("Venda e Instalação de Sistemas Fotovoltaicos")
    st.write("Fornecemos soluções completas para residências, empresas e indústrias.")
    st.subheader("Soluções em TI")
    st.write("Serviços especializados em tecnologia da informação, incluindo suporte e infraestrutura.")

# Função para exibir a página de manutenção e monitoramento
def manutencao_monitoramento():
    st.title("Manutenção e Monitoramento")
    st.subheader("Planos de Manutenção")
    st.write("Oferecemos diversos planos de manutenção para garantir o melhor desempenho do seu sistema fotovoltaico:")
    st.write("- Automonitoramento")
    st.write("- Flex")
    st.write("- Gold")
    st.write("- Diamond")
    st.subheader("Monitoramento Remoto")
    st.write("Utilizamos tecnologia avançada para monitorar e garantir a eficiência dos sistemas instalados.")

# Função para exibir a página de energia por assinatura
def energia_por_assinatura():
    st.title("Energia por Assinatura")
    st.subheader("Energia Solar por Consórcio/Cooperativa")
    st.write("Participe do nosso modelo de energia por assinatura e economize sem precisar instalar um sistema individual.")
    st.write("**Vantagens:** Economia, sustentabilidade e flexibilidade.")
    st.button("Solicitar Adesão", on_click=lambda: st.sidebar.selectbox("Menu", menu, index=5))

# Função para exibir a página do blog
def blog():
    st.title("Blog")
    st.write("Acompanhe as últimas novidades e dicas sobre energia solar, sustentabilidade e TI em nosso blog.")
    st.write("**Artigos em Destaque:**")
    st.write("- [Inovações em Energia Solar](#)")
    st.write("- [Como Economizar Energia](#)")
    st.write("- [Tendências do Mercado Solar](#)")

# Função para exibir a página de contato
def contato():
    st.title("Contato")
    with st.form(key='contact_form'):
        st.subheader("Fale Conosco")
        name = st.text_input("Nome")
        email = st.text_input("E-mail")
        phone = st.text_input("Telefone")
        message = st.text_area("Mensagem")
        submit_button = st.form_submit_button(label='Enviar')

        if submit_button:
            st.success(f"Obrigado {name}, sua mensagem foi enviada com sucesso!")

# Função para exibir a página sobre nós
def sobre_nos():
    st.title("Sobre Nós")
    st.write("Fundada há 7 anos no setor de TI, a Efetividade Tecnologia expandiu suas operações para energia solar em 2019, oferecendo soluções sustentáveis e de alta qualidade.")
    st.subheader("Missão, Visão e Valores")
    st.write("Nosso compromisso é com a inovação, sustentabilidade e atendimento personalizado.")
    st.subheader("Nossa Equipe")
    st.write("Conheça os profissionais por trás das nossas soluções de energia solar e TI.")

# Função para exibir o chatbot
def chatbot():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.subheader("Chatbot")
    user_input = st.text_input("Pergunte sobre Energia Solar")

    if user_input:
        st.session_state.messages.append({"message": user_input, "is_user": True})
        st.session_state.messages.append({"message": f"Para mais informações, entre em contato conosco pelo telefone (82)993022941. Podemos ajudar a solicitar um orçamento?", "is_user": False})

    for message in st.session_state.messages:
        st_message(message["message"], is_user=message["is_user"])

# Função principal para configurar a página e navegação
def main():
    st.set_page_config(page_title="Efetividade Tecnologia - Energia Solar", layout="wide")

    # Sidebar com menu de navegação
    menu = ["Home", "Nossos Serviços", "Manutenção e Monitoramento", "Energia por Assinatura", "Blog", "Contato", "Sobre Nós", "Chatbot"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Chama a função correspondente com base na escolha do menu
    if choice == "Home":
        home()
    elif choice == "Nossos Serviços":
        nossos_servicos()
    elif choice == "Manutenção e Monitoramento":
        manutencao_monitoramento()
    elif choice == "Energia por Assinatura":
        energia_por_assinatura()
    elif choice == "Blog":
        blog()
    elif choice == "Contato":
        contato()
    elif choice == "Sobre Nós":
        sobre_nos()
    elif choice == "Chatbot":
        chatbot()

if __name__ == "__main__":
    main()
