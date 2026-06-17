# 📊 Student Performance Prediction System

A complete **Machine Learning Regression Project** that predicts student exam scores using Streamlit, Scikit-learn, and interactive data visualization.

---

## 🎯 Project Overview

The Student Performance Prediction System is an end-to-end analytics application designed to help educators and analysts understand academic performance trends and forecast exam outcomes.

Key capabilities:
- **Real-time prediction engine** for student exam scores
- **Interactive analytics dashboard** with KPIs and charts
- **Modern purple gradient UI** for a professional business analytics experience
- **Transparent ML pipeline** with preprocessing, training, and evaluation
- **Portable deployment** with Streamlit

---

## 📊 Dataset Description

**Dataset file**: `Dataset/StudentPerformanceFactors.csv`

The dataset contains student records with both numeric and categorical attributes, including:
- **Numeric features**: study hours, attendance rate, previous exam scores, sleep hours, assignment completion, etc.
- **Categorical features**: gender, school type, internet access, parental education, family background, etc.
- **Target variable**: `Exam_Score` (0-100 scale)

This dataset supports regression modeling and educational performance analysis.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd student-performance-app
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If you only want the app dependencies, you can also install from `Model/requirements.txt`.

---

## ▶️ How to Run the Application

### 1. Train the model

```bash
cd Model
python train.py
```

This will generate the required artifacts:
- `model.pkl`
- `scaler.pkl`
- `label_encoders.pkl`
- `pipeline_info.pkl`

### 2. Launch the Streamlit app

```bash
cd Model
streamlit run app.py
```

Open the URL shown in the terminal, typically `http://localhost:8501`.

---

## 🧭 Application Pages

### Home
- Project overview
- KPI summary cards
- Dataset summary and navigation guide
- System purpose and technology stack

### Dashboard
- Dataset preview and summary statistics
- Interactive Plotly charts for exam score distribution
- Scatter comparisons against selected features
- Correlation matrix visualization

### Prediction
- User form for student feature input
- Score prediction using the trained Linear Regression model
- Visual gauge result display
- Grade interpretation and recommendation

### About
- Detailed project information
- Dataset explanation and methodology
- Technology stack and pipeline documentation
- Limitations and future improvement ideas

---

## 🛠️ Technologies Used

- Python 3.8+
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- Plotly
- Matplotlib
- Joblib

---

## 📁 Project Structure

```text
student-performance-app/
├── Dataset/
│   └── StudentPerformanceFactors.csv       # Training dataset
├── Model/
│   ├── app.py                              # Main Streamlit application
│   ├── train.py                            # Model training and artifact generation
│   ├── requirements.txt                    # Streamlit and ML dependencies
│   ├── model.pkl                           # Trained model artifact (generated)
│   ├── scaler.pkl                          # Feature scaler artifact (generated)
│   ├── label_encoders.pkl                  # Label encoders for categorical data (generated)
│   ├── pipeline_info.pkl                   # Training feature metadata (generated)
│   └── pages/
│       ├── Dashboard.py                    # Analytics dashboard page
│       ├── Prediction.py                   # Prediction UI page
│       └── About.py                        # Project info page
├── requirements.txt                        # Root package dependencies
└── README.md                               # Project documentation
```

---

## 📝 Screenshots

> Replace these with actual screenshots after running the app.

### Home Page

![Home Page](screenshots/home.png)

### Dashboard Page

![Dashboard Page](screenshots/dashboard.png)

### Prediction Page

![Prediction Page](screenshots/prediction.png)

### About Page

![About Page](screenshots/about.png)

---

## 💡 Notes

- Make sure the dataset file exists in `Dataset/StudentPerformanceFactors.csv` before training or launching the app.
- If the app fails to load, verify the Python environment and dependency installation.
- Run `python train.py` whenever the dataset changes or you want to refresh the model.

---

## 📬 Contribution

Contributions and improvements are welcome! You can extend this project by adding:
- more advanced regression models,
- feature engineering,
- model explainability (SHAP/LIME),
- API deployment,
- or a mobile-friendly interface.

- Model training and evaluation
- Persistent model storage

### 👥 User-Friendly Interface
- Intuitive form inputs
- Clear instructions and help text
- Error messages and guidance
- Professional formatting
- Beginner-friendly documentation

## 🔧 Configuration

### Modify Train-Test Split
Edit `train.py` line ~230:
```python
X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2)  # Change 0.2 to desired ratio
```

### Change Model Algorithm
Replace LinearRegression in `train.py`:
```python
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100)  # Alternative model
```

### Customize Theme Colors
Edit `app.py` and page files to modify gradient colors:
```css
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

## 📊 Example Output

### Training Results
```
MAE (Mean Absolute Error):  3.45
MSE (Mean Squared Error):   15.23
RMSE (Root Mean Squared Error): 3.90
R² Score: 0.8456
```

### Prediction
```
Predicted Exam Score: 78.50
Grade: B - Good
Interpretation: Good work! Keep it up.
```

## 🐛 Troubleshooting

### Dataset Not Found
- Ensure `StudentPerformanceFactors.csv` exists in `Dataset/` folder
- Check file path and spelling

### Model Files Missing
- Run `python train.py` to generate model artifacts
- Check `Model/` directory for `.pkl` files

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.8+)

### Port Already in Use
- Run on different port: `streamlit run app.py --server.port 8502`

### Slow Predictions
- This is normal for first prediction (model loading)
- Subsequent predictions are cached and fast

## 📚 Learning Resources

- **Scikit-learn Docs**: https://scikit-learn.org/stable/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Machine Learning Basics**: https://www.coursera.org/learn/machine-learning

## 🚀 Future Enhancements

Potential improvements for this system:
1. **Advanced Models**: Random Forest, Gradient Boosting, XGBoost
2. **Hyperparameter Tuning**: GridSearchCV, RandomizedSearchCV
3. **Feature Engineering**: Create new features from existing ones
4. **Cross-Validation**: K-fold validation for robust evaluation
5. **Ensemble Methods**: Combine multiple models
6. **Model Explainability**: SHAP values, LIME
7. **Real-time Updates**: Retrain with new data
8. **REST API**: Deploy as microservice
9. **Mobile App**: React Native or Flutter version
10. **Advanced Analytics**: Predict improvement paths

## 📄 License

This project is provided as-is for educational purposes.

## 👨‍💻 Development Notes

### Code Style
- PEP 8 compliant Python code
- Detailed comments throughout
- Type hints where applicable
- Docstrings for all functions
- Beginner-friendly variable names

### Testing
Run the following to verify setup:
```bash
# Check Python version
python --version

# Verify imports
python -c "import streamlit, pandas, numpy, sklearn"

# Test training
python Model/train.py

# Launch app
streamlit run Model/app.py
```

## 📞 Support

For questions or issues:
1. Check the About page for detailed documentation
2. Review code comments in relevant files
3. Verify all dependencies are installed
4. Ensure dataset file exists

---

**Built with ❤️ using Python, Scikit-learn, and Streamlit**

Last Updated: 2024-2025
