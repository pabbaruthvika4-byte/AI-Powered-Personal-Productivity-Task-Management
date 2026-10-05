import streamlit as st
import pandas as pd
import os

from database import (
    init_db,
    add_task,
    get_tasks,
    delete_task,
    complete_task
)

from ml_model import predict_priority


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Productivity System",
    page_icon="🤖",
    layout="wide"
)


# =====================================================
# DATABASE INITIALIZATION
# =====================================================

os.makedirs("data", exist_ok=True)

init_db()


# =====================================================
# TITLE
# =====================================================

st.title(
    "🤖 AI-Powered Personal Productivity & Task Management"
)

st.write(
    "Manage your tasks, prioritize your work, "
    "and track your productivity."
)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📌 Menu")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Add Task",
        "My Tasks",
        "AI Assistant",
        "Analytics"
    ]
)


# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.header("📊 Productivity Dashboard")

    tasks = get_tasks()

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task.status == "Completed"
    )

    pending_tasks = sum(
        1 for task in tasks
        if task.status == "Pending"
    )

    if total_tasks > 0:
        productivity = (
            completed_tasks / total_tasks
        ) * 100
    else:
        productivity = 0

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Tasks",
            total_tasks
        )

    with col2:
        st.metric(
            "Completed",
            completed_tasks
        )

    with col3:
        st.metric(
            "Pending",
            pending_tasks
        )

    with col4:
        st.metric(
            "Productivity",
            f"{productivity:.1f}%"
        )

    st.divider()

    st.subheader("📋 All Tasks")

    if tasks:

        task_data = []

        for task in tasks:

            task_data.append({
                "ID": task.id,
                "Task": task.title,
                "Category": task.category,
                "Priority": task.priority,
                "Status": task.status,
                "Due Date": task.due_date
            })

        df = pd.DataFrame(task_data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No tasks available. "
            "Go to 'Add Task' to create your first task."
        )


# =====================================================
# ADD TASK
# =====================================================

elif page == "Add Task":

    st.header("➕ Add New Task")

    title = st.text_input(
        "Task Title",
        placeholder="Example: Complete Python assignment"
    )

    description = st.text_area(
        "Task Description",
        placeholder="Enter task details..."
    )

    category = st.selectbox(
        "Category",
        [
            "Study",
            "Coding",
            "Project",
            "Assignment",
            "Personal",
            "Other"
        ]
    )

    urgency = st.selectbox(
        "Urgency",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    importance = st.selectbox(
        "Importance",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    due_date = st.date_input(
        "Due Date"
    )

    st.divider()

    # ---------------------------------------------
    # Predict Priority
    # ---------------------------------------------

    if st.button(
        "🤖 Predict Priority"
    ):

        predicted_priority = predict_priority(
            urgency,
            importance
        )

        st.session_state[
            "predicted_priority"
        ] = predicted_priority

        st.success(
            f"Predicted Priority: {predicted_priority}"
        )

    # Show current prediction
    if "predicted_priority" in st.session_state:

        st.info(
            "Current Priority: "
            + st.session_state["predicted_priority"]
        )

    st.divider()

    # ---------------------------------------------
    # Save Task
    # ---------------------------------------------

    if st.button(
        "💾 Save Task",
        type="primary"
    ):

        if title.strip() == "":

            st.error(
                "Please enter a task title."
            )

        else:

            priority = st.session_state.get(
                "predicted_priority",
                "Medium"
            )

            add_task(
                title=title,
                description=description,
                priority=priority,
                category=category,
                due_date=str(due_date)
            )

            # Remove old prediction
            if "predicted_priority" in st.session_state:
                del st.session_state[
                    "predicted_priority"
                ]

            st.success(
                "✅ Task added successfully!"
            )


# =====================================================
# MY TASKS
# =====================================================

elif page == "My Tasks":

    st.header("📝 My Tasks")

    tasks = get_tasks()

    if not tasks:

        st.info(
            "You don't have any tasks yet."
        )

    else:

        for task in tasks:

            st.subheader(
                f"#{task.id} - {task.title}"
            )

            st.write(
                f"**Description:** {task.description}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"📌 **Priority:** {task.priority}"
                )

            with col2:

                st.write(
                    f"📂 **Category:** {task.category}"
                )

            with col3:

                st.write(
                    f"📅 **Due Date:** {task.due_date}"
                )

            st.write(
                f"**Status:** {task.status}"
            )

            button_col1, button_col2 = st.columns(2)

            # Complete button
            with button_col1:

                if task.status == "Pending":

                    if st.button(
                        "✅ Complete",
                        key=f"complete_{task.id}"
                    ):

                        complete_task(task.id)

                        st.success(
                            "Task completed!"
                        )

                        st.rerun()

            # Delete button
            with button_col2:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task.id}"
                ):

                    delete_task(task.id)

                    st.success(
                        "Task deleted!"
                    )

                    st.rerun()

            st.divider()


