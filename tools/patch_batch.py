import re

src = open("tools/jev_batch.py", encoding="utf-8").read()
# pause anti-429 before each batch print
src = src.replace('        print(f"[GATE]', '        time.sleep(2.0)\n        print(f"[GATE]')
src = src.replace('        print(f"[VERIF]', '        time.sleep(2.0)\n        print(f"[VERIF]')
src = src.replace('        print(f"[SCORE]', '        time.sleep(2.0)\n        print(f"[SCORE]')
# unicode arrow + closing-brace safe
src = src.replace('print(f"\u2192 ', 'print(f"=> ')
src = src.replace('print(f"\u2192', 'print(f"=>')
if "import json, time" not in src:
    src = src.replace("import json", "import json, time", 1)
open("tools/jev_batch.py", "w", encoding="utf-8").write(src)
print("patched OK")
