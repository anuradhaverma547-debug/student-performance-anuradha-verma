"""Student Performance Prediction System - About Page

This page provides comprehensive information about the project,
including the dataset, methodology, features, and technical details.

Beginner-friendly code with detailed comments throughout.
"""

import streamlit as st
from pathlib import Path


def render_about_section():
    """Render the main about information."""
    st.title("ℹ️ About Student Performance Prediction System")
    
    st.markdown("""
    ## 🎯 Project Overview
    
    The **Student Performance Prediction System** is an end-to-end machine learning application
    designed to predict student exam scores based on various academic and personal factors.
    
    This system helps:
    - **Educators** understand which factors influence student success
    - **Students** get personalized score predictions based on their profile
    - **Institutions** identify at-risk students who need additional support
    """)


def render_dataset_info():
    """Display information about the dataset."""
    st.subheader("📊 Dataset")
    
    st.markdown("""
    ### File: `StudentPerformanceFactors.csv`
    
    The dataset contains multiple features that influence student exam performance:
    
    **Numeric Features:**
    - Study hours per week
    - Attendance rate (%)
    - Previous exam scores
    - Sleep hours per night
    - Number of assignments completed
    - And more...
    
    **Categorical Features:**
    - Gender (Male/Female)
    - School Type (Public/Private)
    - Family background
    - Internet access
    - Parental education level
    - And more...
    
    **Target Variable:**
    - `Exam_Score`: The final exam score (0-100) we're predicting
    
    ### Statistics
    - Total Records: Multiple student entries
    - Features: Mix of numeric and categorical data
    - No missing values (cleaned dataset)
    """)


def render_methodology():
    """Explain the ML methodology."""
    st.subheader("🔬 Machine Learning Methodology")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Data Preprocessing
        1. **Categorical Encoding**: Convert text fields to numbers using LabelEncoder
        2. **Feature Scaling**: Normalize features using StandardScaler
        3. **Train-Test Split**: 80% training, 20% testing (random seed: 42)
        
        ### Model Selection
        - **Algorithm**: Linear Regression
        - **Why Linear Regression?**
          - Simple and interpretable
          - Good baseline for regression tasks
          - Fast to train and predict
          - Clear coefficient interpretation
        """)
    
    with col2:
        st.markdown("""
        ### Model Training
        1. Load and preprocess the dataset
        2. Split into training and test sets
        3. Fit Linear Regression model on training data
        4. Evaluate on test data
        5. Save model artifacts for later use
        
        ### Evaluation Metrics
        - **MAE** (Mean Absolute Error): Average prediction error in points
        - **MSE** (Mean Squared Error): Penalizes larger errors more
        - **RMSE** (Root Mean Squared Error): Error in same units as target
        - **R² Score**: Percentage of variance explained (0-1 scale)
        """)


def render_pipeline():
    """Visualize the complete pipeline."""
    st.subheader("⚙️ Complete Pipeline")
    
    pipeline_text = """
    ```
    1. RAW DATA
       ↓
    2. LOAD DATASET (StudentPerformanceFactors.csv)
       ↓
    3. EXPLORE DATA (shape, types, missing values, statistics)
       ↓
    4. HANDLE CATEGORICAL COLUMNS (LabelEncoder)
       ↓
    5. PREPARE FEATURES & TARGET (X, y)
       ↓
    6. SPLIT DATA (80% train, 20% test)
       ↓
    7. SCALE FEATURES (StandardScaler)
       ↓
    8. TRAIN LINEAR REGRESSION MODEL
       ↓
    9. MAKE PREDICTIONS (on test set)
       ↓
    10. EVALUATE MODEL (MAE, MSE, RMSE, R²)
        ↓
    11. SAVE ARTIFACTS (model.pkl, scaler.pkl, label_encoders.pkl)
        ↓
    12. DEPLOY IN STREAMLIT APP
    ```
    """
    st.markdown(pipeline_text)


def render_technology_stack():
    """Display the technology stack used."""
    st.subheader("🛠️ Technology Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Backend & ML
        - **Python 3.8+**: Programming language
        - **Scikit-learn**: ML algorithms
        - **Pandas**: Data manipulation
        - **NumPy**: Numerical computing
        - **Joblib**: Model serialization
        """)
    
    with col2:
        st.markdown("""
        ### Frontend & Visualization
        - **Streamlit**: Web application framework
        - **Plotly**: Interactive charts
        - **Matplotlib**: Static visualizations
        - **Seaborn**: Statistical plotting
        """)
    
    with col3:
        st.markdown("""
        ### Project Structure
        - **train.py**: Training script
        - **app.py**: Main app entry point
        - **pages/Dashboard.py**: Data exploration
        - **pages/Prediction.py**: Score prediction
        - **pages/About.py**: This page
        """)


