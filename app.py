from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi import Body,Response, Cookie
from fastapi.responses import JSONResponse
import os, shutil, uuid, time
import pandas as pd
import io

from Backend.state import ChatRequest
from Backend.graph import eda_workflow
from Backend.mongo import store_eda_data, delete_all_data
from Backend.storage_graphs import delete_all_visual_outputs
from Backend.prompt import mongo_prompt
from Backend.models import llm_groq
from Backend.chat_nodes import chat_with_data
# from Backend.session_store import set_session

app = FastAPI(title="DataMind EDA API", version="2.0")

@app.post("/run-eda")
async def run_eda(file: UploadFile = File(...),response: Response = None):

    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        run_id = f"eda_{uuid.uuid4().hex[:10]}"
        # session_id = f"session_{uuid.uuid4().hex[:10]}"
        # set_session(session_id, run_id)
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        initial_state = {
            "data": df,

            "graph_file_path": [],
            "data_overview": {},
            "data_quality_overview": {},
            "data_stat_overview": {},
            "categorical_analysis_overview": {},
            "data_outlier_overview": [],
            "data_correlation_overview": {},
            "data_target_overview": {},
            "eda_insight_summary": ""
        }

        final_state = eda_workflow.invoke(initial_state)

        mongo_doc = {
            "dataset_overview": final_state["data_overview"],
            "data_quality": final_state["data_quality_overview"],
            "numerical_statistics": final_state["data_stat_overview"],
            "categorical_analysis": final_state["categorical_analysis_overview"],
            "outlier_analysis": final_state["data_outlier_overview"],
            "correlation_analysis": final_state["data_correlation_overview"],
            "target_analysis": final_state["data_target_overview"],
            "EDA_summary": final_state["eda_insight_summary"],
            "visual_outputs": final_state["graph_file_path"],
        }

        prompt = mongo_prompt.format_prompt(mongo_doc=mongo_doc)
        llm_response = llm_groq.invoke(prompt)

        document = {
            "run_id": run_id,
            "created_at": time.time(),
            "original_filename": file.filename,
            "llm_overview": llm_response.content,
            "eda_summary": final_state["eda_insight_summary"],
            "visual_outputs": final_state["graph_file_path"],
        }

        mongo_id = store_eda_data(document)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "run_id": run_id,
                "mongo_id": mongo_id,
                "summary": final_state["eda_insight_summary"],
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat_endpoint(payload: ChatRequest):
    try:
        response = chat_with_data(
            run_id=payload.run_id,
            user_query=payload.message
        )

        return {
            "status": "success",
            "response": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cleanup-images/{run_id}")
def cleanup_images(run_id: str):
    try:
        delete_result = delete_all_visual_outputs(run_id=run_id)

        return {
            "status": "success",
            "run_id": run_id,
            "delete_result": delete_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cleanup-data/{run_id}")
def cleanup_data(run_id : str):
    try:
        delete_data = delete_all_data(run_id=run_id)

        return{
            "status": "success",
            "run_id": run_id,
            "delete_data": delete_data
        }
    except Exception as e : 
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
