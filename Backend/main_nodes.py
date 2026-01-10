from Backend.models import llm_cohere,llm_google,llm_groq

from Backend.state import SummaryState
from Backend.tools_functions import data_overview,data_quality,data_statistics,get_important_numerical_columns, data_categorical, analyze_categorical_columns, data_outlier, data_correlation, data_target_analysis
from Backend.prompt import target_identify_prompt,eda_insight_summary_prompt
from Backend.storage_graphs import save_plotly_figure

import json 
import re
import pandas as pd
import plotly.express as px

def Overview(state:SummaryState):
    """
    Compute high-level dataset overview including shape, data types, and memory usage.
    """
    print("Analyzing overall data !!\n")
    if state.get("data") is None:
        df = pd.read_csv(state["dataset_path"])
        state["data"] = df
    else:
        df = state["data"]
    data = df
    overview = data_overview(data)
    return {
        "data_overview":overview,
    }

def quality(state:SummaryState):
    """
    Assess data quality by checking missing values, duplicates, and generate missing value heatmap if needed.
    """
    print("Analyzing the quality of the data !!\n")
    data = state["data"]
    quality = data_quality(data)
    heatmap_path = None
    if quality["missing_value"].sum() > 0:
        heatmap_df = data.isnull().astype(int)

        fig = px.imshow(
            heatmap_df.T,
            color_continuous_scale="Blues",
            title="Missing Value Heatmap",
            aspect="auto"
        )

        heatmap_path = save_plotly_figure(
            fig,
            plot_name="missing_value_heatmap"
        )

    state["graph_file_path"].append({"data_quality":heatmap_path})
    return {
        "data_quality_overview":quality,
    }

def statistics(state:SummaryState):
    """
    Generate numerical statistics and visualize key numerical features using boxplots and histograms.
    """
    print("Analyzing the statistics of the data !!\n")
    data = state["data"]
    box_path =[]
    hist_path=[]
    stat = data_statistics(data)
    important_cols = get_important_numerical_columns(data, top_k=5)
    for col in important_cols:
        try:
            fig_box = px.box(data,y=col,title=f"Box Plot - {col}")
            boxplot_path = save_plotly_figure(fig_box,plot_name=f"boxplot_{col}")
            box_path.append(boxplot_path)
        except Exception:
            pass

        try:
            fig_hist = px.histogram(data,x=col,nbins=30,title=f"Histogram - {col}")
            histogram_path = save_plotly_figure(fig_hist,plot_name=f"histogram_{col}")
            hist_path.append(histogram_path)
        except Exception:
            pass

    state["graph_file_path"].append({"data_statistics_boxplot":box_path})
    state["graph_file_path"].append({"data_statistics_histogram":hist_path})
    return{
        "data_stat_overview" : stat,
    }

def categorical_analysis(state : SummaryState) -> dict:
    """
    Analyze categorical features for distribution, cardinality, encoding strategy, and generate count plots.
    """
    print("Analyzing the categorical features !!\n")
    data = state["data"]
    result = data_categorical(data)
    analyzed = analyze_categorical_columns(data)
    bar_path = []
    for item in analyzed:
        col = item["column"]
        value_counts = item["value_counts"]

        plot_df = value_counts.reset_index()
        plot_df.columns = [col, "count"]

        fig = px.bar(
            plot_df,
            x=col,
            y="count",
            title=f"Category Distribution - {col}"
        )
        path = save_plotly_figure(fig,plot_name=f"count_plot_{col}")
        bar_path.append(path)

    state["graph_file_path"].append({"categorical_analysis":bar_path})
    return{
        "categorical_analysis_overview" : result,
    }

def outlier (state:SummaryState) -> dict:
    """
    Detect numerical outliers using IQR and visualize anomalous features with box plots.
    """
    print("Analyzing the outliers in the data !!\n")
    df = state["data"]
    outlier_data,anomaly_columns = data_outlier(df)
    outlier_path = []
    for col in anomaly_columns:
        fig = px.box(
            df,
            y=col,
            title=f"Outlier Box Plot - {col}"
        )
        path = save_plotly_figure(fig,plot_name=f"outlier_box_plot_{col}")
        outlier_path.append(path)

    state["graph_file_path"].append({"data_outlier_plot":outlier_path})
    return{
        "data_outlier_overview" : [outlier_data,anomaly_columns],
    }

def correlation(state:SummaryState)->dict:
    """
    Analyze numerical feature relationships using correlation matrix and VIF to detect multicollinearity.
    """
    print("Analyzing the correlation among the columns in the data !!\n")
    df = state["data"]
    corr_data = data_correlation(df)
    fig = px.imshow(
        corr_data["correlation_matrix"],
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Correlation Heatmap"
    )
    path = save_plotly_figure(fig,plot_name=f"corr_heatmap")
    state["graph_file_path"].append({"data_correlation":path})

    return{
        "data_correlation_overview" : corr_data,
    }

def target_analysis(state: SummaryState) -> dict:
    """
    Identify the most suitable target column using LLM reasoning and visualize its distribution.
    """
    print("Analyzing the target node in the data !!\n")
    df = state["data"]

    column_metadata = data_target_analysis(df)

    prompt_text = target_identify_prompt.format(
        column_metadata=column_metadata
    )

    raw = llm_google.invoke(prompt_text)
    clean_text = re.sub(r"```json|```", "", raw.content).strip()
    response = json.loads(clean_text)

    col = response["target_column"]
    task_type = response["task_type"]

    if task_type == "classification":
        fig = px.bar(
            df[col].value_counts(),
            title=f"Target Class Distribution - {col}"
        )
    else:
        fig = px.histogram(
            df, x=col, nbins=30,
            title=f"Target Distribution - {col}"
        )

    path = save_plotly_figure(fig, "target_distribution")
    state["graph_file_path"].append({"data_targer_analysis":path})

    return {"data_target_overview": response}

def eda_insight_summary(state: SummaryState) -> dict:
    """
    Generate a comprehensive, human-readable EDA insight summary using all prior analysis outputs.
    """
    print("Generating summary of the overall analysis !!")
    # print(state["graph_file_path"],"\n\n")
    prompt = eda_insight_summary_prompt.format(
        data_overview=state["data_overview"],
        data_quality=state["data_quality_overview"],
        numerical_stats=state["data_stat_overview"],
        categorical_analysis=state["categorical_analysis_overview"],
        outlier_analysis=state["data_outlier_overview"],
        correlation_analysis=state["data_correlation_overview"],
        target_analysis=state["data_target_overview"],
        visual_outputs = state["graph_file_path"],
    )

    response = llm_google.invoke(prompt)

    return {
        "eda_insight_summary": response.content
    }