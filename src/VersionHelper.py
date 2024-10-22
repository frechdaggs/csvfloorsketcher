import re

def get_version():
	with open('version.txt') as f:
		content = f.read()
		tokens = re.findall(r"(\d+)\.(\d+)\.(\d+)\.(\d+)", content)

		return int(tokens[0][0]), int(tokens[0][1]), int(tokens[0][2]), int(tokens[0][3])

def version_to_str(major:int, minor:int, patch:int, rev:int):
    return f'{major:02d}.{minor:03d}.{patch:02d}.{rev:02d}'
