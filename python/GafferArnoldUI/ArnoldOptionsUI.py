##########################################################################
#
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import IECore

import Gaffer
import GafferUI
import GafferArnold

def __renderingSummary( plug ) :

	info = []
	if plug["bucketSize"]["enabled"].getValue() :
		info.append( "Bucket Size %d" % plug["bucketSize"]["value"].getValue() )
	if plug["bucketScanning"]["enabled"].getValue() :
		info.append( "Bucket Scanning %s" % plug["bucketScanning"]["value"].getValue().capitalize() )
	return ", ".join( info )

def __samplingSummary( plug ) :

	info = []
	if plug["aaSamples"]["enabled"].getValue() :
		info.append( "AA %d" % plug["aaSamples"]["value"].getValue() )
	if plug["giDiffuseSamples"]["enabled"].getValue() :
		info.append( "Diffuse %d" % plug["giDiffuseSamples"]["value"].getValue() )
	if plug["giGlossySamples"]["enabled"].getValue() :
		info.append( "Glossy %d" % plug["giGlossySamples"]["value"].getValue() )
	if plug["giRefractionSamples"]["enabled"].getValue() :
		info.append( "Refraction %d" % plug["giRefractionSamples"]["value"].getValue() )
	if plug["giSSSSamples"]["enabled"].getValue() :
		info.append( "SSS %d" % plug["giSSSSamples"]["value"].getValue() )
	if plug["giVolumeSamples"]["enabled"].getValue() :
		info.append( "Volume %d" % plug["giVolumeSamples"]["value"].getValue() )
	return ", ".join( info )

def __rayDepthSummary( plug ) :

	info = []
	if plug["giTotalDepth"]["enabled"].getValue() :
		info.append( "Total %d" % plug["giTotalDepth"]["value"].getValue() )
	if plug["giDiffuseDepth"]["enabled"].getValue() :
		info.append( "Diffuse %d" % plug["giDiffuseDepth"]["value"].getValue() )
	if plug["giGlossyDepth"]["enabled"].getValue() :
		info.append( "Glossy %d" % plug["giGlossyDepth"]["value"].getValue() )
	if plug["giReflectionDepth"]["enabled"].getValue() :
		info.append( "Reflection %d" % plug["giReflectionDepth"]["value"].getValue() )
	if plug["giRefractionDepth"]["enabled"].getValue() :
		info.append( "Refraction %d" % plug["giRefractionDepth"]["value"].getValue() )
	if plug["giVolumeDepth"]["enabled"].getValue() :
		info.append( "Volume %d" % plug["giVolumeDepth"]["value"].getValue() )
	if plug["autoTransparencyDepth"]["enabled"].getValue() :
		info.append( "Transparency %d" % plug["autoTransparencyDepth"]["value"].getValue() )
	if plug["autoTransparencyThreshold"]["enabled"].getValue() :
		info.append( "Threshold %s" % GafferUI.NumericWidget.valueToString( plug["autoTransparencyThreshold"]["value"].getValue() ) )
	return ", ".join( info )


def __featuresSummary( plug ) :

	info = []
	for childName, label in (
		( "ignoreTextures", "Textures" ),
		( "ignoreShaders", "Shaders" ),
		( "ignoreAtmosphere", "Atmos" ),
		( "ignoreLights", "Lights" ),
		( "ignoreShadows", "Shadows" ),
		( "ignoreSubdivision", "Subdivs" ),
		( "ignoreDisplacement", "Disp" ),
		( "ignoreBump", "Bump" ),
		( "ignoreMotionBlur", "MBlur" ),
		( "ignoreSSS", "SSS" ),
	) :
		if plug[childName]["enabled"].getValue() :
			info.append( label + ( " Off " if plug[childName]["value"].getValue() else " On" ) )

	return ", ".join( info )

def __performanceSummary( plug ) :

	info = []
	if plug["threads"]["enabled"].getValue() :
		info.append( "Threads %d" % plug["threads"]["value"].getValue() )
	return ", ".join( info )

def __searchPathsSummary( plug ) :

	info = []
	for prefix in ( "texture", "procedural", "shader" ) :
		if plug[prefix+"SearchPath"]["enabled"].getValue() :
			info.append( prefix.capitalize() )

	return ", ".join( info )

def __errorColorsSummary( plug ) :

	info = []
	for suffix in ( "Texture", "Mesh", "Pixel", "Shader" ) :
		if plug["errorColorBad"+suffix]["enabled"].getValue() :
			info.append( suffix )

	return ", ".join( info )

def __loggingSummary( plug ) :

	info = []
	if plug["logFileName"]["enabled"].getValue() :
		info.append( "File name" )

	return ", ".join( info )

def __licensingSummary( plug ) :

	info = []
	for name, label in (
		( "abortOnLicenseFail", "Abort on Fail" ),
		( "skipLicenseCheck", "Skip Check" )
	) :
		if plug[name]["enabled"].getValue() :
			info.append( label + " " + ( "On" if plug[name]["value"].getValue() else "Off" ) )

	return ", ".join( info )

