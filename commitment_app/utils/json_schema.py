# utils/json_schema.py

def get_goal_json_schema():
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "deadline": {"type": "string", "format": "date"},
            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
        },
        "required": ["name", "deadline"],
    }
