# Automated build script for plugdata powered plugins

Note: this is currently still in development, don't use this in production yet!

1. Fork this repository
2. Add the plugin definitions you want to build to "config.json", and add the plugins you want to process (either as a folder or .zip file)
3. Wait for github actions to complete, and download your plugins!

Note: after building, the patch file you use is directly accessible from the "info" menu. This is a requirement for your plugin to comply with the GPL license (required for both plugdata, and the JUCE free tier)
