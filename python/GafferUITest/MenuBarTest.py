##########################################################################
#
#  Copyright (c) 2015, Image Engine Design Inc. All rights reserved.
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
import weakref
import functools

import IECore

import Gaffer
import GafferUI
import GafferUITest

QtCore = GafferUI._qtImport( "QtCore" )
QtGui = GafferUI._qtImport( "QtGui" )

class MenuBarTest( GafferUITest.TestCase ) :

	def testLifetime( self ) :

		def f() :

			pass

		definition = IECore.MenuDefinition(

			[
				( "/apple/pear/banana", { } ),
				( "/apple/pear/divider", { "divider" : True } ),
				( "/apple/pear/submarine", { "command" : f } ),
				( "/dog/inactive", { "active" : False } ),
			]

		)

		with GafferUI.Window() as window :

			with GafferUI.ListContainer() :

				menu = GafferUI.MenuBar( definition )

		window.setVisible( True )
		self.waitForIdle( 1000 )
		del window

		w = weakref.ref( menu )
		del menu

		wd = weakref.ref( definition )
		del definition

		wf = weakref.ref( f )
		del f

		self.assertEqual( w(), None )
		self.assertEqual( wd(), None )
		self.assertEqual( wf(), None )

	def testShortcuts( self ) :

		commandInvocations = []
		def command( arg ) :

			commandInvocations.append( arg )

		definition = IECore.MenuDefinition( [
			( "/test/command", { "command" : functools.partial( command, "arg1" ), "shortCut" : "Ctrl+A" } ),
		] )

		with GafferUI.Window() as window :
			with GafferUI.ListContainer() :
				menuBar = GafferUI.MenuBar( definition )
				label = GafferUI.Label( "test" )

		window.setVisible( True )
		self.waitForIdle( 1000 )

		self.__simulateShortcut( label )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 1 )
		self.assertEqual( commandInvocations[0], "arg1" )

		menuBar.definition = IECore.MenuDefinition()

		self.__simulateShortcut( label )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 1 )

		menuBar.definition = IECore.MenuDefinition( [
			( "/test/command", { "command" : functools.partial( command, "arg2" ), "shortCut" : "Ctrl+A" } ),
		] )

		self.__simulateShortcut( label )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 2 )
		self.assertEqual( commandInvocations[1], "arg2" )

	def testNesting( self ) :

		commandInvocations = []
		def command( arg ) :

			commandInvocations.append( arg )

		outerDefinition = IECore.MenuDefinition( [
			( "/test/command", { "command" : functools.partial( command, "outer" ), "shortCut" : "Ctrl+A" } ),
		] )

		innerDefinition = IECore.MenuDefinition( [
			( "/test/command", { "command" : functools.partial( command, "inner" ), "shortCut" : "Ctrl+A" } ),
		] )

		with GafferUI.Window() as window :
			with GafferUI.ListContainer() :
				GafferUI.MenuBar( outerDefinition )
				outerLabel = GafferUI.Label( "test" )
				with GafferUI.ListContainer() :
					GafferUI.MenuBar( innerDefinition )
					innerLabel = GafferUI.Label( "test" )

		window.setVisible( True )
		self.waitForIdle( 1000 )

		self.__simulateShortcut( innerLabel )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 1 )
		self.assertEqual( commandInvocations[0], "inner" )

		self.__simulateShortcut( outerLabel )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 2 )
		self.assertEqual( commandInvocations[1], "outer" )

	def testParentChange( self ) :

		commandInvocations = []
		def command( arg ) :

			commandInvocations.append( arg )

		definition = IECore.MenuDefinition( [
			( "/test/command", { "command" : functools.partial( command, "test" ), "shortCut" : "Ctrl+A" } ),
		] )

		with GafferUI.Window() as window :
			with GafferUI.ListContainer() :
				with GafferUI.ListContainer() as container1 :
					menuBar = GafferUI.MenuBar( definition )
					label1 = GafferUI.Label( "test" )
				with GafferUI.ListContainer() as container2 :
					label2 = GafferUI.Label( "test" )

		window.setVisible( True )
		self.waitForIdle( 1000 )

		self.__simulateShortcut( label1 )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 1 )

		self.__simulateShortcut( label2 )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 1 )

		container2.insert( 0, menuBar )

		self.__simulateShortcut( label1 )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 1 )

		self.__simulateShortcut( label2 )
		self.waitForIdle( 1000 )
		self.assertEqual( len( commandInvocations ), 2 )

	def __simulateShortcut( self, widget ) :

		QtGui.QApplication.instance().notify(
			widget._qtWidget(),
			QtGui.QKeyEvent( QtCore.QEvent.KeyPress, QtCore.Qt.Key_A, QtCore.Qt.ControlModifier )
		)

		QtGui.QApplication.instance().notify(
			widget._qtWidget(),
			QtGui.QKeyEvent( QtCore.QEvent.KeyRelease, QtCore.Qt.Key_A, QtCore.Qt.ControlModifier )
		)

if __name__ == "__main__":
	unittest.main()
