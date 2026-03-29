from google import genai
from google.genai import types
import json
import os

# 🔑 Set your Gemini API key here (better: use environment variable)
client = genai.Client(api_key="AIzaSyA1hb2XOJzoNZMiTxop-pawG0o9f5M9byA")


def extract_receipt(path: str):
    """
    Extract structured data from receipt image using Gemini
    """

    # ✅ Read image
    with open(path, "rb") as f:
        image_bytes = f.read()

    # ✅ Detect image type automatically
    if path.lower().endswith(".png"):
        mime_type = "image/png"
    elif path.lower().endswith(".jpg") or path.lower().endswith(".jpeg"):
        mime_type = "image/jpeg"
    else:
        return {"error": "Unsupported image format"}

    # ✅ Prompt
    prompt = """
    Extract the following fields from this receipt:
    - vendor (string)
    - date (format YYYY-MM-DD if possible)
    - amount (total amount as a number)
    - gst (number, or 0 if not present)

    Return ONLY raw JSON.
    Do NOT use markdown.
    Do NOT wrap in ```json.
    """

    try:
        # ✅ Gemini API call (CORRECT FORMAT)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                )
            ]
        )

        text = response.text

        # ✅ Parse JSON safely
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON returned by model",
                "raw_output": text
            }

    except Exception as e:
        return {
            "error": "Gemini API failed",
            "details": str(e)
        }


# ✅ For testing directly (optional)
if __name__ == "__main__":
    test_image = "receipt.png"  # change file name
    result = extract_receipt(test_image)
    print(json.dumps(result, indent=2))