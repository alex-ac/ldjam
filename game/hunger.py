def run(context, bot, action, value=None):
    if getattr(context.hunger, None) is None:
        context.hunger = 0

    if action == 'reset':
        context.hunger = 1

    if action == 'increase':
        context.hunger += 1
