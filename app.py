from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/start-script', methods=['GET'])
def start_script():
    subprocess.run(["python3", "androidLiaison.py"])  
    return "Script lancé avec succès"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)