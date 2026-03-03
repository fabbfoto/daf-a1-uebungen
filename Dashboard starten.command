#!/bin/bash
# Dashboard starten – Doppelklick genügt
cd "$(dirname "$0")"
open http://localhost:8765/a1-1-dashboard.html
python3 -m http.server 8765
