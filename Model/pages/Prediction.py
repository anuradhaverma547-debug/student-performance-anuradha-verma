"""Student Performance Prediction System - Prediction Page

This Streamlit page allows users to input student features and get
predictions for their exam scores using the trained Linear Regression model.

Features:
- User-friendly form for data input
- Real-time predictions
- Visual representation of predicted scores
- Model performance metrics display
- Beginner-friendly, well-commented code

Beginner-friendly code with detailed comments throughout.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import joblib
import plotly.graph_objects as go


# ============================================================================
# MODEL & DATA LOADING
# ============================================================================

@st.cache_resource
def load_model_artifacts(model_dir: str) -> tuple:
    """Load the trained model and preprocessing artifacts from disk.
    
    These objects are cached so they're only loaded once and reused
    across reruns, improving performance significantly.
    
    Args:
        model_dir: Directory containing model.pkl, scaler.pkl, and label_encoders.pkl
        
    Returns:
        A tuple (model, scaler, label_encoders, pipeline_info) or raises error if files not found.
    """
    try:
        model = joblib.load(Path(model_dir) / "model.pkl")
        scaler = joblib.load(Path(model_dir) / "scaler.pkl")
        label_encoders = joblib.load(Path(model_dir) / "label_encoders.pkl")
        pipeline_info = joblib.load(Path(model_dir) / "pipeline_info.pkl")
        return model, scaler, label_encoders, pipeline_info
    except FileNotFoundError as e:
        st.error(f"Model files not found: {e}. Please run train.py first.")
        return None, None, None, None


@st.cache_data
def load_training_data(file_path: str) -> pd.DataFrame:
    """Load the training dataset to understand feature ranges and types.
    
    This helps us know what kind of inputs users can provide.
    
    Args:
        file_path: Path to the CSV file.
        
    Returns:
        A pandas DataFrame with the dataset.
    """
    return pd.read_csv(file_path)


def get_model_dir() -> Path:
    """Get the Model directory path."""
    current_dir = Path(__file__).resolve().parent
    model_dir = current_dir.parent
    return model_dir


# ============================================================================
# INPUT FORM BUILDING
# ============================================================================

def build_input_form(df_train: pd.DataFrame, label_encoders: dict) -> pd.DataFrame:
    """Build an interactive form for users to input student features.
    
    Args:
        df_train: Training dataset (used to understand feature ranges).
        label_encoders: Dictionary of label encoders for categorical features.
        
    Returns:
        A pandas DataFrame with the user inputs (one row).
    """
    st.subheader("📋 Student Information")
    
    # Create a dictionary to store user inputs
    user_data = {}
    
    # Get all numeric columns from training data (excluding Exam_Score)
    numeric_cols = df_train.select_dtypes(include=[np.number]).columns.tolist()
    if "Exam_Score" in numeric_cols:
        numeric_cols.remove("Exam_Score")
    
    # Get all categorical columns
    categorical_cols = list(label_encoders.keys())
    
    # Split form into columns for better layout
    col1, col2 = st.columns(2)
    cols = [col1, col2]
    col_idx = 0
    
    # Create input fields for numeric features
    st.write("**Numeric Features:**")
    for col in numeric_cols:
        with cols[col_idx % 2]:
            min_val = float(df_train[col].min())
            max_val = float(df_train[col].max())
            mean_val = float(df_train[col].mean())
            
            user_data[col] = st.number_input(
                label=col,
                min_value=min_val,
                max_value=max_val,
                value=mean_val,
                step=0.1,
                help=f"Range: {min_val:.2f} to {max_val:.2f}"
            )
            col_idx += 1
    
    # Create input fields for categorical features
    if categorical_cols:
        st.write("**Categorical Features:**")
        col_idx = 0
        for col in categorical_cols:
            with cols[col_idx % 2]:
                encoder = label_encoders[col]
                categories = encoder.classes_
                selected_category = st.selectbox(
                    label=col,
                    options=categories,
                    help=f"Available options: {', '.join(map(str, categories))}"
                )
                # Encode the selected category
                user_data[col] = encoder.transform([selected_category])[0]
                col_idx += 1
    
    # Convert to DataFrame (1 row)
    user_df = pd.DataFrame([user_data])
    
    return user_df


# ============================================================================
# PREDICTION & VISUALIZATION
# ============================================================================

def make_prediction(model, scaler, user_df: pd.DataFrame, pipeline_info: dict) -> float:
    """Use the trained model to predict the exam score.
    
    Args:
        model: Trained LinearRegression model.
        scaler: Fitted StandardScaler for feature normalization.
        user_df: DataFrame with user input features (1 row).
        pipeline_info: Dictionary containing feature names and metadata.
        
    Returns:
        The predicted exam score (float).
    """
    training_feature_names = pipeline_info["feature_names"]
    
    # Ensure all training features exist in the input DataFrame
    for col in training_feature_names:
        if col not in user_df.columns:
            user_df[col] = 0
    
    # Use the training feature order exactly for prediction
    user_df = user_df[training_feature_names]
    
    # Scale the user input using the same scaler as training
    user_scaled = scaler.transform(user_df)
    
    # Make prediction
    prediction = model.predict(user_scaled)[0]
    
    # Clamp prediction to reasonable range (0-100 for exam scores)
    prediction = np.clip(prediction, 0, 100)
    
    return prediction


def display_prediction_result(predicted_score: float):
    """Display the prediction in an attractive, professional manner.
    
    Args:
        predicted_score: The predicted exam score.
    """
    st.subheader("🎯 Prediction Result")
    
    # Create a gauge chart to visualize the score
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=predicted_score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Predicted Exam Score"},
        delta={"reference": 50, "suffix": " vs Average"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 40], "color": "#ff6b6b"},     # Red - Fail
                {"range": [40, 60], "color": "#ffa94d"},    # Orange - Pass
                {"range": [60, 80], "color": "#74c0fc"},    # Light Blue - Good
                {"range": [80, 100], "color": "#51cf66"},   # Green - Excellent
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 90,
            },
        },
    ))
    fig.update_layout(height=500, font={"size": 14})
    st.plotly_chart(fig, use_container_width=True)
    
    # Display score in a highlighted box with interpretation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Predicted Score",
            value=f"{predicted_score:.2f}",
            delta="out of 100"
        )
    
    with col2:
        if predicted_score >= 80:
            grade = "A - Excellent"
            color = "green"
        elif predicted_score >= 60:
            grade = "B - Good"
            color = "blue"
        elif predicted_score >= 40:
            grade = "C - Average"
            color = "orange"
        else:
            grade = "F - Fail"
            color = "red"
        
        st.markdown(f"<h3 style='color: {color};'>{grade}</h3>", unsafe_allow_html=True)
    
    with col3:
        # Interpretation
        if predicted_score >= 80:
            interpretation = "Outstanding performance!"
        elif predicted_score >= 60:
            interpretation = "Good work! Keep it up."
        elif predicted_score >= 40:
            interpretation = "Average. Room for improvement."
        else:
            interpretation = "Below expected. Focus on studies."
        
        st.info(f"💡 {interpretation}")


def display_model_info():
    """Display information about the model and its performance."""
    st.subheader("📊 Model Information")
    
    info_cols = st.columns(3)
    
    with info_cols[0]:
        st.metric(
            label="Model Type",
            value="Linear Regression"
        )
    
    with info_cols[1]:
        st.metric(
            label="Training Status",
            value="✓ Ready"
        )
    
    with info_cols[2]:
        st.metric(
            label="Last Updated",
            value="See train.py"
        )
    
    with st.expander("ℹ️ How the model works"):
        st.markdown("""
        **Linear Regression Model**
        
        This model learns the relationship between student features and exam scores
        from historical training data. It creates a linear equation that estimates
        how each feature influences the final exam score.
        
        **Features Used:**
        - Numeric features (study hours, attendance, previous scores, etc.)
        - Categorical features (school type, gender, family background, etc.)
        
        **How predictions are made:**
        1. User provides their student information
        2. Categorical inputs are encoded to numbers
        3. All features are normalized using StandardScaler
        4. The trained model applies its learned coefficients
        5. A score is predicted (0-100 range)
        """)


# ============================================================================
# PAGE STYLING
# ============================================================================

def inject_css():
    """Inject custom CSS for a polished purple dashboard appearance."""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #f4f4ff 0%, #e9e3ff 50%, #e4d8ff 100%);
    }
    .page-title {
        color: #2b1a52;
        margin-bottom: 0.25rem;
    }
    .section-card {
        background: white;
        border-radius: 22px;
        padding: 1.6rem;
        box-shadow: 0 18px 50px rgba(105, 71, 210, 0.12);
        border: 1px solid rgba(123, 77, 255, 0.14);
        margin-bottom: 1.5rem;
    }
    .form-card {
        background: linear-gradient(135deg, #ffffff 0%, #f9f7ff 100%);
        border-radius: 22px;
        padding: 1.4rem;
        box-shadow: 0 14px 40px rgba(99, 72, 199, 0.08);
        border: 1px solid rgba(120, 95, 255, 0.1);
        margin-bottom: 1.5rem;
    }
    .button-primary > button {
        background: linear-gradient(135deg, #6e3cff 0%, #3b1bd2 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.85rem 1.6rem !important;
        font-weight: 700;
        box-shadow: 0 12px 35px rgba(84, 45, 217, 0.2) !important;
    }
    .button-primary > button:hover {
        transform: translateY(-1px);
    }
    .sidebar-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.04));
        border-radius: 20px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.14);
    }
    .sidebar-card h3 {
        color: white;
        margin-bottom: 0.65rem;
    }
    .sidebar-card p {
        color: rgba(255,255,255,0.82);
        margin: 0;
    }
    .sidebar-card ul {
        list-style: none;
        padding-left: 0;
        margin-top: 1rem;
    }
    .sidebar-card li {
        margin-bottom: 0.75rem;
        color: rgba(255,255,255,0.92);
        font-weight: 600;
    }
    @media (max-width: 768px) {
        .section-card, .form-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN PAGE
# ============================================================================

def main():
    """Main prediction page."""
    st.set_page_config(page_title="Student Performance Prediction", layout="wide")
    inject_css()
    st.markdown(
        """
        <div class='section-card'>
            <div style='display:flex; flex-wrap:wrap; gap:1rem; justify-content:space-between;'>
                <div style='max-width: 760px;'>
                    <h1 class='page-title'>🔮 Predict Student Exam Score</h1>
                    <p style='color:#4c4b70; font-size:1rem; line-height:1.75;'>
                        Enter student details and get a professional exam score forecast with
                        interactive analytics and easy-to-read result summaries.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Sidebar navigation card
    with st.sidebar:
        st.markdown(
            """
            <div class='sidebar-card'>
                <h3>Navigation</h3>
                <p>Quick access to the analytics experience</p>
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
    
    # Get model directory and load artifacts
    model_dir = get_model_dir()
    model, scaler, label_encoders, pipeline_info = load_model_artifacts(str(model_dir))
    
    if model is None or scaler is None or label_encoders is None or pipeline_info is None:
        st.error("Could not load model artifacts. Please ensure train.py has been run successfully.")
        return
    
    # Load training data to understand features
    dataset_path = model_dir.parent / "Dataset" / "StudentPerformanceFactors.csv"
    
    if not dataset_path.exists():
        st.error(f"Dataset not found at {dataset_path}")
        return
    
    df_train = load_training_data(str(dataset_path))
    
    st.markdown(
        """
        <div class='section-card'>
            <h3>Student Input</h3>
            <p style='color:#5b5b82;'>Use the form below to provide student details for prediction.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Build input form
    user_df = build_input_form(df_train, label_encoders)
    
    st.divider()
    
    # Prediction button
    if st.button("🚀 Predict Exam Score", key="predict_button", use_container_width=True):
        try:
            # Make prediction
            predicted_score = make_prediction(model, scaler, user_df, pipeline_info)
            
            # Display results
            display_prediction_result(predicted_score)
            
            st.success("✅ Prediction generated successfully!")
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
            st.write("Please check your inputs and try again.")
    
    st.divider()
    
    # Model information
    display_model_info()


if __name__ == "__main__":
    main()
