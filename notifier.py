from plyer import notification
import sys

if len(sys.argv) < 2:
    sys.exit()

task_name = sys.argv[1]

notification.notify(
    title="Task Manager",
    message=f"its time to do «{task_name}»! 🔔",
    timeout=10
)