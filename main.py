#import libraries
from re import M
from newspaper import Article
import random
import nltk
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
nltk.download('punkt')


warnings.filterwarnings('ignore')

article=Article("https://www.mayoclinic.org/diseases-conditions/chickenpox/symptoms-causes/syc-20351282")
article.download()
article.parse()
article.nlp()
corpus=article.text
# print(corpus)

#tokenization
text=corpus
sentence_list=nltk.sent_tokenize(text) #A list of sentences

#Print the list of sentences
# print(sentence_list)

misspellings_dict = {"chicken pox": "chickenpox", "chikenpox": "chickenpox", "symtoms": "symptoms" }


def misspellings(text):
    text=text.lower()

    if text in misspellings_dict:
        #reponse via normal method but with correct spelling 
        return misspellings_dict[text]
    
    return None

            
    


#Random response to greeting
def greeting_response(text):
    text=text.lower()

    #Bots greeting
    bot_greetings = ["howdy", "hi", "hola", "hey", "hello", "good day to you", "greetings", "wassssup"]

    #User Greetings
    user_greetings = ["helo", "helllo", "wazzup", "wassup", "howdy", "hi", "hola", "hey", "hello", "greetings", "hllo"]
    for word in text.split():
        if word in user_greetings:
            #Random response to greeting
            return random.choice(bot_greetings)

            
def gratitude_response(text):
    text = text.lower()
    #Bots gratitude
    bot_gratitude = ["Glad to help", "You are most welcome", "Pleasure to be of help"]

    #User Gratitude
    user_gratitude = ["thx", "thnx", "thanks", "Thankyou so much", "grateful", "Thankyou", "thankyou", "thank you"]

    for word in text.split():
        if word in user_gratitude:
            return random.choice(bot_gratitude)


def emergency_response(text):
    text = text.lower()
    # bot emergency
    bot_emergency = ["If this is an emergency, please call 911 or call your family doctor!"]

    #User Gratitude
    user_gratitude = ["help", "emergency", "what do i do", "can you help", "please help", "SOS", "911", "police", "dying"]

    for word in text.split():
        if word in user_gratitude:
            return random.choice(bot_emergency)


# Default title text
def index_sort(list_var):
    length = len(list_var)
    list_index=list(range(0,length))
    x=list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]]>x[list_index[j]]:
                #swap
                temp=list_index[i]
                list_index[i]=list_index[j]
                list_index[j]=temp

    return list_index

#Creat Bots Response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ""
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1],cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag =1
            j = j + 1
    
        if j > 2:
            break

    if response_flag == 0:
        bot_response = bot_response + " " + "I apologize, I dont understand"

    sentence_list.remove(user_input) 

    return bot_response

def main():
        
    #Start Chat
    print("*** Doc Bot: Hello, I am chatbot and I can answer your queries about Chicken Pox. If you would like to exit type, exit or bye")

    exit_list=['cya', 'goodbye', 'good bye', 'exit', 'bye', 'see you later', 'quit']

    while(True):
        user_input=input()

        if misspellings(user_input)!= None:
            user_input = misspellings(user_input)

        if user_input.lower() in exit_list:
            print("*** Chat Bot: Thank you, goodbye. ")
            break

        elif emergency_response(user_input)!= None:
            print("*** Chat bot: " + emergency_response(user_input))

        elif greeting_response(user_input)!= None:
            print("*** Chat Bot: " + greeting_response(user_input))

        elif gratitude_response(user_input)!= None:
            print("*** Chat Bot: " + gratitude_response(user_input))
             
        else:
            print("*** Chat Bot: " + bot_response(user_input))


if __name__ == "__main__":
    main()

'''
testing stuff below

'''


# text = "who are you"
# out = greeting_response(text)
# print(out)

# text = "wow thanks"
# out = gratitude_response(text)
# print(out)


# a = [1,2, 9, 0, -1, 7, 4, 3]
# out = index_sort(a)
# print(out)
