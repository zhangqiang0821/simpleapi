import os

from simpleapi import create_app

config_name = os.getenv('simpleapi_cfg'.upper()) or "dev"
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
