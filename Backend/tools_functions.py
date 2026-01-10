import numpy as np
import pandas as pd
import plotly as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression

def data_overview(df:pd.DataFrame) -> dict:
    """
    Extracts dataset overview information for EDA.
    Returns a JSON-serializable dictionary.
    """

    overview = {
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "memory_usage_mb": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2), 2
        )
    }

    return overview

def data_quality(df:pd.DataFrame) -> dict:
    """
    Performs data quality checks:
    - Missing values
    - Duplicate rows
    - Constant / near-constant columns

    Returns a JSON-serializable dictionary.
    """
    # low_variance_columns = []

    quality = {
        "missing_value" : df.isnull().sum(),
        "percentage_missing_data" : df.isnull().mean() * 100,
        "duplicated_rows" : df[df.duplicated()].shape[0],
        "constant_columns" : [col for col in df.columns if df[col].nunique()<=1]
    }
    return quality

def data_statistics(df:pd.DataFrame) -> dict:
    """
    Compute descriptive statistics for numerical columns, including skewness and kurtosis.
    (mean, std, quartiles, min, max)
    """
    df_num = df.select_dtypes(include="number")
    stat = df_num.describe().T
    stat["skewness"] = df_num.skew()
    stat["kurtosis"] = df_num.kurt()
    return stat.to_dict()

def get_important_numerical_columns(df, top_k=5):
    """
    Select top-k important numerical features using variance, skewness, kurtosis, and missing values.
    """
    num_df = df.select_dtypes(include="number")
    n = len(num_df)
    score = (
        num_df.var().rank(ascending=False) +
        num_df.skew().abs().rank(ascending=False) +
        num_df.kurt().abs().rank(ascending=False) +
        num_df.isnull().mean().rank(ascending=False)
    )
    id_like = num_df.nunique() / n > 0.9
    score = score[~id_like]
    return score.sort_values().head(top_k).index.tolist()


def data_categorical(df : pd.DataFrame, rare_threshold: float = 0.05) -> dict:
    """
    Analyze categorical features for cardinality, rare categories, and encoding recommendations.
    """
    cat_df = df.select_dtypes(include=["object", "category"]).columns
    result = {}
    for cat in cat_df :
        cardinality = {}
        unique = df[cat].value_counts(dropna=False)
        cardinality.update({cat : df[cat].nunique()})

        percentages = round((unique / len(df)) * 100, 2)
        rare_categories = percentages[percentages < (rare_threshold * 100)].index.tolist()

        if df[cat].nunique() <= 5:
            encoding = "One-Hot Encoding"
        elif df[cat].nunique() <= 20:
            encoding = "Target / Frequency Encoding"
        else:
            encoding = "Hashing / Embeddings (High Cardinality)"

        result[cat] = {
            "unique_values_in_column":unique,
            "Cardinality":cardinality,
            "rare_categories":rare_categories,
            "possible_encoding":encoding,
        }
    
    return result

def analyze_categorical_columns(df: pd.DataFrame,top_k: int = 5,rare_threshold: float = 0.05):
    """
    Rank categorical columns by importance using cardinality, rarity, and dominance metrics.
    """
    categorical_cols = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    results = []

    for col in categorical_cols:
        value_counts = df[col].value_counts(dropna=False)
        total = value_counts.sum()
        cardinality = len(value_counts)

        if cardinality < 2:
            continue
        rare_count = (value_counts / total < rare_threshold).sum()
        dominance = value_counts.iloc[0] / total
        score = (cardinality * 1.0 +rare_count * 2.0 -dominance * 3.0)

        results.append({
            "column": col,
            "cardinality": cardinality,
            "rare_categories": rare_count,
            "dominant_ratio": round(dominance, 3),
            "importance_score": round(score, 2),
            "value_counts": value_counts
        })

    results = sorted(results,key=lambda x: x["importance_score"],reverse=True)[:top_k]
    return results

