import os
import json
import anthropic
from slack import WebClient
from slack_bolt import App
from tool_processor import process_tool_call, tools, MESSAGES

# 이미 존재하는 모듈 (calendar_functions, utils)는 그대로 사용합니다.
from calendar_functions import create_event, delete_event, check_event
from utils import retrieve_context

# Slack API 초기화
app = App(token=os.environ['SLACK_BOT_TOKEN'])
slack_client = WebClient(os.environ['SLACK_BOT_TOKEN'])
anthropic_client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

@app.event("app_mention")
def handle_message_events(body, logger):
    # 사용자 메시지 파싱 (멘션 이후 텍스트)
    user_text = str(body["event"]["text"]).split(">")[1]
    logger.info(f"User Message: {user_text}")
    
    # 슬랙에 처리중임을 알림 메시지 전송
    slack_client.chat_postMessage(
        channel=body["event"]["channel"],
        thread_ts=body["event"]["event_ts"],
        text="안녕하세요, 개인 비서 슬랙봇입니다! :robot_face:\n곧 전달 주신 문의사항 처리하겠습니다!"
    )
    
    # 사용자 메시지를 기록
    MESSAGES.append({
        "role": "user",
        "content": user_text
    })

    # Anthropic API 호출 (툴 리스트를 함께 전달)
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        tools=tools,
        messages=MESSAGES,
    )
    logger.info(f"Initial Response:\nStop Reason: {message.stop_reason}\nContent: {message.content}")

    # 만약 툴 사용 요청이 있다면 처리
    if message.stop_reason == "tool_use":
        tool_use = next(block for block in message.content if getattr(block, "type", None) == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input

        logger.info(f"Tool Used: {tool_name}\nTool Input: {tool_input}")

        tool_result = process_tool_call(tool_name, tool_input)
        logger.info(f"Tool Result: {tool_result}")

        # 툴 결과를 Anthropic API에 다시 전달
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            messages=MESSAGES + [
                {"role": "assistant", "content": message.content},
                {
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": json.dumps(tool_result),
                    }],
                },
            ],
            tools=tools,
        )
    else:
        response = message

    # 최종 응답 파싱
    final_response = next(
        (block.text for block in response.content if hasattr(block, "text")),
        None,
    )
    logger.info(f"Final Response: {final_response}")

    # 슬랙 스레드에 최종 응답 전송
    slack_client.chat_postMessage(
        channel=body["event"]["channel"], 
        thread_ts=body["event"]["event_ts"],
        text=final_response
    )
    MESSAGES.append({"role": "assistant", "content": final_response})
    return
