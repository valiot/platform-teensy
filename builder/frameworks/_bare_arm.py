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

#
# Default flags for bare-metal programming (without any framework layers)
#

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-flto"
        "-Wall",  # show warnings
        "-Wextra",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-mthumb",
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        "-fsingle-precision-constant"
    ],

    CXXFLAGS=[
        "-fno-exceptions",
        "-fno-unwind-tables",
        "-felide-constructors",
        "-fno-rtti",
        "-std=gnu++17",
        "-Wno-error=narrowing",
        "-fpermissive"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU"),
        "LAYOUT_US_ENGLISH"
    ],

    RANLIBFLAGS=["-s"],

    LINKFLAGS=[
        "-Os",
        "-flto",
        "-ffunction-sections",
        "-fdata-sections",
        "-Wl,--gc-sections,--relax",
        "-mthumb",
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        "-Wl,--defsym=__rtc_localtime=$UNIX_TIME"
    ],

    LIBS=["m", "stdc++"]
)

if env.BoardConfig().id_ in ("teensy35", "teensy36"):
    env.Append(
        CFLAGS=[
            "-std=gnu17"
        ],

        CCFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv4-sp-d16"
        ],

        CXXFLAGS=[
            "-std=gnu++17"
        ],

        LINKFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv4-sp-d16"
        ]
    )

if env.BoardConfig().id_ in ("teensy40", "teensy41"):
    env.Append(
        CFLAGS=[
            "-std=gnu17"
        ],

        CCFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv5-d16"
        ],

        CXXFLAGS=[
            "-std=gnu++17"
        ],

        LINKFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv5-d16"
        ]
    )

if "BOARD" in env:
    env.Append(
        CCFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu")
        ],
        LINKFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu")
        ]
    )

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])
