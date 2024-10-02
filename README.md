SETUP ENVIRONMENT WINDOWS
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt

SETUP ENVIRONMENT ANACONDA
conda create --name .venv python=3.10.11
conda activate main-ds
pip install -r requirements.txt

RUN STREAMLIT APP
streamlit run dashboard.py