import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pymongo import MongoClient

import tempfile
import plotly.io as pio
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.environ["MONGO_URI"])
collection = client[os.environ["DB_NAME"]][os.environ["COLLECTION_NAME"]]

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def save_plotly_figure(
    fig,
    plot_name: str,
    folder: str = "eda_outputs/plots",
    format: str = "png"
) -> dict:
    """
    Saves a Plotly figure to Cloudinary.
    Returns Cloudinary metadata (url + public_id).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    public_id = f"{folder}/{plot_name}_{timestamp}"

    with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as tmp:
        temp_path = tmp.name
    pio.write_image(fig, temp_path, format=format)

    response = cloudinary.uploader.upload(
        temp_path,
        public_id=public_id,
        resource_type="image"
    )
    os.remove(temp_path)

    return {
        "url": response["secure_url"],
        "public_id": response["public_id"],
        "format": response["format"],
        "bytes": response["bytes"]
    }

def delete_all_visual_outputs(run_id: str):
    doc = collection.find_one({"run_id": run_id}, {"visual_outputs": 1})
    if not doc or not doc.get("visual_outputs"):
        return {"deleted": 0}

    public_ids = []
    for block in doc["visual_outputs"]:
        for v in block.values():
            if isinstance(v, list):
                public_ids.extend([i["public_id"] for i in v if "public_id" in i])
            elif isinstance(v, dict) and "public_id" in v:
                public_ids.append(v["public_id"])

    if public_ids:
        cloudinary.api.delete_resources(public_ids, resource_type="image")

    collection.update_one(
        {"run_id": run_id},
        {"$set": {"visual_outputs": []}}
    )

    return {"deleted": len(public_ids)}