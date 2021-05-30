from bs4 import BeautifulSoup
import requests
import json
import tkinter as tk
from PIL import Image, ImageTk
import random

WEBSITE = "https://www.merriam-webster.com/dictionary/"
filename = "learnt_words.txt"
global score
score = 0

# check if file exists, create if does not
with open(filename, 'a+') as create:
    pass
    
#loads the dictionary in the file
def read_data(filename):
    global js_data
    with open(filename, 'r+') as reader:
        try:
            js_data = json.loads(reader.read())
        except:
            js_data = {}

read_data(filename)

#check if word is in dict, otherwise append it
def word_in_dict(word, dict):
    definitions = ""
    if word not in dict:
        list = web_scrap(word)
        dict[word] = list
        dict_to_file(dict, filename)
        for i in range(len(list)):
            definitions += str(i+1) + ": " + list[i] + "\n"
        definition_label['text'] = definitions
    else:
        list = dict[word]
        for i in range(len(list)):
            definitions += str(i+1) + ": " + list[i] + "\n"
        definition_label['text'] = definitions

#write dict to file
def dict_to_file(dict, file):
    with open(file, 'r+') as writer:
       writer.write(json.dumps(dict))

#webscrpping function here
def web_scrap(word):
    list = []
    content = requests.get(WEBSITE + word).text
    soup = BeautifulSoup(content, 'lxml')
    word_definitions = soup.find_all('div', class_ = 'sense has-num-only')
    for definition in word_definitions:
        meaning = definition.find('span', class_ = 'dtText').text
        meaning = meaning.split(": ")
        try:    
            list.append(meaning[1])
        except:
            list.append(meaning[0])
    return list

def no_input():
    tk.messagebox.showerror("No search input", "There is no word to search.")
 
#actionListener function for search button
def searchClick():
    if input_field.get() == "":
        no_input()
    else:
        word_in_dict(input_field.get().lower(), js_data)

# opens up window for search
def searchWindow():
    searchWindow = tk.Toplevel()
    searchWindow.title("Search Window")
    
    inputFrame = tk.LabelFrame(searchWindow, text = "Enter word to search:")
    inputFrame.grid(row = 0, column = 0, padx = 10, columnspan = 3)
    
    global input_field
    input_field = tk.Entry(inputFrame, width = 50, borderwidth = 5)
    input_field.pack(padx = 10, pady = 5)
    
    searchButton = tk.Button(inputFrame, text = "Search", padx = 20, command = searchClick)
    searchButton.pack(padx = 10, pady = 5)
    
    blankLabel = tk.Label(searchWindow, text = "Definitions:")
    blankLabel.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5)
        
    global definition_label
    definition_label = tk.Label(searchWindow, text = "")
    definition_label.grid(row = 2, column = 0, columnspan = 3, padx = 10)
    
    exit_button = tk.Button(searchWindow, text = "Exit", padx = 20, command = searchWindow.destroy)
    exit_button.grid(row = 3, column = 2, pady = 5, padx = 10, sticky = 'e')

# opens up window for game/quiz
def gameWindow():
    
    global gameWindow
    gameWindow = tk.Toplevel()
    gameWindow.title("Game Window")
    
    read_data(filename)
    
    if len(js_data) <= 1:
        noQuiz = tk.Label(gameWindow, text = "There is less than 2 words in the dictionary, no able to do quiz.")
        noQuiz.pack(pady = 5, padx = 10)
        
        exitButton = tk.Button(gameWindow, text = "Exit", pady= 5, padx = 20, command = gameWindow.destroy)
        exitButton.pack(pady = 5, padx = 10)
        
    else:
        buttonFrame = tk.LabelFrame(gameWindow, text = "Do you want to test your knowledge?")
        buttonFrame.grid(row = 0, column = 0, columnspan = 1, padx = 10, pady = 5)
        
        yesButton = tk.Button(buttonFrame, text = "YES!", padx = 20, command = quizWindow)
        yesButton.grid(row = 0, column = 0, pady = 5, padx= 20, sticky = "e")
        
        noButton = tk.Button(buttonFrame, text = "NO!", padx = 20, command = gameWindow.destroy)
        noButton.grid(row = 0, column = 1, pady = 5)

def selected_options(answer, score):
    nextButton['state'] = "active"
    if answer in correct_answers:
        correction['text'] = "That's right!"
    else:
        for option in options:
            if option in correct_answers:
                correction['text'] = "The correct answer is:  " + option.upper()
                break

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def for_options(options, correct_answers, num_options, word_index):
    options.append(correct_answers[random.randint(0, len(correct_answers) - 1)])
    for i in range (num_options - 1):
        randomInt = random.randint(0, len(word_list) - 1)
        while randomInt == word_index:
            randomInt = random.randint(0, len(word_list) - 1)
        randomWord = js_data[word_list[randomInt]]
        randomInt = random.randint(0, len(randomWord) - 1)
        wrong_option = randomWord[randomInt]
        while wrong_option in options:
            randomInt = random.randint(0, len(randomWord) - 1)
            wrong_option = randomWord[randomInt]
        options.append(wrong_option)
    random.shuffle(options)
    return options
    
    
