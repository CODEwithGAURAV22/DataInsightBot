import sqlite3
import os
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor


# ============================================================
# LOAD SALES DATA
# ============================================================

def load_sales_data():

    base_path = os.path.dirname(
        os.path.abspath(__file__)
    )

    database_path = os.path.join(
        base_path,
        "database",
        "company.db"
    )

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        sale_date,
        revenue
    FROM sales
    ORDER BY sale_date
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return df


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data():

    df = load_sales_data()

    if df.empty:
        raise ValueError("No sales data found.")

    # Convert date column
    df["sale_date"] = pd.to_datetime(
        df["sale_date"]
    )

    # Convert revenue to numeric
    df["revenue"] = pd.to_numeric(
        df["revenue"],
        errors="coerce"
    )

    # Remove invalid values
    df = df.dropna(
        subset=["sale_date", "revenue"]
    )

    # Sort by date
    df = df.sort_values(
        "sale_date"
    )

    return df


# ============================================================
# CREATE FEATURES
# ============================================================

def create_features(df):

    data = df.copy()

    data["day"] = data["sale_date"].dt.day

    data["month"] = data["sale_date"].dt.month

    data["year"] = data["sale_date"].dt.year

    data["day_of_week"] = (
        data["sale_date"].dt.dayofweek
    )

    return data


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model():

    df = prepare_data()

    data = create_features(df)

    features = [
        "day",
        "month",
        "year",
        "day_of_week"
    ]

    X = data[features]

    y = data["revenue"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X,
        y
    )

    return model, data


# ============================================================
# PREDICT FUTURE SALES
# ============================================================

def predict_future_sales(
    days=30
):

    model, data = train_model()

    last_date = data["sale_date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=days,
        freq="D"
    )

    future_data = pd.DataFrame(
        {
            "sale_date": future_dates
        }
    )

    future_data["day"] = (
        future_data["sale_date"].dt.day
    )

    future_data["month"] = (
        future_data["sale_date"].dt.month
    )

    future_data["year"] = (
        future_data["sale_date"].dt.year
    )

    future_data["day_of_week"] = (
        future_data["sale_date"].dt.dayofweek
    )

    features = [
        "day",
        "month",
        "year",
        "day_of_week"
    ]

    future_data["predicted_revenue"] = model.predict(
        future_data[features]
    )

    return future_data[
        [
            "sale_date",
            "predicted_revenue"
        ]
    ]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("Testing ML Prediction")
    print("=" * 50)

    data = prepare_data()

    print("\nHistorical Sales Data:")
    print(data.head())

    predictions = predict_future_sales(
        days=30
    )

    print("\nFuture Sales Prediction:")
    print(predictions)

    print("\nML prediction completed successfully!")