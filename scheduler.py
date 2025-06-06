import threading
import time
import os
from datetime import datetime
def run_predictions_periodically():
    while True:
        print(datetime.now().strftime("%H:%M:%S"))
        print("[Scheduler] Rulăm predicțiile...")
        os.system("python predictions.py")
        time.sleep(300)  # in secunde

# Rulează într-un thread separat
def start_scheduler():
    t = threading.Thread(target=run_predictions_periodically, daemon=True)
    t.start()
