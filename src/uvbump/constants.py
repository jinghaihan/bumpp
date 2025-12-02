from typing import TypedDict

import coloredstrings as c


class SymbolsDict(TypedDict):
  success: str
  info: str


symbols: SymbolsDict = {
  'success': c.green('✔'),
  'info': c.blue('ℹ'),
}
