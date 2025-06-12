import speech_recognition as sr
import pyttsx3
import json
import os

engine = pyttsx3.init()

TASK_FILE = "tasks.json"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that.")
        return ""
    except sr.RequestError:
        speak("API unavailable.")
        return ""

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

def add_task(task, tasks):
    tasks.append(task)
    save_tasks(tasks)
    speak(f"Task added: {task}")

def list_tasks(tasks):
    if not tasks:
        speak("You have no tasks.")
    else:
        for i, task in enumerate(tasks, 1):
            speak(f"{i}. {task}")

def remove_task(task, tasks):
    if task in tasks:
        tasks.remove(task)
        save_tasks(tasks)
        speak(f"Task completed and removed: {task}")
    else:
        speak("Task not found.")

if __name__ == "__main__":
    speak("Voice-controlled To-Do List started.")
    tasks = load_tasks()

    while True:
        speak("What would you like to do? Add, list, or complete a task. Say quit to exit.")
        command = listen()

        if "add" in command:
            speak("What is the task?")
            task = listen()
            if task:
                add_task(task, tasks)

        elif "list" in command:
            list_tasks(tasks)

        elif "complete" in command or "remove" in command:
            speak("Which task did you complete?")
            task = listen()
            if task:
                remove_task(task, tasks)

        elif "quit" in command or "exit" in command:
            speak("Goodbye!")
            break
