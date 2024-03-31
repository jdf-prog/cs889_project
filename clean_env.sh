# clean_env.sh
# Path: clean_env.sh
conda deactivate
conda remove -n cs889 --all
conda remove -n developergpt --all

# kill the background process for task 6 after the environment is cleaned
pkill -f backup_script.sh
pkill -f monitor.sh