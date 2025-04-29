
. venv

rm runs/*.csv

app_dir=$(pwd)

kernel_dir=$(python3 -c "import json; print(json.load(open('config.json'))['paths']['kernel'])")

cd "$kernel_dir"

python3 ecosimp.py "$app_dir" "model_test_02.json" "scenarios_test_02.json"

cd /home/rivero/Dropbox/Workspace_Current/Projects/Apps/EcoSim/EcoSim_p/apps/ipd/ipd/

Rscript -e 'rmarkdown::render("analisys/ipd.rmd", output_format="html_document", output_dir="results")'

firefox results/ipd.html&
#sensible-browser results/ipd.html&
