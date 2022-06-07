import subprocess

def install_wx():
    # wxpython
    try:
        import wx
        print('wxpython already installed, only imported')
    except:
        subprocess.call(['pip', 'install', 'wxpython'])
        import wx
        print('wxpython was not installed, installed and imported')

def install_libs():
    # geopy
    try:
        import geopy
        print('Geopy already installed, only imported')
    except:
        subprocess.call(['pip', 'install', 'geopy'])
        import geopy
        print('Geopy was not installed, installed and imported')

    # neo4j
    try:
        import neo4j
        print('neo4j already installed, only imported')
    except:
        subprocess.call(['pip', 'install', 'neo4j'])
        import neo4j
        print('neo4j was not installed, installed and imported')

    # bs4
    try:
        import bs4
        print('bs4 already installed, only imported')
    except:
        subprocess.call(['pip', 'install', 'bs4'])
        import bs4
        print('bs4 was not installed, installed and imported')

if __name__ == '__main__':
    install_libs()
    print('test')
