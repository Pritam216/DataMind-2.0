from langgraph.graph import StateGraph,START,END
from state import SummaryState
from main_nodes import Overview, quality, statistics, categorical_analysis, outlier, correlation, target_analysis, eda_insight_summary

graph = StateGraph(SummaryState)

graph.add_node("overview",Overview)
graph.add_node("quality",quality)
graph.add_node("stat",statistics)
graph.add_node("category",categorical_analysis)
graph.add_node("outlier",outlier)
graph.add_node("correlation",correlation)
graph.add_node("target_analysis",target_analysis)
graph.add_node("summary",eda_insight_summary)

graph.set_entry_point("overview")
graph.add_edge("overview","quality")
graph.add_edge("quality","stat")
graph.add_edge("stat","category")
graph.add_edge("category","outlier")
graph.add_edge("outlier","correlation")
graph.add_edge("correlation","target_analysis")
graph.add_edge("target_analysis","summary")
graph.add_edge("summary",END)

eda_workflow = graph.compile()

# initial_state = {
#     "data": pd.read_csv("data/drug200.csv"),
#     "graph_file_path": [],
#     "data_overview": {},
#     "data_quality_overview": {},
#     "data_stat_overview":{},
#     "categorical_analysis_overview":{},
#     "data_outlier_overview":[],
#     "data_correlation_overview":{},
#     "data_target_overview":{},
#     "eda_insight_summary":""
# }
# result = app.invoke(input=initial_state)
# for message_chunk, metadata in app.stream(
#     input=initial_state,
#     stream_mode="messages",  
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)
