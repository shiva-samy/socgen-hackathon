#install the below module using 'pip install google-generativeai'

import google.generativeai as ai
import csv

ai.configure(api_key="<API_KEY>")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    }
]

model=ai.GenerativeModel(model_name="gemini-1.5-flash",
                         generation_config=generation_config,
                         safety_settings=safety_settings)

def extract_csv(pathname: str) -> list[str]:
    parts = [f"--- START OF CSV ${pathname} ---"]
    with open(pathname,"r",newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            str=" "
            parts.append(str.join(row))

    return parts

convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": extract_csv("avocado.csv")
    }
])

convo.send_message(str(input("Enter prompt:")))
print(convo.last.text)