#Importando bibliotecas
import os
import sys
import subprocess

#Verifica a existência do ambiente virtual
python_venv = os.path.join("venv","Scripts","python.exe") if os.name == "nt" else os.path.join("venv","bin","python")

#Garante um ambiente virtual
if not os.path.exists(python_venv):
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    except subprocess.CalledProcessError:
        print("[ERRO] Não foi possível criar o ambiente virtual python venv")
        print("[MOTIVO] A instalação do pacote venv está incompleta")

#Atualiza o ambiente virtual
subprocess.check_call([python_venv,"-m","pip","install","--upgrade","pip"])
subprocess.check_call([python_venv,"-m","pip","install","-r","requirements.txt","--upgrade"])

#Iniciando o Bot
try:
    subprocess.check_call([python_venv,"bis_bot.py"])
except:
    print("processo encerrado")
