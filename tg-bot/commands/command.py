from aiogram.types import Message
from commands.errors import CommandNotFound


class Command:
    def __init__(self, args: list[str], execution):
        self.args = list(map(lambda s: s.lower(), args))
        self.execution = execution

    def execute(self, message: Message):
        return self.execution(message)


class CommandContainer:
    def __init__(self):
        self._container = list()

    def _exists_command(self, arg: str):
        for cmd in self._container:
            if arg.lower() in cmd.args:
                return True
        return False

    def add_command(self, cmd: Command):
        for arg in cmd.args:
            if self._exists_command(arg.lower()):
                raise RuntimeError(f'Arg for command {arg.lower()} already added')
        self._container.append(cmd)

    def get_command(self, arg: str) -> Command:
        for cmd in self._container:
            if arg.lower() in cmd.args:
                return cmd
        raise CommandNotFound('Command with name not founded')
