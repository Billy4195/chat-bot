import sys
sys.path.append("C:/Users/plum/Documents/Python Scripts/chat-bot")
from bot import bot_function as bot
from bot import method 

def extract_type(type, slots):
    if type == "iQA":
        type = "iQA"
    elif type == "gQA":
        type = "gQA"
    elif type == "sQA":
        if slots.get("space"):
            type = "sQA_with_space"
        else:   
            type = "sQA_without_space"
    elif type == "SUB":
        type = "SUB"
    elif type == "UNSUB":
        type = "UNSUB"
    else: 
        if slots.get('space') and slots.get('time'):
            type = "space_and_time"
        elif slots.get('space'):
            type = "space"
        elif slots.get('time'):
            type = "time"
        else:
            type = "neither"
    return type

def QA(question):
    words = bot.segment(question)
    slots, rest_words = bot.get_slots(words)
    if len(rest_words) == 0:
        type = "neither"
        question_num = 0
    elif "訂閱" in rest_words:
        if "取消" in rest_words:
            type = "UNSUB"
        else:
            type = "SUB"
        question_num = 0
    else:
        type, question_num = method.integrateQA(rest_words)
        
    type = extract_type(type, slots)
    return type, question_num, slots

def gQA_get_answer(question_num):
    answer = bot.get_answer(question_num,{})
    return answer
    
def sQA_get_answer(question_num,slots):
    answer = bot.get_answer(question_num,slots.copy())
    return answer
    
def iQA_get_answer(question_num,slots): 
    answer = bot.get_answer(question_num,slots)
    return answer
    
def sQA_location_get_answer(question_num,slots,location):
    answer = bot.get_location_sQA_answer(question_num,slots.copy(),location)
    return answer

def QAlocation(question,location):
    words = bot.segment(question+location)
    slots, rest_words = bot.get_slots(words)
    type, question_num = method.integrateQA(rest_words)
    if type == "sQA" :
        answer = bot.get_answer(question_num,slots)
    else: 
        answer = ""
        print ("Err: not correct type (sQA)")
    return type, question_num, answer, slots

def old_QAlocation(question,location):
    weighting_method = 'fre_prob'
    question_word = bot.segment(question)
    location_word = bot.segment(location)
    question_word.extend(location_word)
    scores_sorted = method.get_score(question_word, weighting_method)
    slots, rest_words = bot.get_slots(question_word)
    question_num = scores_sorted[0][0]
    answer = bot.get_answer(question_num,slots)
    return answer
    
def old_QA(question):
    weighting_method = 'fre_prob'
    question_word = bot.segment(question)
    scores_sorted = method.get_score(question_word, weighting_method)
    slots, rest_words = bot.get_slots(question_word)
    print(slots)
    if "space" not in slots:
        return 1,""
    question_num = scores_sorted[0][0]
    answer = bot.get_answer(question_num,slots)
    return 0,answer
