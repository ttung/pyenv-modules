import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        # conflict checking
        for module_name in env.loaded_modules:
            if (module_name.startswith('com.facebook.init.paths')):
                raise pyenv.ModulePreloadError("Cannot load two facebook init paths modules at the same time")

        return []


    def load(self, env, shell):
        # path
        engshare = os.path.join(os.sep, "home", "engshare")
        shell.append_path(os.path.join(engshare, "admin", "facebook", "scripts"),
                          "PATH", pyenv.ShellConstants.VALIDATE_PATH)
        shell.append_path(os.path.join(engshare, "admin", "scripts"),
                          "PATH", pyenv.ShellConstants.VALIDATE_PATH)
        shell.append_path(os.path.join(engshare, "svnroot", "tfb", "trunk", "www",
                                       "scripts", "bin"),
                          "PATH", pyenv.ShellConstants.VALIDATE_PATH)


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
