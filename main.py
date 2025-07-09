from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

with open("employees.json", "r") as f:
    employee_data = json.load(f)

class EmployeeRequest(BaseModel):
    employee_id: str

@app.post("/get-qr")
def generate_qr(request: EmployeeRequest):
    emp_id = request.employee_id

    if emp_id not in employee_data:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp_details = employee_data[emp_id]
    qr_text = (
    f"ID: {emp_id} | "
    f"Name: {emp_details['name']} | "
    f"Dept: {emp_details['department']} | "
    f"Role: {emp_details['role']}"
    )
    qr_img = qrcode.make(qr_text)
    img_io = BytesIO()
    qr_img.save(img_io, format="PNG")
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")
