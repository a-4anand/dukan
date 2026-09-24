import os


# Render's dashboard may keep an older start command.  Keep the application
# reachable there as well as when the command comes from render.yaml/Procfile.
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
preload_app = True
