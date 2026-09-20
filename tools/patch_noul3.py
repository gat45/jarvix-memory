src = open("src/jarvix_memory/decision/jev_logits.py", encoding="utf-8").read()
import io
# Replace all 3 noul prompts to end with "Reponse:" (verified working style)
src = src.replace(
    '"Faut-il injecter cette memoire dans le contexte MAINTENANT ? OUI ou NON.",',
    '"Faut-il injecter cette memoire dans le contexte MAINTENANT ?"\n                ' 
    + ' "Reponds par UN mot (OUI ou NON). Reponse:"')
src = src.replace(
    'f"({\', \'.join(sorted({e.get(\'type\', \'\') for e in ev if hasattr(e, \'get\')}))}.\\n"\n'
    + '                "Les preuves supportent-elles le claim ? OUI ou NON.",',
    'f"({\', \'.join(sorted({e.get(\'type\', \'\') for e in ev if hasattr(e, \'get\')}))}\\n"\n'
    + '                "Les preuves supportent-elles le claim ?"\n'
    + '                "Reponds par UN mot (OUI ou NON). Reponse:",')
src = src.replace(
    '"Cette action est-elle DESTRUCTIVE/irreversible ? OUI ou NON.",',
    '"Cette action est-elle DESTRUCTIVE/irreversible ?"\n'
    + '                "Reponds par UN mot (OUI ou NON). Reponse:",')
open("src/jarvix_memory/decision/jev_logits.py", "w", encoding="utf-8").write(src)
print("patch3 applied")
