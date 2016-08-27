from collections import Counter

def run(context, bot, action, item=None):
    if getattr(context, 'inventory', None) is None:
        context.inventory = Counter()

    if action == 'put':
        context.inventory[item] += 1

    if action == 'has':
        return context.inventory[item] > 0

    if action == 'is empty':
        return sum(context.inventory.values()) == 0
