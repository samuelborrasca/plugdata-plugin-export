import json
import subprocess
from pathlib import Path
import platform
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description="Build plugins with CMake")
parser.add_argument(
    "--compiler-launcher",
    type=str,
    help="Optional compiler launcher (e.g., ccache, sccache)"
)
args = parser.parse_args()

# Detect platform and choose CMake generator
system = platform.system()
if system == "Windows":
    cmake_generator = ["-G", "Visual Studio 17 2022"]
else:
    cmake_generator = ["-G", "Ninja"]

# Load config.json
with open("config.json") as f:
    plugins_config = json.load(f)

plugdata_dir = Path("plugdata").resolve()
builds_parent_dir = plugdata_dir.parent  # Build folders go here

plugins_dir = os.path.join("plugdata", "Plugins")
build_output_dir = os.path.join("Build")
os.makedirs(build_output_dir, exist_ok=True)

if not plugdata_dir.is_dir():
    print(f"plugdata directory not found: {plugdata_dir}")
    exit(1)

for plugin in plugins_config:
    name = plugin["name"]
    zip_path = Path(plugin["path"]).resolve()
    formats = plugin.get("formats", [])
    is_fx = plugin.get("type", "").lower() == "fx"

    build_dir = builds_parent_dir / f"Build-{name}"
    print(f"\nProcessing: {name}")

    author = plugin.get("author", False)
    enable_gem = plugin.get("enable_gem", False)
    enable_sfizz = plugin.get("enable_sfizz", False)
    enable_ffmpeg = plugin.get("enable_ffmpeg", False)

    cmake_configure = [
        "cmake",
        *cmake_generator,
        f"-B{build_dir}",
        f"-DCUSTOM_PLUGIN_NAME={name}",
        f"-DCUSTOM_PLUGIN_PATH={zip_path}",
        f"-DCUSTOM_PLUGIN_COMPANY={author}",
        "-DCMAKE_BUILD_TYPE=Release",
        f"-DENABLE_GEM={'1' if enable_gem else '0'}",
        f"-DENABLE_SFIZZ={'1' if enable_sfizz else '0'}",
        f"-DENABLE_FFMPEG={'1' if enable_ffmpeg else '0'}",
        f"-DCUSTOM_PLUGIN_IS_FX={'1' if is_fx else '0'}"
    ]

    if args.compiler_launcher:
        cmake_configure.append(f"-DCMAKE_C_COMPILER_LAUNCHER={args.compiler_launcher}")
        cmake_configure.append(f"-DCMAKE_CXX_COMPILER_LAUNCHER={args.compiler_launcher}")

    result_configure = subprocess.run(cmake_configure, cwd=plugdata_dir)
    if result_configure.returncode != 0:
        print(f"Failed cmake configure for {name}")
        continue

    # Build all combinations of type + format
    for fmt in formats:
        if system != "Darwin" and fmt == "AU":
            continue
        target = f"plugdata_{'fx_' if is_fx else ''}{fmt}"
        if fmt == "Standalone":
            target = "plugdata_standalone"

        cmake_build = [
            "cmake",
            "--build", str(build_dir),
            "--target", target,
            "--config Release"
        ]
        print(f"Building target: {target}")
        result_build = subprocess.run(cmake_build, cwd=plugdata_dir)
        if result_build.returncode != 0:
            print(f"Failed to build target: {target}")
        else:
            print(f"Successfully built: {target}")
        format_path = os.path.join(plugins_dir, fmt)
        target_dir = os.path.join(build_output_dir, fmt)

        if fmt == "Standalone":
            if os.path.isdir(format_path):
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                shutil.copytree(format_path, target_dir)
        else:
            extension = ""
            if fmt == "VST3":
                extension = ".vst3"
            elif fmt == "AU":
                extension = ".component"
            elif fmt == "LV2":
                extension = ".lv2"
            elif fmt == "CLAP":
                extension = ".clap"

            plugin_filename = name + extension;
            os.makedirs(target_dir, exist_ok=True)
            src = os.path.join(format_path, plugin_filename);
            dst = os.path.join(target_dir, plugin_filename);
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                if os.path.exists(dst):
                    os.remove(dst)
                shutil.copy2(src, dst)
