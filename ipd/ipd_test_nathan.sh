
. venv

rm runs/*.csv

app_dir=$(pwd)

kernel_dir=$"/home/nathan/home/UFCG/gEco/Projetos/EcoSim_p/kernel"

cd "$kernel_dir"

python3 /home/nathan/home/UFCG/gEco/Projetos/EcoSim_p/ecosimp.py "$app_dir" "model_test_02.json" "scenarios_test_02.json"

cd "$app_dir"

Rscript -e 'rmarkdown::render("analisys/ipd.rmd", output_format="html_document", output_dir="results")'

firefox results/ipd.html&

#sensible-browser results/ipd.html&