# =====================================================
# AI ASSISTANT
# =====================================================

elif page == "AI Assistant":

    st.header("🤖 AI Productivity Assistant")

    st.write(
        "Get productivity suggestions based on your tasks."
    )

    tasks = get_tasks()

    if not tasks:

        st.info(
            "Add some tasks first."
        )

    else:

        pending = [
            task for task in tasks
            if task.status == "Pending"
        ]

        completed = [
            task for task in tasks
            if task.status == "Completed"
        ]

        high_priority = [
            task for task in pending
            if task.priority == "High"
        ]

        st.subheader("📊 Current Situation")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Pending Tasks",
                len(pending)
            )

        with col2:
            st.metric(
                "Completed Tasks",
                len(completed)
            )

        with col3:
            st.metric(
                "High Priority",
                len(high_priority)
            )

        st.divider()

        st.subheader("💡 Productivity Advice")

        if high_priority:

            st.warning(
                f"You have {len(high_priority)} "
                "high-priority task(s). "
                "Complete these first."
            )

        elif pending:

            st.info(
                "You have pending tasks. "
                "Try completing the most important task first."
            )

        else:

            st.success(
                "🎉 Excellent! All your tasks are completed."
            )


# =====================================================
# ANALYTICS
# =====================================================

elif page == "Analytics":

    st.header("📈 Productivity Analytics")

    tasks = get_tasks()

    if not tasks:

        st.info(
            "Add tasks to view analytics."
        )

    else:

        # ---------------------------------------------
        # Task Status
        # ---------------------------------------------

        completed = sum(
            1 for task in tasks
            if task.status == "Completed"
        )

        pending = sum(
            1 for task in tasks
            if task.status == "Pending"
        )

        st.subheader(
            "Task Completion"
        )

        status_data = pd.DataFrame({
            "Status": [
                "Completed",
                "Pending"
            ],
            "Tasks": [
                completed,
                pending
            ]
        })

        st.bar_chart(
            status_data.set_index("Status")
        )

        # ---------------------------------------------
        # Productivity
        # ---------------------------------------------

        total = len(tasks)

        productivity = (
            completed / total
        ) * 100

        st.subheader(
            "Productivity Score"
        )

        st.progress(
            int(productivity)
        )

        st.write(
            f"Your productivity score is "
            f"**{productivity:.1f}%**"
        )

        # ---------------------------------------------
        # Category Analysis
        # ---------------------------------------------

        st.subheader(
            "Tasks by Category"
        )

        category_counts = {}

        for task in tasks:

            category = task.category

            if category not in category_counts:
                category_counts[category] = 0

            category_counts[category] += 1

        category_data = pd.DataFrame({
            "Category": list(
                category_counts.keys()
            ),
            "Tasks": list(
                category_counts.values()
            )
        })

        st.bar_chart(
            category_data.set_index(
                "Category"
            )
        )