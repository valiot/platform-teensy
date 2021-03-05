# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from platform import system

from platformio import exception, util
from platformio.managers.platform import PlatformBase
from platformio.util import get_systype


class TeensyPlatform(PlatformBase):

    @staticmethod
    def _is_macos():
        systype = util.get_systype()
        return "darwin_x86_64" in systype

    @staticmethod
    def _is_linux():
        systype = util.get_systype()
        return "linux_x86_64" in systype
    @staticmethod
    def _is_windows():
        systype = util.get_systype()
        return "windows" in systype

    def configure_default_packages(self, variables, targets):
        if variables.get("board"):
            board_config = self.board_config(variables.get("board"))
            del_toolchain = "toolchain-gccarmnoneeabi"
            if board_config.get("build.core") != "teensy":
                del_toolchain = "toolchain-atmelavr"
            if del_toolchain in self.packages:
                del self.packages[del_toolchain]
            if self._is_linux() and "toolchain-arm-cortexm-mac" in self.packages:
                del self.packages['toolchain-arm-cortexm-mac']
            if self._is_linux() and "toolchain-arm-cortexm-win64" in self.packages:
                del self.packages['toolchain-arm-cortexm-win64']
            if self._is_linux() and "toolchain-gccarmnoneeabi" in self.packages:
                del self.packages['toolchain-gccarmnoneeabi']
            if self._is_macos() and "toolchain-arm-cortexm-linux" in self.packages:
                del self.packages['toolchain-arm-cortexm-linux']
            if self._is_macos() and "toolchain-arm-cortexm-win64" in self.packages:
                del self.packages['toolchain-arm-cortexm-win64']
            if self._is_macos() and "toolchain-gccarmnoneeabi" in self.packages:
                del self.packages['toolchain-gccarmnoneeabi']
            if self._is_windows() and "toolchain-arm-cortexm-linux" in self.packages:
                del self.packages['toolchain-arm-cortexm-linux']
            if self._is_windows() and "toolchain-arm-cortexm-mac" in self.packages:
                del self.packages['toolchain-arm-cortexm-mac']
            if self._is_windows() and "toolchain-gccarmnoneeabi" in self.packages:
                del self.packages['toolchain-gccarmnoneeabi']

        if "mbed" in variables.get("pioframework", []):
            self.packages["toolchain-gccarmnoneeabi"][
                'version'] = ">=1.60301.0,<1.80000.0"

        # configure J-LINK tool
        jlink_conds = [
            "jlink" in variables.get(option, "")
            for option in ("upload_protocol", "debug_tool")
        ]
        if variables.get("board"):
            board_config = self.board_config(variables.get("board"))
            jlink_conds.extend([
                "jlink" in board_config.get(key, "")
                for key in ("debug.default_tools", "upload.protocol")
            ])
        jlink_pkgname = "tool-jlink"
        if not any(jlink_conds) and jlink_pkgname in self.packages:
            del self.packages[jlink_pkgname]

        return PlatformBase.configure_default_packages(
            self, variables, targets)

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        upload_protocols = board.manifest.get("upload", {}).get(
            "protocols", [])
        if "tools" not in debug:
            debug['tools'] = {}

        if "jlink" in upload_protocols and "jlink" not in debug['tools']:
            assert debug.get("jlink_device"), (
                "Missed J-Link Device ID for %s" % board.id)
            debug['tools']['jlink'] = {
                "server": {
                    "package": "tool-jlink",
                    "arguments": [
                        "-singlerun",
                        "-if", "SWD",
                        "-select", "USB",
                        "-device", debug.get("jlink_device"),
                        "-port", "2331"
                    ],
                    "executable": ("JLinkGDBServerCL.exe"
                                   if system() == "Windows" else
                                   "JLinkGDBServer")
                }
            }

        board.manifest['debug'] = debug
        return board
