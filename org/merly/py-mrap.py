import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        # conflict checking
        for module_name in env.loaded_modules:
            if (module_name.startswith("org.merly.py-mrap")):
                raise pyenv.ModulePreloadError("Cannot load two py-mrap modules at the same time")

        return []


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")

        py_mrap_base = os.path.join(home, "software", "py-mrap")
        # python extra paths are expanded in ~/software/python/sitecustomize.py
        shell.append_path(os.path.join(py_mrap_base, "lib"), "PYTHON_EXTRA_PATH")


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
