from random import choice

from .useragents import USER_AGENTS


def get_random_useragent():
    return choice(USER_AGENTS)
