from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import requests
import os
import uuid

app = FastAPI()

# GPT Azure OpenAI-inställningar
AZURE_OPENAI_ENDPOINT = "https://YOUR_RESOURCE_NAME.openai.azure.com/"
AZURE_OPENAI_KEY = "DIN_API_NYCKEL"
GPT_DEPLOYMENT = "juridiskGPT"

# Azure Cognitive OCR
CV_ENDPOINT = "https://YOUR_CV_RESOURCE.cognitiveservices.azure.com/"
CV_KEY = "DIN_CV_KEY"

# GPT-anrop
def call_gpt_analysis(text: str) -> str:
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{GPT_DEPLOYMENT}/chat/completions?api-version=2024-06-01"
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "messages": [{"role": "user", "content": f"Analysera följande text enligt RB 35 kap. och koppla till rättsfaktum:\n\n{text}"}],
        "temperature": 0.1,
        "max_tokens": 2048
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()["choices"][0]["message"]["content"]

# OCR-anrop
def extract_text_ocr(file: UploadFile) -> str:
    headers = {"Ocp-Apim-Subscription-Key": CV_KEY, "Content-Type": file.content_type}
    ocr_url = f"{CV_ENDPOINT}vision/v3.2/read/analyze"

    data = file.file.read()
    response = requests.post(ocr_url, headers=headers, data=data)
    operation_url = response.headers["Operation-Location"]

    # Polling (väntar på OCR-resultat)
    import time
    for _ in range(10):
        result = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": CV_KEY})
        if result.json().get("status") == "succeeded":
            lines = result.json()["analyzeResult"]["readResults"][0]["lines"]
            return "\n".join([line["text"] for line in lines])
        time.sleep(1)
    return "OCR timeout"

@app.post("/analysera/")
async def analysera_dokument(file: UploadFile = File(...)):
    text = extract_text_ocr(file)
    gpt_output = call_gpt_analysis(text)
    return JSONResponse(content={"OCR_text": text, "GPT_analys": gpt_output})
