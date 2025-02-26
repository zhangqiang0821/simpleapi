class DevConfig(object):
    "dev config class"
    DEBUG = True

    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:@127.0.0.1:5432/simple"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Ny12!xNCPxmajL.ZNC@172.16.0.5:54322/gamesdk"
    SQLALCHEMY_BINDS = {
        "gamesdk": "postgresql://postgres:Ny12!xNCPxmajL.ZNC@172.16.0.5:54322/gamesdk",
        "zqdb": "postgresql://postgres:123456@172.16.0.5:54324/zqdb"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
