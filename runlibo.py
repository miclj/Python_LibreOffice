import os, sys, subprocess, threading, ctypes, time, winreg
import uno, unohelper

def startLibO(folder):
    command = f'"{folder}\soffice.bin" --accept="socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" --norestore --nologo --nodefault --headless'
    subprocess.call(command)

# Boîte de dialogue Windows
def afficheMessage(mess, frm="{}", titre="Information"):
    msgbox = ctypes.windll.user32.MessageBoxW
    msgbox(None, frm.format(mess), titre, 0)

# Dossier contenant les exécutables LibreOffice
liboPath = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\LibreOffice\\UNO\\InstallPath")
param = [liboPath]
# Lancement du serveur LibreOffice dans un thread
t1 = threading.Thread(target=startLibO, args=(param), daemon=True)
t1.start()

# Context d'exécution du script
localContext = uno.getComponentContext()

# Création d'une instance de UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", localContext )

# Tentative de connexion au serveur LibreOffice
conn = ""
for i in range(10):
    try:
        ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        conn = "ok"
        break
    except:
        time.sleep(.2)

# Si connexion réussie...
if conn == "ok":
    # ... on continue
    smgr = ctx.ServiceManager
    # Création d'un bureau LibreOffice pour la manipulation des fichiers
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)

    if len(sys.argv) > 1:
        import sys.argv[1]

    # Destruction du bureau LibreOffice
    desktop.terminate()
else:
    afficheMessage("Connexion au serveur LibraOffice impossible", titre="Erreur")