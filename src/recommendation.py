def recommend_scheme(interest, objective, output):

    scores = {
        "PKM-RE": 0,
        "PKM-RSH": 0,
        "PKM-K": 0,
        "PKM-KC": 0,
        "PKM-KI": 0,
        "PKM-PM": 0,
        "PKM-PI": 0,
        "PKM-AI": 0,
        "PKM-VGK": 0,
        "PKM-GFT": 0,
    }

    # ======================================================
    # Main Objective
    # ======================================================

    objective_rules = {

        "Research": {
            "PKM-RE": 50,
            "PKM-RSH": 40,
            "PKM-AI": 15,
        },

        "Entrepreneurship": {
            "PKM-K": 50,
            "PKM-KI": 20,
        },

        "Community Service": {
            "PKM-PM": 50,
            "PKM-PI": 30,
        },

        "Technology Development": {
            "PKM-KC": 50,
            "PKM-KI": 30,
        },

        "Scientific Writing": {
            "PKM-AI": 50,
            "PKM-GFT": 20,
        },

        "Future Ideas": {
            "PKM-GFT": 50,
            "PKM-VGK": 30,
        }

    }

    # ======================================================
    # Expected Output
    # ======================================================

    output_rules = {

        "Research Findings": {
            "PKM-RE": 25,
            "PKM-RSH": 25,
        },

        "Prototype": {
            "PKM-KC": 25,
            "PKM-KI": 20,
        },

        "Business Product": {
            "PKM-K": 25,
        },

        "Scientific Article": {
            "PKM-AI": 25,
        },

        "Community Empowerment": {
            "PKM-PM": 25,
            "PKM-PI": 20,
        },

        "Innovation": {
            "PKM-KC": 20,
            "PKM-KI": 20,
            "PKM-VGK": 20,
        }

    }

    # ======================================================
    # Area of Interest
    # ======================================================

    interest_rules = {

        "Artificial Intelligence": {
            "PKM-RE": 10,
            "PKM-KC": 10,
            "PKM-KI": 10,
        },

        "Health": {
            "PKM-RE": 10,
            "PKM-RSH": 10,
            "PKM-PM": 10,
        },

        "Education": {
            "PKM-PM": 10,
            "PKM-PI": 10,
            "PKM-RSH": 10,
        },

        "Agriculture": {
            "PKM-RE": 10,
            "PKM-K": 10,
        },

        "Environment": {
            "PKM-RE": 10,
            "PKM-PM": 10,
            "PKM-GFT": 10,
        },

        "Business": {
            "PKM-K": 10,
        },

        "Technology": {
            "PKM-KC": 10,
            "PKM-KI": 10,
            "PKM-RE": 10,
        },

        "Social": {
            "PKM-RSH": 10,
            "PKM-PM": 10,
        },

        "Creative Industry": {
            "PKM-K": 10,
            "PKM-VGK": 10,
        },

        "Other": {}

    }

    # ======================================================

    if objective in objective_rules:
        for scheme, score in objective_rules[objective].items():
            scores[scheme] += score

    if output in output_rules:
        for scheme, score in output_rules[output].items():
            scores[scheme] += score

    if interest in interest_rules:
        for scheme, score in interest_rules[interest].items():
            scores[scheme] += score

    ranking = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranking