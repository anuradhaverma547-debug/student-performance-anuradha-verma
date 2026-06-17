"""Student Performance Prediction System - Model Training Script

This script handles the complete machine learning pipeline:
1. Load and explore the dataset
2. Preprocess data (handle categorical columns, scale features)
3. Split into train/test sets
4. Train a Linear Regression model
5. Evaluate with MAE, MSE, RMSE, and R² Score
6. Save the trained model for later use in the Streamlit app

Beginner-friendly with detailed comments throughout.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


# ============================================================================
# 1. UTILITY FUNCTIONS
# ============================================================================

def load_dataset(file_path: str) -> pd.DataFrame:
    """Load the CSV dataset into a pandas DataFrame.
    
    Args:
        file_path: Path to the CSV file.
        
    Returns:
        A pandas DataFrame containing the dataset.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at: {file_path}")
    
    df = pd.read_csv(file_path)
    print(f"✓ Dataset loaded successfully. Shape: {df.shape}")
    return df


def explore_dataset(df: pd.DataFrame):
    """Print basic info about the dataset to understand it better."""
    print("\n--- Dataset Exploration ---")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"\nColumn names and types:\n{df.dtypes}")
    print(f"\nFirst few rows:\n{df.head()}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nBasic statistics:\n{df.describe()}")


def handle_categorical_columns(df: pd.DataFrame, target_col: str = "Exam_Score") -> tuple:
    """Convert categorical columns to numeric using LabelEncoder.
    
    This function identifies non-numeric columns (except the target) and encodes them.
    The label encoders are returned so they can be used during prediction time.
    
    Args:
        df: The DataFrame to process.
        target_col: Name of the target column (excluded from encoding).
        
    Returns:
        A tuple containing:
        - The processed DataFrame with encoded categorical columns.
        - A dictionary mapping column names to their LabelEncoders.
    """
    df_processed = df.copy()
    label_encoders = {}
    
    # Find categorical columns (those with object dtype and not the target)
    categorical_cols = df_processed.select_dtypes(include=['object']).columns.tolist()
    
    if target_col in categorical_cols:
        categorical_cols.remove(target_col)
    
    print(f"\nFound {len(categorical_cols)} categorical columns: {categorical_cols}")
    
    # Encode each categorical column
    for col in categorical_cols:
        le = LabelEncoder()
        df_processed[col] = le.fit_transform(df_processed[col].astype(str))
        label_encoders[col] = le
        print(f"  Encoded '{col}' -> {len(le.classes_)} unique values")
    
    return df_processed, label_encoders


# ============================================================================
# 2. PREPROCESSING FUNCTIONS
# ============================================================================

def prepare_features_target(df: pd.DataFrame, target_col: str = "Exam_Score") -> tuple:
    """Separate features (X) and target (y) from the DataFrame.
    
    Args:
        df: The processed DataFrame.
        target_col: Name of the target column.
        
    Returns:
        A tuple (X, y) where X is features and y is the target.
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame.")
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    print(f"✓ Features shape: {X.shape}, Target shape: {y.shape}")
    return X, y


def split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, 
               random_state: int = 42) -> tuple:
    """Split the data into training and testing sets.
    
    Args:
        X: Feature matrix.
        y: Target vector.
        test_size: Proportion of data to use for testing (default 20%).
        random_state: Seed for reproducibility.
        
    Returns:
        A tuple (X_train, X_test, y_train, y_test).
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"✓ Data split: Train {X_train.shape[0]} samples, Test {X_test.shape[0]} samples")
    return X_train, X_test, y_train, y_test


def scale_features(X_train: pd.DataFrame, X_test: pd.DataFrame) -> tuple:
    """Standardize features using StandardScaler.
    
    Scaling ensures features are on a similar scale, which improves model performance.
    We fit the scaler on training data and apply it to test data.
    
    Args:
        X_train: Training features.
        X_test: Testing features.
        
    Returns:
        A tuple (X_train_scaled, X_test_scaled, scaler).
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("✓ Features scaled using StandardScaler")
    return X_train_scaled, X_test_scaled, scaler


# ============================================================================
# 3. MODEL TRAINING
# ============================================================================

def train_model(X_train: np.ndarray, y_train: pd.Series) -> LinearRegression:
    """Train a Linear Regression model on the training data.
    
    Linear Regression finds the best-fit line (or hyperplane) that predicts
    the target variable from the features.
    
    Args:
        X_train: Scaled training features (numpy array).
        y_train: Training target values.
        
    Returns:
        A trained LinearRegression model object.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    print("✓ Linear Regression model trained successfully")
    print(f"  Model coefficients: {len(model.coef_)} features")
    print(f"  Intercept: {model.intercept_:.4f}")
    
    return model


# ============================================================================
# 4. MODEL EVALUATION
# ============================================================================

