# Automated build script for plugdata powered plugins

Note: this is currently still in development, don't use this in production yet!

1. Fork this repository.
2. Click on the "Actions" tab and enable github actions
3. Add your patch files and plugin definitions to config.json.
4. Wait for GitHub Actions to complete the build.
5. Download your VST3 / AU / CLAP / LV2 / Standalone plugins!


# Config syntax

Example:
```
[
  {
    "name": "N-SPEC COMP LITE 2",
    "author": "Nasko",
    "path": "Plugins/N-SPEC COMP LITE 2.zip",
    "formats": ["VST3", "AU", "LV2", "CLAP"],
    "type": "fx",
    "enable_gem": false,
    "enable_sfizz": false,
    "enable_ffmpeg": false
  },
  {
    "name": "N-TILT",
    "author": "Nasko",
    "path": "Plugins/N-TILT.zip",
    "formats": ["Standalone"],
    "type": "fx",
    "enable_gem": false,
    "enable_sfizz": false,
    "enable_ffmpeg": false
  }
]
```

## Parameter Reference

### Required Fields

| Field     | Type     | Description |
|-----------|----------|-------------|
| `name`    | `string` | **Unique name** of the plugin. This is how it will appear in your DAW. <br>_Note: You cannot load two plugdata plugins with the same name._ |
| `author`  | `string` | Name of the plugin's creator, displayed inside the DAW. |
| `path`    | `string` | Path to the patch location within the repository. Can be a **folder** or a **.zip** file. |
| `formats` | `array`  | List of plugin formats to build. Valid values: `VST3`, `AU`, `CLAP`, `LV2`, `Standalone`. |
| `type`    | `string` | Type of plugin: either `"fx"` for effects or `"instrument"` for instruments/synths. |

---

### Optional Fields

| Field           | Type      | Description |
|------------------|-----------|-------------|
| `enable_gem`     | `boolean` | Enables experimental [GEM](https://puredata.info/downloads/Gem) support <br>_Default: `false`_ |
| `enable_sfizz`   | `boolean` | Enables the `[sfz~]` object for SFZ sample playback. <br>_Default: `false`_ |
| `enable_ffmpeg`  | `boolean` | Enables FFmpeg-based audio objects. <br>Recommended if your patch plays audio files. <br>_Default: `false`_ |


# Licensing note
After building, the original patch file you used is directly accessible via the “Info” menu in the plugin. This is required to comply with the GPL license (required by both plugdata and the JUCE free tier), as your patch could now legally be considered as "source code" of the generated plugins.
