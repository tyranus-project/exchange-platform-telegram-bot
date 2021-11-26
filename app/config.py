from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PASSWORD = env.str("REDIS_PASSWORD")
REDIS_PORT = env.str("REDIS_PORT")
