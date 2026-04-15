import os
import sys

os.environ['LINE_CHANNEL_SECRET'] = 'b6d74bdf0f0b6f610ae2bb6272868b43'
os.environ['LINE_ACCESS_TOKEN'] = 'fo8tvjs5FhEB/Qq5Jf4FJtqB9RpmqAYgONTTx1oQoUnCkHnTy0vFPo+CqAKZpkl4hnU4TLoQS8aE257IFiAtQonAFaFku+kNCvjmnaqTVpWGjvgGFcUSh08AlcYCR73k6rwK7HYOknyxXfEjdAv/VQdB04t89/1O/w1cDnyilFU='

sys.path.insert(0, os.path.dirname(__file__))

from app import app

print("=" * 50)
print("ElderCare Bot starting on port 5000")
print("=" * 50)
app.run(host='0.0.0.0', port=5000, debug=False)