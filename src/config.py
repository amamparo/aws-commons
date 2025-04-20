import tomllib


def __load_config(config_path: str = 'config.toml') -> dict:
    with open(config_path, 'rb') as f:
        return tomllib.load(f)


config = __load_config()