def evaluate_model(model: LinearRegression, X_test: np.ndarray, 
                   y_test: pd.Series) -> dict:
    """Evaluate the model on the test set using multiple metrics.
    
    Metrics:
    - MAE (Mean Absolute Error): Average absolute difference between predicted and actual.
    - MSE (Mean Squared Error): Average squared difference. Penalizes larger errors.
    - RMSE (Root Mean Squared Error): Square root of MSE. In same units as target.
    - R² Score: Proportion of variance explained by the model (0-1, higher is better).
    
    Args:
        model: Trained model.
        X_test: Test features (numpy array).
        y_test: Test target values.
        
    Returns:
        A dictionary containing all evaluation metrics.
    """
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2_Score": r2
    }
    
    # Print results
    print("\n--- Model Performance Metrics ---")
    print(f"MAE (Mean Absolute Error):  {mae:.4f}")
    print(f"MSE (Mean Squared Error):   {mse:.4f}")
    print(f"RMSE (Root Mean Squared Error): {rmse:.4f}")
    print(f"R² Score: {r2:.4f}")
    
    return metrics


# ============================================================================
# 5. MODEL PERSISTENCE
# ============================================================================

def save_model(model: LinearRegression, scaler: StandardScaler, 
               label_encoders: dict, pipeline_info: dict, output_dir: str = "Model"):
    """Save the trained model, scaler, label encoders, and pipeline metadata to disk.
    
    These saved objects will be loaded by the Streamlit app to make predictions.
    
    Args:
        model: Trained LinearRegression model.
        scaler: Fitted StandardScaler.
        label_encoders: Dictionary of fitted LabelEncoders.
        pipeline_info: Metadata including feature names and feature groups.
        output_dir: Directory where to save the files.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    model_path = os.path.join(output_dir, "model.pkl")
    joblib.dump(model, model_path)
    print(f"✓ Model saved to {model_path}")
    
    scaler_path = os.path.join(output_dir, "scaler.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"✓ Scaler saved to {scaler_path}")
    
    encoders_path = os.path.join(output_dir, "label_encoders.pkl")
    joblib.dump(label_encoders, encoders_path)
    print(f"✓ Label encoders saved to {encoders_path}")
    
    pipeline_info_path = os.path.join(output_dir, "pipeline_info.pkl")
    joblib.dump(pipeline_info, pipeline_info_path)
    print(f"✓ Pipeline info saved to {pipeline_info_path}")


# ============================================================================
# 6. MAIN PIPELINE
# ============================================================================

def main():
    """Execute the complete machine learning pipeline."""
    print("=" * 70)
    print("STUDENT PERFORMANCE PREDICTION SYSTEM - MODEL TRAINING")
    print("=" * 70)
    
    # Determine dataset path (assumes script runs from project root or Model folder)
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent
    dataset_path = project_root / "Dataset" / "StudentPerformanceFactors.csv"
    
    # If file not found, also check relative path
    if not dataset_path.exists():
        dataset_path = Path("../Dataset/StudentPerformanceFactors.csv").resolve()
    
    # Step 1: Load and explore the dataset
    print("\n[Step 1/7] Loading dataset...")
    df = load_dataset(str(dataset_path))
    explore_dataset(df)
    
    # Step 2: Handle categorical columns
    print("\n[Step 2/7] Handling categorical columns...")
    df_processed, label_encoders = handle_categorical_columns(df, target_col="Exam_Score")
    
    # Step 3: Prepare features and target
    print("\n[Step 3/7] Preparing features and target...")
    X, y = prepare_features_target(df_processed, target_col="Exam_Score")
    
    feature_names = X.columns.tolist()
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = [col for col in feature_names if col in label_encoders]
    pipeline_info = {
        "feature_names": feature_names,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "target_column": "Exam_Score"
    }
    
    print(f"\nTraining feature names ({len(feature_names)}): {feature_names}")
    print(f"Numeric features ({len(numeric_features)}): {numeric_features}")
    print(f"Categorical features ({len(categorical_features)}): {categorical_features}")
    
    # Step 4: Split data into train/test
    print("\n[Step 4/7] Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)
    
    # Step 5: Scale features
    print("\n[Step 5/7] Scaling features...")
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    
    # Step 6: Train the model
    print("\n[Step 6/7] Training Linear Regression model...")
    model = train_model(X_train_scaled, y_train)
    
    # Step 7: Evaluate the model
    print("\n[Step 7/7] Evaluating model performance...")
    metrics = evaluate_model(model, X_test_scaled, y_test)
    
    # Step 8: Save the model and auxiliary objects
    print("\n[Step 8/8] Saving model artifacts...")
    save_model(model, scaler, label_encoders, pipeline_info, output_dir=str(current_dir))
    
    print("\n" + "=" * 70)
    print("✓ Training pipeline completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
