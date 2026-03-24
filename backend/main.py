from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import InstructionRequest, InstructionResponse
from interpreter import interpret_literally

app = FastAPI(title="정확한 지침 챌린지 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def root():
    return {
        "message" : "정확한 지침 챌린지 API"
    }
    

@app.post("/interpret", response_model=InstructionResponse)
def interpret(request: InstructionRequest):
    try:
        result = interpret_literally(request.instruction, request.step_number)
        return InstructionResponse(
            step_number = request.step_number,
            original = request.instruction,
            literal_response = result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/reset")
def reset():
    return {
        "message" : "게임이 초기화 되었습니다!"
    }