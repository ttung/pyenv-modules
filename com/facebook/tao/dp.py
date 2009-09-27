import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        import re

        cre = re.compile(r"com\.facebook\.tao.dp(\.|$)")

        # conflict checking
        for module_name in env.loaded_modules:
            if (cre.match(module_name)):
                raise pyenv.ModulePreloadError("Cannot load two tao dp modules at the same time")

        return []


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")
        machtype = os.getenv("MACHTYPE")
        ostype = os.getenv("OSTYPE")

        if (machtype is None or
            ostype is None):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        tao_dp_base = os.path.join(home, "vc_sync", "fbcode", "_bin", "tao")

        shell.append_path(tao_dp_base, "LD_LIBRARY_PATH")


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
