import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

if __name__ == "__main__":
    print(config)
