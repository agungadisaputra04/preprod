cd ~/preprod
source preprod/bin/activate
uvicorn main:app --host 0.0.0.0 --port 9000
