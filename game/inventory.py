from collections import Counter

def run(context, bot, action, item=None):
    if action == 'exists':
        return context.inventory is not None

    if action == 'can_take':
        return any(item.name != context.item_in_hands.name for item in context.location.items)

    if action == 'take':
        item = context.location.items[0]
        context.item_in_hands = item

    if action == 'put':
        context.inventory[item] += 1

    if action == 'has':
        return context.item_in_hands == item or context.inventory[item] > 0

    if action == 'is_empty':
        return sum(context.inventory.values()) == 0
