from fastapi import FastAPI, UploadFile, File
from deepface import DeepFace
import shutil
import os
import easyocr
from passporteye import read_mrz
from database import check_passport

app = FastAPI()

THRESHOLD = 85
reader = easyocr.Reader(['en'])


def verify_person(live_img_path, passport_img_path):

    result = DeepFace.verify(
        img1_path=live_img_path,
        img2_path=passport_img_path,
        model_name="Facenet",
        detector_backend="opencv"
    )

    similarity = (1 - result["distance"]) * 100

    if similarity >= THRESHOLD:
        status = "VERIFIED"
    else:
        status = "NOT VERIFIED"

    return similarity, status


def extract_passport_details(passport_img_path):

    data = {}

    # MRZ extraction
    mrz = read_mrz(passport_img_path)

    if mrz:
        mrz_data = mrz.to_dict()

        data["surname"] = mrz_data.get("surname")
        data["given_name"] = mrz_data.get("names")
        data["passport_number"] = mrz_data.get("number")
        data["nationality"] = mrz_data.get("nationality")
        data["country_code"] = mrz_data.get("country")
        data["date_of_birth"] = mrz_data.get("date_of_birth")
        data["expiration_date"] = mrz_data.get("expiration_date")
        data["MRZ_code"] = mrz_data.get("raw_text")

    # OCR fallback
    text = reader.readtext(passport_img_path, detail=0)

    data["raw_text"] = " ".join(text)

    # Placeholder fields (may require advanced OCR layout parsing)
    data["place_of_birth"] = None
    data["place_of_issue"] = None
    data["date_of_issue"] = None
    data["type_of_passport"] = "P"

    return data


@app.post("/verify-face")
async def verify_face(
    live_image: UploadFile = File(...),
    passport_image: UploadFile = File(...)
):

    live_path = f"temp_{live_image.filename}"
    passport_path = f"temp_{passport_image.filename}"

    with open(live_path, "wb") as buffer:
        shutil.copyfileobj(live_image.file, buffer)

    with open(passport_path, "wb") as buffer:
        shutil.copyfileobj(passport_image.file, buffer)

    similarity, status = verify_person(live_path, passport_path)

    passport_data = None
    db_status = None

    if status == "VERIFIED":

        passport_data = extract_passport_details(passport_path)

        passport_number = passport_data.get("passport_number")

        if passport_number:
            db_status = check_passport(passport_number)

    os.remove(live_path)
    os.remove(passport_path)

    return {
        "face_similarity": round(similarity, 2),
        "face_verification": status,
        "passport_data": passport_data,
        "database_match": db_status
    }