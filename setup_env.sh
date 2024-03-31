conda create -n cs889 python=3.9
conda activate cs889
pip install -r requirements.txt
conda deactivate


# developerGPT
conda create -n developergpt python=3.10
conda activate developergpt
pip install developergpt
conda deactivate

# run the background process for task 6
bash ./UserTest/template/Task-6/Run\ by\ researcher/backup_script.sh &
bash ./UserTest/template/Task-6/Run\ by\ researcher/monitor.sh &

conda activate cs889
cd UserTestWebPage/
python usertestwebsite.py