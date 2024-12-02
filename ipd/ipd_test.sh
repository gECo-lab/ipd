
. venv

rm runs/*.csv

cd /home/rivero/Dropbox/Workspace_Current/Projects/Apps/EcoSim/EcoSim_p/main/EcoSim_p/

python3 ecosimp.py /home/rivero/Dropbox/Workspace_Current/Projects/Apps/EcoSim/EcoSim_p/app/ipd/ipd/config.json "/home/rivero/Dropbox/Workspace_Current/Projects/Apps/EcoSim/EcoSim_p/app/ipd/ipd/models/model_test_01.json" "/home/rivero/Dropbox/Workspace_Current/Projects/Apps/EcoSim/EcoSim_p/app/ipd/ipd/scenarios/scenarios_test_01.json"

cd /home/rivero/Dropbox/Workspace_Current/Projects/Apps/EcoSim/EcoSim_p/app/ipd/ipd/

Rscript -e 'rmarkdown::render("analisys/ipd.rmd", output_format="html_document", output_dir="results")'

#firefox results/ipd.html&
sensible-browser results/ipd.html&
