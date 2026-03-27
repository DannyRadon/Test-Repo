import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score



EMISSIONS_FACTOR = 0.52

def fe(aeso_clean):
    monthly = (
        aeso_clean.groupby(['year', 'month'], as_index=False)
        .agg({
            'total_generation__solar': 'sum',
            'maximum_capacity__solar': 'mean',
            'system_available__solar': 'mean',
            'pool_price': 'mean',
            'total_gen_all': 'sum',
            'emissions_avoided': 'sum'
        })
    )

    monthly['time'] = pd.to_datetime(
        monthly[['year', 'month']].assign(day=1)
    )
    monthly = monthly.sort_values('time').reset_index(drop=True)

    monthly['solar_generation_per_capacity'] = (
        monthly['total_generation__solar'] / monthly['maximum_capacity__solar']
    )

    monthly['solar_market_share'] = (
        monthly['total_generation__solar'] / monthly['total_gen_all']
    )

    target = 'solar_generation_per_capacity'

    monthly['time_index'] = np.arange(len(monthly))
    monthly['month_num'] = monthly['time'].dt.month

    for k in range(1, 5):
        monthly[f'sin_year_{k}'] = np.sin(2 * np.pi * k * monthly['month_num'] / 12)
        monthly[f'cos_year_{k}'] = np.cos(2 * np.pi * k * monthly['month_num'] / 12)

    monthly['availability_ratio'] = (
        monthly['system_available__solar'] / monthly['maximum_capacity__solar']
    )

    monthly['gen_per_cap_lag_1'] = monthly[target].shift(1)
    monthly['gen_per_cap_lag_12'] = monthly[target].shift(12)

    monthly['pool_price_roll_3'] = monthly['pool_price'].shift(1).rolling(3).mean()
    monthly['pool_price_roll_6'] = monthly['pool_price'].shift(1).rolling(6).mean()

    monthly = (
        monthly.replace([np.inf, -np.inf], np.nan)
        .dropna()
        .reset_index(drop=True)
    )

    return monthly


def get_features():
    return [
        "time_index",
        "sin_year_1", "cos_year_1",
        "sin_year_2", "cos_year_2",
        "sin_year_3", "cos_year_3",
        "sin_year_4", "cos_year_4",
        "system_available__solar",
        "availability_ratio",
        "pool_price",
        "pool_price_roll_3",
        "pool_price_roll_6",
        "gen_per_cap_lag_1",
        "gen_per_cap_lag_12",
    ]


def get_model():
    return XGBRegressor(
        max_depth=2,
        learning_rate=0.05,
        n_estimators=300,
        subsample=0.8,
        colsample_bytree=1.0,
        objective="reg:squarederror",
        random_state=42
    )


def calc_metrics(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return {
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "R2": float(r2_score(y_true, y_pred)),
        "MAPE": float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)
    }


def train_main_model(monthly):
    features = get_features()
    target = "solar_generation_per_capacity"

    test_size = int(np.ceil(len(monthly) * 0.20))
    train_df = monthly.iloc[:-test_size].copy()
    test_df = monthly.iloc[-test_size:].copy()

    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]

    model = get_model()
    model.fit(X_train, y_train)

    test_pred = model.predict(X_test)

    main_metrics = calc_metrics(y_test, test_pred)

    results = test_df[["time"]].copy()
    results["actual"] = y_test.values
    results["pred"] = test_pred
    results["maximum_capacity__solar"] = test_df["maximum_capacity__solar"].values
    results["total_gen_all"] = test_df["total_gen_all"].values
    results["emissions_avoided"] = test_df["emissions_avoided"].values

    results["actual_total_generation__solar"] = (
        results["actual"] * results["maximum_capacity__solar"]
    )
    results["pred_total_generation__solar"] = (
        results["pred"] * results["maximum_capacity__solar"]
    )

    results["actual_solar_market_share"] = (
        results["actual_total_generation__solar"] / results["total_gen_all"]
    )
    results["pred_solar_market_share"] = (
        results["pred_total_generation__solar"] / results["total_gen_all"]
    )

    results["actual_emissions_avoided"] = (
        results["actual_total_generation__solar"] * EMISSIONS_FACTOR
    )
    results["pred_emissions_avoided"] = (
        results["pred_total_generation__solar"] * EMISSIONS_FACTOR
    )

    converted_metrics = {
        "solar_generation_per_capacity": main_metrics,
        "total_generation__solar": calc_metrics(
            results["actual_total_generation__solar"],
            results["pred_total_generation__solar"]
        ),
        "solar_market_share": calc_metrics(
            results["actual_solar_market_share"],
            results["pred_solar_market_share"]
        ),
        "emissions_avoided": calc_metrics(
            results["actual_emissions_avoided"],
            results["pred_emissions_avoided"]
        )
    }

    feature_importance = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)

    return {
        "model": model,
        "train_df": train_df,
        "test_df": test_df,
        "results": results,
        "metrics": converted_metrics,
        "feature_importance": feature_importance,
        "monthly": monthly
    }


