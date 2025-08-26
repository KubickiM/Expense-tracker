import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet


def prepare_dataframe(expenses, language):

    if not expenses:
        print(language["analysis_no_data"])
        return None

    df = pd.DataFrame(expenses)

    if "date" not in df.columns or "value" not in df.columns:
        print(language["analysis_no_data"])
        return None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    return df


def analyze_trend(expenses, language):

    df = prepare_dataframe(expenses, language)
    if df is None:
        return

    daily_expenses = df.groupby("date")["value"].sum().reset_index()

    plt.figure(figsize=(10, 5))
    plt.plot(daily_expenses["date"], daily_expenses["value"], marker="o", linestyle="-", linewidth=2)
    plt.title(language["trend_title"], fontsize=14)
    plt.xlabel(language["trend_x_label"])
    plt.ylabel(language["trend_y_label"])
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def analyze_seasonality(expenses, language):

    df = prepare_dataframe(expenses, language)
    if df is None:
        return

    df["weekday"] = df["date"].dt.day_name()
    df["month"] = df["date"].dt.strftime("%B")

    plt.figure(figsize=(10, 5))
    sns.barplot(x="weekday", y="value", data=df, estimator=sum, order=[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])
    plt.title(language["seasonality_title_weekday"])
    plt.ylabel(language["seasonality_y_label"])
    plt.xlabel(language["seasonality_x_weekday"])
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.barplot(x="month", y="value", data=df, estimator=sum,
                order=["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"])
    plt.title(language["seasonality_title_month"])
    plt.ylabel(language["seasonality_y_label"])
    plt.xlabel(language["seasonality_x_month"])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def forecast_expenses(expenses, language, days_ahead=30):
    df = prepare_dataframe(expenses, language)
    if df is None:
        return

    forecast_df = df.groupby("date")["value"].sum().reset_index()
    forecast_df = forecast_df.rename(columns={"date": "ds", "value": "y"})

    model = Prophet()
    model.fit(forecast_df)

    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)

    plt.figure(figsize=(12, 6))
    model.plot(forecast)
    plt.title(language["forecast_title"].format(days=days_ahead), fontsize=14)
    plt.xlabel(language["forecast_x_label"])
    plt.ylabel(language["forecast_y_label"])
    plt.grid(True)
    plt.show()