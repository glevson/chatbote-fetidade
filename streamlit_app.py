import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from streamlit_chat import message as st_message
from fpdf import FPDF
import base64


# Função para calcular o retorno do investimento
def calcular_retorno_investimento(preco_inicial, economia_mensal, meses):
    retorno_investimento = [-preco_inicial + (economia_mensal * i) for i in range(meses + 1)]
    return retorno_investimento


# Função para gerar o gráfico de retorno do investimento
def gerar_grafico_retorno(df_kits, meses_durabilidade, kit_selecionado):
    plt.figure(figsize=(10, 5))

    # Filtrar dados do kit selecionado
    kit_info = df_kits[df_kits['Kit (kWh)'] == kit_selecionado].iloc[0]
    preco_inicial = kit_info['Preço à vista (R$)']
    economia_mensal = (kit_info['Painéis'] * kit_info['Potência do Painel (W)'] * 5 * 30 * 0.80) / 1000  # Considerando custo de R$ 0,80/kWh
    retorno_investimento = calcular_retorno_investimento(preco_inicial, economia_mensal, meses_durabilidade)

    plt.plot(range(meses_durabilidade + 1), retorno_investimento, label=f"Kit {kit_selecionado} kWh")

    # Calculando a probabilidade de retorno positivo após 300 meses
    media = np.mean(retorno_investimento)
    desvio_padrao = np.std(retorno_investimento)
    probabilidade_retorno_positivo = 1 - norm.cdf(0, loc=media, scale=desvio_padrao)

    # Adicionando a probabilidade no gráfico
    plt.text(meses_durabilidade, retorno_investimento[-1], f"Prob. Retorno +: {probabilidade_retorno_positivo:.2%}", ha='left', va='center')

    plt.xlabel('Meses')
    plt.ylabel('Retorno do Investimento (R$)')
    plt.title(f'Retorno do Investimento - Kit {kit_selecionado} kWh')
    plt.legend()
    plt.grid(True)
    return plt


