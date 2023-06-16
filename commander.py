from dataclasses import dataclass
from parser import parser_remove_list_articles

@dataclass
class command_t:
    keyword: str
    parameters: list[str]=None

def command_run(inputCmd):
    processedCmd = parser_remove_list_articles(inputCmd.lower().split())
    print(processedCmd)
    input()
