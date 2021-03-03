# import os
from app import app

# os.chdir('app')
# print(os.getcwd())
app.run(host='0.0.0.0', port=8080, debug=True)
