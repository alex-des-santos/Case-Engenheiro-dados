# -*- coding: utf-8 -*-
"""
Funções auxiliares para processamento de dados
"""

import pandas as pd
from colorama import Fore, Style, init

# Inicializar colorama para Windows
init(autoreset=True)

def create_carros_dataframe():
    """Cria o dataframe de carros conforme especificado no desafio"""
    data = {
        'carro': ['Onix', 'Polo', 'Sandero', 'Fiesta', 'City'],
        'cor': ['Prata', 'Branco', 'Prata', 'Vermelho', 'Preto'],
        'montadora': ['Chevrolet', 'Volkswagen', 'Renault', 'Ford', 'Honda']
    }
    
    df = pd.DataFrame(data)
    print(f"{Fore.GREEN}? Dataframe 'Carros' criado com sucesso!")
    print(f"{Fore.CYAN}?? Dados:")
    print(df.to_string(index=False))
    print()
    
    return df

def create_montadoras_dataframe():
    """Cria o dataframe de montadoras conforme especificado no desafio"""
    data = {
        'montadora': ['Chevrolet', 'Volkswagen', 'Renault', 'Ford', 'Honda'],
        'pais': ['EUA', 'Alemanha', 'França', 'EUA', 'Japão']
    }
    
    df = pd.DataFrame(data)
    print(f"{Fore.GREEN}? Dataframe 'Montadoras' criado com sucesso!")
    print(f"{Fore.CYAN}?? Dados:")
    print(df.to_string(index=False))
    print()
    
    return df

def dataframe_to_dict(df):
    """Converte dataframe para lista de dicionários para inserção no MongoDB"""
    return df.to_dict('records')

def print_success(message):
    """Imprime mensagem de sucesso formatada"""
    print(f"{Fore.GREEN}? {message}{Style.RESET_ALL}")

def print_error(message):
    """Imprime mensagem de erro formatada"""
    print(f"{Fore.RED}? {message}{Style.RESET_ALL}")

def print_info(message):
    """Imprime mensagem informativa formatada"""
    print(f"{Fore.CYAN}??  {message}{Style.RESET_ALL}")

def print_warning(message):
    """Imprime mensagem de aviso formatada"""
    print(f"{Fore.YELLOW}??  {message}{Style.RESET_ALL}")

def print_header(title):
    """Imprime cabeçalho formatado"""
    print(f"\n{Fore.MAGENTA}{'='*50}")
    print(f"{Fore.MAGENTA}{title.center(50)}")
    print(f"{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}\n")
