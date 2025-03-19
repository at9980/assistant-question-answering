import json
from calendar_functions import create_event, delete_event, check_event
from utils import retrieve_context

# Anthropic API와 슬랙 앱 전역에서 사용할 메시지 리스트
MESSAGES = []

def process_tool_call(tool_name, tool_input):
    if tool_name == "create_event":
        return create_event(**tool_input)
    elif tool_name == "delete_event":
        return delete_event(**tool_input)
    elif tool_name == "check_event":
        return check_event(**tool_input)
    elif tool_name == "retrieve_context":
        return retrieve_context(**tool_input)
    else:
        return {"error": f"Unknown tool: {tool_name}"}

# Anthropic API에 전달할 tools 리스트
tools = [
    {
        "name": "create_event",
        "description": "Create new Google Calender Event",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Name of Google Calender Event"
                },
                "start": {
                    "type": "string",
                    "description": "Starting date of Google Calender Event in UTC+9 Time i.e. 2024-08-08T09:00:00+09:00"
                },
                "end": {
                    "type": "string",
                    "description": "Ending date of Google Calender Event in UTC+9 Time i.e. 2024-08-08T10:00:00+09:00"
                }
            },
            "required": ["summary", "start"]
        }
    },
    {
        "name": "check_event",
        "description": "Check Google Calender Events",
        "input_schema": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "string",
                    "description": "Starting date of Google Calender Event in UTC+9 Time i.e. 2024-08-08T09:00:00+09:00"
                },
                "end": {
                    "type": "string",
                    "description": "Ending date of Google Calender Event in UTC+9 Time i.e. 2024-08-08T10:00:00+09:00"
                }
            },
            "required": ["start", "end"]
        }
    },
    {
        "name": "delete_event",
        "description": "Delete Google Calender Event. Delete immediately if you already have Calendar Event ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Unique ID of Calendar Event. Can be fetched using check_event()"
                }
            },
            "required": ["id"]
        }
    },
    {
        "name": "retrieve_context",
        "description": "Retrieve top-1 context relevant to given question about ABC 컴퍼니. Any question related to company should point to this function.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Question related to Korean firm ABC 컴퍼니."
                }
            },
            "required": ["question"]
        }
    },
]
