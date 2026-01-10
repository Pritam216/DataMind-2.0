import os
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional,List

from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
collection = client[os.environ["DB_NAME"]][os.environ["COLLECTION_NAME"]]

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

    # NumPy scalars
    if isinstance(obj, (np.integer,)):
        return int(obj)

    if isinstance(obj, (np.floating,)):
        return float(obj)

    if isinstance(obj, (np.bool_,)):
        return bool(obj)

    return obj


def store_eda_data(data: Dict[str, Any]) -> str:
    """
    Store EDA overview + summary in MongoDB
    Returns inserted document ID
    """
    safe_data = make_mongo_safe(data)
    result = collection.insert_one(safe_data)
    return str(result.inserted_id)

def fetch_eda_data(run_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch stored EDA data using document ID
    """

    return collection.find_one(
        {"run_id": run_id},
        {"llm_overview": 1, "eda_summary":1}
    )

def delete_all_data(run_id : str):
    doc = collection.update_one({"run_id": run_id},{"$unset": {"llm_overview": "", "eda_summary": ""}})
    return {
        "success": True,
        "run_id": run_id,
        "matched": doc.matched_count,
        "modified": doc.modified_count
    }