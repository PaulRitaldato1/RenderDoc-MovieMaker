# RenderDoc Documentation is available: https://renderdoc.org/docs/python_api/index.html

import sys
import os

# Import renderdoc if not already imported (e.g. in the UI)
if 'renderdoc' not in sys.modules and '_renderdoc' not in sys.modules:
	import renderdoc

rd = renderdoc

#tweakables start
colorEnable = True
depthEnable = False #Can be very slow

colorResourceID = 0
depthResourceID = 0

blackpoint = 0.0
whitepoint = 1.0

colorOutPath = ""
depthOutPath = ""
#tweakables end

#removes all files of the same size from a given directory
#Can potentionally use TextureDescription() from the renderdoc API to check sizes before SetFrameEvent()
# as an early out. This would prevent duplicates before they get saved, which should cause a considerable
#speedup. Not tested yet though
def removeDuplicateTextures(path):
	lastSize = 0

	for file in os.listdir(path):
		if lastSize == os.stat(path+file).st_size:
			print("Deleting " + path+file)
			os.remove(path+file)
		else:
			lastSize = os.stat(path+file).st_size


def saveColorOut(d, controller, path):
	global blackpoint
	global whitepoint
	global colorResourceID

	for output in d.outputs:
		
		if int(output) == colorResourceID:
			
			controller.SetFrameEvent(d.eventId, True)
			texsave = rd.TextureSave()
			texsave.resourceId = output
			filename = str(int(d.eventId))
			
			texsave.alpha = rd.AlphaMapping.BlendToCheckerboard
			texsave.mip = 0
			texsave.slice.sliceIndex = 0

			texsave.destType = rd.FileType.JPG
			wbRange = rd.TextureComponentMapping()
			wbRange.blackPoint = blackpoint
			wbRange.whitePoint = whitepoint
			texsave.comp = wbRange

			controller.SaveTexture(texsave, path + filename + ".jpg")
			print("Saving images of %s at %d: %s" % (path + filename, d.eventId, d.name))

			
	for d in d.children:
		saveColorOut(d, controller, path)
			
def saveDepthOut(d, controller, path):
	global blackpoint
	global whitepoint
	global depthResourceID

	output = d.depthOut()
		
	if int(output) == depthResourceID:
			
		controller.SetFrameEvent(d.eventId, True)
		texsave = rd.TextureSave()
		texsave.resourceId = output
		filename = str(int(d.eventId))
			
		texsave.alpha = rd.AlphaMapping.BlendToCheckerboard
		texsave.mip = 0
		texsave.slice.sliceIndex = 0

		texsave.destType = rd.FileType.JPG
		wbRange = rd.TextureComponentMapping()
		wbRange.blackPoint = blackpoint
		wbRange.whitePoint = whitepoint
		texsave.comp = wbRange

		controller.SaveTexture(texsave, path + filename + ".jpg")
		print("Saving images of %s at %d: %s" % (path + filename, d.eventId, d.name))

			
	for d in d.children:
		saveDepthOut(d, controller, path)

def saveController(controller):
	global colorEnable
	global depthEnable
	global colorOutPath
	global depthOutPath

	for d in controller.GetDrawcalls():
		if(colorEnable):
			global colorOutPath
			saveColorOut(d, controller, colorOutPath)
			removeDuplicateTextures(colorOutPath)
		if(depthEnable):
			global depthOutPath
			saveDepthOut(d, controller, depthOutPath)
			removeDuplicateTextures(depthOutPath)


def loadCapture(filename):

	cap = rd.OpenCaptureFile()

	status = cap.OpenFile(filename, '', None)

	if status != rd.ReplayStatus.Succeeded:
		raise RuntimeError("Couldn't open file: " + str(status))

	if not cap.LocalReplaySupport():
		raise RuntimeError("Capture cannot be replayed")

	status,controller = cap.OpenCapture(rd.ReplayOptions(), None)

	if status != rd.ReplayStatus.Succeeded:
		raise RuntimeError("Couldn't initialise replay: " + str(status))

	return cap,controller

def main():
	pyrenderdoc.Replay().BlockInvoke(saveController)

main()