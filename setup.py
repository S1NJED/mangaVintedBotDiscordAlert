import os

# Windows
if os.name == 'nt':
    cmd = 'python3 -m venv .venv && echo ".venv\Scripts\\activate && start.bat" > start.bat && start.bat'
    os.system(cmd)
else:
    cmd = 'python3 -m venv .venv && echo ".venv/bin/activate && ./start" > start.sh && chmod +x start  && ./start'
    os.system(cmd)    
