import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from websocket import create_connection

from task_manager.models import Task

scheduler = BackgroundScheduler()
scheduler.start()

LIVE2D_API_URI = "ws://127.0.0.1:10086/api"

def send_toast(task_id):
    task = Task.objects.get(id=task_id)
    data = {
        "msg": 11000,
        "msgId": 1,
        "data": {
            "id": 0,
            "text": f"你的任务 {task.name} 仅剩下一天时间了",
            "choices": [
                "我知道了",
                "不再提醒"
            ],
            "duration": -1
        }
    }
    try:
        ws = create_connection(LIVE2D_API_URI)
        ws.send(json.dumps(data))
        response_data = json.loads(ws.recv())
        button_index = response_data["data"]
        if button_index == 1:
            remove_task(task_id)
            print(f"设置任务{task_id}为不再提醒")


    except Exception as e:
        print("ERROR: ", str(e))

def schedule_task(task_id, run_time):
    # trigger = DateTrigger(run_date=run_time)

    trigger = IntervalTrigger(hours=2, start_date=run_time)

    scheduler.add_job(func=send_toast,
                      trigger=trigger,
                      args=[task_id],
                      id=f"task_{task_id}",
                      replace_existing=True
                      )
    print(f"任务 {task_id} 已安排在 {run_time}")
def remove_task(task_id):
    job_id = f"task_{task_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        return True
    else:
        print(f"Task {task_id} doesn't exist")
        return False
