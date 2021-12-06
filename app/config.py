from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PASSWORD = env.str("REDIS_PASSWORD")
REDIS_PORT = env.str("REDIS_PORT")

PG_NAME = env.str("POSTGRES_NAME")
PG_USER = env.str("POSTGRES_USER")
PG_PASSWORD = env.str("POSTGRES_PASSWORD")
PG_HOST = env.str("POSTGRES_HOST")
PG_PORT = env.str("POSTGRES_PORT")
