import os
from file_scanner import scan_folder
from content_reader import extract_content
from decision_engine import choose_or_create_category
from organizer import move_file, delete_empty_folders


def parse_ai_response(response):
    category = "Miscellaneous"
    reason = "No reason"

    for line in response.split("\n"):
        if "Category:" in line:
            category = line.split("Category:")[1].strip()
        if "Reason:" in line:
            reason = line.split("Reason:")[1].strip()

    return normalize_category(category), reason


# ---- Normalize similar names (very important) ----
def normalize_category(name):
    name = name.strip().lower()

    mapping = {
        "exam schedule": "Exam Schedules",
        "examination timetable": "Exam Schedules",
        "test schedule": "Exam Schedules",

        "poultry": "Poultry Farming",
        "poultry farming": "Poultry Farming",
        "chicken farming": "Poultry Farming",
    }

    return mapping.get(name, name.title())


def get_existing_folders(base_folder):
    return [
        f for f in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, f))
    ]


def preview_organization(project_folder):
    preview_results = []

    existing_folders = get_existing_folders(project_folder)
    files = scan_folder(project_folder)

    for file in files:
        content = extract_content(file)
        if not content.strip():
            continue

        ai_response = choose_or_create_category(
            content, file, existing_folders
        )

        category, reason = parse_ai_response(ai_response)

        preview_results.append({
            "file": file,
            "category": category,
            "reason": reason
        })

        # update existing list so next files reuse it
        if category not in existing_folders:
            existing_folders.append(category)

    return preview_results


def execute_organization(project_folder, preview_results):
    for item in preview_results:
        move_file(item["file"], project_folder, item["category"])

    delete_empty_folders(project_folder)
