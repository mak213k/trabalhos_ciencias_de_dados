import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title(" Dashboard - Licenciamento de Veículos")

df = pd.read_csv("licenciamento_frota.csv")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

st.subheader(" Base de dados")
st.write(df.head())


st.sidebar.header("Filtros")

municipios = st.sidebar.multiselect(
    "Selecione o município",
    df["municipio"].unique(),
    default=df["municipio"].unique()[:5]
)

categoria = st.sidebar.multiselect(
    "Categoria",
    df["categoria"].unique(),
    default=df["categoria"].unique()
)

df_filtrado = df[
    (df["municipio"].isin(municipios)) &
    (df["categoria"].isin(categoria))
]

st.subheader(" Total de veículos em atraso")
total = df_filtrado["quantidade_veiculos_com_licenciamento_atraso"].sum()
st.metric("Total", int(total))


st.subheader(" Veículos em atraso por município")

dados_municipio = df_filtrado.groupby("municipio")[
    "quantidade_veiculos_com_licenciamento_atraso"
].sum().sort_values(ascending=False)

st.bar_chart(dados_municipio)



st.subheader(" Por tipo de veículo")

fig, ax = plt.subplots()
sns.barplot(
    x="tipo_veiculo",
    y="quantidade_veiculos_com_licenciamento_atraso",
    data=df_filtrado,
    ax=ax
)

plt.xticks(rotation=45)
st.pyplot(fig)




st.subheader(" Distribuição por combustível")

dados_comb = df_filtrado.groupby("combustivel")[
    "quantidade_veiculos_com_licenciamento_atraso"
].sum()

st.bar_chart(dados_comb)

# streamlit run dashboard.py