import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        import re

        cre = re.compile(r"com\.android\.developer.SDK(\.|$)")

        # conflict checking
        for module_name in env.loaded_modules:
            if (cre.match(module_name)):
                raise pyenv.ModulePreloadError("Cannot load two android SDK modules at the same time")

        return []


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")

        # no platform-dependent files for android SDK.
        android_sdk_base = os.path.join(home, "software", "AndroidSDK") # platform-independent

        shell.append_path(os.path.join(android_sdk_base, "tools"), "PATH")
        shell.append_path(os.path.join(android_sdk_base, "platform-tools"), "PATH")


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
