def get_productivity_advice(tasks):

    if not tasks:
        return "You don't have any tasks yet. Add a task to get started!"

    pending = [
        task for task in tasks
        if task.status == "Pending"
    ]

    completed = [
        task for task in tasks
        if task.status == "Completed"
    ]

    advice = []

    advice.append(
        f"You currently have {len(pending)} pending task(s)."
    )

    advice.append(
        f"You have completed {len(completed)} task(s)."
    )

    high_priority = [
        task for task in pending
        if task.priority == "High"
    ]

    if high_priority:
        advice.append(
            f"You have {len(high_priority)} high-priority task(s). "
            "Consider completing these first."
        )
    else:
        advice.append(
            "You currently have no high-priority pending tasks."
        )

    if len(pending) > 5:
        advice.append(
            "Try breaking large tasks into smaller tasks."
        )
    else:
        advice.append(
            "Your workload looks manageable. Keep going!"
        )

    return "\n\n".join(advice)