from flask import Flask, render_template, request, redirect, session, url_for,jsonify
import json
import markdown
import os
import pandas as pd


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management
import markdown
import re

def parse_readme():
    device_descriptions = {}
    task_descriptions = {}
    with open('../UserTest/README.md', 'r') as file:
        content = file.read()
        # Example: Extracting device descriptions (you need to adapt this based on your actual README.md structure)
        # Regular expression to match the device sections
        device_pattern = re.compile(r'### Device (\d+): (.+?)\n- \*\*Description:\*\* (.+?)(?=\n###|\Z)', re.DOTALL)

        for match in device_pattern.finditer(content):
            device_id, device_name, description = match.groups()
            # Storing device info. Converting Markdown to HTML if necessary.
            device_descriptions[device_id] = {
                'name': device_name,
                'details': markdown.markdown(description)
            }
        # Similar extraction logic for task_descriptions goes here
        # Regex to match task sections, capturing task ID and details
        task_pattern = re.compile(r'### Task (\d+): (.+?)\n(.*?)(?=### Task|\Z)', re.DOTALL)
        tasks = task_pattern.findall(content)

        for task in tasks:
            task_id, task_name, details = task
            # Do not format here, just store the details as is
            task_descriptions[task_id] = {
                'name': task_name,
                'details': markdown.markdown(details.strip()).replace("\n", "<br>")
            }

    return device_descriptions, task_descriptions

device_descriptions, task_descriptions = parse_readme()

@app.route('/')
def index():
    if 'user_id' in session:
        # Assuming there's a function to determine the next device for the user
        next_device_id = get_next_device_for_user(session['user_id'])
        if next_device_id is not None:
            return render_template('index.html',next_page=url_for('device', device_id=next_device_id))
        else:
            return render_template('index.html', next_page=url_for('study_complete'))
    else:
        return render_template('index.html', next_page='')

def load_tasks_description():
    with open('README.md', 'r') as file:
        content = file.read()
        return markdown.markdown(content)

