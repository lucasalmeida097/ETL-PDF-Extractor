import streamlit as st
import pandas as pd
import altair as alt
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine


env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

st.set_page_config(page_title="Financial Dashboard", layout="wide")


@st.cache_resource
def load_data():
    try:
        db_url = (
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/"
            f"{os.getenv('DB_NAME')}"
        )
        engine = create_engine(db_url)
        query = """
        SELECT
            n_nota,
            data_de_pregao,
            qted,
            mercadoria,
            txop,
            tx_corretagem,
            cotacao,
            movimentacao,
            cv
        FROM gold_invoices;
        """
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()


df = load_data()
df["data_de_pregao"] = pd.to_datetime(df["data_de_pregao"]).dt.date


st.sidebar.header("Filters")
with st.sidebar:
    mercadoria_selecionada = st.multiselect(
        "Merchandise:",
        options=df["mercadoria"].unique(),
        default=df["mercadoria"].unique(),
    )
    data_range = st.date_input(
        "Date Range:",
        value=[df["data_de_pregao"].min(), df["data_de_pregao"].max()],
        min_value=df["data_de_pregao"].min(),
        max_value=df["data_de_pregao"].max(),
    )


df_filtered = df[
    (df["mercadoria"].isin(mercadoria_selecionada))
    & (df["data_de_pregao"].between(data_range[0], data_range[1]))
]


st.title("📊 Financial Dashboard - Gold Fatura")


st.subheader("🔢 General Indicators")
total_mov = df_filtered["movimentacao"].sum()
total_qted = df_filtered["qted"].sum()

col1, col2 = st.columns(2)
col1.metric("💰 Total Movement", f"R${total_mov:,.2f}")
col2.metric("📦 Total Quantity", f"{total_qted:,}")


tab1, tab2 = st.tabs(["📈 Charts", "📋 Filtered Table"])

with tab1:
    st.subheader("📦 Quantity by Merchandise")
    qted_chart = (
        alt.Chart(df_filtered)
        .mark_bar()
        .encode(
            x=alt.X("mercadoria:N", title="Merchandise"),
            y=alt.Y("sum(qted):Q", title="Total Quantity"),
            color="mercadoria:N",
            tooltip=["mercadoria:N", "sum(qted):Q"],
        )
        .properties(width="container")
    )
    st.altair_chart(qted_chart, use_container_width=True)

    st.subheader("📉 Movement Over Time")
    mov_chart = (
        alt.Chart(df_filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("data_de_pregao:T", title="Date"),
            y=alt.Y("sum(movimentacao):Q", title="Movement"),
            color="mercadoria:N",
            tooltip=["data_de_pregao:T", "mercadoria:N", "sum(movimentacao):Q"],
        )
        .properties(width="container")
    )
    st.altair_chart(mov_chart, use_container_width=True)

with tab2:
    st.subheader("📄 Filtered Data")
    st.dataframe(df_filtered, use_container_width=True)
