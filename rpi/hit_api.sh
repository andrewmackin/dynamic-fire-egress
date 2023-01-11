python index.py &
sleep 5 && curl -X POST -H "Content-Type: application/json" -d '{"test": 200}' localhost:8101/alert