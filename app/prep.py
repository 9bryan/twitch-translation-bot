from transformers import pipeline, MBartForConditionalGeneration, MBart50TokenizerFast

# setup language detection model and pipeline
detect_model = "papluca/xlm-roberta-base-language-detection"
language_detection_pipeline = pipeline("text-classification", model=detect_model)

# setup translation model and tokenizer
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

print("language detection model, translation model, and tokenizer loaded")
