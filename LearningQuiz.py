from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import json
import random
import json
import math
import os
from json import JSONEncoder

class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Learning Quiz App")

        # Creating the main frame
        self.frame = Frame(master, bg='#c9bdf7')
        self.frame.pack(expand=True, fill=BOTH)
        master.geometry("1200x600")
        
        # Loading the image for banner
        script_dir = os.path.dirname(__file__)
        rel_path = "./images/StudyBanner.png"
        image_path = os.path.join(script_dir, rel_path)

        self.img = Image.open(image_path)
        self.img = self.img.resize((1200, 200))

        # Converting the image to a PhotoImage object
        self.banner_photo = ImageTk.PhotoImage(self.img)

        # Creating a label widget to display the banner image
        self.banner_label = Label(self.frame, image=self.banner_photo)
        self.banner_label.pack(fill=X)

        # Creating the title label
        self.title_label = Label(self.frame, text="Welcome to Quiz!", font=("Arial", 30), fg="#1C1C1C", bg="#c9bdf7", width=20, height=3)
        self.title_label.pack(pady=20)

        # Creating a frame for the buttons
        self.button_frame = Frame(self.frame, bg="#c9bdf7")
        self.button_frame.pack(pady=10)

        # Creating the add question button
        self.add_question_button = Button(self.button_frame, text="Add New Question", font=("Arial", 20), fg='#FFFFFF', bg='#FF8C42', activebackground='#FF6F00', command=self.open_add_question_frame, width=15, height=2, relief="raised", borderwidth=4)
        self.add_question_button.pack(side="left", padx=(200,50))
        self.add_question_button.bind("<Enter>", lambda event: self.add_question_button.configure(bg='#f4ceb7'))
        self.add_question_button.bind("<Leave>", lambda event: self.add_question_button.configure(bg='#FF8C42'))

        # Creating the do questions button
        self.play_quiz_button = Button(self.button_frame, text="Play Quiz", font=("Arial", 20), fg='#FFFFFF', bg='#FF8C42', activebackground='#FF6F00', command=self.open_practice_questions_frame, width=15, height=2, relief="raised", borderwidth=4)
        self.play_quiz_button.pack(side="right", padx=(50,200))
        self.play_quiz_button.bind("<Enter>", lambda event: self.play_quiz_button.configure(bg='#f4ceb7'))
        self.play_quiz_button.bind("<Leave>", lambda event: self.play_quiz_button.configure(bg='#FF8C42'))
   
    # This method will handle all process of adding a question and answer for a subject
    def open_add_question_frame(self):
        
        # Creating the add question panel
        self.add_question_window = Toplevel(self.master, bg='#d8f5f5')
        add_question_frame = self.add_question_window
        add_question_frame.title("Add Question")
        add_question_frame.geometry("900x300") # set the window size

        # Creating the subject dropdown menu
        subject_label = Label(add_question_frame, text="Subject:", bg='#d8f5f5', fg='#1C1C1C', font=('Arial', 14))
        subject_label.grid(row=0, column=1, sticky="W")
        subject_label.grid(padx=30, pady=20)
        
        # Defining the options for the OptionMenu
        subjectOptions = ["Biology", "Business Studies", "Chemistry", "Computer Science", "Economics", "English Literature", "Geography", "Maths", "Physics", "Religious Studies"]
        # Finding the maximum length of the options
        max_len = max(len(option) for option in subjectOptions)
        
        self.subject_var = StringVar(add_question_frame)
        self.subject_var.set(subjectOptions[0]) # Set the default value to "Biology"
        subject_dropdown = OptionMenu(add_question_frame, self.subject_var, *subjectOptions)
        subject_dropdown.config(bg='#FF8C42', font=('Arial', 12), highlightthickness=0, bd=0, width=max_len, relief="raised", borderwidth=3)


        # Setting the menu configuration option to have the same color and font as the dropdown itself
        subject_dropdown['menu'].config(bg='#FF8C42', font=('Arial', 12))
        subject_dropdown.grid(row=0, column=2, sticky="W")

        # Setting Hover effect for the subject dropdown
        subject_dropdown.bind("<Enter>", lambda event, widget=subject_dropdown: widget.config(bg='#f4ceb7'))
        subject_dropdown.bind("<Leave>", lambda event, widget=subject_dropdown: widget.config(bg='#ff8c42'))

        # Creating the question textbox
        self.question_label = Label(add_question_frame, text="Question:", bg='#d8f5f5', fg='#1C1C1C', font=('Arial', 14))
        self.question_label.grid(row=1, column=1, sticky="W")
        self.question_label.grid(padx=30, pady=15)
        self.question_textbox = Text(add_question_frame, height=2, width=50, font=('Arial', 12))
        self.question_textbox.grid(row=1, column=2, padx=10, pady=10, sticky="W") # add padding to the text box
        self.question_textbox.insert('end', 'Please enter the question you want to add here.')
        self.question_textbox.bind("<FocusIn>", lambda event: self.clear_question_textbox())
        self.question_textbox.bind("<FocusOut>", lambda event: self.validate_question_textbox())

        # Creating the answer textbox
        self.answer_label = Label(add_question_frame, text="Answer:", bg='#d8f5f5', fg='#1C1C1C', font=('Arial', 14))
        self.answer_label.grid(row=2, column=1, sticky="W")
        self.answer_label.grid(padx=30, pady=15)
        self.answer_textbox = Text(add_question_frame, height=2, width=50, font=('Arial', 12))
        self.answer_textbox.grid(row=2, column=2, padx=10, pady=10, sticky="W") # add padding to the text box
        self.answer_textbox.insert('end', 'Please enter the answer to the question.')
        self.answer_textbox.bind("<FocusIn>", lambda event: self.clear_answer_textbox())
        self.answer_textbox.bind("<FocusOut>", lambda event: self.validate_answer_textbox())
        
        # Creating the submit button
        self.submit_button = Button(add_question_frame, text="Submit", command=self.add_question_handler, bg='#FF8C42', font=('Arial', 12), highlightthickness=0, bd=0, relief="raised", borderwidth=3)
        self.submit_button.grid(row=3, column=2, pady=10)

        # Creating an error label for question validation error
        self.question_error_label = Label(add_question_frame, text="Please enter a valid question", bg='#d8f5f5', fg='red', font=('Arial', 14))
        self.question_error_label.grid_remove()
      
        # Creating an error label for answer validation error
        self.answer_error_label = Label(add_question_frame, text="Please enter a valid answer", bg='#d8f5f5', fg='red', font=('Arial', 14))
        self.answer_error_label.grid_remove()
      
        self.status_label = Label(add_question_frame, text="Question and answer added successfully.",fg="green", font=('Arial', 14), bg='#d8f5f5')
        self.status_label.grid_remove()
        
        # Hover effect for the submit button
        self.submit_button.bind("<Enter>", lambda event, widget=self.submit_button: widget.config(bg='#f4ceb7'))
        self.submit_button.bind("<Leave>", lambda event, widget=self.submit_button: widget.config(bg='#FF8C42'))
        
    # Validating question text box
    def validate_question_textbox(self):
        questionText =self.question_textbox.get(1.0, 'end-1c')
        if questionText == "" or questionText == "Please enter the question you want to add here.":
            self.question_error_label.grid(row=1, column=3)
            self.status_label.grid_remove()
        else:
            self.question_error_label.grid_remove()
            
    # Validating answer textbox
    def validate_answer_textbox(self):
        answerText = self.answer_textbox.get(1.0, 'end-1c')
        if answerText == "" or answerText == "Please enter the answer to the question.":
            self.answer_error_label.grid(row=2, column=3)
            self.status_label.grid_remove()
        else:
            self.answer_error_label.grid_remove()
    
    # Clearing question test box content
    def clear_question_textbox(self):
        questionText =self.question_textbox.get(1.0, 'end-1c')
        if questionText == "Please enter the question you want to add here.":
            self.question_textbox.delete('0.0', 'end')
    
    # Clearing answer test box content
    def clear_answer_textbox(self):
        answerText =self.answer_textbox.get(1.0, 'end-1c')
        if answerText == "Please enter the answer to the question.":
            self.answer_textbox.delete('0.0', 'end')
                
    # This method will allow user to add new questions and answers            
    def add_question_handler(self):
        
        self.validate_question_textbox()
        self.validate_answer_textbox()
        # Get the subject, question, and answer from the UI
        selectedSubject = self.subject_var.get()
        newQuestionText = self.question_textbox.get(1.0, 'end-1c')
        newAnswerText = self.answer_textbox.get(1.0, 'end-1c')

        if(newQuestionText =="" or newQuestionText =="Please enter the question you want to add here." or newAnswerText =="" or newAnswerText =="Please enter the answer to the question."):
            return    
        
        currentDir = os.path.dirname(__file__)
        relativePathToDataFolder = "./data"
        subjectDataFilePath = os.path.join(currentDir, relativePathToDataFolder, selectedSubject) + ".json"
        with open(subjectDataFilePath, 'r+') as f:
            
            # Loading already existing question and answers for selected subjects in JSON data from file
            existingFlashCardsInFile = json.load(f)
            
            # Create a list to hold instances of the flash card data
            existingFlashCards = []

            # Iterating all existing flash cards
            
            for existingFlashCard in existingFlashCardsInFile:
                # Create a new instance of flashCard object 
                existingFlashCardItem = flashCard(existingFlashCard['id'], existingFlashCard['ques'], existingFlashCard['ans'])
                # Add the new instance of flashCard object to the array
                existingFlashCards.append(existingFlashCardItem)
           
            # Getting last stored flashcard object
            lastStoredFlashCard= max(existingFlashCards, key=lambda flashCard: flashCard.id)
            
            # Creating nextId for new flashCard 
            newFlashCardId = int(lastStoredFlashCard.id) + 1
            newFlashCard = flashCard(newFlashCardId, newQuestionText, newAnswerText)

            # Add the new question to the list of existing questions
            existingFlashCards.append(newFlashCard)
            
            # Rewind the file pointer to the beginning of the file
            f.seek(0)
            
            # Truncate the file to remove any existing flashCards
            f.truncate()
            
            # Save the updated list of questions to the JSON file
            json.dump(existingFlashCards, f, indent=4, cls=flashCardEncoder)
            
             # Show a success message to the user
            self.status_label.grid(row=4, column=2, sticky="W")

        # Reset the subject, question, and answer widgets
        self.question_textbox.delete(1.0, 'end')
        self.answer_textbox.delete(1.0, 'end')
        
    # This method will handle all process of practicing qiz for a subject
    def open_practice_questions_frame(self):
       
        # Creating the a practice quiz panel
        self.do_questions_menu = Toplevel(self.master, bg='#efe2bb')
        practice_questions_frame = self.do_questions_menu
        practice_questions_frame.title("Practice yor learning")
        practice_questions_frame.geometry("1200x540") # set  
        
            
        # Creating subject label
        self.subject_label = Label(practice_questions_frame, text="Subject:", bg='#efe2bb', fg='#1C1C1C', font=('Arial', 14))
        self.subject_label.grid(row=0, column=0, sticky="W")
        self.subject_label.grid(padx=30, pady=20)
        
        # Defining the options for the OptionMenu
        subjectOptions = ["Biology", "Business Studies", "Chemistry", "Computer Science", "Economics", "English Literature", "Geography", "Maths", "Physics", "Religious Studies"]

        # Finding the maximum length of the options
        max_len = max(len(option) for option in subjectOptions)
        self.subject_var = StringVar(practice_questions_frame)
        self.subject_var.set(subjectOptions[0]) # Set the 
        subject_dropdown = OptionMenu(practice_questions_frame, self.subject_var, *subjectOptions, command=self.on_option_change)
        subject_dropdown.config(bg='#FF8C42', font=('Arial', 12), highlightthickness=0, bd=0, width=max_len, relief="raised", borderwidth=3)

        # Setting the menu configuration option to have the same color and font as the dropdown itself
        subject_dropdown['menu'].config(bg='#FF8C42', font=('Arial', 12))
        subject_dropdown.grid(row=0, column=1, sticky="W")
        subject_dropdown.grid(padx=30, pady=20)
        
        # Setting Hover effect for the subject dropdown
        subject_dropdown.bind("<Enter>", lambda event, widget=subject_dropdown: widget.config(bg='#f4ceb7'))
        subject_dropdown.bind("<Leave>", lambda event, widget=subject_dropdown: widget.config(bg='#ff8c42'))
        
        # Creating the label for no of questions
        self.num_questions_label = Label(practice_questions_frame, text="Number of Questions", bg='#efe2bb', fg='#1C1C1C', font=('Arial', 14))
        self.num_questions_label.grid(row=1, column=0, sticky="W")
        self.num_questions_label.grid(padx=30, pady=15)
        
        # Getting total number of questions of default selected subject
        totalQuestionCount = self.get_total_question_count(subjectOptions[0])
         
        # Creating a  number of question selection slider bar
        self.num_questions_slider = Scale(practice_questions_frame, from_=1, to=totalQuestionCount, orient=HORIZONTAL, font=("Arial", 12), bg='#efe2bb')
        self.num_questions_slider.grid(row=1, column=1, sticky="W")
        self.num_questions_slider.grid(padx=30, pady=15)
        
        # Creating the submit button fro starting quiz
        self.start_quiz_button = Button(practice_questions_frame, text="Start Quiz", command=self.start_quiz_handler, bg='#FF8C42', font=('Arial', 12), highlightthickness=0, bd=0, relief="raised", borderwidth=3)
        self.start_quiz_button.grid(row=2, column=1, sticky="W")
        self.start_quiz_button.grid(padx=30, pady=15)
        self.start_quiz_button.bind("<Enter>", lambda event, widget=self.start_quiz_button: widget.config(bg='#f4ceb7'))
        self.start_quiz_button.bind("<Leave>", lambda event, widget=self.start_quiz_button: widget.config(bg='#FF8C42'))
        
        # Creating the question label
        self.question_label = Label(practice_questions_frame, text="Question:", bg='#efe2bb', fg='#1C1C1C', font=('Arial', 14))
        self.question_label.grid(row=4, column=0, sticky="W")
        self.question_label.grid(padx=30, pady=15)
        
        # Creating the question text label
        self.question_label_text = Label(practice_questions_frame, text="", bg='#efe2bb', fg='#1C1C1C', font=('Arial', 14))
        self.question_label_text.grid(row=4, column=1, sticky="W")
        self.question_label_text.grid(padx=30, pady=15)
        
        self.question_label_id = Label(practice_questions_frame, text="", bg='#efe2bb', fg='#1C1C1C', font=('Arial', 14))

        # Creating the answer label
        self.answer_label = Label(practice_questions_frame, text="Answer:", bg='#efe2bb', fg='#1C1C1C', font=('Arial', 14))
        self.answer_label.grid(row=5, column=0, sticky="W")
        self.answer_label.grid(padx=30, pady=15)
        
        # Creating the answer text box
        self.answer_textbox = Text(practice_questions_frame, height=2, width=50, font=('Arial', 12))
        self.answer_textbox.grid(row=5, column=1, sticky="W") # add padding to the text box
        self.answer_textbox.grid(padx=30, pady=15)
        
        # Creating the correct answer text label
        self.correct_answer_label = Label(practice_questions_frame, text="", bg='#efe2bb', fg='#008000', font=('Arial', 14))
        self.correct_answer_label.grid(row=6, column=1, sticky="W")
        self.correct_answer_label.grid(padx=30, pady=15)
        
        # Creating the answer submit button 
        self.submit_answer_button = Button(practice_questions_frame, text="Submit Answer", command=self.validate_user_answer, bg='#FF8C42', font=('Arial', 12), highlightthickness=0, bd=0, relief="raised", borderwidth=3)
        self.submit_answer_button.grid(row=7, column=1, sticky="W")
        self.submit_answer_button.grid(padx=30, pady=15)
        self.submit_answer_button.bind("<Enter>", lambda event, widget=self.submit_answer_button: widget.config(bg='#f4ceb7'))
        self.submit_answer_button.bind("<Leave>", lambda event, widget=self.submit_answer_button: widget.config(bg='#FF8C42'))
        
        # Creating the score label
        self.score_label = Label(practice_questions_frame, text="Score:", bg='#efe2bb', fg='#1C1C1C', font=('Arial', 14))
        self.score_label.grid(row=8, column=1, sticky="W")
        self.score_label.grid(padx=30, pady=15)  
    
    def get_total_question_count(self, subject):
       existingFlashCards = self.load_existing_flashcards(subject)
       return len(existingFlashCards)
         
    def on_option_change(self,value):
       totalQuestionCount = self.get_total_question_count(value)
       self.num_questions_slider.config(to=str(totalQuestionCount))     
    
    def load_existing_flashcards(self, selected_subject):
        current_dir = os.path.dirname(__file__)
        relative_path_to_data_folder = "./data"
        subject_data_file_path = os.path.join(current_dir, relative_path_to_data_folder, selected_subject) + ".json"
        with open(subject_data_file_path, 'r') as f:
            # Load already existing question and answers for selected subjects in JSON data from file
            existing_flashcards_in_file = json.load(f)
            
            # Create a list to hold instances of the flash card data
            existing_flashcards = []

            # Iterating all existing flash cards
            for existing_flashcard in existing_flashcards_in_file:
                # Create a new instance of flashCard object 
                existing_flashcard_item = flashCard(existing_flashcard['id'], existing_flashcard['ques'], existing_flashcard['ans'])
                # Add the new instance of flashCard object to the array
                existing_flashcards.append(existing_flashcard_item)
            
        return existing_flashcards
    
    # This method will start quiz for practice    
    def start_quiz_handler(self):
        global randomQuestions
        self.correct_answer_label.config(text='')     
        selectedSubject = self.subject_var.get()
        
        # Getting total number of selection from slider
        numQuestions = self.num_questions_slider.get()
        
        # Enabling button
        self.submit_answer_button.config(state='normal')

        # Fetching number of random questions of a selected subject
        existingFlashCards = self.load_existing_flashcards(selectedSubject)
        
        global randomQuestions, currentQuestion, numCorrect
        numCorrect = 0
        # Selecting random questions from all question
        randomQuestions = random.sample(existingFlashCards, numQuestions)
        currentQuestion = 0
        global questionText, answerEntry
        card = randomQuestions[currentQuestion]

        # Showing first question on screen
        self.question_label_text.config(text=card.ques) 
        self.question_label_id.config(text=card.id) 
    
     # This method will show question on quiz screen
    def display_question(self):
        global currentQuestion, questionText, answerEntry
        # Fetch current question to display on frame
        card = randomQuestions[currentQuestion]
       
        # Setting current question text to label
        self.question_label_text.config(text=card.ques) 
        self.question_label_id.config(text=card.id) 
        
    # This method will check the user's answer and update the score
    def display_score(self):
        global numCorrect
        
         # Setting current score label
        score_label.config(text="Final Score: {}/{}".format(numCorrect, len(randomQuestions)))
        self.answer_textbox.delete(0, 'end-1c')   
         
    # This method will validate user answer
    def validate_user_answer(self):
        global currentQuestion, numCorrect, score_label
        
        # Getting answer provided by user
        userAnswer = self.answer_textbox.get(1.0, 'end-1c')
        
        # Getting correct answer
        correctAnswer = randomQuestions[currentQuestion].ans
        
        # Checking answer
        if userAnswer.lower() == correctAnswer.lower():
            # Increasing count of correct answers
            numCorrect += 1
        else:
            # User answer is wrong therefore showing correct answer to user
            correctAnswerLabelText = "Correct Answer: " + correctAnswer
            self.correct_answer_label.config(text=correctAnswerLabelText) 
        
        # Displaying total score
        self.score_label.config(text="Score: {}/{}".format(numCorrect, len(randomQuestions)))
        
        # Moving to next question
        currentQuestion += 1
        if currentQuestion < len(randomQuestions):
            global questionText, answerEntry
            card = randomQuestions[currentQuestion]
            self.question_label_text.config(text=card.ques) 
            self.question_label_id.config(text=card.id) 
        else:
            self.score_label.config(text="Final Score: {}/{}. Now select a subject and click on Start Quiz.".format(numCorrect, len(randomQuestions)))
            self.submit_answer_button.config(state='disabled')
            


# This is a mapping class for data stored in files for questions and answers
class flashCard:
        def __init__(self, id, ques, ans):
            self.id = id
            self.ques = ques
            self.ans = ans

# subclass JSONEncoder
class flashCardEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
               
root = Tk()
app = QuizApp(root)
root.mainloop()
