from flask import Flask, request, redirect, url_for, session, jsonify
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask_cors import CORS, cross_origin
import urllib.request
import re
import datetime
import os
import openai

os.chdir(os.path.dirname(os.path.abspath(__file__))) # Making sure your directory is the backend folder

cred = credentials.Certificate("secrets/serviceAccount.json")
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
cors = CORS(app)

openai.api_key = "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"

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    fname = request.form['fname']
    lname = request.form['lname']
    gender = request.form['gender']
    goal = request.form['goal']
    days = request.form['days']
    weight = request.form['weight']
    height = request.form['height']
    buildMuscle = request.form['buildMuscle']
    muscleType = request.form['muscleType']
    age = request.form['age']

    fname = fname.capitalize()
    lname = lname.capitalize()
    if muscleType == "":
        muscleType = "everything"

    prompt = f"A person wants to {buildMuscle} weight and build muscle for {muscleType}. They are {weight}lbs and are {height} inches tall. The person only wants to work out for {days} days out of the week. Respond only in one JSON response, with the response being an array of days, with each day having an array of workouts (\"workouts\"), a day number (\"day\"), and a specific body part focus (\"focus\"). Each workout in the array will have a workout name (\"name\"), a number of reps (\"reps\"), and a number of sets(\"sets\"). Do not include \\n or \\t in any response.",
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
    )
    workoutPlan = response["choices"][0]["text"]
    
    if email is None or password is None:
        return {'message': 'Please fill in all fields'}, 400
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=fname,
        )
        db.collection("Accounts").document(user.uid).set({
          "email": email,
          "id": user.uid,
          "fname": fname,
          "lname": lname,
          "goal": goal,
          "weight": weight,
          "height": height,
          "buildMuscle": buildMuscle,
          "muscleType": muscleType,
          "days": days,
          "workoutPlans": workoutPlan,
          "nutritionLog": [],
          "waterLog": [],
          "gender": gender,
          "age": age
        })

        return jsonify({'message': f'Successfully created user {user.uid}'}),200
    except Exception as e:
        return {'message': f'Error creating user {e}'},400

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/workout_plan', methods=['POST'])
@cross_origin()
def workout_plan():
    uid = request.get_json()['uid']
    resp = jsonify({'message': db.collection('Accounts').document(uid).get().to_dict()['workoutPlans']}), 200
    return resp

@app.route('/account_info', methods=['POST'])
@cross_origin()
def account_info():
    uid = request.get_json()['uid']
    resp = db.collection('Accounts').document(uid).get().to_dict()
    target = dict(targets(uid))
    resp['target'] = target
    return jsonify(resp), 200


@app.route('/account_save', methods=['POST'])
@cross_origin()
def account_save():
    uid = request.get_json()['uid']
    data = request.get_json()['data']
    resp = db.collection('Accounts').document(uid).set(data)
    return jsonify({ 'ok': 'yes'}), 200

@app.route('/regenerate', methods=['POST'])
@cross_origin()
def regenerate():
    uid = request.get_json()['uid']

    doc = db.collection('Accounts').document(uid).get().to_dict()
    days = doc['days']
    weight = doc['weight']
    height = doc['height']
    buildMuscle = doc['buildMuscle']
    muscleType = doc['muscleType']
    
    prompt = f"A person wants to {buildMuscle} weight and build muscle for {muscleType}. They are {weight}lbs and are {height} inches tall. The person only wants to work out for {days} days out of the week. Respond only in one JSON response, with the response being an array of days, with each day having an array of workouts (\"workouts\"), a day number (\"day\"), and a specific body part focus (\"focus\"). Each workout in the array will have a workout name (\"name\"), a number of reps for one set (\"reps\"), and a number of sets (\"sets\"). Do not include \\n or \\t in any response.",
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
    )
    db.collection("Accounts").document(uid).update({
        "workoutPlans": response["choices"][0]["text"]
    })

    return jsonify({'message': response["choices"][0]["text"]})
    
@app.route('/nutrition', methods=['POST'])
@cross_origin()
def nutrition():
    food = request.get_json()['food']
    uid = request.get_json()['uid']

    prompt = f"Tell me the macros for {food}. Respond only in one JSON response, with the response being an object of all the macros and the food name (\"name\"). The six main nutrients are calories, protein, carbs, fats, sodium, and sugar. Include these EXACTLY as typed. Include the macro values in a string with the unit. The json should be formatted with the macro: value, and one key-value for each macro. Keep all JSON keys lowercased and exactly how I specified them."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=500,
    )

    db.collection("Accounts").document(uid).update({
        "nutritionLog": firestore.ArrayUnion([
            {
                "foodData": response["choices"][0]["text"],
                "time": datetime.datetime.now().isoformat()
            }
        ])
    })

    return jsonify({'data': response["choices"][0]["text"]}), 200

@app.route('/videoSearch', methods=['POST'])
def videoSearch():
    workout = request.get_json()['workout'] + " tutorial"
    workout = re.sub(r'\s', '-', workout)
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + workout)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    firstVideo = "https://www.youtube.com/watch?v=" + video_ids[0]

    return jsonify({'data': firstVideo}), 200

def targets(uid):
    data = db.collection('Accounts').document(uid).get().to_dict()
    age = float(data['age'])
    height = float(data['height']) * 2.54 # height in cm
    weight = float(data['weight']) / 2.25 # height in kg
    goal = data['goal']
    gender = data['gender']
    protein = float(data['weight'])

    # BMR Formula https://www.garnethealth.org/news/basal-metabolic-rate-calculator#:~:text=Your%20basal%20metabolism%20rate%20is,4.330%20x%20age%20in%20years)

    if gender == "m":
        calories = 13.397 * weight + 4.799 * height - 5.677 * age + 88.362
    else:
        calories = 9.247 * weight + 3.098 * height - 4.330 * age + 447.593
    if goal == "lose":
        calories = calories - 250
    elif goal == "gain":
        calories = calories + 250

    data = db.collection('Accounts').document(uid).get().to_dict()
    weight = float(data['weight'])
    water_log = data['waterLog']

    reccommended_amount = weight / 2 # half an ounce of water for every pound u weigh
    
    water_today = 0
    for log in water_log:
        if log['date'] == datetime.datetime.now().strftime("%Y-%m-%d"):
            water_today += float(log['waterData'])

    waterAmt = reccommended_amount - water_today

    if calories < 0:
        calories = 0
    if waterAmt < 0:
        waterAmt = 0
    if protein < 0:
        protein = 0

    resp = {
        'food': int(calories), 
        'water': int(waterAmt),
        'protein': int(protein)
    }
    return resp

@app.route('/waterLog', methods=['POST'])
def water_log():
    uid = request.get_json()['uid']
    water = request.get_json()['water'] # in ounces please

    data = {
        "waterData": water,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.datetime.now().strftime("%H:%M:%S")
    }

    db.collection("Accounts").document(uid).update({
        "waterLog": firestore.ArrayUnion([data])
    })

    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)