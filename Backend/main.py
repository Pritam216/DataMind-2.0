# from graph import eda_workflow, initial_state
# from mongo import store_eda_data
# from prompt import mongo_prompt
# from models import llm_groq
# import uuid 
# import time

# final_state = eda_workflow.invoke(initial_state)
# print(final_state["eda_insight_summary"])


# mongo_doc = {
#     "dataset_overview": final_state["data_overview"],
#     "data_quality": final_state["data_quality_overview"],
#     "numerical_statistics": final_state["data_stat_overview"],
#     "categorical_analysis": final_state["categorical_analysis_overview"],
#     "outlier_analysis": final_state["data_outlier_overview"],
#     "correlation_analysis": final_state["data_correlation_overview"],
#     "target_analysis": final_state["data_target_overview"],
#     "EDA_summary": final_state["eda_insight_summary"],
#     "visual_outputs": final_state["graph_file_path"],
# }

# formated_prompt = mongo_prompt.format_prompt(mongo_doc = mongo_doc)
# result = llm_groq.invoke(formated_prompt)

# document = {
#     "run_id": f"eda_{uuid.uuid4().hex[:10]}",
#     "created_at": time.time(),

#     "data_overview":result.content,
#     "insight_summary": final_state["eda_insight_summary"],
# }

# doc_id = store_eda_data(document)
# print("Stored EDA run:", doc_id)