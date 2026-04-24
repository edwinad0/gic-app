to create and activate virtual environment 
    python3 -m venv .venv 
    source .venv/bin/activate 

to run app: 
    python app.py 

output:
    Address already in use
    Port 8050 is in use by another program. Either identify and stop that program, or start the server with a different port.

    need to kill current port and run again 
        lsof -i :8050 
        kill -9 <PID> 