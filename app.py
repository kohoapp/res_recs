#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 19:13:22 2023

@author: davidooooo
"""
#%%
import os
import openai
#%%
app = Flask(__name__)

#%% Your OpenAI API key
openai.api_key = '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'

# Your getRecs function (modify as needed)
def getRecs(likes="",dislikes="", restaurant="", menu=""):
    
    #convert liked foods into an object for the model
    def likes_message(likes):
        return eval("""{{"role": "user",
        "content": "Foods I like: {}"
        }}""".format(likes.capitalize()))
                    
    #convert disliked foods into an object for the model
    def dislikes_message(dislikes):
        return eval("""{{"role": "user",
        "content": "Foods I dislike: {}"
        }}""".format(dislikes.capitalize()))
    
    #convert restaurant and menu into an object for the model
    def restaurant_message(restaurant, menu):
         return eval("""{{"role": "user",
         "content": "This is the restaurant I'm at: {r}. This is what they serve: {m}. What should I eat at the restaurant I'm at based on my likes?"
         }}""".format(r = restaurant.capitalize(), m = menu.capitalize()))
    
    #initate the convo, say who the agent is
    convo = [{"role": "system",
     "content": "You are a renowned meal recommender"
     }]
    
    #add the likes to the end of the convo object as a user message
    convo.append(likes_message(likes))
     #add the dislikes to the end of the convo object as a user message
    convo.append(dislikes_message(dislikes))
    #add the restaurant and menu to the end of the convo object as a user message
    convo.append(restaurant_message(restaurant, menu))
    #call the model
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=convo,
      stream=True,
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
            
    )
    rec =  ""
    #print out the results
    for chunk in response:
        try:
            content_value = chunk['choices'][0]['delta']['content']
            if content_value is not None:
                rec = rec + content_value
                #print(content_value)
        except:
            pass
    return rec
#%%
a = getRecs("chicken", "beer", "chipotle", "burritos, tacos")

