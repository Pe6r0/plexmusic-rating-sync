python -m venv ./venv
venv\Scripts\Activate.ps1
pip install plexapi
pip install plexapi[alert]
pip install eyeD3
pip install eyeD3[display-plugin]
pip install python-magic-bin
python script.py
deactivate
pip list