import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        # conflict checking
        for module_name in env.loaded_modules:
            if (module_name.startswith("oss.pexpect")):
                raise pyenv.ModulePreloadError("Cannot load two pexpect modules at the same time")

        return []


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")

        pexpect_base = os.path.join(home, "software", "pexpect-2.3")
        # python extra paths are expanded in ~/software/python/sitecustomize.py
        shell.append_path(os.path.join(pexpect_base, "lib"), "PYTHON_EXTRA_PATH",
                          check_path = pyenv.ShellConstants.ENFORCE_PATH)


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
