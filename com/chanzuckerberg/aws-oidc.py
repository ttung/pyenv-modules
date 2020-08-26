import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        import re

        cre = re.compile(r"com\.chanzuckerberg\.aws-oidc(\.|$)")

        # conflict checking
        for module_name in env.loaded_modules:
            if (cre.match(module_name)):
                raise pyenv.ModulePreloadError("Cannot load two chanzuckerberg aws-oidc modules at the same time")

        return []


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")

        shell.append_path(os.path.join(home, "software", "chanzuckerberg-aws-oidc"), "PATH")


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
