import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from streamlit_chat import message as st_message


# Função para calcular o retorno do investimento
def calcular_retorno_investimento(preco_inicial, economia_mensal, meses):
    retorno_investimento = [-preco_inicial + (economia_mensal * i) for i in range(meses + 1)]
    return retorno_investimento


# Função para gerar o gráfico de retorno do investimento
def gerar_grafico_retorno(df_kits, meses_durabilidade):
    plt.figure(figsize=(10, 5))
    for index, row in df_kits.iterrows():
        preco_inicial = row['Preço à vista (R$)']
        economia_mensal = (row['Painéis'] * row['Potência do Painel (W)'] * 5 * 30 * 0.80) / 1000  # Considerando custo de R$ 0,80/kWh
        retorno_investimento = calcular_retorno_investimento(preco_inicial, economia_mensal, meses_durabilidade)

        plt.plot(range(meses_durabilidade + 1), retorno_investimento, label=f"Kit {row['Kit (kWh)']} kWh")

        # Calculando a probabilidade de retorno positivo após 300 meses
        media = np.mean(retorno_investimento)
        desvio_padrao = np.std(retorno_investimento)
        probabilidade_retorno_positivo = 1 - norm.cdf(0, loc=media, scale=desvio_padrao)

        # Adicionando a probabilidade no gráfico
        plt.text(meses_durabilidade, retorno_investimento[-1], f"Prob. Retorno +: {probabilidade_retorno_positivo:.2%}", ha='left', va='center')

    plt.xlabel('Meses')
    plt.ylabel('Retorno do Investimento (R$)')
    plt.title('Retorno do Investimento dos Kits de Energia Solar')
    plt.legend()
    plt.grid(True)
    return plt


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


# Função para exibir a logo
def mostrar_logo():
    st.image("logo.png", width=200)  # Substitua "logo.png" pelo caminho da sua logo


# Configuração da página
st.set_page_config(page_title="Efetividade Tecnologia - Energia Solar", page_icon=":sunny:")


# Cabeçalho
st.title("Efetividade Tecnologia - Energia Solar e Soluções em TI")
mostrar_logo()  # Chamando a função para exibir a logo
st.markdown("Sua energia limpa e inteligente.")


# Seção Home
st.header("Gere sua própria energia e economize!")
st.markdown(
    "Com nossos sistemas de energia solar fotovoltaica, você reduz sua conta de luz, contribui para o meio ambiente e valoriza seu imóvel."
)


# Destaques de produtos/serviços (pode ser melhorado com imagens/carousel)
st.subheader("Nossos Destaques:")
st.markdown("- **Soluções Residenciais:** Kits de energia solar para casas de todos os tamanhos.")
st.markdown("- **Soluções Comerciais:** Sistemas fotovoltaicos para empresas e indústrias.")
st.markdown("- **Monitoramento Remoto:** Acompanhe a geração de energia do seu sistema em tempo real.")
st.markdown("- **Manutenção Preventiva:** Garanta o melhor desempenho do seu sistema com nossos planos de manutenção.")
st.markdown("- **Energia por Assinatura:** Tenha energia solar sem investimento inicial.")


# Botões Call to Action
col1, col2 = st.columns(2)
with col1:
    st.button("Solicitar Orçamento")
with col2:
    st.button("Consulta Técnica Gratuita")


# Chatbot
st.header("Converse com nosso especialista em energia solar:")
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.text_input("Digite sua mensagem:", key='input')

if user_input:
    st.session_state.past.append(user_input)
    st.session_state.generated.append(
        "Olá! Sou o especialista em energia solar da Efetividade Tecnologia. "
        "Em que posso ajudar?"
    )

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        st_message(st.session_state["generated"][i], key=str(i))
        st_message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


# ... (Restante das seções do site - Nossos Serviços, Manutenção e Monitoramento, Energia por Assinatura, Blog, Contato, Sobre Nós) ...


# Rodapé
st.markdown("---")
st.markdown("**Efetividade Tecnologia**")
st.markdown("Telefone: (82) 99302-2941 (WhatsApp)")
st.markdown("Email: contato@efetividadetecnologia.com.br")  # Substitua pelo email da empresa


# Gráfico de Retorno do Investimento
meses_durabilidade = 300
plt = gerar_grafico_retorno(df_kits, meses_durabilidade)
st.pyplot(plt)
