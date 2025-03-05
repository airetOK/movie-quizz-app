from cachelib.file import FileSystemCache


class SessionConfiguration:

    __CACHE_DIR = "flask_session"

    SESSION_TYPE = "cachelib"
    SESSION_CACHELIB = FileSystemCache(cache_dir=__CACHE_DIR, threshold=500)
