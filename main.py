#Importando bibliotecas
import os
import sys
import subprocess

#Verifica a existência do ambiente virtual
python_venv = os.path.join(os.path.dirname(__file__),"venv","Scripts","python.exe") if os.name == "nt" else os.path.join(os.path.dirname(__file__),"venv","bin","python")

#Garante um ambiente virtual
if not os.path.exists(python_venv):
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    except subprocess.CalledProcessError:
        print("[ERRO] Não foi possível criar o ambiente virtual python venv")
        print("[MOTIVO] A instalação do pacote venv está incompleta")
        sys.exit(1)

#Atualiza o ambiente virtual
try:
    subprocess.check_call([python_venv,"-m","pip","install","--upgrade","pip"])
    subprocess.check_call([python_venv,"-m","pip","install","-r","requirements.txt","--upgrade"])
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