@app.route('/study_complete')
def study_complete():
    return render_template('study_complete.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        session['user_id'] = user_id
        # Redirect to the first device/task page
        _, next_device_id = determine_next_step(user_id, 0, load_user_progress(user_id), load_latin_square())
        return redirect(url_for('device', device_id=next_device_id))
    else:
        available_user_ids = get_available_user_ids()
        return render_template('register.html', available_user_ids=available_user_ids)

def get_available_user_ids():
    try:
        with open('time_recording.json', 'r') as file:
            records = json.load(file)
            used_ids = {record['userID'] for record in records}
            all_ids = set(range(1, 13))  # Assuming 12 users max
            return list(all_ids - used_ids)
    except (FileNotFoundError, json.JSONDecodeError):
        return list(range(1, 13))



@app.route('/device/<int:device_id>', methods=['GET'])
def device(device_id):
    if 'user_id' not in session:
        return redirect(url_for('register'))
    device_description = device_descriptions.get(str(device_id))
    # Assuming tasks is a list of task identifiers like ["Task-1", "Task-2"]
    return render_template('device_page.html', device_description=device_description['details'],
                           device_id=device_id,device_name=device_description['name'])

@app.route('/device/<int:device_id>/task/<task_id>', methods=['GET'])
def task(device_id, task_id):
    # Assuming user_id is stored in session and task details in task_descriptions
    user_id = session.get('user_id')
    task_id=task_id.split('-')[-1]
    if task_id=='0':
        return redirect(url_for('next_step',currentDeviceId=device_id))
    if task_id in task_descriptions:
        task = task_descriptions[task_id]
        task_name = task['name']
        # Now replace placeholders with actual values
        task_details = task['details'].replace("{user_id}", str(user_id)).replace("{task_id}", task_id)
        return render_template('task_page.html', task_name=task_name, task_details=task_details, device_name=device_id, task_id=task_id, user_id=user_id)
    else:
        return task_id, 404

def load_latin_square():
    csv_path = 'latin_square_tasks.csv'  # Adjust path as necessary
    return pd.read_csv(csv_path)

def get_next_device_for_user(user_id):
    # Placeholder: Read progress tracking data
    try:
        with open('time_recording.json', 'r') as file:
            records = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []

    # Assuming records is a list of dicts with 'userID' and 'deviceID' keys
    user_records = [record for record in records if record['userID'] == user_id]

    if not user_records:
        return 1  # No records found, start with the first device

    # Assuming device IDs are sequential integers starting at 1
    completed_devices = {int(record['deviceID'].split('-')[-1]) if isinstance(record['deviceID'],str) else record['deviceID']  for record in user_records}
    next_device = max(completed_devices) + 1 if completed_devices else 1

    # Assuming there are 3 devices in total
    if next_device > 3:
        return None  # All devices completed
    else:
        return next_device

def get_tasks_for_user_device(user_id, device_id):
    latin_square = load_latin_square()
    if isinstance(user_id, str):
        user_id = int(user_id)
    user_row = latin_square.loc[user_id - 1]

    if device_id == 1:
        device_tasks = user_row['Device 1 (Tasks)']
    elif device_id == 2:
        device_tasks = user_row['Device 2 (Tasks)']
    else:  # device_id == 3
        device_tasks = user_row['Device 3 (Tasks)']

    tasks = device_tasks.split(', ')
    return tasks

@app.route('/record_timing', methods=['POST'])
def record_timing():
    print("record_timing called")
    data = request.json
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'User not in session'}), 400

    # Append timing data to time_recording.json
    try:
        with open('time_recording.json', 'r') as file:
            try:
                records = json.load(file)
            except json.JSONDecodeError:
                print("json.JSONDecodeError")
                records = []
            assert isinstance(records, list)
            records.append({
                'userID': user_id,
                'taskID': data['taskId'],
                'deviceID': data['deviceId'],
                'startTime': data['startTime'],
                'endTime': data['endTime'],
                'duration': data['duration']
            })
        with open('time_recording.json', 'w') as file:
            json.dump(records, file)
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/next_step', methods=['POST', 'GET'])
def next_step():
    user_id = session.get('user_id')
    if request.method == 'POST':
        print("next_step called post")
        print(request.json)
        data = request.json
        current_device_id = int(data['currentDeviceId'])  # Ensure this is an integer for comparisons
    else:
        print("next_step called get")
        current_device_id = int(request.args.get('device_id'))
    # Load user's progress and Latin square
    user_progress = load_user_progress(user_id)
    latin_square = load_latin_square()

    # Find next task and device based on current progress
    next_task, next_device = determine_next_step(user_id, current_device_id, user_progress, latin_square)
    print("next_task",next_task)
    print("next_device",next_device)
    # Determine action based on whether a next task/device was found
    if next_task and next_device:
        action = 'next_task'
        if request.method == 'POST':
            return jsonify({
                'action': action,
                'deviceId': next_device,
                'taskId': next_task
            })
        return redirect(url_for('task', device_id=next_device, task_id=next_task))
    elif not next_task and next_device:
        action = 'next_device'
        if request.method == 'POST':
            return jsonify({
                'action': action,
                'deviceId': next_device
            })
        return redirect(url_for('device', device_id=next_device))
    else:
        action = 'complete'
        if request.method == 'POST':
            return jsonify({
                'action': action
            })
        return render_template('study_complete.html')

    # return jsonify({
    #     'action': action,
    #     'deviceId': next_device,
    #     'taskId': next_task
    # })
def load_user_progress(user_id):
    try:
        with open('time_recording.json', 'r') as file:
            records = json.load(file)
        user_records = [record for record in records if record['userID'] == str(user_id)]
        return user_records
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def determine_next_step(user_id, current_device_id, user_progress, latin_square):
    # Identify completed tasks for the current device
    print("current_device_id",current_device_id)
    completed_tasks = [record['taskID'] for record in user_progress if int(record['deviceID']) == current_device_id]

    # Get tasks for the current device from the Latin square
    if current_device_id>0:
        current_device_tasks = get_tasks_for_user_device(user_id, current_device_id)
        for i in range(len(current_device_tasks)):
            current_device_tasks[i]=current_device_tasks[i].split('-')[-1]
        print("current_device_tasks",current_device_tasks)
        print("completed_tasks",completed_tasks)
        # Find the first uncompleted task for the current device
        for task in current_device_tasks:
            if task not in completed_tasks:
                return task, current_device_id  # Next task in current device

    user_id = int(session['user_id'])
    device_id_sequence = []
    device_name2id = {
        "Normal Terminal with ChatGPT": 1,
        "Terminal with Built-in LLM": 2,
        "Web Terminal with Chatbox": 3
    }
    user_row = latin_square.loc[user_id - 1]
    device_id_sequence.append(device_name2id[user_row['Device 1']])
    device_id_sequence.append(device_name2id[user_row['Device 2']])
    device_id_sequence.append(device_name2id[user_row['Device 3']])
    print("device_id_sequence",device_id_sequence)
    # If all tasks in the current device are completed, check for next device
    if current_device_id == 0:
        return None, device_id_sequence[0]
    if current_device_id != device_id_sequence[-1]:  # Assuming there are 3 devices
        next_device_id = device_id_sequence[device_id_sequence.index(current_device_id) + 1]
        return None, next_device_id
    else:
        return None, None

if __name__ == '__main__':
    app.run(debug=True, port=5002)