def data_outlier(df : pd.DataFrame) -> tuple:
    """
    Outlier analysis function

    -calculate iqr
    - z scores
    - has outlier or not
    - return outlier report and columns with anomalies
    """
    df_num = df.select_dtypes(include="number")
    outlier_report = {}
    columns_with_anomalies = []

    for col in df_num.columns:
        series = df_num[col].dropna()
        if series.empty:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5*iqr
        upper = q3 + 1.5*iqr
        mask = (series < lower) | (series > upper)

        mean = series.mean()
        std = series.std()
        if std == 0:
            z_scores = pd.Series([0]*len(series), index=series.index)
        else:
            z_scores = ((series - mean) / std).abs()
        has_outliers = mask.sum() > 0

        outlier_report[col] = {
            "iqr_outliers": mask.sum(),
            "iqr_percent": round((mask.sum() / len(series)) * 100, 2),
            "zscore_outliers": z_scores,
            "has_outliers": has_outliers
        }

        if has_outliers:
            columns_with_anomalies.append(col)
        
    return outlier_report,columns_with_anomalies


def data_correlation(df: pd.DataFrame) -> dict:
    """
    Safe correlation + VIF analysis.
    Never produces NaNs.
    """
    df_num = df.select_dtypes(include="number").copy()
    df_num = df_num.loc[:, df_num.std(numeric_only=True) > 0]
    df_num = df_num.dropna(axis=1, how="all")

    if df_num.shape[1] < 2:
        return {
            "correlation_matrix": None,
            "high_correlation_features": [],
            "redundant_features": [],
            "VIF_factor": [],
            "note": "Not enough valid numeric columns for correlation analysis"
        }

    corr_matrix = df_num.corr().fillna(0)
    threshold = 0.8
    high_corr_features = []

    cols = corr_matrix.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) >= threshold:
                high_corr_features.append({
                    "feature_1": cols[i],
                    "feature_2": cols[j],
                    "correlation": round(float(corr_value), 3)
                })

    redundant_features = list(
        set(pair["feature_2"] for pair in high_corr_features)
    )
    vif_factor = []
    vif_df = df_num.dropna()

    if vif_df.shape[1] < 2 or vif_df.shape[0] <= vif_df.shape[1]:
        return [{"note": "VIF skipped (insufficient rows or columns)"}]

    X = vif_df.values.astype(float)

    for idx, col in enumerate(vif_df.columns):
        try:
            with np.errstate(divide='ignore', invalid='ignore'):
                vif_value = variance_inflation_factor(X, idx)
            if np.isnan(vif_value) or np.isinf(vif_value):
                vif_value = 0.0

        except Exception:
            vif_value = 0.0

        vif_factor.append({
            "feature": col,
            "vif": round(float(vif_value), 2),
            "status": (
                "Severe" if vif_value > 10 else
                "High" if vif_value > 5 else
                "Acceptable"
            )
        })

    return {
        "correlation_matrix": corr_matrix,
        "high_correlation_features": high_corr_features,
        "redundant_features": redundant_features,
        "VIF_factor": vif_factor
    }


def data_target_analysis(df: pd.DataFrame) -> dict:
    """
    Target column finding node
    Here we pass column name, datatype, unique values, missing percent of each column
    then return all the columns meta data in a dictionary format
    """
    metadata = []
    for col in df.columns:
        column_name = col
        data_type = df[col].dtype
        unique_values = df[col].nunique()
        missing_percent = round(df[col].isna().mean() * 100, 2)

        metadata.append({
            "column_name":column_name,
            "data_type":data_type,
            "unique_values":unique_values,
            "missing_percent":missing_percent,
        })
    return metadata

def make_mongo_safe(obj):
    if isinstance(obj, dict):
        return {k: make_mongo_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [make_mongo_safe(v) for v in obj]

    if isinstance(obj, tuple):
        return [make_mongo_safe(v) for v in obj]

    # Pandas
    if isinstance(obj, pd.Series):
        return obj.to_dict()

    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="records")

    # NumPy
    if isinstance(obj, (np.integer,)):
        return int(obj)

    if isinstance(obj, (np.floating,)):
        return float(obj)

    if isinstance(obj, (np.bool_,)):
        return bool(obj)

    # Everything else (str, int, float, bool, None)
    return obj