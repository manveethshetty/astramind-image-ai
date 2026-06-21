import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from styles import STYLE_MODES

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_API_KEY")
)

def generate_image(user_input, style):
    try:
        style_descriptor = STYLE_MODES[style]
        final_prompt = f"{user_input}, {style_descriptor}"
        
        image = client.text_to_image(
            final_prompt,
            model="black-forest-labs/FLUX.1-dev",
        )
        
        return image, None
    
    except Exception as e:
        return None, f"⚠️ Error generating image: {str(e)}"