def forecast_60_months(monthly, model):
    features = get_features()
    forecast_horizon = 60

    cap = monthly["maximum_capacity__solar"].replace(0, np.nan).dropna()
    first_cap = cap.iloc[0]
    last_cap = cap.iloc[-1]
    n_periods = len(cap) - 1
    base_monthly_growth = (last_cap / first_cap) ** (1 / n_periods) - 1 if n_periods > 0 else 0

    scenario_growth = {
        "Conservative": 0.05 * base_monthly_growth,
        "Moderate": 0.10 * base_monthly_growth,
        "Aggressive": 0.20 * base_monthly_growth,
    }

    month_avg_total_gen = monthly.groupby("month")["total_gen_all"].mean().to_dict()
    month_avg_pool_price = monthly.groupby("month")["pool_price"].mean().to_dict()

    future_availability_ratio = monthly["availability_ratio"].tail(12).mean()
    if pd.isna(future_availability_ratio):
        future_availability_ratio = 1.0

    all_forecasts = []

    for scenario_name, growth in scenario_growth.items():
        temp = monthly.copy().reset_index(drop=True)
        forecast_rows = []

        for _ in range(forecast_horizon):
            next_time = temp["time"].max() + pd.offsets.MonthBegin(1)
            next_month = next_time.month

            prev_cap = temp["maximum_capacity__solar"].iloc[-1]
            next_cap = prev_cap * (1 + growth)
            next_available = next_cap * future_availability_ratio
            next_pool = month_avg_pool_price.get(next_month, temp["pool_price"].tail(12).mean())
            next_total_gen_all = month_avg_total_gen.get(next_month, temp["total_gen_all"].tail(12).mean())

            new_row = {
                "year": next_time.year,
                "month": next_time.month,
                "time": next_time,
                "total_generation__solar": np.nan,
                "maximum_capacity__solar": next_cap,
                "system_available__solar": next_available,
                "pool_price": next_pool,
                "total_gen_all": next_total_gen_all,
                "emissions_avoided": np.nan,
                "solar_generation_per_capacity": np.nan,
                "solar_market_share": np.nan,
            }

            temp = pd.concat([temp, pd.DataFrame([new_row])], ignore_index=True)

            # rebuild features on full temp df
            temp["time_index"] = np.arange(len(temp))
            temp["month_num"] = temp["time"].dt.month

            for k in range(1, 5):
                temp[f"sin_year_{k}"] = np.sin(2 * np.pi * k * temp["month_num"] / 12)
                temp[f"cos_year_{k}"] = np.cos(2 * np.pi * k * temp["month_num"] / 12)

            temp["availability_ratio"] = (
                temp["system_available__solar"] / temp["maximum_capacity__solar"]
            )

            target = "solar_generation_per_capacity"
            temp["gen_per_cap_lag_1"] = temp[target].shift(1)
            temp["gen_per_cap_lag_12"] = temp[target].shift(12)
            temp["pool_price_roll_3"] = temp["pool_price"].shift(1).rolling(3).mean()
            temp["pool_price_roll_6"] = temp["pool_price"].shift(1).rolling(6).mean()

            X_next = temp.iloc[[-1]][features]
            pred_intensity = max(model.predict(X_next)[0], 0)

            pred_generation = max(pred_intensity * next_cap, 0)
            pred_market_share = pred_generation / next_total_gen_all if next_total_gen_all != 0 else np.nan
            pred_emissions = pred_generation * EMISSIONS_FACTOR

            temp.loc[temp.index[-1], "solar_generation_per_capacity"] = pred_intensity
            temp.loc[temp.index[-1], "total_generation__solar"] = pred_generation
            temp.loc[temp.index[-1], "solar_market_share"] = pred_market_share
            temp.loc[temp.index[-1], "emissions_avoided"] = pred_emissions

            forecast_rows.append({
                "time": next_time,
                "scenario": scenario_name,
                "forecast_generation_per_capacity": pred_intensity,
                "forecast_total_generation__solar": pred_generation,
                "forecast_solar_market_share": pred_market_share,
                "forecast_emissions_avoided": pred_emissions,
            })

        all_forecasts.append(pd.DataFrame(forecast_rows))

    return pd.concat(all_forecasts, ignore_index=True)


def run_modeling_pipeline(aeso_clean: pd.DataFrame):
    monthly = fe(aeso_clean)
    trained = train_main_model(monthly)
    forecast_df = forecast_60_months(trained["monthly"], trained["model"])
    trained["forecast_df"] = forecast_df
    return trained