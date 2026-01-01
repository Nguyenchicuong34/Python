import google.generativeai as genai

API_KEY = "AIzaSyAfn2xZfh7ySdEYmrZM6ST_V5jR45-P2WM"  
genai.configure(api_key=API_KEY)

print("Đang kiểm tra các model khả dụng...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Lỗi: {e}")
