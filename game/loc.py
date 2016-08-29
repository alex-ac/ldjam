def run(context, bot, action, x, y=None):
    if action == 'set':
        context.location = context.map.get(int(x), int(y))

    if action == 'move':
        direction = x
        if direction == 'forward':
            context.location = context.map.get(
                context.location.x + 1,
                context.location.y)
        elif direction == 'left':
            context.location = context.map.get(
                context.location.x,
                context.location.y - 1)
        elif direction == 'right':
            context.location = context.map.get(
                context.location.x,
                context.location.y + 1)
        elif direction == 'back':
            context.location = context.map.get(
                context.location.x - 1,
                context.location.y)
