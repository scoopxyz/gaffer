##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
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

import unittest
import threading

import IECore

import Gaffer
import GafferScene
import GafferSceneTest

class AttributesTest( unittest.TestCase ) :
		
	def test( self ) :
	
		sphere = IECore.SpherePrimitive()
		input = GafferSceneTest.CompoundObjectSource()
		input["in"].setValue(
			IECore.CompoundObject( {
				"bound" : IECore.Box3fData( sphere.bound() ),
				"children" : {
					"ball1" : {
						"object" : sphere,
						"bound" : IECore.Box3fData( sphere.bound() ),
					},
					"ball2" : {
						"object" : sphere,
						"bound" : IECore.Box3fData( sphere.bound() ),
					},
				},
			} )
		)
	
		a = GafferScene.Attributes()
		a["in"].setInput( input["out"] )
		
		# should be no attributes until we've specified any
		self.assertEqual( a["out"].attributes( "/" ), None )
		self.assertEqual( a["out"].attributes( "/ball1" ), None )
		self.assertEqual( a["out"].attributes( "/ball2" ), None )	

		# when we specify some, they should be applied to everything because
		# we haven't specified a filter yet. but not to the root because it
		# isn't allowed attributes.
		a["attributes"].addParameter( "ri:shadingRate", IECore.FloatData( 0.25 ) )
		self.assertEqual( a["out"].attributes( "/" ), None )
		self.assertEqual( a["out"].attributes( "/ball1" ), IECore.CompoundObject( { "ri:shadingRate" : IECore.FloatData( 0.25 ) } ) )
		self.assertEqual( a["out"].attributes( "/ball2" ), IECore.CompoundObject( { "ri:shadingRate" : IECore.FloatData( 0.25 ) } ) )

		# finally once we've applied a filter, we should get some attributes.
		f = GafferScene.PathFilter()
		f["paths"].setValue( IECore.StringVectorData( [ "/ball1" ] ) )
		a["filter"].setInput( f["match"] )

		self.assertEqual( a["out"].attributes( "/" ), None )
		self.assertEqual( a["out"].attributes( "/ball1" ), IECore.CompoundObject( { "ri:shadingRate" : IECore.FloatData( 0.25 ) } ) )
		self.assertEqual( a["out"].attributes( "/ball2" ), None )
	
	def testOverrideAttributes( self ) :
	
		sphere = IECore.SpherePrimitive()
		input = GafferSceneTest.CompoundObjectSource()
		input["in"].setValue(
			IECore.CompoundObject( {
				"bound" : IECore.Box3fData( sphere.bound() ),
				"children" : {
					"ball1" : {
						"object" : sphere,
						"bound" : IECore.Box3fData( sphere.bound() ),
					},
				},
			} )
		)
	
		a = GafferScene.Attributes()
		a["in"].setInput( input["out"] )
		
		a["attributes"].addParameter( "ri:shadingRate", IECore.FloatData( 0.25 ) )
		a["attributes"].addParameter( "user:something", IECore.IntData( 1 ) )
		self.assertEqual(
			a["out"].attributes( "/ball1" ),
			IECore.CompoundObject( {
				"ri:shadingRate" : IECore.FloatData( 0.25 ),
				"user:something" : IECore.IntData( 1 ),
			} )
		)

		a2 = GafferScene.Attributes()
		a2["in"].setInput( a["out"] )
		
		self.assertEqual(
			a2["out"].attributes( "/ball1" ),
			IECore.CompoundObject( {
				"ri:shadingRate" : IECore.FloatData( 0.25 ),
				"user:something" : IECore.IntData( 1 ),
			} )
		)
	
		a2["attributes"].addParameter( "ri:shadingRate", IECore.FloatData( .5 ) )
		a2["attributes"].addParameter( "user:somethingElse", IECore.IntData( 10 ) )
		
		self.assertEqual(
			a2["out"].attributes( "/ball1" ),
			IECore.CompoundObject( {
				"ri:shadingRate" : IECore.FloatData( 0.5 ),
				"user:something" : IECore.IntData( 1 ),
				"user:somethingElse" : IECore.IntData( 10 ),
			} )
		)
	
	def testRendering( self ) :
	
		sphere = IECore.SpherePrimitive()
		input = GafferSceneTest.CompoundObjectSource()
		input["in"].setValue(
			IECore.CompoundObject( {
				"bound" : IECore.Box3fData( sphere.bound() ),
				"children" : {
					"ball1" : {
						"object" : sphere,
						"bound" : IECore.Box3fData( sphere.bound() ),
					},
				},
			} )
		)
	
		a = GafferScene.Attributes()
		a["in"].setInput( input["out"] )
		
		a["attributes"].addParameter( "ri:shadingRate", IECore.FloatData( 0.25 ) )
		a["attributes"].addParameter( "user:something", IECore.IntData( 1 ) )
		
		r = IECore.CapturingRenderer()
		with IECore.WorldBlock( r ) :
			r.procedural( GafferScene.SceneProcedural( a["out"], Gaffer.Context(), "/" ) )
			
		g = r.world()
		attributes = g.children()[0].children()[0].children()[0].children()[0].state()[0]
		self.assertEqual(
			attributes.attributes,
			IECore.CompoundData( {
				"name" : IECore.StringData( "/ball1" ),
				"ri:shadingRate" : IECore.FloatData( 0.25 ),
				"user:something" : IECore.IntData( 1 ),
			} )
		)
			
if __name__ == "__main__":
	unittest.main()