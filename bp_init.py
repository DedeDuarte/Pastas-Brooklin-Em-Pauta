import os
import sys
from datetime import datetime, timedelta
import subprocess
import webbrowser as wb
from time import sleep

class bp_init_error(Exception):
    pass

def newFolder(date: str) -> str:
    """
    Cria nova pasta em './..' com nome de acordo com a data do próximo sábado no formato:  
    'BP dd.mm.aa - py'.

    Args:
        date (str): Data do próximo sábado

    Returns:
        str: Caminho da pasta
    """
    # Diretório do script
    origem: str = os.path.dirname(os.path.abspath(__file__))

    # Diretório anterior
    prev: str = os.path.dirname(origem)

    # Verifica segurança do diretório anterior
    prev_dir: str = 'BPs'
    if os.path.basename(prev) != prev_dir and '-ff' not in sys.argv:
        print(
           f'A pasta anterior deve se chamar "{prev_dir}" para garantir a segurança dos arquivos\n'
            'Finalizando (1)'
        )
        exit(1)

    # Pasta origem
    source: str = os.path.join(origem, 'BP init - Files')

    # Verifica se pasta origem existe
    if not os.path.isdir(source):
        raise bp_init_error(f'A pasta de origem "{source}" não foi encontrada.\n'
                              'Todos os arquivos iniciais devem estar em uma pasta, no mesmo local do .py, chamada "BP init - Files"\n'
                              '(por segurança, essa pasta nao esta incluida no git do projeto, basta criar a pasta como desejar)')

    # Ano atual
    year: str = str(datetime.now().year)

    # Caminho da pasta do ano
    year_path: str = os.path.join(prev, year)

    # Cria pasta do ano se não existir
    os.makedirs(year_path, exist_ok=True)

    # Pasta destino
    folder: str = f'BP {date} - py'
    destination: str = os.path.join(year_path, folder)

    # Cancela se a pasta já existir
    if os.path.exists(destination) and '-ff' not in sys.argv:
        raise bp_init_error(f'A pasta "{folder}" já existe!')

    # Cria nova pasta
    print(f'Criando pasta: "{folder}"')
    subprocess.run(
        ["robocopy", source, destination, "/E", "/XF", ".gitkeep"],
        stdout=subprocess.DEVNULL
    )

    # Retorna o caminho da pasta
    return destination

def getNextSaturday() -> str:
    """
    Calcula a data do próximo sábado no formato: dd.mm.aa

    Returns:
        str: dd.mm.aa
    """
    # Data de hoje
    today: datetime = datetime.today()

    # Dias até o próximo sábado
    days_to_saturday: int = (5 - today.weekday()) % 7

    # Data do próximo sábado
    saturday: datetime = today + timedelta(days=days_to_saturday)
    return saturday.strftime('%d.%m.%y')

def sys_verifyErrorArgs(args:list[str], argv: list[str]) -> None:
    error_args: list[str] = []
    for arg in argv:
        if arg not in args and arg.startswith('-'):
            error_args.append(arg)
    if len(error_args) != 0:
        print(f'Argumentos inválidos: {', '.join(map(str, error_args))}\n')
        sys_help()
        exit(4)

def sys_help() -> None:
    """
    Ajuda: Lista de comandos e funções
    """
    # Print de ajuda
    print(
        'Lista de comandos:\n'
        '-h ou -help: Exibe esse painel\n'
        '-l: Abre os links\n'
        '-f: Cria nova pasta\n'
        '-ff: Força a criação da nova pasta'
    )

def sys_createFiles() -> None:
    # Tenta criar novo arquivo
    try:
        path: str = newFolder(getNextSaturday())

    # Erros esperados
    except bp_init_error as e:
        print(e)

    # Erros inesperados
    except Exception as e: 
        print(f'Erro ao criar pasta: {e}')
        exit(2)

    # Sem erros
    else:
        print(f'Pasta criada em: "{path}"')
    
def openLink(link: str):
    wb.open(link)
    sleep(0.1)
    

def openLinks(links_args: list[str]) -> None:
    # BUG: Se usuário rodar algo como: 'py bp_init.py -l c d -f -l t', o programa executara duas vezes o primeiro -l
    
    argv: list[str] = [arg.lower() for arg in sys.argv]

    # Lista de links a serem abertos
    link_gabi: str = 'https://drive.google.com/drive/folders/1D0wmKlpCKbeKVZA4mVFKTgwPR1RtWx4v'
    link_editors: str = 'https://drive.google.com/drive/u/2/folders/1Ru_7QlElb9FKwv1FVHlyJJYcpt1eLCNP'
    link_general: str = 'https://drive.google.com/drive/folders/1MX8DoS57xz7OK1SDmOLQCZtzbcHYRrK8'
    link_canvaEditores: str = 'https://www.canva.com/design/DAG7gEU9kRU/Fd8ZGxvIsJl4dTOnLbqXCg/edit'
    link_canvaThumbs: str = 'https://www.canva.com/design/DAGab21FXbk/udHbbKXgoo-44U3gQrJBZw/edit'
    links: list[str] = [
            link_gabi,          # Gabi
            link_editors,       # Editores
            link_general,       # Geral
            link_canvaEditores, # Canva Editores
            link_canvaThumbs,   # Canva Thumbs
    ]

    gabi: list[str] = ['g', 'gabi', 'video']
    editors: list[str] = ['e', 'editores']
    general: list[str] = ['d', 'drive']
    canvaEditores: list[str] = ['c', 'canva']
    canvaThumbs: list[str] = ['t', 'thumb']
    links_options: list[str] = gabi + editors + general + canvaEditores + canvaThumbs

    openned: bool = False
    for arg in argv:
        if arg in links_args:
            index: int = argv.index(arg) + 1
            while index < len(sys.argv) and not argv[index].startswith('-'):
                arg: str = argv[index]
                if arg in links_options:
                    openned = True
                    if   arg in gabi: openLink(link_gabi)
                    elif arg in editors: openLink(link_editors)
                    elif arg in general: openLink(link_general)
                    elif arg in canvaEditores: openLink(link_canvaEditores)
                    elif arg in canvaThumbs: openLink(link_canvaThumbs)
                index += 1

    if not openned:
        for link in links: openLink(link)

def sys_openLinks(links_args: list[str]) -> None:
    # Abre links
    try:
        openLinks(links_args)
    except Exception as e:
        print(f'Erro ao abrir links: {e}')
        exit(3)

if __name__ == '__main__':
    print('Use -h para comandos\n')

    argv: list[str] = [arg.lower() for arg in sys.argv]
    help_args: list[str] = ['-h', '-help']
    file_args: list[str] = ['-f', '-file']
    links_args: list[str] = ['-l', '-link', '-links']
    args: list[str] = [argv[0]] + help_args + file_args + links_args

    # Args inválidos
    sys_verifyErrorArgs(args, argv)

    # Executar tudo
    if len(argv) == 1:
        sys_createFiles()
        sys_openLinks(links_args)

    # Menu de ajuda
    if all(arg in argv for arg in help_args):
        sys_help()
        exit(0)

    # Criar nova pasta
    if any(arg in argv for arg in file_args):
        sys_createFiles()

    # Abrir links
    if any(arg in argv for arg in links_args):
        sys_openLinks(links_args)