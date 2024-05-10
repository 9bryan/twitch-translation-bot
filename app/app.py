import os
import argparse
from dotenv import load_dotenv
from transformers import pipeline, MBartForConditionalGeneration, MBart50TokenizerFast
from twitchio.ext import commands

# enable argparse and load dotenv if --dotenv flag is provided
parser = argparse.ArgumentParser()
parser.add_argument("--dotenv", help="load .env file", action="store_true")
args = parser.parse_args()
if args.dotenv:
    load_dotenv()

# setup language detection model and pipeline
detect_model = "papluca/xlm-roberta-base-language-detection"
language_detection_pipeline = pipeline("text-classification", model=detect_model)

# setup translation model and tokenizer
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

print("language detection model, translation model, and tokenizer loaded")

target_language_code = os.environ['TARGET_LANGUAGE_CODE']

language_codes = {
    'ar' : 'ar_AR',
    'bg' : None,
    'de' : 'de_DE',
    'el' : None,
    'en' : 'en_XX',
    'es' : 'es_XX',
    'fr' : 'fr_XX',
    'hi' : 'hi_IN',
    'it' : 'it_IT',
    'ja' : 'ja_XX',
    'nl' : 'nl_XX',
    'pl' : 'pl_PL',
    'pt' : 'pt_XX',
    'ru' : 'ru_RU',
    'sw' : 'sw_KE',
    'th' : 'th_TH',
    'tr' : 'tr_TR',
    'ur' : 'ur_PK',
    'vi' : 'vi_VN',
    'zh' : 'zh_CN'
}

language_names = {
    'ar' : 'arabic',
    'bg' : 'bulgarian',
    'de' : 'german',
    'el' : 'greek',
    'en' : 'english',
    'es' : 'spanish',
    'fr' : 'french',
    'hi' : 'hindi',
    'it' : 'italian',
    'ja' : 'japanese',
    'nl' : 'dutch',
    'pl' : 'polish',
    'pt' : 'portuguese',
    'ru' : 'russian',
    'sw' : 'swahili',
    'th' : 'thai',
    'tr' : 'turkish',
    'ur' : 'urdu',
    'vi' : 'vietnamese',
    'zh' : 'chinese'
}

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.environ['ACCESS_TOKEN'], prefix='', initial_channels=[os.environ['CHANNEL']])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # ignore our own messages
        if message.echo:
            return

        # detect language
        language_classification = language_detection_pipeline(message.content, top_k=1, truncation=True)
        detected_language_code = language_classification[0]['label']
        detected_language = language_names[detected_language_code]
        print(message.content)
        print(f'Detected language: {detected_language}')

        # bail if message is already in desired language
        if detected_language_code == target_language_code:
            print(f'Language {detected_language} same as target language')
            return

        # bail if language is unsupported
        if language_codes[detected_language_code] == None:
            print(f'Language {detected_language} not supported')
            return

        if language_classification[0]['score'] > 0.95:
            ctx = await self.get_context(message)

            tokenizer.src_lang = language_codes[detected_language_code]
            encoded_ar = tokenizer(message.content, return_tensors="pt")
            generated_tokens = model.generate(
                **encoded_ar,
                forced_bos_token_id=tokenizer.lang_code_to_id[language_codes[target_language_code]]
            )
            translated_message = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

            # bail if translated message is two words or less
            if len(translated_message.split()) <= 1:
                print(len(translated_message.split()))
                print('Message too short')
                return

            print(f'Language: {detected_language}. Translation: {translated_message}')
            await ctx.reply(f'Language: {detected_language}. Translation: {translated_message}')

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

bot = Bot()
bot.run()
