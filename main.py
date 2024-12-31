import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import MBartForConditionalGeneration, MBartTokenizer, MBartConfig

# Load model and tokenizer at startup
MODEL_PATH = "model"  # Path to your model folder
tokenizer = MBartTokenizer.from_pretrained(MODEL_PATH)
model = MBartForConditionalGeneration.from_pretrained(MODEL_PATH)

app = FastAPI()

# List of allowed origins (the frontend URL you are serving the HTML from)
origins = [
    "http://127.0.0.1:5500",  # Your frontend origin (adjust port if needed)
    "http://localhost:5500",   # Another common frontend origin
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)

# Input model for translation
class TranslationRequest(BaseModel):
    text: str

@app.get('/')
def index():
    return {'message': 'Jawi Translater API'}

@app.post("/translate")
async def translate(data: TranslationRequest):
    sentence = data.text.strip()
    if not sentence:
        raise HTTPException(status_code=400, detail="No text provided for translation")

    try:
        # Translate the text
        inputs = tokenizer(sentence, return_tensors="pt")
        translated_tokens = model.generate(**inputs,  decoder_start_token_id=tokenizer.lang_code_to_id["ar_AR"], early_stopping=True, max_length=120)
        pred = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        pred = pred.replace("ar_AR", "").strip()

        return {"translated_text": pred}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with this command inside terminal
# uvicorn main:app --reload