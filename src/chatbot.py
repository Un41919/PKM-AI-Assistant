from retriever import retrieve_context
from llm import generate_answer


def ask(question):

    # ==========================================
    # Retrieve Context
    # ==========================================

    context = retrieve_context(question)

    print("\n" + "=" * 100)
    print("RETRIEVED CONTEXT")
    print("=" * 100)
    print(context)
    print("=" * 100)

    # ==========================================
    # Generate Answer
    # ==========================================

    answer = generate_answer(
        question,
        context
    )

    # ==========================================
    # Citation
    # ==========================================

    citation = ""

    try:

        first_block = context.split("-" * 80)[0]

        for line in first_block.split("\n"):

            if line.startswith("[Sumber:"):

                citation = (
                    line.replace("[", "")
                        .replace("]", "")
                        .strip()
                )
                break

    except Exception:
        citation = ""

    return answer, citation


if __name__ == "__main__":

    print("=" * 80)
    print("PKM AI Assistant")
    print("=" * 80)

    while True:

        question = input("\nQuestion : ")

        if question.lower() == "exit":
            break

        answer, citation = ask(question)

        print("\n" + "=" * 80)
        print("ANSWER")
        print("=" * 80)

        print(answer)

        if citation:

            print("\n" + "-" * 80)
            print("SOURCE")
            print("-" * 80)
            print(citation)