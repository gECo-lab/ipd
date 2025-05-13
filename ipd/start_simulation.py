import os
import json
import subprocess
import shutil
import webbrowser

def main():
    # Activate virtual environment (if needed, adjust path accordingly)
    venv_path = os.path.join(os.getcwd(), "venv")
    if os.path.exists(venv_path):
        activate_script = os.path.join(venv_path, "bin", "activate_this.py")
        with open(activate_script) as f:
            exec(f.read(), {'__file__': activate_script})

        # Read kernel_dir from config.json
    with open("config.json") as config_file:
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
    subprocess.run(["python3", "ecosimp.py", app_dir, model_file, scenarios_file], check=True)

    # Change back to the original directory
    os.chdir(app_dir)

    analisys_path = analisys_dir+analisys_file


    # Render the R Markdown file
    r_command = (
        'rmarkdown::render( "' + analisys_path + 
        '", output_format="html_document", output_dir= "' + 
        results_dir + 
        '")'
    )
    subprocess.run(["Rscript", "-e", r_command], check=True)

    # Open the resulting HTML file in the default web browser
    results_file = os.path.join(app_dir, results_dir, "ipd.html")
    if os.path.exists(results_file):
        webbrowser.open(f"file://{results_file}")
    else:
        print("Error: Results file not found.")

if __name__ == "__main__":
    main()