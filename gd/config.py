from environs import Env

env = Env()
env.read_env()

b_client = env.str("b_client")
b_secret = env.str("b_secret")
