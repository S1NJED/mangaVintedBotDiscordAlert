import os

# Windows
if os.name == 'nt':
    cmd = 'python3 -m venv .venv && echo ".venv\Scripts\\activate && start.bat" > run.bat && start.bat && pip install -r requirements.txt'
    os.system(cmd)
else:
    cmd = 'python3 -m venv .venv && echo ".venv/bin/activate && ./start" > run.sh && chmod +x start  && ./start && pip3 install -r requirements.txt'
    os.system(cmd)    
