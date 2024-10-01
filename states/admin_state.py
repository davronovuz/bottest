from aiogram.dispatcher.filters.state import State, StatesGroup


class ReklamaState(StatesGroup):
    rek = State()


class AddChannelState(StatesGroup):
    username = State()
    channel_id = State()


class DeleteChannelState(StatesGroup):
    username = State()


