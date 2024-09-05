import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd

# Simulação de dados (tabela de preços)
data = {
    'Geracao_KWH_MES': ['400 KWH/mês', '500 KWH/mês', '600 KWH/mês', '700 KWH/mês', '800 KWH/mês'],
    'Valor_Kit': [11500, 12600, 15000, 16600, 17800],
    'Retorno_Investimento': [108380, 127260, 149160, 183200, 201980]
}

df = pd.DataFrame(data)

# Função para gerar PDF personalizado do orçamento
def gerar_orcamento_pdf(nome_cliente, telefone_cliente, kit_selecionado, valor_kit, retorno_investimento):
    pdf = FPDF()
    pdf.add_page()

    # Título do documento
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Orçamento Personalizado - Efetividade Tecnologia", ln=True, align="C")

    # Informações do cliente
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nome do Cliente: {nome_cliente}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Telefone: {telefone_cliente}", ln=True, align="L")

    # Detalhes do kit selecionado
    pdf.cell(200, 10, txt=f"Kit Selecionado: {kit_selecionado}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Valor do Kit: R$ {valor_kit:.2f}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Retorno Estimado (25 anos): R$ {retorno_investimento:.2f}", ln=True, align="L")

    # Salvar o PDF
    pdf_output = "/mnt/data/orcamento_personalizado.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Layout do site em Streamlit
st.set_page_config(page_title="Efetividade Tecnologia - Energia Solar", layout="centered")

# Título e Descrição
st.title("Efetividade Tecnologia - Orçamento de Energia Solar")
st.subheader("Escolha seu Kit e receba um orçamento personalizado")

# Formulário de captura de informações (slide-like form)
nome_cliente = st.text_input("Nome Completo")
telefone_cliente = st.text_input("Telefone")

# Seleção do Kit de energia solar
kit_opcoes = df['Geracao_KWH_MES'].tolist()
kit_selecionado = st.selectbox("Selecione o Kit de Energia Solar", kit_opcoes)

# Filtrar dados do kit selecionado
kit_info = df[df['Geracao_KWH_MES'] == kit_selecionado].iloc[0]
valor_kit = kit_info['Valor_Kit']
retorno_investimento = kit_info['Retorno_Investimento']

# Exibir gráficos e dados
if st.button("Gerar Orçamento"):
    st.write(f"**Kit Selecionado:** {kit_selecionado}")
    st.write(f"**Valor do Kit:** R$ {valor_kit:.2f}")
    st.write(f"**Retorno Estimado em 25 anos:** R$ {retorno_investimento:.2f}")

    # Gráfico de retorno do investimento
    fig, ax = plt.subplots()
    ax.bar(['Retorno'], [retorno_investimento], color='green')
    ax.set_ylabel('R$')
    ax.set_title(f'Retorno do Investimento - {kit_selecionado}')
    st.pyplot(fig)

    # Geração do PDF
    pdf_file = gerar_orcamento_pdf(nome_cliente, telefone_cliente, kit_selecionado, valor_kit, retorno_investimento)
    st.success("Orçamento gerado com sucesso!")
    st.download_button(label="Baixar Orçamento em PDF", data=open(pdf_file, "rb"), file_name="orcamento_efetividade.pdf")

# Links para Instagram e WhatsApp
st.markdown(f"[Instagram da empresa](https://www.instagram.com/efetividadetec)")
st.markdown(f"[Fale com o Vendedor no WhatsApp](https://wa.me/5582993022941)")
