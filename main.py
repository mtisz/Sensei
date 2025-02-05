import json
import numpy as np

from concurrent.futures import ThreadPoolExecutor
from llm_handler import send_to_llm
from params import OUTPUT_FILE_PATH, NUM_WORKERS, PROVIDER, NUM_TURNS
from utils import get_code_topics, get_general_topics

from system_messages import (
    SYSTEM_MESSAGES_ORCA,
    SYSTEM_MESSAGES_TESS,
    SYSTEM_MESSAGES_CODE,
    SYSTEM_MESSAGES_FOLLOW_UP,
)

code_data = True

if code_data:
    TOPICS = get_code_topics()
    SYSTEM_MESSAGES = SYSTEM_MESSAGES_CODE
    PROMPT_1 = """For the following SUBJECT_AREA, generate a question that covers a very narrow topic in the SUBJECT_AREA, with sufficient depth and breadth. The topic in the question should be important to the SUBJECT_AREA, with known-answers present. The generated question should be detailed, seek true nature of our universe from first principles, curiosity invoking, thought provoking, difficult, and also should be able to be answered by an intelligence like yourself. The question *must* seek an answer in the form of lengthy computer code. Only return the question."""


else:
    TOPICS = get_general_topics()
    SYSTEM_MESSAGES = SYSTEM_MESSAGES_ORCA + SYSTEM_MESSAGES_TESS
    PROMPT_1 = """For the following SUBJECT_AREA, generate a question that covers a very narrow topic in the SUBJECT_AREA, with sufficient depth and breadth. The topic in the question should be important to the SUBJECT_AREA, with known-answers present. The generated question should be detailed, seek true nature of our universe from first principles, curiosity invoking, thought provoking, and also should be able to be answered by an intelligence like yourself. Make sure the question is sufficiently harder, like a graduate level course question. Only return the question."""


msg_context = {"role": "system", "content": str(PROMPT_1)}


def generate_data(
    topic_selected,
    system_message_generation,
    system_message_selected,
    OUTPUT_FILE_PATH,
):
    system_contexts = [
        system_message_generation,
        system_message_selected,
    ]

    llm_usage = 0

    user_prompts = [f"SUBJECT_AREA: {topic_selected}"]
    gpt_outputs = []

    for pp in range(len(system_contexts)):
        msg_list = []
        msg_system = {"role": "system", "content": str(system_contexts[pp])}
        msg_list.append(msg_system)
        msg_prompt = {"role": "user", "content": user_prompts[pp]}
        msg_list.append(msg_prompt)

        llm_response, llm_usage_a = send_to_llm(PROVIDER, msg_list)

        print("=" * 132)
        print(OUTPUT_FILE_PATH)
        print(llm_response)
        print("=" * 132)

        user_prompts.append(llm_response)
        gpt_outputs.append(llm_response)

    human_gpt_chat = f"""
    AI: {str(user_prompts[1])}
    USER: {str(gpt_outputs[1])}
    """

    conversations = [
        {"from": "system", "value": str(system_contexts[1])},
        {"from": "human", "value": str(user_prompts[1])},
        {"from": "gpt", "value": str(gpt_outputs[1])},
    ]

    full_conversation = [
        {"role": "system", "content": str(system_contexts[1])},
        {"role": "user", "content": str(user_prompts[1])},
        {"role": "assistant", "content": str(gpt_outputs[1])},
    ]

    for kk in range(NUM_TURNS - 1):

        system_message_follow_up = SYSTEM_MESSAGES_FOLLOW_UP[
            np.random.randint(0, len(SYSTEM_MESSAGES_FOLLOW_UP))
        ]
        msg_list_follow_up = []
        msg_system = {"role": "system", "content": str(system_message_follow_up)}
        msg_list_follow_up.append(msg_system)
        msg_prompt = {"role": "user", "content": human_gpt_chat}
        msg_list_follow_up.append(msg_prompt)

        llm_response_follow_up, llm_usage_follow_up = send_to_llm(
            PROVIDER, msg_list_follow_up
        )

        print(f"follow-up question {kk}")
        print(OUTPUT_FILE_PATH)
        print(llm_response_follow_up)
        print("=" * 132)

        full_conversation.append(
            {"role": "user", "content": str(llm_response_follow_up)}
        )

        llm_response_follow_up_answer, llm_usage_follow_up_answer = send_to_llm(
            PROVIDER, full_conversation
        )

        full_conversation.append(
            {"role": "assistant", "content": str(llm_response_follow_up_answer)}
        )

        human_gpt_chat = (
            human_gpt_chat
            + f"""
        AI: {str(llm_response_follow_up)}
        USER: {str(llm_response_follow_up_answer)}
        """
        )

        print(llm_response_follow_up_answer)
        print("=" * 132)

        conversations.append({"from": "human", "value": str(llm_response_follow_up)})
        conversations.append(
            {"from": "gpt", "value": str(llm_response_follow_up_answer)}
        )

    data = {"conversations": conversations}

    with open(OUTPUT_FILE_PATH, "a") as output_file:
        output_file.write(json.dumps(data) + "\n")

    return data, llm_usage


def main():
    nn = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        # Create a list of futures, one for each topic
        futures = []
        for ll in range(NUM_WORKERS):
            print(f"starting generation {ll}")
            topic_number = np.random.randint(0, len(TOPICS))
            topic_selected = TOPICS[topic_number]
            system_message_number = np.random.randint(0, len(SYSTEM_MESSAGES))
            system_message_selected = SYSTEM_MESSAGES[system_message_number]
            system_message_generation = PROMPT_1
            system_message_follow_up = SYSTEM_MESSAGES_FOLLOW_UP[
                np.random.randint(0, len(SYSTEM_MESSAGES_FOLLOW_UP))
            ]
            futures.append(
                executor.submit(
                    generate_data,
                    topic_selected,
                    system_message_generation,
                    system_message_selected,
                    OUTPUT_FILE_PATH,
                )
            )

        # Wait for all futures to complete
        for future in futures:
            data, gpt_usage = future.result()
            if gpt_usage is not None:
                nn += 1
                print(data)
                print(
                    f"Generation {nn} Complete, Token usage: {gpt_usage}, Failed: {failed}"
                )
            else:
                failed += 1
            print("=" * 132)


while True:
    try:
        main()
    except:
        continue
