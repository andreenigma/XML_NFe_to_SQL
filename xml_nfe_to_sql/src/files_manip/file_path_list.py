
import pathlib
# from pathlib import PurePath


def files_path_list(path: str, file_filter: str = '*.txt') -> list:


    """Retorna uma lista de objetos das classes pathlib.PurePath, WindowsPath ou PosixPath.  

    Args:
        path (str): Caminho (path) da pasta de trabalho onde será feita a varredura.
        extention (str, optional): String que representa a extensão de arquivo, que será o filtro da varredura. Defaults to 'txt'.

    Returns:
        list[PurePath]: A lista de caminhos (path) no formato estabelecido na biblioteca 'pathlib'.
    """

    # Implementar tratamento dos caminhos (path) de entrada.
    p = pathlib.Path(path)
    glob_base_string = '**/'
    glob_strig_parameter = glob_base_string + file_filter
    return list(p.glob(glob_strig_parameter))


def files_path_str_list(path: str, file_filter: str = '*.txt') -> list:
    
    """Retorna uma lista de caminhos (path) absolutos, no formato texto (str),
     dos arquivos com a extensão requerida. Trata-se de um filtro de arquivos na pasta.

    Args:
        path (str): Caminho (path) da pasta de trabalho onde será feita a varredura.
        extention (str, optional): String que representa a extensão de arquivo, que
        será o filtro da varredura. Defaults to 'txt'.

    Returns:
        list[str]: A lista de caminhos (path) no formato texto (str).
    """
    string_list = list()

    path_object_list = files_path_list(path, file_filter)

    for path_obj in path_object_list:
        string_list.append(str(path_obj))

    return string_list



