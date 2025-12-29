from config.settings import PREMIUM_MIN, PREMIUM_MAX


def select_option_by_volume(option_chain, option_type):
    """
    option_type: 'CE' or 'PE'
    """
    filtered = [
        opt for opt in option_chain
        if opt["type"] == option_type
        and PREMIUM_MIN <= opt["ltp"] <= PREMIUM_MAX
    ]

    if not filtered:
        return None

    # 🔥 core rule: highest volume wins
    selected_option = max(filtered, key=lambda x: x["volume"])
    return selected_option
