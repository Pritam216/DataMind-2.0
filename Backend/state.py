from typing import TypedDict, List, Optional
import pandas as pd
from pydantic import BaseModel

class DataState(TypedDict):
    dataset_path: Optional[str]
    data: Optional[pd.DataFrame]

class SummaryState(DataState):
    graph_file_path: List[dict]
    data_overview: dict
    data_quality_overview: dict
    data_stat_overview : dict
    categorical_analysis_overview : dict
    data_outlier_overview : List[dict]
    data_correlation_overview: dict
    data_target_overview : dict
    eda_insight_summary : str

class ChatRequest(BaseModel):
    run_id: str
    message: str