Gaffer.Metadata.registerNode(

	GafferArnold.ArnoldOptions,

	"description",
	"""
	Sets global scene options applicable to the Arnold
	renderer. Use the StandardOptions node to set
	global options applicable to all renderers.
	""",

	plugs = {

		# Sections

		"options" : [

			"layout:section:Rendering:summary", __renderingSummary,
			"layout:section:Sampling:summary", __samplingSummary,
			"layout:section:Ray Depth:summary", __rayDepthSummary,
			"layout:section:Features:summary", __featuresSummary,
			"layout:section:Performance:summary", __performanceSummary,
			"layout:section:Search Paths:summary", __searchPathsSummary,
			"layout:section:Error Colors:summary", __errorColorsSummary,
			"layout:section:Logging:summary", __loggingSummary,
			"layout:section:Licensing:summary", __licensingSummary,

		],

		# Rendering

		"options.bucketSize": [

			"description",
			"""
			Controls the size of the image buckets.
			The default size is 64x64 pixels.
			Bigger buckets will increase memory usage
			while smaller buckets may render slower as
			they need to perform redundant computations
			and filtering.
			""",

			"layout:section", "Rendering",
			"label", "Bucket Size",

		],

		"options.bucketScanning": [

			"description",
			"""
			Controls the order in which buckets are
			processed. A spiral pattern is the default.
			""",

			"layout:section", "Rendering",
			"label", "Bucket Scanning",

		],

		"options.bucketScanning.value": [

			"plugValueWidget:type", 'GafferUI.PresetsPlugValueWidget',
			"presetNames", IECore.StringVectorData( ["Top", "Bottom", "Left", "Right", "Random", "Woven", "Spiral", "Spiral"] ),
			"presetValues", IECore.StringVectorData( ["top", "bottom", "left", "right", "random", "woven", "spiral", "spiral"] ),
		],

		# Sampling

		"options.aaSamples" : [

			"description",
			"""
			Controls the number of rays per pixel
			traced from the camera. The more samples,
			the better the quality of antialiasing,
			motion blur and depth of field. The actual
			number of rays per pixel is the square of
			the AA samples value - so a value of 3
			means 9 rays are traced, 4 means 16 rays are
			traced and so on.
			""",

			"layout:section", "Sampling",
			"label", "AA Samples",

		],

		"options.giDiffuseSamples" : [

			"description",
			"""
			Controls the number of rays traced when
			computing indirect illumination ("bounce light").
			The number of actual diffuse rays traced is the
			square of this number.
			""",

			"layout:section", "Sampling",
			"label", "Diffuse Samples",

		],

		"options.giGlossySamples" : [

			"description",
			"""
			Controls the number of rays traced when
			computing glossy specular reflections.
			The number of actual specular rays traced
			is the square of this number.
			""",

			"layout:section", "Sampling",
			"label", "Glossy Samples",

		],

		"options.giRefractionSamples" : [

			"description",
			"""
			Controls the number of rays traced when
			computing refractions. The number of actual
			specular rays traced is the square of this number.
			""",

			"layout:section", "Sampling",
			"label", "Refraction Samples",

		],

		"options.giSSSSamples" : [

			"description",
			"""
			Controls the number of rays traced when
			computing subsurface scattering. The number of actual
			subsurface rays traced is the square of this number.
			""",

			"layout:section", "Sampling",
			"label", "SSS Samples",

		],

		"options.giVolumeSamples" : [

			"description",
			"""
			Controls the number of rays traced when
			computing indirect lighting for volumes.
			The number of actual rays traced
			is the square of this number. The volume
			ray depth must be increased from the default
			value of 0 before this setting is of use.
			""",

			"layout:section", "Sampling",
			"label", "Volume Samples",

		],

		# Ray Depth

		"options.giTotalDepth" : [

			"description",
			"""
			The maximum depth of any ray (Diffuse + Glossy +
			Reflection + Refraction + Volume).
			""",

			"layout:section", "Ray Depth",
			"label", "Total Depth",

		],

		"options.giDiffuseDepth" : [

			"description",
			"""
			Controls the number of ray bounces when
			computing indirect illumination ("bounce light").
			""",

			"layout:section", "Ray Depth",
			"label", "Diffuse Depth",

		],

		"options.giGlossyDepth" : [

			"description",
			"""
			Controls the number of ray bounces when
			computing glossy specular reflections.
			""",

			"layout:section", "Ray Depth",
			"label", "Glossy Depth",

		],

		"options.giReflectionDepth" : [

			"description",
			"""
			Controls the number of ray bounces when
			computing reflections.
			""",

			"layout:section", "Ray Depth",
			"label", "Reflection Depth",

		],


		"options.giRefractionDepth" : [

			"description",
			"""
			Controls the number of ray bounces when
			computing refractions.
			""",

			"layout:section", "Ray Depth",
			"label", "Refraction Depth",

		],

		"options.giVolumeDepth" : [

			"description",
			"""
			Controls the number of ray bounces when
			computing indirect lighting on volumes.
			""",

			"layout:section", "Ray Depth",
			"label", "Volume Depth",

		],

		"options.autoTransparencyDepth" : [

			"description",
			"""
			The number of allowable transparent layers - after
			this the last object will be treated as opaque.
			""",

			"layout:section", "Ray Depth",
			"label", "Transparency Depth",

		],

		"options.autoTransparencyThreshold" : [

			"description",
			"""
			A threshold for accumulated opacity, after which the
			last object will be treated as opaque.
			""",

			"layout:section", "Ray Depth",
			"label", "Opacity Threshold",
		],

		# Features

		"options.ignoreTextures" : [

			"description",
			"""
			Ignores all file textures, rendering as
			if they were all white.
			""",

			"layout:section", "Features",

		],

		"options.ignoreShaders" : [

			"description",
			"""
			Ignores all shaders, rendering as a
			simple facing ratio shader instead.
			""",

			"layout:section", "Features",

		],

		"options.ignoreAtmosphere" : [

			"description",
			"""
			Ignores all atmosphere shaders.
			""",

			"layout:section", "Features",

		],

		"options.ignoreLights" : [

			"description",
			"""
			Ignores all lights.
			""",

			"layout:section", "Features",

		],

		"options.ignoreShadows" : [

			"description",
			"""
			Skips all shadow calculations.
			""",

			"layout:section", "Features",

		],

		"options.ignoreSubdivision" : [

			"description",
			"""
			Treats all subdivision surfaces
			as simple polygon meshes instead.
			""",

			"layout:section", "Features",

		],

		"options.ignoreDisplacement" : [

			"description",
			"""
			Ignores all displacement shaders.
			""",

			"layout:section", "Features",

		],

		"options.ignoreBump" : [

			"description",
			"""
			Ignores all bump mapping.
			""",

			"layout:section", "Features",

		],

		"options.ignoreMotionBlur" : [

			"description",
			"""
			Ignores motion blur. Note that the turn
			off motion blur completely, it is more
			efficient to use the motion blur controls
			in the StandardOptions node.
			""",

			"layout:section", "Features",

		],

		"options.ignoreSSS" : [

			"description",
			"""
			Disables all subsurface scattering.
			""",

			"layout:section", "Features",

		],

		# Performance

		"options.threads" : [

			"description",
			"""
			Specifies the number of threads Arnold
			is allowed to use. A value of 0 gives
			Arnold access to all available threads.
			""",

			"layout:section", "Performance",

		],

		# Search Paths

		"options.textureSearchPath" : [

			"description",
			"""
			The locations used to search for texture
			files.
			""",

			"layout:section", "Search Paths",
			"label", "Textures",

		],

		"options.proceduralSearchPath" : [

			"description",
			"""
			The locations used to search for procedural
			DSOs.
			""",

			"layout:section", "Search Paths",
			"label", "Procedurals",

		],

		"options.shaderSearchPath" : [

			"description",
			"""
			The locations used to search for shader plugins.
			""",

			"layout:section", "Search Paths",
			"label", "Shaders",

		],

		# Error Colors

		"options.errorColorBadTexture" : [

			"description",
			"""
			The colour to display if an attempt is
			made to use a bad or non-existent texture.
			""",

			"layout:section", "Error Colors",
			"label", "Bad Texture",

		],

		"options.errorColorBadMesh" : [

			"description",
			"""
			The colour to display if bad geometry
			is encountered.
			""",

			"layout:section", "Error Colors",
			"label", "Bad Mesh",

		],

		"options.errorColorBadPixel" : [

			"description",
			"""
			The colour to display for a pixel where
			a NaN is encountered.
			""",

			"layout:section", "Error Colors",
			"label", "Bad Pixel",

		],

		"options.errorColorBadShader" : [

			"description",
			"""
			The colour to display if a problem occurs
			in a shader.
			""",

			"layout:section", "Error Colors",
			"label", "Bad Shader",

		],

		# Logging

		"options.logFileName" : [

			"description",
			"""
			The name of a log file which Arnold will generate
			while rendering.
			""",

			"layout:section", "Logging",
			"label", "File Name",

		],

		"options.logFileName.value" : [

			"plugValueWidget:type", "GafferUI.FileSystemPathPlugValueWidget",
			"pathPlugValueWidget:leaf", True,
			"fileSystemPathPlugValueWidget:extensions", IECore.StringVectorData( [ "txt", "log" ] ),
			"fileSystemPathPlugValueWidget:extensionsLabel", "Show only log files",

		],

		# Licensing

		"options.abortOnLicenseFail" : [

			"description",
			"""
			Aborts the render if a license is not available,
			instead of rendering with a watermark.
			""",

			"layout:section", "Licensing",

		],

		"options.skipLicenseCheck" : [

			"description",
			"""
			Skips the check for a license, always rendering
			with a watermark.
			""",

			"layout:section", "Licensing",

		],

	}

)
