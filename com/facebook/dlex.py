import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        # conflict checking
        for module_name in env.loaded_modules:
            if (module_name.startswith('com.facebook.dlex')):
                raise pyenv.ModulePreloadError("Cannot load two dlex modules at the same time")

        return []


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")

        dlex_base = os.path.join(home, "software", "dlex")

        shell.append_path(os.path.join(dlex_base, "lib"), "PYTHON_EXTRA_PATHS")
        shell.append_path(os.path.join(dlex_base, "bin"), "PATH")


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