# Função para gerar PDF do orçamento personalizado
def gerar_orcamento_pdf(nome, telefone, kit_selecionado, valor_kit, retorno_investimento):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Orçamento Personalizado - Efetividade Tecnologia", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Nome: {nome}", ln=True)
    pdf.cell(200, 10, f"Telefone: {telefone}", ln=True)
    pdf.cell(200, 10, f"Kit Selecionado: {kit_selecionado} kWh", ln=True)
    pdf.cell(200, 10, f"Valor do Kit: R$ {valor_kit:.2f}", ln=True)
    pdf.cell(200, 10, f"Retorno Estimado (25 anos): R$ {retorno_investimento:.2f}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, "Obrigado por solicitar um orçamento. Entraremos em contato em breve!", ln=True)

    # Converte o PDF para base64 para download no Streamlit
    pdf_output = pdf.output(dest='S').encode('latin1')
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="orcamento_personalizado.pdf">Baixar PDF</a>'
    return href


# Dados dos kits de energia solar
dados_kits = {
    'Kit (kWh)': [400, 500, 600, 700, 800, 1000, 2000, 4000],
    'Inversor (kW)': [3, 3, 5, 5, 5, 6, 10, 20],
    'Painéis': [6, 7, 8, 10, 11, 14, 28, 56],
    'Potência do Painel (W)': [555, 555, 570, 555, 555, 555, 555, 555],
    'Preço à vista (R$)': [11500, 12600, 15000, 16600, 17800, 22000, 40000, 75000],
    'Parcela 60x (R$)': [394.55, 422.79, 497.41, 547.15, 584.46, 715.04, 1355.93, 2541.67],
    'Parcela 72x (R$)': [367.00, 391.79, 460.93, 507.03, 541.60, 662.60, 1256.94, 2354.17]
}
df_kits = pd.DataFrame(dados_kits)

# Função para chamar o chatbot
def chatbot():
    st.subheader("Chatbot Inteligente")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Digite sua mensagem:")

    if user_input:
        # Adiciona a mensagem do usuário na sessão
        st.session_state.messages.append({"message": user_input, "is_user": True})

        # Obtém a resposta do chatbot
        bot_response = (
            "Obrigado por entrar em contato! "
            "Para solicitar um orçamento personalizado, por favor, preencha o formulário na seção 'Orçamento Personalizado'. "
            "Ou se preferir, ligue para (82) 99302-2941."
        )
        st.session_state.messages.append({"message": bot_response, "is_user": False})

    # Exibe as mensagens na tela
    for message in st.session_state.messages:
        if message["is_user"]:
            st.write(f"Você: {message['message']}")
        else:
            st.write(f"Chatbot: {message['message']}")


# Função para exibir ícones e layout dinâmico
def display_icons():
    st.markdown(
        """
    <style>
    .icon {
        font-size: 50px;
        color: #ff4b4b;
        padding: 10px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="text-align: center;">
        <span class="icon">💡</span><span class="icon">🔧</span><span class="icon">📊</span><span class="icon">⚡</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.write("### Nossos Serviços:")
    st.write("- 💡 **Consultoria**: Avaliação de viabilidade e projetos personalizados.")
    st.write("- 🔧 **Instalação**: Sistemas residenciais e comerciais de energia solar.")
    st.write("- 📊 **Monitoramento**: Manutenção e monitoramento remoto para eficiência.")
    st.write("- ⚡ **Energia por Assinatura**: Alternativa para quem deseja economia sem instalação própria.")


# Função para exibir o formulário de orçamento em etapas
def form_slides():
    st.subheader("Solicite seu Orçamento Personalizado")

    # Slide 1 - Coleta do nome
    if "step" not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        st.session_state.nome = st.text_input("Digite seu nome:")
        if st.session_state.nome:
            if st.button("Próximo"):
                st.session_state.step = 2

    # Slide 2 - Coleta do telefone
    elif st.session_state.step == 2:
        st.session_state.telefone = st.text_input("Digite seu telefone:")
        if st.session_state.telefone:
            if st.button("Próximo"):
                st.session_state.step = 3

    # Slide 3 - Seleção do Kit
    elif st.session_state.step == 3:
        st.session_state.kit_selecionado = st.selectbox(
            "Escolha o Kit de Energia Solar:",
            df_kits['Kit (kWh)'].tolist()
        )
        if st.button("Gerar Orçamento"):
            st.session_state.step = 4

    # Slide final - Gerar PDF e Gráfico
    if st.session_state.step == 4:
        kit_info = df_kits[df_kits['Kit (kWh)'] == st.session_state.kit_selecionado].iloc[0]
        valor_kit = kit_info['Preço à vista (R$)']
        retorno_investimento = calcular_retorno_investimento(valor_kit, (kit_info['Painéis'] * kit_info['Potência do Painel (W)'] * 5 * 30 * 0.80) / 1000, 300)[-1]

        st.success("Orçamento gerado com sucesso!")

        # Exibe o gráfico de retorno do investimento
        meses_durabilidade = 300
        plt = gerar_grafico_retorno(df_kits, meses_durabilidade, st.session_state.kit_selecionado)
        st.pyplot(plt)

        # Gera o link para download do PDF
        pdf_link = gerar_orcamento_pdf(st.session_state.nome, st.session_state.telefone, st.session_state.kit_selecionado, valor_kit, retorno_investimento)
        st.markdown(pdf_link, unsafe_allow_html=True)

# Função para exibir a logo
def mostrar_logo():
    st.image("logo-efetividade.png", width=200)  # Substitua "logo.png" pelo caminho da sua log
    
  
# Função principal do site
def main():
    
    # Função para exibir a logo
    mostrar_logo()
    # Redimensiona a logo (ajuste o tamanho conforme necessário)
    logo.thumbnail((100, 100), Image.Resampling.LANCZOS)
    # Exibe a logo alinhada à esquerda com fundo transparente
    st.markdown(
        f'<div style="display: flex; align-items: center;"><img src="data:image/png;base64,{base64.b64encode(logo.tobytes()).decode()}" style="width: 100px; height: auto;"></div>',
        unsafe_allow_html=True,
    )
    
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
        st.write(
            "Entre em contato conosco pelo telefone (82) 99302-2941 ou pelo e-mail contato@efetividade.com.br."
        )

        # Links para Instagram e WhatsApp
        st.markdown(
            f"[Instagram da empresa](https://www.instagram.com/efetividadetec)"
        )
        st.markdown(
            f"[Fale com o Vendedor no WhatsApp](https://wa.me/5582993022941)"
        )


# Executa a aplicação
if __name__ == "__main__":
    main()
