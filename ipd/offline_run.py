# Importando as bibliotecas necessárias
import os
import json
import subprocess
from pathlib import Path

# Configurando os diretórios
input_dir = Path("runs")
output_dir = Path("results")
output_dir.mkdir(exist_ok=True)

def main():
    # Activate virtual environment (if needed, adjust path accordingly)
    venv_path = os.path.join(os.getcwd(), "venv")
    if os.path.exists(venv_path):
        activate_script = os.path.join(venv_path, "bin", "activate_this.py")
        with open(activate_script) as f:
            exec(f.read(), {'__file__': activate_script})

    # Read kernel_dir from config.json
    config_json_file = "config_zd_base.json"        
    with open('config_zd_base.json') as config_file:
        config = json.load(config_file)
        kernel_dir = config["paths"]["kernel"]
        analisys_dir = config["paths"]["analisys"]
        results_dir = config["paths"]["results"]
        runs_dir = config["paths"]["runs"]
        model_file = config["files"]["model"]
        scenarios_file = config["files"]["scenarios"]
        analisys_file = config["files"]["analisys"]

    # Remove CSV files in the 'runs' directory
    if os.path.exists(runs_dir):
        for file in os.listdir(runs_dir):
            if file.endswith(".csv"):
                os.remove(os.path.join(runs_dir, file))

    # Get current directory as app_dir
    app_dir = os.getcwd()

    # Change directory to kernel_dir and run ecosimp.py
    os.chdir(kernel_dir)
    subprocess.run(["python3", "ecosimp.py", app_dir, config_json_file, model_file, scenarios_file], check=True)

    # Change back to the original directory
    os.chdir(app_dir)

if __name__ == "__main__":
    main()
