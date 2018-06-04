from pyhooked import Hook, KeyboardEvent, MouseEvent

global chatFrame

def handle_events(args):
    if isinstance(args, KeyboardEvent):
        global chatFrame
        if args.current_key == 'Return' and args.event_type == 'key down':
            chatFrame.send(None)

    if isinstance(args, MouseEvent):
        print(args.mouse_x)
        print(args.mouse_y)
        return

def notifyListen(chatWdw):
    global chatFrame
    chatFrame = chatWdw
    hk = Hook()
    hk.handler = handle_events
    hk.hook()
