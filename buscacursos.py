import requests
from bs4 import BeautifulSoup
import schedule
import time
from playsound import playsound

def play_notification_sound():
    try:
        playsound('notification.mp3')  # Make sure to have this file in the same directory
    except Exception as e:
        print(f"Couldn't play sound: {e}")

def check_semester_option():
    url = "https://buscacursos.uc.cl/"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            semester_select = soup.find('select', {'name': 'cxml_semestre'})
            
            if semester_select:
                option = semester_select.find('option', string="2024 Segundo Semestre")
                
                if option:
                    print("'2024 Segundo Semestre' Ta redy mi paipai")
                    print(f"Option found at {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    play_notification_sound()
                    return True  # Signal that we found the option
                else:
                    print("The option '2024 Segundo Semestre' is not yet , CALMA, CALMA.")
            else:
                print("No te encontre el  'Semestres' field.")
        else:
            print(f"Failed to access the website (NO pude po). Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

    print(f"Check completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    play_notification_sound()
    return False  # Signal to continue checking

def run_scheduled_check():
    if check_semester_option():
        return schedule.CancelJob  # This will stop the scheduled job

print("Script started (Partio el scripteo). Will check immediately and then every 15 minutes (cada 15 mins te chequeo).")
play_notification_sound()

# Perform an immediate check
if run_scheduled_check() != schedule.CancelJob:
    # Only schedule future checks if the first check didn't find the option
    schedule.every(15).minutes.do(run_scheduled_check)

    # Run the scheduled jobs
    while True:
        schedule.run_pending()
        if not schedule.jobs:  # If there are no more jobs, exit the loop
            break
        time.sleep(60)  # Sleep for 60 seconds between checks

print("Script has finished (uy) running as the semester option was found.\nYa haga su horario mario.")
play_notification_sound()
