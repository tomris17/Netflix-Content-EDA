import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Netflix Content EDA App", layout="centered")

st.title("Netflix Content Exploratory Data Analysis App")
st.write(
    "Bu uygulama, Netflix veri seti üzerinden içerik trendlerini, ülke dağılımlarını ve film/dizi oranlarını görselleştirir."
)

@st.cache_data
def load_data():
    return pd.read_csv("netflix1.csv")

try:
    df = load_data()
    st.subheader("Veri Seti On Izleme")
    st.dataframe(df.head())

    st.subheader("Gorsellestirme Paneli")
    chart_type = st.selectbox(
        "Grafik Turunu Seciniz",
        [
            "Film ve Dizi Sayilari Dagilimi",
            "En Çok İçerik Üreten 10 Ülke",
            "Yillara Gore Netflix İçerik Trendi (2000+)"
        ]
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    if chart_type == "Film ve Dizi Sayilari Dagilimi":
        ax = sns.countplot(
            x="type", data=df, palette=["cornflowerblue", "lightcoral"], ax=ax
        )
        ax.set_title("Distribution of Netflix Movies & TV Shows", fontsize=14, fontweight="bold")
        ax.set_xlabel("Type", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        for p in ax.patches:
            ax.annotate(
                f"{int(p.get_height())}",
                (p.get_x() + p.get_width() / 2.0, p.get_height() / 2),
                ha="center",
                va="center",
                color="white",
                fontweight="bold",
                fontsize=12,
            )
    elif chart_type == "En Çok İçerik Üreten 10 Ülke":
        top_countries = df["country"].value_counts().head(10)
        sns.barplot(
            x=top_countries.values,
            y=top_countries.index,
            palette="viridis",
            hue=top_countries.index,
            legend=False,
            ax=ax
        )
        ax.set_title("Top 10 Countries Producing Netflix Content", fontsize=14, fontweight="bold")
        ax.set_xlabel("Number of Titles", fontsize=12)
        ax.set_ylabel("Country", fontsize=12)
    elif chart_type == "Yillara Gore Netflix İçerik Trendi (2000+)":
        year_counts = (
            df[df["release_year"] >= 2000]["release_year"].value_counts().sort_index()
        )
        sns.lineplot(
            x=year_counts.index,
            y=year_counts.values,
            marker="o",
            color="darkblue",
            linewidth=2.5,
            ax=ax
        )
        ax.set_title("Trend of Netflix Releases Over the Years (2000+)", fontsize=14, fontweight="bold")
        ax.set_xlabel("Release Year", fontsize=12)
        ax.set_ylabel("Number of Releases", fontsize=12)
        plt.setp(ax.get_xticklabels(), rotation=45)

    st.pyplot(fig)
except Exception as e:
    st.error(f"Veri yuklenirken veya gorsellestirilirken bir hata olustu: {e}")