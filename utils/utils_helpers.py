def calculate_productivity(tasks):

    if not tasks:
        return 0

    completed = sum(
        1 for task in tasks
        if task.status == "Completed"
    )

    return round((completed / len(tasks)) * 100, 2)