import threading
import time
import os
from datetime import datetime

def run_predictions_periodically():
    while True:
        now = datetime.now()
        with open("last_run.txt", "w") as f:
            f.write(now.isoformat())

        print("[Scheduler] Rulăm predicțiile...")
        os.system("python predictions.py")
        time.sleep(120)

# Rulează într-un thread separat
def start_scheduler():
    t = threading.Thread(target=run_predictions_periodically, daemon=True)
    t.start()
