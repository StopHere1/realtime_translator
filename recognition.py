from googletrans import Translator
from whisper_mic import WhisperMic

translator = Translator(service_urls=['translate.googleapis.com'])

stringbuffer = ""

def process_voice_command(text):
    if "hello" in text.lower():
        print("Hello! I am Baymax!")
    else: 
        pass
    return False

def translate(text):
    destination_language = {  # predefined destination language
    "Chinese":"zh-CN",
        }
    translator=Translator()
    for key, value in destination_language.items():
        print(translator.translate(text, dest=value).text)

def parsing(result):
    global stringbuffer # global buffer for string handling
    stringbuffer += result
    stringsplit = stringbuffer.split(".")
    if len(stringsplit)>1:
        for i in range(0,len(stringsplit)-1):
            if len(stringsplit[i])>0:
                if not stringsplit[i][-1].isnumeric(): # if . is end of a sentence
                    print(stringsplit[i])
                    translate(stringsplit[i])
                    print("-------------------")
                else: #if . is separating numbers, stitch to the next sentence.
                    stringsplit[i+1] = stringsplit[i]+"."+stringsplit[i+1]
        stringbuffer = stringsplit[-1]

def main():
    end_program = False
    mic = WhisperMic(model="small.en") # small size English only model
    while not end_program:
        for result in mic.listen_continuously(phrase_time_limit=10): # Edit phrase_time_limit for the time duration of the recording   
            parsing(result=result) # parse recognition output to string buffer
            end_program = process_voice_command(result)
            if "goodbye" in result.lower(): # if goodbye appears in the sentence, quit the app
                print("My pleasure!")
                return True
            
if __name__ == "__main__":
    main()