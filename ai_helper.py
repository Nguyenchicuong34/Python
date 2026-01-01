import google.generativeai as genai
import PIL.Image


API_KEY = "AIzaSyAfn2xZfh7ySdEYmrZM6ST_V5jR45-P2WM"  
genai.configure(api_key=API_KEY)


MODEL_NAME = 'gemini-flash-latest' 

def ask_ai_comprehensive(text_content, mode="general"):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        base_prompt = """
        Bạn là Trợ lý Ảo Smart Study Mate (được tạo bởi Nguyen Chi Cuong).
        Nhiệm vụ: Hỗ trợ học tập và cuộc sống.
        Ngôn ngữ: Trả lời song ngữ (Tiếng Việt là chính, Tiếng Anh bổ sung nếu cần thuật ngữ).
        Phong cách: Thân thiện, Tự nhiên, Chính xác.
        """

       
        if mode == "code":
            sys_prompt = f"""{base_prompt}
            YÊU CẦU ĐẶC BIỆT VỀ CODE (C/C++):
            - Viết code hoàn chỉnh, chạy được ngay.
            - Giải thích logic thuật toán.
            - Đưa ra các bài tập trắc nghiệm liên quan nếu được hỏi.
            Câu hỏi: {text_content}"""
            
        elif mode == "translate": 
            sys_prompt = f"""{base_prompt}
            YÊU CẦU DỊCH THUẬT CHUYÊN NGÀNH:
            - Nếu văn bản là Tiếng Anh: Hãy dịch sang Tiếng Việt chuẩn ngữ cảnh IT/Khoa học.
            - Nếu văn bản là Tiếng Việt: Hãy dịch sang Tiếng Anh chuyên ngành.
            - Chỉ đưa ra kết quả dịch, giữ nguyên ý nghĩa gốc.
            Nội dung cần dịch: "{text_content}" """
            
        else: 
            sys_prompt = f"""{base_prompt}
            YÊU CẦU: Giải thích chi tiết, dễ hiểu. Nếu là vấn đề cuộc sống, hãy đưa ra lời khuyên khách quan.
            Câu hỏi: {text_content}"""

        response = model.generate_content(sys_prompt)
        return response.text
    except Exception as e:
        return f"Lỗi kết nối AI ({e}). Hãy kiểm tra mạng hoặc API Key."

def analyze_image_study(image_path, user_req):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        img = PIL.Image.open(image_path)
        prompt = f"Hãy đóng vai gia sư. Nhìn vào ảnh này và: {user_req}. Giải thích chi tiết bằng tiếng Việt."
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Không thể phân tích ảnh: {e}"