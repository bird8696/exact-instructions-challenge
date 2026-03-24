from pydantic import BaseModel

class InstructionRequest(BaseModel):
    instruction: str
    step_number: int

class InstructionResponse(BaseModel):
    step_number: int
    original: str
    literal_response: str