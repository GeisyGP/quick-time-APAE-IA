from flask import Flask, request, jsonify 
import json
from src.geneticAlgorithm import GeneticAlgorithm

app = Flask(__name__)

@app.route("/run-algorithm", methods=["POST"])
def runAlgorithm():
    if 'dataFile' not in request.files:
        return jsonify({"error": "File 'dataFile' is required"}), 400

    file = request.files['dataFile']

    if file.filename == '':
        return jsonify({"error": "File 'dataFile is require and cant be empty"}), 400

    if not file.filename.endswith('.json'):
        return jsonify({"error": "The file must be .json"}), 400

    try:
        content = file.read().decode('utf-8')
        data = json.loads(content)

        activities = data.get('activities')
        periods = data.get('periods')
        print("Activities", activities, "Periods", periods)
        if not activities or not periods:
            return jsonify({"error": "File must contain activities and periods"}), 400
        geneticAlgorithm = GeneticAlgorithm(activities, periods)
        best, conflicts = geneticAlgorithm.run()

        return jsonify({
            "message": "Algorithm successfully executed",
            "data": {
                "conflicts": conflicts,
                "best": best
            }
        }), 200

    except json.JSONDecodeError:
        return jsonify({"error": "The file is not a valid JSON"}), 400
