
print("script started")


from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Meal Planner API!"})

if __name__ == '__main__':
    app.run(debug=True)
