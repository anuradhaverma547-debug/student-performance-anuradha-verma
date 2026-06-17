"""Student Performance Prediction System - Dashboard page

This Streamlit page shows dataset KPIs, an overview table,
and interactive visualizations using Plotly and Matplotlib.

Beginner-friendly, well-commented code so you can follow along.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


def inject_custom_styles():
    """Inject dashboard styles for cards, layout, and sidebar."""
    custom_css = """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f8f7ff 0%, #ede8ff 50%, #ece3ff 100%);
    }
    .dashboard-hero {
        border-radius: 24px;
        padding: 2rem;
        background: linear-gradient(135deg, #6f42ff 0%, #7640d5 100%);
        color: white;
        box-shadow: 0 22px 60px rgba(79, 47, 186, 0.22);
        margin-bottom: 1.8rem;
    }
    .dashboard-hero h1 {
        margin: 0;
        font-size: 2.7rem;
    }
    .dashboard-hero p {
        color: rgba(255,255,255,0.88);
        font-size: 1.05rem;
        line-height: 1.8;
    }
    .dashboard-card {
        background: white;
        border-radius: 20px;
        padding: 1.6rem;
        box-shadow: 0 16px 40px rgba(99, 64, 196, 0.1);
        border: 1px solid rgba(128, 95, 255, 0.12);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        margin-bottom: 1.4rem;
    }
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 48px rgba(99, 64, 196, 0.16);
    }
    .kpi-card { padding: 22px; border-radius: 20px; color: white; min-height: 140px; }
    .kpi-1 { background: linear-gradient(135deg, #7c4dff 0%, #6320fd 100%); }
    .kpi-2 { background: linear-gradient(135deg, #5f25d5 0%, #3c1ec3 100%); }
    .kpi-3 { background: linear-gradient(135deg, #4d2ee8 0%, #2e20bb 100%); }
    .kpi-4 { background: linear-gradient(135deg, #6f52ff 0%, #5833bd 100%); }
    .kpi-card h4 { margin-bottom: 0.8rem; font-size: 1rem; color: rgba(255,255,255,0.9);} 
    .kpi-card h2 { margin: 0; font-size: 2.1rem; }
    .sidebar-card { background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02)); border-radius: 20px; padding: 1.2rem; margin-bottom: 1rem; border: 1px solid rgba(255,255,255,0.14); }
    .sidebar-card h3 { color: white; margin-bottom: 0.75rem; }
    .sidebar-card p { color: rgba(255,255,255,0.85); margin-bottom: 1rem; }
    .sidebar-card li { margin-bottom: 0.75rem; color: rgba(255,255,255,0.92); font-weight: 600; }
    .section-title { color: #2b2360; }
    .section-subtitle { color: #5f5a85; }
    @media (max-width: 768px) {
        .dashboard-hero { padding: 1.4rem; }
        .dashboard-card { padding: 1.2rem; }
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from CSV. Cached to speed up reloads in Streamlit.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A pandas DataFrame with the dataset.
    """
    df = pd.read_csv(file_path)
    return df


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Compute simple KPIs useful for the dashboard."""
    kpis = {}
    # Average and median of the target
    kpis["Average Score"] = df["Exam_Score"].mean()
    kpis["Median Score"] = df["Exam_Score"].median()
    # Basic pass-rate (example threshold: 50)
    kpis["Pass Rate (%)"] = (df["Exam_Score"] >= 50).mean() * 100
    # Number of records
    kpis["Records"] = len(df)
    return kpis


def kpi_cards(kpis: dict):
    """Display KPI cards in a horizontal layout with polished styling."""
    cols = st.columns(len(kpis), gap="large")

    for idx, (label, value) in enumerate(kpis.items()):
        with cols[idx]:
            st.markdown(
                f"""
                <div class='kpi-card kpi-{idx+1}'>
                    <h4>{label}</h4>
                    <h2>{value:,.2f}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )


def dataset_overview(df: pd.DataFrame):
    """Show a quick preview and descriptive stats of the dataset."""
    st.markdown(
        """
        <div class='dashboard-card'>
            <h3 class='section-title'>Dataset Overview</h3>
            <p class='section-subtitle'>Preview the first 10 records and summary statistics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(df.head(10), use_container_width=True)
    st.dataframe(df.describe().T, use_container_width=True)


def visualizations(df: pd.DataFrame):
    """Provide interactive plots for exploratory data analysis."""
    st.markdown(
        """
        <div class='dashboard-card'>
            <h3 class='section-title'>Interactive Visualizations</h3>
            <p class='section-subtitle'>Explore exam score trends using responsive charts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "Exam_Score" in numeric_cols:
        numeric_cols.remove("Exam_Score")
    num_choice = st.selectbox("Choose a numeric feature to compare with Exam Score:", [None] + numeric_cols)

    fig_hist = px.histogram(
        df,
        x="Exam_Score",
        nbins=25,
        title="Exam Score Distribution",
        color_discrete_sequence=["#7b2ff7"],
        template="plotly_white",
    )
    fig_hist.update_layout(margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_hist, use_container_width=True)

    if num_choice:
        fig_scatter = px.scatter(
            df,
            x=num_choice,
            y="Exam_Score",
            trendline="ols",
            title=f"Exam Score vs {num_choice}",
            color_discrete_sequence=["#6a11cb"],
            template="plotly_white",
        )
        fig_scatter.update_layout(margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    corr = df.select_dtypes(include=[np.number]).corr()
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Purples",
        title="Correlation Matrix",
    )
    fig_corr.update_layout(margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_corr, use_container_width=True)


def main():
    st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
    inject_custom_styles()

    with st.sidebar:
        st.markdown(
            """
            <div class='sidebar-card'>
                <h3>Analytics Menu</h3>
                <p>Navigate the performance dashboard.</p>
                <ul>
                    <li>🏠 Home</li>
                    <li>📊 Dashboard</li>
                    <li>🔮 Prediction</li>
                    <li>ℹ️ About</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class='dashboard-hero'>
            <h1>Student Performance Analytics</h1>
            <p>Visualize performance drivers and trends so you can make data-driven decisions faster.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Resolve dataset path relative to this file so the page is portable
    base_dir = Path(__file__).resolve().parents[2]
    data_path = base_dir / "Dataset" / "StudentPerformanceFactors.csv"

    try:
        df = load_data(str(data_path))
    except FileNotFoundError:
        st.error(f"Dataset not found at: {data_path}. Please make sure the CSV exists.")
        return

    # KPIs
    kpis = calculate_kpis(df)
    kpi_cards(kpis)

    # Dataset preview and stats
    dataset_overview(df)

    # Visualizations
    visualizations(df)


if __name__ == "__main__":
    main()
