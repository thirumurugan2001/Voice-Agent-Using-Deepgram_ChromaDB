from pathlib import Path
import yaml

# Load configuration from a YAML file
def load_config():
    # Determine the path to the config.yaml file relative to this script
    config_path = Path(__file__).parent / "config.yaml"
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)