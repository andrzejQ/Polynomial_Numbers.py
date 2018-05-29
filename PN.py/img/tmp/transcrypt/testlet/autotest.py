import org.transcrypt.autotester

import testlet0
import testlet1sin

import testletPN0

autoTester = org.transcrypt.autotester.AutoTester ()

autoTester.run (testlet0, 'testlet0')
autoTester.run (testlet1sin, 'testlet1sin')

autoTester.run (testletPN0, 'testletPN0')

autoTester.done ()