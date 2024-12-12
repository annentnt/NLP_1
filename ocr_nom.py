import os
import json
import requests

# Định nghĩa các đường dẫn
input_folder = "./datasets/nom/draft/"  # Thư mục chứa ảnh
output_folder = "./datasets/nom/ocr/"  # Thư mục chứa file JSON
os.makedirs(output_folder, exist_ok=True)

# Domain và endpoint của API
API_DOMAIN = "https://tools.clc.hcmus.edu.vn"
UPLOAD_ENDPOINT = "/api/web/clc-sinonom/image-upload"
OCR_ENDPOINT = "/api/web/clc-sinonom/image-ocr"

# Hàm upload ảnh và nhận tên file trên server
def upload_image(file_path):
    with open(file_path, "rb") as image_file:
        files = {"image_file": image_file}
        response = requests.post(
            API_DOMAIN + UPLOAD_ENDPOINT,
            files=files,
            headers={"User-Agent": "Custom-Client"}
        )
        response_data = response.json()
        if response_data.get("is_success") and response_data.get("code") == "000000":
            return response_data["data"]["file_name"]
        else:
            raise Exception(f"Upload failed: {response_data}")

# Hàm OCR ảnh
def ocr_image(file_name, ocr_id=1):
    payload = {
        "ocr_id": ocr_id,
        "file_name": file_name
    }
    response = requests.post(
        API_DOMAIN + OCR_ENDPOINT,
        json=payload,
        headers={"User-Agent": "Custom-Client"}
    )
    response_data = response.json()
    if response_data.get("is_success") and response_data.get("code") == "000000":
        return response_data["data"]
    else:
        raise Exception(f"OCR failed: {response_data}")

# Duyệt qua các file trong thư mục đầu vào và xử lý
for image_file in os.listdir(input_folder):
    image_path = os.path.join(input_folder, image_file)
    try:
        print(f"Processing {image_file}...")
        # Upload ảnh
        uploaded_file_name = upload_image(image_path)
        # OCR ảnh
        ocr_result = ocr_image(uploaded_file_name)
        # Lưu kết quả vào file JSON
        output_file = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}.json")
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(ocr_result, json_file, ensure_ascii=False, indent=4)
        print(f"Processed and saved: {output_file}")
    except Exception as e:
        print(f"Error processing {image_file}: {e}")
