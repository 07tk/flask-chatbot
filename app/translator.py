import deepl
from concurrent.futures import ThreadPoolExecutor

api_key = "0d329862-d2b7-4d64-9ef7-beda58be1f1d:fx"
translator = deepl.Translator(api_key)


def translate_ru(word, src='EN', dest='RU'):


    return translator.translate_text(word,source_lang=src, target_lang=dest).text


def translate_en(input_text, src='RU', dest='EN-US'):

    return translator.translate_text(input_text,source_lang=src, target_lang=dest).text    
    
def translate_parallel(input_text, dest):
    words = input_text.split()
    if dest == 'RU':
        src = 'EN'
        with ThreadPoolExecutor() as executor:
            translated_words = list(executor.map(lambda word: translate_ru(word, src, dest),words))
    else:
        src = 'RU'
        with ThreadPoolExecutor() as executor:
            translated_words = list(executor.map(lambda word: translate_en(word, src, dest),words))

    translated_sentence = ' '.join(translated_words)
    return translated_sentence
if __name__ == '__main__':
    print(translate_ru("Almetyevsk has a variety of cafes, including Coffee Shop No. 1 with coffee and desserts, Terrace offering European and Asian cuisine, Shokoladnitsa with desserts and drinks, and Chaikhona No. 1 serving Uzbek cuisine."))
    print(translate_en("Привет, как дела?"))
    print(translate_ru("Almetyevsk"))