from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1


@app.route("/tasks", methods=["POST"])
def create_task():
  global task_id_control
  data = request.get_json()

  if not data:
    return jsonify({"message": "No data provided"}), 400

  new_task = Task(id=task_id_control, title=data['title'], description=data['description'])
  task_id_control += 1
  tasks.append(new_task)
  return jsonify({"message": "Task created successfully", "id": new_task.id}), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
  task_list = [task.to_dict() for task in tasks]

  output = {
    "tasks": task_list,
    "total_tasks": len(tasks)
  }

  return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  for t in tasks:
    if t.id == id:
      return jsonify(t.to_dict())
  
  return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
  data = request.get_json()

  if not data:
    return jsonify({"message": "No data provided"}), 400

  for t in tasks:
    if t.id == id:
      t.title = data['title']
      t.description = data['description']
      return jsonify({"message": "Task updated successfully"}), 200
  
  return jsonify({"message": "Task not found"}), 404
  
@app.route('/tasks/complete/<int:id>', methods=['PUT'])
def complete_task(id):
  for t in tasks:
    if t.id == id:
      t.completed = True
      return jsonify({"message": "Task completed successfully"}), 200
  
  return jsonify({"message": "Task not found"}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
  for t in tasks:
    if t.id == id:
      tasks.remove(t)
      return jsonify({"message": "Task deleted successfully"}), 200
  
  return jsonify({"message": "Task not found"}), 404



if __name__ == "__main__":
  app.run(debug=True)