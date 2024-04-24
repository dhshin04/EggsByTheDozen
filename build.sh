# Shell Script to install Python packages in requirements.txt once app deployed
if [ "$NODE_ENV" == "development" ]; then
    pip install -r requirements.txt
fi