import subprocess
#uruchamia wszystkie programy po sobie

subprocess.call(["python", "pobranie_piosenki.py"])

subprocess.call(["python", "AI.py"])

subprocess.call(["python", "zwrócenie_piosenki.py"])