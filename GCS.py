# Julian Bonnells

import networking
from rich.console import Console
from rich.markdown import Markdown

class Command:
    def __init__(self, name, id, description):
        self.name = name
        self.id = int(id)
        self.description = description

commands = [
        Command('SAFE_MODE_ENABLE', 1, 'Will switch the FSW to safe mode. This command is invalid when in BBQ mode or in safe mode.'),
        Command('SAFE_MODE_DISABLE',2, 'Will switch the FSW back to the ready state. This command is always valid.'),
        Command('SHOW_CMDS_RCVD',   3, 'Will return the total number of valid commands received since startup of the FSW. This command is invalid when in BBQ mode or in safe mode.'),
        Command('SHOW_NUM_SAFES',   4, 'Will return the number of times the FSW has switched to safe mode since startup. This command is invalid when in BBQ mode.'),
        Command('SHOW_UPTIME',      5, 'Will return the number of seconds since the FSW was started. This command is invalid when in BBQ mode or in safe mode.'),
        Command('RESET_CMD_CNTR',   6, 'Will reset the command counter to zero and then return the number of commands received (i.e. zero). This command is invalid when in BBQ mode or in safe mode.'),
        Command('SHUTDOWN',         7, 'Will return the state of the FSW, close the socket and stop the process. This command is always valid.')
    ]

def main():

    console = Console()
    with open('README.md') as f:
        md = Markdown(f.read())
        console.print(md)

    while True:
        inp = input('Enter Command: ')
        if not inp:
            continue

        msg_to_send = ''
        for cmd in commands:
            if str(cmd.id) == inp or cmd.name == inp:
                msg_to_send = cmd.name
                break
        if len(msg_to_send) == 0:
            print('Invalid Input. Try again.\n')
            continue

        try:
            networking.send(msg_to_send)
            msg = networking.receive()
            print(f'Received Reply: {msg}\n')
            if 'Shutdown Initiated' in msg:
                break
        except TimeoutError:
            print('Timeout. Try again\n')
            continue

    networking.shutdown()


if __name__ == '__main__':
    main()