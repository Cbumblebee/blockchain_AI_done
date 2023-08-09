# blockchain_AI

(You should have installed python, pip, and curl first)

Open cmd prompt and go to the path, where blockchain_try1.py is. 


Then, write: python blockchain_try1.py

on another cmd prompt, you write different cURL requests you need:
for the transaction:
  curl "http://127.0.0.1:5000/txion" -d "{\"from\": \"akjflw\", \"to\": \"fjlakdj\", \"amount\": 3}" -H "Content-Type: application/json"
for displaying all blocks:
  curl "http://127.0.0.1:5000/blocks"
for mining:
  curl "http://127.0.0.1:5000/mine"

in PowerShell, you might need to replace "curl" with: C:\Windows\System32\curl.exe

if this works, you can then use the cmd prompt to open make_worksteps2_wtinker.py (make sure you have the realsense camera plugged into your device!)

Then, open the file called test.ipynb and run both first blocks. This will start the camera recording and the yolo application simultaneously. 

If you have done all of these steps, you have run the whole project. With the curl for mining or for displaying all blocks, you can see the whole history on the blockchain ^--^