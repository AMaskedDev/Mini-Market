import configparser
import os

# Print the current working directory
print("Current Working Directory:", os.getcwd())

# Specify the path to the configuration file
config_file_path = os.path.abspath('Mini-Market/settings.ini')

# Create a ConfigParser object
config = configparser.ConfigParser()

# Check if the 'Theme' section exists, if not, create it
if 'Theme' not in config.sections():
    config.add_section('Theme')
    config.set('Theme', 'darked-theme', 'False')

# Read the configuration file
config.read(config_file_path)

# Print available sections
print("Available Sections:", config.sections())

# Get the boolean value of 'darked-theme' from the 'Theme' section
dark_theme_enabled = config.getboolean('Theme', 'darked-theme')

# Print the current value
print("Current Dark Theme Enabled:", dark_theme_enabled)

# Modify the boolean value (toggle it for example)
dark_theme_enabled = not dark_theme_enabled

# Set the updated value in the configuration
config.set('Theme', 'darked-theme', str(dark_theme_enabled))

# Save the changes back to the configuration file
with open(config_file_path, 'w') as config_file:
    config.write(config_file)

# Print the updated value
print("Updated Dark Theme Enabled:", dark_theme_enabled)
