# RenderDoc-MovieMaker
Saves out a given resource (color or depth) output (by resource ID) at each API call in a given frame. 

# Usage
1. Load the script into the renderDoc editor Window->Python Shell
2. Change from interactive shell to 'Run Scripts'
3. Click 'Open' to load in the file
4. Adjust tweakables at the top of the script. You must provide the enables, a resource ID to search, and an output path minimum

## Tweakables
* colorEnable: Enables saving out the color output.
* depthEnable: Enables saving out the depth output. 
* colorResourceID: The color output resource ID to track and save
* depthResourceID: The depth output resource ID to track and save
* blackpoint: The blackpoint to give the texture before saving it out. Useful for textures not in the 0.0 - 1.0 range
* whitepoint: The blackpoint to give the texture before saving it out. Useful for textures not in the 0.0 - 1.0 range
* colorOutPath: Directory to save outputs to. Make sure to add a trailing \ (for windows) or / (for nix) depending on your OS
* DepthOutPath: Directory to save outputs to. Make sure to add a trailing \ (for windows) or / (for nix) depending on your OS

# TODO
Check for duplicate textures before saving them out. SetFrameEvent() and SaveTexture() are very slow, so preventing duplicate textures would speed the script up considerably.
