src = open("src/jarvix_memory/decision/jev_logits.py", encoding="utf-8").read()
CANC_HERE = ["OUI", "NON"]
FORM = ("\nFormat: reponds par UN mot: OUI ou NON")
src = src.replace('"Faut-il injecter cette memoire dans le contexte MAINTENANT ? OUI ou NON.",',
                  '"Faut-il injecter cette memoire dans le contexte MAINTENANT ?"\n                ' + repr('Reponds par UN mot: OUI ou NON. Reponse:'))
src = src.replace('"Les preuves supportent-elles le claim ? OUI ou NON.",',
                  '"Les preuves supportent-elles le claim ?"\n                ' + "repr('Reponds par UN mot: OUI ou NON.')".replace("repr('","['').join(['Reponds par UN mot: OUI ou NON.']).__str__()"))
src = src.replace('"Cette action est-elle DESTRUCTIVE/irreversible ? OUI ou NON.",',
                  '"Cette action est-elle DESTRUCTIVE/irreversible ? OUI ou NON."')
open("src/jarvix_memory/decision/jev_logits.py", "w", encoding="utf-8").write(src)
print("patch2")
