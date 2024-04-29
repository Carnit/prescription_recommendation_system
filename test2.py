from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle
import pandas as pd

app = FastAPI()
app.mount("/static", StaticFiles(directory="css"), name="static")
templates = Jinja2Templates(directory="templates")

# Application Backend
medicines_dict = pickle.load(open("medicine_dict.pkl", "rb"))
medicines = pd.DataFrame(medicines_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))


def recommend(medicine):
    if medicines.empty:
        return ["No recommendations available"]  # Handle empty DataFrame
    try:
        medicine_index = medicines[medicines["Drug_Name"] == medicine].index[0]
    except IndexError:
        return ["Medicine not found"]  # Handle medicine not found
    distances = similarity[medicine_index]
    medicines_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicine = medicines.iloc[i[0]].Drug_Name
        if recommended_medicine == "Medicine not found":
            recommended_medicines.append(recommended_medicine)
        else:
            recommended_medicines.append(
                (
                    recommended_medicine,
                    f"https://pharmeasy.in/search/all?name={recommended_medicine}",
                )
            )
    return recommended_medicines


# Application Frontend
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/recommend", response_class=HTMLResponse)
async def recommend_medicine(request: Request, selected_medicine_name: str = Form(...)):
    recommendations = recommend(selected_medicine_name)
    return templates.TemplateResponse(
        "recommend.html",
        {
            "request": request,
            "selected_medicine_name": selected_medicine_name,
            "recommendations": recommendations,
        },
    )
