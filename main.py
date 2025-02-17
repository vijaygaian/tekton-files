from fastapi import FastAPI, UploadFile, File, HTTPException
import yaml

app = FastAPI()


def validate_yaml_kind(file_content: bytes, expected_kind: str):
    """
    Validate that the uploaded YAML file contains a 'kind' field that matches expected_kind.
    Raises an HTTPException if the file is not valid or does not match.
    """
    try:
        # Decode bytes into string (assuming UTF-8) and load the YAML
        data = yaml.safe_load(file_content.decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML format: {e}")

    if not data:
        raise HTTPException(status_code=400, detail="Empty YAML file.")

    if "kind" not in data:
        raise HTTPException(status_code=400, detail="YAML file missing 'kind' field.")

    if data["kind"] != expected_kind:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid kind: expected '{expected_kind}', got '{data['kind']}'."
        )

    return data


@app.post("/api/secret")
async def submit_secret(file: UploadFile = File(...)):
    """
    Endpoint to submit a Secret file.
    Only accepts files with kind: Secret.
    """
    content = await file.read()
    validate_yaml_kind(content, "Secret")
    return {"message": "Secret file accepted."}


@app.post("/api/pipeline")
async def submit_pipeline(file: UploadFile = File(...)):
    """
    Endpoint to submit a Pipeline file.
    Only accepts files with kind: Pipeline.
    """
    content = await file.read()
    validate_yaml_kind(content, "Pipeline")
    return {"message": "Pipeline file accepted."}


@app.post("/api/triggertemplate")
async def submit_trigger_template(file: UploadFile = File(...)):
    """
    Endpoint to submit a TriggerTemplate file.
    Only accepts files with kind: TriggerTemplate.
    """
    content = await file.read()
    validate_yaml_kind(content, "TriggerTemplate")
    return {"message": "TriggerTemplate file accepted."}


@app.post("/api/triggerbinding")
async def submit_trigger_binding(file: UploadFile = File(...)):
    """
    Endpoint to submit a TriggerBinding file.
    Only accepts files with kind: TriggerBinding.
    """
    content = await file.read()
    validate_yaml_kind(content, "TriggerBinding")
    return {"message": "TriggerBinding file accepted."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
