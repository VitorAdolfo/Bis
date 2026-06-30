#Importando bibliotecas
import os
import sys
import json
import time
import subprocess
from datetime import datetime

#Caminhos do Projeto
project_path = os.path.dirname(__file__)
requirements_path = os.path.join(project_path, "requirements.txt")
project_metadata_path = os.path.join(project_path, "project_metadata.json")

#Interpretador python do Venv
python_venv = os.path.join(project_path, "venv","Scripts","python.exe") if os.name == "nt" else os.path.join(project_path, "venv","bin","python")

#Garante um ambiente virtual
if not os.path.exists(python_venv):
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    except subprocess.CalledProcessError:
        print("[ERRO] Não foi possível criar o ambiente virtual python venv")
        print("[MOTIVO] A instalação do pacote venv está incompleta")
        sys.exit(1)

#Verifica os metadados do projeto
def need_update() -> bool:
    if not os.path.exists(project_metadata_path):
        return True

    with open(project_metadata_path,"r",encoding="utf-8") as file:
        data = json.load(file)
        if not data.get("timestamp"):
            return True
        if (time.time() - data["timestamp"]) > 86400:
            return True

#Atualiza o ambiente virtual
if os.path.exists(requirements_path) and need_update():
    try:
        subprocess.check_call([python_venv,"-m","pip","install","--upgrade","pip"])
        subprocess.check_call([python_venv,"-m","pip","install","-r","requirements.txt","--upgrade"])
        with open(project_metadata_path,"w",encoding="utf-8") as file:
            json.dump({
                "last_update":datetime.now().isoformat(timespec="seconds"),
                "timestamp":time.time()
            }, file)
    
    except Exception as error:
        print("[ERRO] Não foi possível atualizar o ambiente virtual")
        print(f"[MOTIVO] {error}")

#Iniciando o Bot
try:
    subprocess.check_call([python_venv,"bot.py"])
except KeyboardInterrupt:
    print("Processo finalizado manualmente")
except Exception as error:
    print("[ERRO] Processo foi finalizado de forma forçada")
    print(f"[MOTIVO] {error}")