def render_how_to_use():
    """Guide on how to use the system."""
    st.subheader("🚀 How to Use This System")
    
    st.markdown("""
    ### Step 1: Train the Model
    Run the training script from the Model directory:
    ```bash
    python train.py
    ```
    This will:
    - Load the dataset
    - Preprocess the data
    - Train the Linear Regression model
    - Save model artifacts
    
    ### Step 2: Launch the Dashboard
    Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
    
    ### Step 3: Navigate the Pages
    - **Home**: Overview and quick statistics
    - **Dashboard**: Explore data with interactive visualizations
    - **Prediction**: Input student data and get score predictions
    - **About**: Learn about the system (you're here!)
    
    ### Step 4: Make Predictions
    1. Go to the Prediction page
    2. Fill in the student's information
    3. Click "Predict Exam Score"
    4. View the predicted score and interpretation
    """)


def render_model_coefficients():
    """Explain model coefficients and interpretability."""
    st.subheader("📈 Model Interpretability")
    
    st.markdown("""
    ### Understanding Coefficients
    
    Linear Regression creates an equation:
    ```
    Exam_Score = Intercept + (Coef₁ × Feature₁) + (Coef₂ × Feature₂) + ...
    ```
    
    **Positive Coefficient**: Feature increases → Score increases
    **Negative Coefficient**: Feature increases → Score decreases
    **Larger Coefficient**: Feature has more influence on the score
    
    ### Example Interpretation
    If the model shows:
    - Study Hours coefficient = 3.5 → Each extra study hour adds ~3.5 points
    - Attendance coefficient = 2.1 → Each 1% attendance increase adds ~2.1 points
    
    This helps identify which factors matter most for student success!
    """)


def render_limitations():
    """Discuss system limitations."""
    st.subheader("⚠️ Limitations & Assumptions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Limitations
        - **Linear Model**: Assumes linear relationships
        - **Historical Data**: Predictions based on past patterns
        - **Not Individual**: General predictions, not personalized counseling
        - **Training Data**: Accuracy depends on dataset quality
        - **Features Only**: Cannot account for external events
        """)
    
    with col2:
        st.markdown("""
        ### Assumptions
        - Features are independent variables
        - Linear relationship with target variable
        - No multicollinearity among features
        - Normal distribution of residuals
        - Constant variance of errors
        
        **Note**: These assumptions may not always hold perfectly,
        but the model still provides useful predictions in practice.
        """)


def render_future_improvements():
    """Suggest potential improvements."""
    st.subheader("🔮 Future Improvements")
    
    improvements = """
    Potential enhancements to this system:
    
    1. **Advanced Models**: Use Random Forest, Gradient Boosting, Neural Networks
    2. **Hyperparameter Tuning**: Find optimal model parameters
    3. **Feature Engineering**: Create new features from existing ones
    4. **Cross-Validation**: More robust model evaluation
    5. **Ensemble Methods**: Combine multiple models for better predictions
    6. **Explainability**: SHAP values, LIME for model interpretability
    7. **Real-time Learning**: Update model with new data
    8. **API Deployment**: REST API for external integrations
    9. **Mobile App**: Extend to mobile platforms
    10. **Feedback Loop**: Track prediction accuracy and improve over time
    """
    st.markdown(improvements)


def render_contact_footer():
    """Display contact and footer information."""
    st.divider()
    
    st.subheader("📞 Contact & Support")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Documentation
        - See README.md for setup instructions
        - Check code comments for implementation details
        - Review train.py for model training logic
        """)
    
    with col2:
        st.markdown("""
        ### Troubleshooting
        - Ensure dataset exists at `Dataset/StudentPerformanceFactors.csv`
        - Run `train.py` before using prediction features
        - Check Python version (3.8+) and dependencies
        """)
    
    with col3:
        st.markdown("""
        ### Resources
        - Scikit-learn: https://scikit-learn.org
        - Streamlit: https://streamlit.io
        - Pandas: https://pandas.pydata.org
        """)
    
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #718096; font-size: 12px; margin-top: 2rem;'>
        <p>Student Performance Prediction System | Machine Learning for Education | 2024-2025</p>
        <p>Built with ❤️ using Python, Scikit-learn, and Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """Main about page."""
    st.set_page_config(page_title="About - Student Performance Prediction", layout="wide")
    
    # Render all sections
    render_about_section()
    st.divider()
    
    render_dataset_info()
    st.divider()
    
    render_methodology()
    st.divider()
    
    render_pipeline()
    st.divider()
    
    render_technology_stack()
    st.divider()
    
    render_how_to_use()
    st.divider()
    
    render_model_coefficients()
    st.divider()
    
    render_limitations()
    st.divider()
    
    render_future_improvements()
    
    render_contact_footer()


if __name__ == "__main__":
    main()
