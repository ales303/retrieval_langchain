import vector_db_utils

profile_id = 2
chat_history = [] #always start with empty list for new session


def get_answer(question_input):
    global chat_history
    print(question_input, '\n')
    answer, chat_history = vector_db_utils.question_answer(profile_id, question_input, chat_history)
    print(answer, '\n')

    answer, chat_history = vector_db_utils.question_answer(profile_id, "that is incorrect, try again", chat_history)
    print(answer, '\n\n')


if __name__ == "__main__":
    get_answer(question_input="What is the smartconnect license needed to display e-docs?")
    get_answer(question_input="What is the smartconnect license needed to process online contracts?")
    get_answer(question_input="What is the smartconnect license needed for fuel ordering")
    get_answer(question_input="List for the configurations and what each does for fds site installations.")
    get_answer(question_input="How do i set degree days in ARM?")
    get_answer(question_input="How do I update pricing in the admin portal")
    get_answer(question_input="How do I create a marketing message and display it in the customer portal.")

    keep_going = True
    while keep_going:
        q = input(f"\n\nPlease enter new question or prompt. Enter quit or exit to stop.\n\n")
        if q.lower() in ['quit', 'exit']:
            exit()
        else:
            get_answer(question_input=q)
