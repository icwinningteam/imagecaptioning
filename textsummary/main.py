# import openai
#
# from bs4 import BeautifulSoup
# import requests
#
# # import torch
# from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
#
# import torch
# from transformers import AutoTokenizer, AutoModelWithLMHead
#
# # Initialize the OpenAI API client
# openai.api_key = "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"
# model_engine = "text-davinci-002"
#
# # Load the pre-trained model and tokenizer
# model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-cased')
# tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased')
#
# # initialise t5 model
# t5tokenizer = AutoTokenizer.from_pretrained('t5-base')
# t5model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)
#
# def parse_text(url):
#     # Use Beautiful Soup to parse the HTML source
#     response = requests.get(url)
#     html_source = response.content
#     soup = BeautifulSoup(html_source, 'html.parser')
#
#     # Extract the text from the HTML
#     text_paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
#     its = 0
#     ret = ""
#     for t in text_paragraphs:
#         if its >= 60:
#             break
#         if len(t) > 510:
#             t = t[:510]
#         ret += (summarize_t5(t) + '\n')
#         its += 1
#     return ret
#
#
# def summarize_local(text):
#     # Tokenize the input text
#     input_ids = torch.tensor(tokenizer.encode(text, add_special_tokens=True)).unsqueeze(0)
#
#     # Generate the summary using the model
#     with torch.no_grad():
#         outputs = model(input_ids)
#
#     # Extract the summary from the model output
#     summary = tokenizer.decode(input_ids[0], skip_special_tokens=True)
#
#     return summary
#
#
# def summarize_t5(text):
#     inputs = t5tokenizer.encode("summarize: " + text,
#                               return_tensors='pt',
#                               max_length=512,
#                               truncation=True)
#     summary_ids = t5model.generate(inputs, max_length=70, min_length=10, length_penalty=5., num_beams=2)
#     summary = t5tokenizer.decode(summary_ids[0])
#     return summary
#
#
# def summarize_text(text):
#     prompt = "Briefly summarize the following text: \n" + text
#     completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=100, n=1, stop=None,
#                                            temperature=0.5)
#
#     # Extract the summary from the API response
#     summary = completions.choices[0].text
#     return summary

import requests
from bs4 import BeautifulSoup
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the T5 model
model = T5ForConditionalGeneration.from_pretrained("t5-base")
tokenizer = T5Tokenizer.from_pretrained("t5-base")

# Define the summarization function
def summarize(text, max_length=100):
    input_ids = tokenizer.encode(text, return_tensors="pt", padding=True, max_length=512)
    summary_ids = model.generate(input_ids, max_length=max_length, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Function to scrape the text from a webpage
def scrape_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = " ".join([p.text for p in soup.find_all("p")])
    return text

# Use the summarization function



if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/Minecraft"
    text = scrape_webpage(url)
    summary = summarize(text)
    print(summary)
    #print(parse_text(r"https://en.wikipedia.org/wiki/Minecraft"))