def for_num_options(options_length, num_options):
    if options_length < 3:
        num_options += options_length
        return num_options
    else:
        return 4

def radioButtons():
    answer = tk.StringVar()
    answer.set(options[0])
    
    for option in options:
        tk.Radiobutton(optionFrame, text = option, variable = answer, value = option).pack(padx = 0, pady = 0, anchor = 'w')
    
    confirmButton = tk.Button(optionFrame, text = "Confirm", padx = 10, pady= 3, command = lambda: selected_options(answer.get(), score))
    confirmButton.pack(padx = 10, pady = 5)

def next_question():
    word = word_list[random.randint(0, len(word_list) - 1)]
    word_index = word_list.index(word)
    
    wordLabel['text'] = word
    correction['text'] = ""
    
    global correct_answers
    correct_answers = js_data[word]
    
    global options
    options = []
    
    len_of_wrong_options = 0
    for words in word_list:
        if words != word: 
            len_of_wrong_options += len(js_data[words])
    
    num_options = 1
    num_options = for_num_options(len_of_wrong_options, num_options)
    
    options = for_options(options, correct_answers, num_options, word_index)
    
    clear_frame(optionFrame)
    
    radioButtons()
    
    nextButton['command'] = next_question
    nextButton['state'] = "disabled"

def quizWindow():
    gameWindow.destroy()    
    quizWindow = tk.Toplevel()
    quizWindow.title("Quiz")
    
    num_quiz = 0
    
    #number of quizzes
    if len(js_data) < 10:
        num_quiz = len(js_data)
    else:
        num_quiz = 10
    
    #list of all the words in dictionary
    global word_list
    word_list = []
    for key in js_data.keys():
        word_list.append(key)
    
    word = word_list[random.randint(0, len(word_list) - 1)]
    word_index = word_list.index(word)
    
    questionLabel = tk.Label(quizWindow, text = "What is the meaning of this word?", padx = 10, pady = 5)
    questionLabel.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5)
    
    global wordLabel
    wordLabel = tk.Label(quizWindow, text = word, padx = 10, pady = 5, font = "bold")
    wordLabel.grid(row = 1, column = 0, padx = 10, pady = 5, columnspan = 3)
    
    global correction
    correction = tk.Label(quizWindow, text = "", padx = 10, pady = 5, fg = "red")
    correction.grid(row = 2, column = 0, padx = 10, pady = 5, columnspan = 3, sticky = "w")
    
    global optionFrame
    optionFrame = tk.LabelFrame(quizWindow, text = "Select your answer.", padx = 10, pady = 5)
    optionFrame.grid(row = 3, column = 0, columnspan = 3, padx = 10, pady = 5)
    
    # list of all the correct answers, used to check if right or wrong
    global correct_answers
    correct_answers = js_data[word]
    
    global options
    options = []
        
    len_of_wrong_options = 0
    for words in word_list:
        if words != word: 
            len_of_wrong_options += len(js_data[words])
    
    num_options = 1
    num_options = for_num_options(len_of_wrong_options, num_options)
    
    options = for_options(options, correct_answers, num_options, word_index)
    
    radioButtons()
    
    global nextButton
    nextButton = tk.Button(quizWindow, text = "Next", padx = 10, pady = 3, command = next_question, state = "disabled")
    nextButton.grid(row = 4, column = 1, padx = 10, pady = 5)
    
    """
    status bar to show current question e.g. 1 out of 10
    """
    

root = tk.Tk()
root.title("Merriam Webster Scrapper")
    
title = tk.Label(root, text = "English Dictionary!", font = "bold")
title.grid(row = 0, column = 0, columnspan = 2)

dict_image = ImageTk.PhotoImage(Image.open('dict_image.png').resize((250, 250), Image.ANTIALIAS))
imageLabel = tk.Label(image = dict_image)
imageLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2)

buttonFrame = tk.LabelFrame(root, text = "")
buttonFrame.grid(row = 2, column = 0, padx = 10, pady = 5, columnspan = 2)

searchWin_Button = tk.Button(buttonFrame, text = "Search", padx = 20, command = searchWindow)
searchWin_Button.grid(row = 0, column = 0, padx = 5, pady = 2)

gameButton = tk.Button(buttonFrame, text = "Test!", padx = 20, command = gameWindow)
gameButton.grid(row = 0, column = 1, padx = 5, pady = 2)

exitButton = tk.Button(buttonFrame, text = "Quit", padx = 26, command = root.destroy)
exitButton.grid(row = 1, column = 0, padx = 5, pady = 2)

root.mainloop()
