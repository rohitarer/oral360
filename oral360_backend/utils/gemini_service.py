import requests
import json

API_KEY = ""  # 🔐 Secure in production
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={API_KEY}"

def get_gemini_diagnosis(tooth_number, base64_image):
    prompt = f"""
You are a professional dental diagnostic assistant.

Task:
Analyze the high-resolution image of Tooth {tooth_number}.
Detect visible signs of the following:
- Caries
- Plaque
- Missing Tooth
- Gum Recession
- Restoration or Cement
- Root Stumps

🧠 Output in short, clinical format like:
"Tooth 16 shows cervical caries and marginal plaque. Suggest oral hygiene improvement and possible restoration."

🎯 Be accurate, concise, and dentist-friendly. Avoid vague suggestions.
"""

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",  # Or image/png if needed
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    }

    print(f"\n📨 Sending Gemini Vision prompt for Tooth {tooth_number}:\n{prompt.strip()}")

    try:
        response = requests.post(
            GEMINI_URL,
            headers={"Content-Type": "application/json"},
            json=body
        )

        if response.status_code == 200:
            data = response.json()
            raw_text = data['candidates'][0]['content']['parts'][0]['text']

            print("\n🧠 Gemini Vision Raw Output (first 500 chars):")
            print(raw_text[:500].strip())

            print("\n✅ Final Diagnosis Summary:")
            print(raw_text.strip())

            return raw_text.strip()

        else:
            print(f"\n❌ Gemini API Error: {response.status_code}")
            print(response.text)
            return "Gemini diagnosis failed. Please retry or use YOLO fallback."

    except Exception as e:
        print(f"\n❌ Gemini Exception: {e}")
        return f"Gemini error: {str(e)}"
