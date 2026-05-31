import time, os
time.sleep(3)
with open(os.path.join(os.path.dirname(__file__), "pythonw_ok.txt"), "w") as f:
    f.write("pythonw works")
