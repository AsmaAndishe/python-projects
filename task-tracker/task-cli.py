import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"

# ------------------ Utility Functions ------------------

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)

def get_new_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

# ------------------ Commands ------------------

def add_task(description):
    tasks = load_tasks()
    new_id = get_new_id(tasks)
    now = datetime.now().isoformat()

    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def update_task(task_id, description):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if not task:
        print("Task not found!")
        return

    task["description"] = description
    task["updatedAt"] = datetime.now().isoformat()
    save_tasks(tasks)
    print("Task updated successfully.")

def delete_task(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if not task:
        print("Task not found!")
        return

    tasks.remove(task)
    save_tasks(tasks)
    print("Task deleted successfully.")
    
def mark_status(task_id, new_status):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if not task:
        print("Task not found!")
        return

    task["status"] = new_status
    task["updatedAt"] = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"Task marked as {new_status}.")


def list_tasks(filter_status=None):
    tasks = load_tasks()

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("No tasks found.")
        return

    for t in tasks:
        print(f"[{t['id']}] {t['description']} - {t['status']}")

# ------------------ CLI Dispatcher ------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        add_task(" ".join(sys.argv[2:]))

    elif command == "update":
        update_task(int(sys.argv[2]), " ".join(sys.argv[3:]))

    elif command == "delete":
        delete_task(int(sys.argv[2]))

    elif command == "mark-in-progress":
        mark_status(int(sys.argv[2]), "in-progress")

    elif command == "mark-done":
        mark_status(int(sys.argv[2]), "done")

    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        else:
            list_tasks(sys.argv[2])

    else:
        print("Unknown command!")


if __name__ == "__main__":
    main()