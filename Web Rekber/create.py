import os

# Struktur direktori dan file
structure = {
    "rekber": {
        "app": {
            "__init__.py": "",
            "models.py": "",
            "routes.py": "",
            "templates": {
                "base.html": "",
                "index.html": "",
                "dashboard.html": "",
                "login.html": "",
                "register.html": ""
            },
            "static": {
                "css": {
                    "styles.css": ""
                },
                "js": {
                    "scripts.js": ""
                },
                "images": {}
            }
        },
        "config.py": "",
        "run.py": "",
        "requirements.txt": "",
        ".env": ""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)

# Buat struktur direktori dan file
create_structure('.', structure)
