from ..lib import requests
from ..lib.errors import ExpectedError

class Languages:
  JAVASCRIPT = "JavaScript"
  GO = "Go"
  PYTHON = "Python"

class Extensions:
  PY = ".py"
  GO = ".go"
  JS = ".js"
  JSX = ".jsx"
  VUE = ".vue"

LEXICAL_EXTS = (Extensions.GO, Extensions.JS, Extensions.JSX, Extensions.VUE)

SUPPORTED_EXTS_TO_LANG = {
    Extensions.PY: Languages.PYTHON,
    Extensions.GO: Languages.GO,
    Extensions.JS: Languages.JAVASCRIPT,
    Extensions.JSX: Languages.JAVASCRIPT,
    Extensions.VUE: Languages.JAVASCRIPT,
}

_LANG_TO_ENABLED_PATH = {
    Languages.GO: "/clientapi/settings/kite_lexical_enabled",
    Languages.JAVASCRIPT: "/clientapi/settings/kite_js_enabled",
}

def ext_to_lang(ext):
    return SUPPORTED_EXTS_TO_LANG[ext]

def kited_ext_enabled(ext):
    # Python enabled by default as of 2020/03/30
    if ext == Extensions.PY:
        return True

    try:
        lang = ext_to_lang(ext)
        _, enabled = requests.kited_get(_LANG_TO_ENABLED_PATH[lang])
        return enabled.decode("utf-8") == 'true'
    except ExpectedError:
        # Default to not enabled if the copilot isn't up.
        return False