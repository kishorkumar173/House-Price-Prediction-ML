from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS MUST COME AFTER app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = joblib.load("models/house_price_model.pkl")

# Input schema
class HouseData(BaseModel):
    OverallQual: int
    GrLivArea: float
    GarageCars: float
    TotalBsmtSF: float
    FullBath: int
    YearBuilt: int

@app.get("/")
def home():
    return {"message": "House Price Prediction API is running"}

@app.post("/predict")
def predict(data: HouseData):
    input_data = [[
        data.OverallQual,
        data.GrLivArea,
        data.GarageCars,
        data.TotalBsmtSF,
        data.FullBath,
        data.YearBuilt
    ]]
    
    prediction = model.predict(input_data)[0]
    
    return {"predicted_price": float(prediction)}