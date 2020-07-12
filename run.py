import os
from imdbapp import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=bool(os.getenv("DEBUG")) or True)
