"""Student Performance Prediction System - Main Streamlit App

This is the entry point for the Student Performance Prediction dashboard.
It provides:
- A modern, professional interface with purple gradient theme
- Navigation to Dashboard, Prediction, and About pages
- Home page with key information and statistics

The app is built with Streamlit and uses a multi-page structure:
- app.py (this file): Main entry point
- pages/Dashboard.py: Data exploration and visualizations
- pages/Prediction.py: Make predictions on new data
- pages/About.py: Information about the project

Beginner-friendly code with detailed comments throughout.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


# ============================================================================
# PAGE CONFIGURATION & THEME
# ============================================================================

def set_page_config():
    """Configure Streamlit page settings with custom theme and layout."""
    st.set_page_config(
        page_title="Student Performance Prediction",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# Custom CSS for purple gradient theme and styling
def inject_custom_css():
    """Inject custom CSS for purple gradient theme and card styling."""
    custom_css = """
    <style>
    :root {
        color-scheme: light;
    }
    .stApp {
        background: linear-gradient(180deg, #f4f5ff 0%, #e1defe 45%, #d6c8ff 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3b0764 0%, #5a2d91 45%, #7c46e0 100%);
        color: #f8f8ff;
        padding-top: 1.5rem;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        padding-left: 0.5rem;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h1 {
        color: #ffffff;
    }
    .sidebar-nav {
        padding: 1rem 0.5rem;
        color: #e9e9ff;
    }
    .sidebar-item {
        padding: 10px 14px;
        border-radius: 12px;
        margin-bottom: 8px;
        transition: background 0.25s ease, transform 0.25s ease;
        color: #f8f8ff;
    }
    .sidebar-item:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(3px);
    }
    .sidebar-link {
        color: #f8f8ff;
        text-decoration: none;
    }
    .hero-banner {
        border-radius: 28px;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(122, 90, 255, 0.95), rgba(73, 41, 255, 0.95));
        color: white;
        box-shadow: 0 18px 60px rgba(64, 42, 157, 0.24);
        margin-bottom: 2rem;
    }
    .hero-banner h1 {
        color: white;
        margin-bottom: 0.5rem;
    }
    .hero-banner p {
        color: rgba(255, 255, 255, 0.88);
        font-size: 1.05rem;
        line-height: 1.7;
    }
    .dashboard-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 16px 40px rgba(112, 97, 255, 0.12);
        border: 1px solid rgba(115, 89, 255, 0.18);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        margin-bottom: 1.25rem;
    }
    .dashboard-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 52px rgba(112, 97, 255, 0.18);
    }
    .metric-card {
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(135deg, #7b4bff 0%, #5e2dfd 100%);
        color: white;
        box-shadow: 0 16px 36px rgba(117, 80, 255, 0.22);
        min-height: 125px;
    }
    .metric-card h4 {
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
    }
    .metric-card h2 {
        margin: 0;
        font-size: 2.2rem;
        letter-spacing: 0.02em;
    }
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f4f1ff 100%);
        border-radius: 20px;
        padding: 1.4rem;
        box-shadow: 0 10px 30px rgba(90, 50, 170, 0.08);
        border: 1px solid rgba(120, 100, 255, 0.1);
        min-height: 220px;
        margin-bottom: 1rem;
    }
    .feature-card h4 {
        margin: 0 0 0.75rem 0;
        color: #2d2d5b;
    }
    .feature-card p {
        color: #525174;
        line-height: 1.7;
    }
    .section-heading {
        color: #2b2b5f;
    }
    .section-subtitle {
        color: #535275;
    }
    @media (max-width: 768px) {
        .hero-banner {
            padding: 1.5rem;
        }
        .metric-card {
            min-height: 120px;
        }
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data
def load_dataset(file_path: str) -> pd.DataFrame:
    """Load the student performance dataset. Cached for performance.
    
    Args:
        file_path: Path to the CSV file.
        
    Returns:
        A pandas DataFrame with the dataset, or None if not found.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return None


def get_dataset_path() -> Path:
    """Determine the dataset file path relative to the app location.
    
    Returns:
        A Path object to the dataset CSV file.
    """
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent
    dataset_path = project_root / "Dataset" / "StudentPerformanceFactors.csv"
    
    if not dataset_path.exists():
        dataset_path = Path("../Dataset/StudentPerformanceFactors.csv").resolve()
    
    return dataset_path


# ============================================================================
# HOME PAGE COMPONENTS
# ============================================================================

def render_header():
    """Render the main header with title and subtitle."""
    st.markdown(
        """
        <div class='hero-banner'>
            <div style='display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1.5rem;'>
                <div style='max-width: 720px;'>
                    <h1>Student Performance Prediction Analytics</h1>
                    <p>
                        Turn student data into actionable academic insights with a modern
                        predictive analytics dashboard designed for educators and decision-makers.
                    </p>
                </div>
                <div style='display: grid; gap: 0.75rem;'>
                    <div style='background: rgba(255,255,255,0.12); padding: 1rem 1.2rem; border-radius: 18px;'>
                        <strong style='font-size: 0.95rem;'>Dashboard</strong><br>
                        Explore performance metrics and trends
                    </div>
                    <div style='background: rgba(255,255,255,0.12); padding: 1rem 1.2rem; border-radius: 18px;'>
                        <strong style='font-size: 0.95rem;'>Prediction</strong><br>
                        Estimate exam scores for new students
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_quick_stats(df: pd.DataFrame):
    """Display quick statistics about the dataset."""
    if df is None:
        st.warning("Dataset not loaded. Please check if the file exists.")
        return
    
    st.subheader("📈 Key Performance Indicators")
    
    cols = st.columns(4, gap="large")
    metrics = [
        ("Average Score", f"{df['Exam_Score'].mean():.2f}", "Performance"),
        ("Highest Score", f"{df['Exam_Score'].max():.2f}", "Top result"),
        ("Lowest Score", f"{df['Exam_Score'].min():.2f}", "Lowest result"),
        ("Total Records", f"{len(df)}", "Student entries"),
    ]
    
    for col, metric in zip(cols, metrics):
        label, value, subtitle = metric
        with col:
            st.markdown(
                f"""
                <div class='metric-card'>
                    <h4>{label}</h4>
                    <h2>{value}</h2>
                    <p style='margin-top: 0.75rem; color: rgba(255,255,255,0.85);'>{subtitle}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_about_section():
    """Render information about the system."""
    st.subheader("ℹ️ About This System")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown(
            """
            <div class='dashboard-card'>
                <h3>Purpose</h3>
                <p>
                    This system uses <strong>Machine Learning</strong> to predict student exam scores
                    based on academic and personal features. It gives educators a clear, data-driven view
                    of student performance drivers.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class='dashboard-card'>
                <h3>Insights</h3>
                <ul style='margin: 0; padding-left: 1.2rem; color: #4b4b7b;'>
                    <li>Interactive analytics and KPI tracking</li>
                    <li>Predictive modeling with real-time inputs</li>
                    <li>Beautiful visualizations for faster decision-making</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_navigation_guide():
    """Show how to navigate between pages."""
    st.subheader("🗺️ Navigation Guide")
    
    nav_text = """
    Use the **sidebar** on the left to navigate between pages:
    
    | Page | Description |
    |------|-------------|
    | 🏠 **Home** | You are here! Quick overview and statistics |
    | 📊 **Dashboard** | Interactive data exploration and visualizations |
    | 🔮 **Prediction** | Predict exam scores for new students |
    | ℹ️ **About** | Detailed information about this project |
    """
    st.markdown(nav_text)


def render_sidebar_navigation():
    """Render a polished sidebar navigation card with icons."""
    with st.sidebar:
        st.markdown(
            """
            <div class='dashboard-card' style='background: rgba(255,255,255,0.08); padding: 1.2rem;'>
                <h3 style='color:#ffffff; margin-bottom: 0.75rem;'>Navigation</h3>
                <p style='color: rgba(255,255,255,0.82); margin-bottom: 1rem;'>Use this menu to move between pages</p>
                <ul style='list-style: none; padding-left: 0; margin: 0;'>
                    <li style='margin-bottom: 0.8rem; color: #f0f0ff;'>🏠 <strong>Home</strong></li>
                    <li style='margin-bottom: 0.8rem; color: #f0f0ff;'>📊 <strong>Dashboard</strong></li>
                    <li style='margin-bottom: 0.8rem; color: #f0f0ff;'>🔮 <strong>Prediction</strong></li>
                    <li style='margin-bottom: 0.8rem; color: #f0f0ff;'>ℹ️ <strong>About</strong></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_how_it_works():
    """Explain the ML model and how it works."""
    st.subheader("⚙️ How It Works")
    
    steps = """
    The prediction system follows this process:
    
    1. **Data Collection**: Gathers student data with various features
    2. **Preprocessing**: Cleans data, encodes categorical variables, scales features
    3. **Model Training**: Uses Linear Regression to learn patterns from historical data
    4. **Validation**: Tests the model on unseen data to ensure accuracy
    5. **Prediction**: Makes predictions for new students using the trained model
    
    ### Performance Metrics
    - **MAE** (Mean Absolute Error): Average prediction error
    - **R² Score**: How well the model explains the variance in scores
    """
    st.markdown(steps)


def render_footer():
    """Render a professional footer."""
    footer_html = f"""
    <hr style='margin-top: 3rem; border: none; border-top: 1px solid #e2e8f0;'>
    <div style='text-align: center; padding-top: 1rem; color: #718096; font-size: 14px;'>
        <p>Student Performance Prediction System | Built with Streamlit & Machine Learning | {datetime.now().year}</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application entry point."""
    # Configure page
    set_page_config()
    inject_custom_css()
    render_sidebar_navigation()
    
    # Load dataset
    dataset_path = get_dataset_path()
    df = load_dataset(str(dataset_path))
    
    # Render home page
    render_header()
    
    if df is not None:
        render_quick_stats(df)
    else:
        st.error(f"⚠️ Could not load dataset from {dataset_path}. Please ensure the file exists.")
    
    # About and navigation sections
    st.divider()
    render_about_section()
    
    st.divider()
    render_navigation_guide()
    
    st.divider()
    render_how_it_works()
    
    render_footer()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
